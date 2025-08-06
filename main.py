import streamlit as st
import pandas as pd

# -------- Quarter Processing Helpers --------

def load_and_process_quarterly_data(file_path, id_type, sheet_name='reportTable'):
    # Read the Excel file, skipping explanatory headers
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=3)
    df.columns = [str(col).strip() for col in df.columns]
    df = df.dropna(axis=1, how='all')
    # Identify ID column
    id_col = next((col for col in df.columns if id_type in col), df.columns[1])
    # Identify all month columns
    month_keys = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG']
    month_cols = [col for col in df.columns if col.upper()[:3] in month_keys]
    # Clean up the month columns
    for col in month_cols:
        df[col] = (
            df[col].astype(str)
            .str.replace(',', '')
            .str.replace('nan', '0', case=False)
        )
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    # Calculate quarters (Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Aug (missing Sep in this data))
    quarters = {
        'Q1': month_cols[0:3],   # Jan, Feb, Mar
        'Q2': month_cols[3:6],   # Apr, May, Jun
        'Q3': month_cols[6:8],   # Jul, Aug
    }
    for q in quarters:
        q_cols = quarters[q]
        df[q] = df[q_cols].sum(axis=1) if q_cols else 0
    quarters_order = ['Q1', 'Q2', 'Q3']  # Only available quarters
    df_quarterly = df[[id_col] + quarters_order]
    # Melt to long form
    df_long = df_quarterly.melt(id_vars=[id_col], var_name='Quarter', value_name='Registrations')
    return df_long.rename(columns={id_col: 'ID'}), id_col

def calculate_qoq_growth(df):
    # Calculate quarter-over-quarter growth % for each ID
    df = df.copy()
    df['Quarter_num'] = df['Quarter'].str.extract(r'(\d+)').astype(int)
    df = df.sort_values(['ID', 'Quarter_num'])
    df['QoQ Growth %'] = df.groupby('ID')['Registrations'].pct_change() * 100
    df = df.drop('Quarter_num', axis=1)
    return df

