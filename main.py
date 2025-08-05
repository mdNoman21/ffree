import streamlit as st
import pandas as pd
import numpy as np

# Helper to clean numeric columns (remove commas, convert to int)
def clean_numeric_cols(df):
    years = [col for col in df.columns if str(col).isdigit()]
    for col in years:
        # Remove commas and convert to numeric
        df[col] = df[col].astype(str).str.replace(',', '').astype(float)
    return df

# Load and preprocess vehicle category data
@st.cache_data
def load_category_data():
    df_cat = pd.read_excel('Vehicle-Category-Wise-Calendar-Year-Data-For-All-State.xlsx', sheet_name='reportTable', skiprows=4)
    # Select needed columns and rename
    df_cat = df_cat.iloc[:, 1:7]
    df_cat.columns = ['Vehicle Category', '2024', '2022', '2020', '2018', '2016']
    df_cat = clean_numeric_cols(df_cat)
    # Melt to long format for easier filtering
    df_cat_long = df_cat.melt(id_vars=['Vehicle Category'], var_name='Year', value_name='Registrations')
    df_cat_long['Year'] = df_cat_long['Year'].astype(int)
    return df_cat_long

# Load and preprocess maker-wise data
@st.cache_data
def load_maker_data():
    df_maker = pd.read_excel('Maker-Wise-Calendar-Year-Data-For-All-State.xlsx', sheet_name='reportTable', skiprows=4)
    # Select needed columns and rename
    df_maker = df_maker.iloc[:, 1:7]
    df_maker.columns = ['Maker', '2024', '2022', '2020', '2018', '2016']
    df_maker = clean_numeric_cols(df_maker)
    # Melt to long format
    df_maker_long = df_maker.melt(id_vars=['Maker'], var_name='Year', value_name='Registrations')
    df_maker_long['Year'] = df_maker_long['Year'].astype(int)
    return df_maker_long

# Calculate YoY growth
def calculate_yoy(df, group_col):
    df = df.sort_values(['Year'])
    df['YoY Growth %'] = df.groupby(group_col)['Registrations'].pct_change() * 100
    return df

# Streamlit app UI
def main():
    st.title('Vehicle Registration Dashboard')

    # Load data
    df_cat = load_category_data()
    df_maker = load_maker_data()

    # Sidebar filters
    st.sidebar.header('Filters')

    year_min, year_max = int(df_cat['Year'].min()), int(df_cat['Year'].max())
    years = sorted(df_cat['Year'].unique().tolist())
    selected_years = st.sidebar.slider('Select Year Range', year_min, year_max, (year_min, year_max), step=2)

    categories = df_cat['Vehicle Category'].unique().tolist()
    selected_categories = st.sidebar.multiselect('Select Vehicle Categories', categories, default=categories)

    makers = df_maker['Maker'].unique().tolist()
    selected_makers = st.sidebar.multiselect('Select Makers', makers, default=makers[:20])  # limiting default to first 20 for performance

    # Filter data
    df_cat_filtered = df_cat[
        (df_cat['Year'] >= selected_years[0]) &
        (df_cat['Year'] <= selected_years[1]) &
        (df_cat['Vehicle Category'].isin(selected_categories))
    ]
    df_maker_filtered = df_maker[
        (df_maker['Year'] >= selected_years[0]) &
        (df_maker['Year'] <= selected_years[1]) &
        (df_maker['Maker'].isin(selected_makers))
    ]

    # Calculate YoY growth
    df_cat_filtered = calculate_yoy(df_cat_filtered, 'Vehicle Category')
    df_maker_filtered = calculate_yoy(df_maker_filtered, 'Maker')

    # Display charts
    st.subheader('Vehicle Registrations by Category')
    for category in selected_categories:
        df_plot = df_cat_filtered[df_cat_filtered['Vehicle Category'] == category]
        st.line_chart(df_plot.set_index('Year')['Registrations'], use_container_width=True)
        st.write(f"YoY Growth % for {category}")
        st.line_chart(df_plot.set_index('Year')['YoY Growth %'], use_container_width=True)

    st.subheader('Vehicle Registrations by Maker')
    for maker in selected_makers:
        df_plot = df_maker_filtered[df_maker_filtered['Maker'] == maker]
        st.line_chart(df_plot.set_index('Year')['Registrations'], use_container_width=True)
        st.write(f"YoY Growth % for {maker}")
        st.line_chart(df_plot.set_index('Year')['YoY Growth %'], use_container_width=True)

if __name__ == "__main__":
    main()
