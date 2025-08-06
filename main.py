import streamlit as st
import pandas as pd

ALL_YEARS = list(range(2016, 2026))

def load_category_data():
    df = pd.read_excel('vehicle_category_registrations_2016_2025.xlsx')
    # Calculate missing year counts
    missing_years = (
        df.groupby('Vehicle Category')['Year']
          .apply(lambda yrs: len(set(ALL_YEARS) - set(yrs)))
          .reset_index(name='Missing Year Count')
    )
    df = df.merge(missing_years, on='Vehicle Category', how='left')
    return df

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

def main():
    st.title('Vehicle Registration Dashboard')

    df_cat = load_category_data()
    df_maker = load_maker_data()

    # Sidebar filters
    st.sidebar.header('Filters')
    year_min, year_max = int(df_cat['Year'].min()), int(df_cat['Year'].max())
    selected_years = st.sidebar.slider(
        'Select Year Range',
        min_value=year_min, max_value=year_max,
        value=(year_min, year_max), step=1
    )

    categories = sorted(df_cat['Vehicle Category'].unique())
    selected_categories = st.sidebar.multiselect('Select Vehicle Categories', categories, default=categories[:5])
    makers = sorted(df_maker['Maker'].unique())
    selected_makers = st.sidebar.multiselect('Select Makers', makers, default=makers[:5])

    # Filtered data
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

    # Data completeness in sidebar
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

if __name__ == "__main__":
    main()