# --------- Main App ---------
def main():
    st.title('Vehicle Registration Dashboard (With Quarterly Analysis)')

    st.sidebar.header('Switch Data Level')
    dataset_type = st.sidebar.radio("Choose Analysis Level", ("Annual (YoY)", "Quarterly (QoQ)"))

    if dataset_type == "Annual (YoY)":
        # --- Annual Processing ---
        ALL_YEARS = list(range(2016, 2026))

        @st.cache_data
        def load_category_data():
            df = pd.read_excel('vehicle_category_registrations_2016_2025.xlsx')
            missing_years = (
                df.groupby('Vehicle Category')['Year']
                  .apply(lambda yrs: len(set(ALL_YEARS) - set(yrs)))
                  .reset_index(name='Missing Year Count')
            )
            df = df.merge(missing_years, on='Vehicle Category', how='left')
            return df

        @st.cache_data
        def load_maker_data():
            df = pd.read_excel('maker_wise_registrations_2016_2025.xlsx')
            missing_years = (
                df.groupby('Maker')['Year']
                  .apply(lambda yrs: len(set(ALL_YEARS) - set(yrs)))
                  .reset_index(name='Missing Year Count')
            )
            df = df.merge(missing_years, on='Maker', how='left')
            return df

        def calculate_yoy(df, group_col):
            df = df.sort_values(['Year'])
            df['YoY Growth %'] = df.groupby(group_col)['Registrations'].pct_change() * 100
            return df

        df_cat = load_category_data()
        df_maker = load_maker_data()

        year_min, year_max = int(df_cat['Year'].min()), int(df_cat['Year'].max())
        selected_years = st.sidebar.slider(
            'Select Year Range', min_value=year_min, max_value=year_max,
            value=(year_min, year_max), step=1
        )
        categories = sorted(df_cat['Vehicle Category'].unique())
        selected_categories = st.sidebar.multiselect('Select Vehicle Categories', categories, default=categories[:5])
        makers = sorted(df_maker['Maker'].unique())
        selected_makers = st.sidebar.multiselect('Select Makers', makers, default=makers[:5])
        df_cat_filtered = df_cat[
            (df_cat['Year'] >= selected_years[0]) & (df_cat['Year'] <= selected_years[1]) &
            (df_cat['Vehicle Category'].isin(selected_categories))
        ]
        df_maker_filtered = df_maker[
            (df_maker['Year'] >= selected_years[0]) & (df_maker['Year'] <= selected_years[1]) &
            (df_maker['Maker'].isin(selected_makers))
        ]
        df_cat_filtered = calculate_yoy(df_cat_filtered, 'Vehicle Category')
        df_maker_filtered = calculate_yoy(df_maker_filtered, 'Maker')

        # Sidebar data completeness
        st.sidebar.markdown("### Data Completeness")
        st.sidebar.dataframe(
            df_cat_filtered[['Vehicle Category', 'Missing Year Count']].drop_duplicates().sort_values('Missing Year Count'),
            hide_index=True
        )
        st.sidebar.dataframe(
            df_maker_filtered[['Maker', 'Missing Year Count']].drop_duplicates().sort_values('Missing Year Count'),
            hide_index=True
        )

        # Category tabs
        st.subheader('Vehicle Registrations by Category')
        if selected_categories:
            category_tabs = st.tabs(selected_categories)
            for idx, category in enumerate(selected_categories):
                with category_tabs[idx]:
                    df_plot = df_cat_filtered[df_cat_filtered['Vehicle Category'] == category]
                    st.line_chart(df_plot.set_index('Year')['Registrations'], use_container_width=True)
                    st.write(f"YoY Growth % for {category}")
                    st.line_chart(df_plot.set_index('Year')['YoY Growth %'], use_container_width=True)

        # Maker tabs
        st.subheader('Vehicle Registrations by Maker')
        if selected_makers:
            maker_tabs = st.tabs(selected_makers)
            for idx, maker in enumerate(selected_makers):
                with maker_tabs[idx]:
                    df_plot = df_maker_filtered[df_maker_filtered['Maker'] == maker]
                    st.line_chart(df_plot.set_index('Year')['Registrations'], use_container_width=True)
                    st.write(f"YoY Growth % for {maker}")
                    st.line_chart(df_plot.set_index('Year')['YoY Growth %'], use_container_width=True)

    else:
        # ------- Quarterly Processing -------
        st.sidebar.markdown("#### (Covers 2025 quarterly only)")

        # Load quarterly data for categories and makers
        df_cat_q, vehicle_id_col = load_and_process_quarterly_data('vcmw_2025.xlsx', 'Vehicle Category')
        df_maker_q, maker_id_col = load_and_process_quarterly_data('mcmw_2025.xlsx', 'Maker')
        df_cat_q = calculate_qoq_growth(df_cat_q)
        df_maker_q = calculate_qoq_growth(df_maker_q)

        # Filters
        categories = sorted(df_cat_q['ID'].unique())
        makers = sorted(df_maker_q['ID'].unique())
        selected_cat = st.sidebar.selectbox('Select Vehicle Category', categories)
        selected_maker = st.sidebar.selectbox('Select Maker', makers)

        # Category chart
        st.subheader(f'Quarterly Registrations: {selected_cat}')
        cat_data = df_cat_q[df_cat_q['ID'] == selected_cat].set_index('Quarter')
        st.bar_chart(cat_data['Registrations'], use_container_width=True)
        st.write("Quarter-over-Quarter Growth %")
        st.bar_chart(cat_data['QoQ Growth %'], use_container_width=True)

        # Maker chart
        st.subheader(f'Quarterly Registrations: {selected_maker}')
        maker_data = df_maker_q[df_maker_q['ID'] == selected_maker].set_index('Quarter')
        st.bar_chart(maker_data['Registrations'], use_container_width=True)
        st.write("Quarter-over-Quarter Growth %")
        st.bar_chart(maker_data['QoQ Growth %'], use_container_width=True)

if __name__ == "__main__":
    main()
