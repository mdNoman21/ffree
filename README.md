# Vehicle Registration Dashboard

## Overview
This project is an interactive dashboard built with Streamlit that visualizes vehicle registration data sourced from the [Vahan Dashboard](https://vahan.nic.in/). The focus is on providing investor-friendly insights into vehicle registration trends categorized by vehicle types (2W, 3W, 4W) and manufacturers.

The dashboard displays both Year-over-Year (YoY) growth percentages alongside registration trends for annual data, as well as Quarter-over-Quarter (QoQ) growth for the most recent quarterly data (2025), enabling investors and analysts to track performance and identify promising opportunities in the automotive market.

You can access the **deployed live dashboard here:**  
[https://a82kpdsjpwvq86tdu9ntmu.streamlit.app/](https://a82kpdsjpwvq86tdu9ntmu.streamlit.app/)

---

## Features
- Interactive year range slider for filtering annual data dynamically
- Support for quarterly data analysis with QoQ growth visualization (for latest available quarters, e.g., 2025)
- Multi-select filters for vehicle category and manufacturer across both annual and quarterly data
- Visualizations include line charts (annual registrations and YoY growth) and bar charts (quarterly registrations and QoQ growth)
- Clean and intuitive UI optimized for investor insights and decision-making

---

## Data Source
- Public datasets originally obtained from the Vahan Dashboard
- Excel data files included directly in the repository for user convenience:
  - `Vehicle-Category-Wise-Calendar-Year-Data-For-All-State.xlsx`
  - `Maker-Wise-Calendar-Year-Data-For-All-State.xlsx`
  - `vcmw_2025.xlsx` (Quarterly vehicle category data for 2025)
  - `mcmw_2025.xlsx` (Quarterly maker-wise data for 2025)

---

## Setup Instructions

To run the app locally:

1. **Clone the repository:**
    ```
    git clone https://github.com/mdNoman21/ffree.git
    cd <repo_folder>
    ```

2. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

3. **Run the Streamlit dashboard:**
    ```
    python -m streamlit run main.py
    ```

---

## Code Structure
- `main.py` — The main Streamlit app script that contains all UI, data processing, and visualization logic, including both annual and quarterly analysis
- `requirements.txt` — Defines the Python dependencies for this project
- Excel data files as listed in Data Source

---

## Data Assumptions
- The data accuracy relies on the original Vahan Dashboard source.
- Annual data covers 2016 through 2025; quarterly data is included only for the year 2025.
- For annual data, only Year-over-Year (YoY) growth analysis is possible as no quarterly breakdown exists.
- For 2025, quarterly data supports Quarter-over-Quarter (QoQ) growth metrics.
- Numeric data columns have been cleaned by removing commas and converting to numeric types.
- Default filters usually show recent years and a subset of top manufacturers for optimal performance.

---

## How to Use the Dashboard
- Select between **Annual (YoY)** and **Quarterly (QoQ)** analysis via the sidebar radio button.
- Use the filters on the sidebar to choose the range of years (for annual data) or select specific vehicle categories and manufacturers.
- View the data separated into tabs for each category and manufacturer to reduce clutter.
- Explore registrations alongside their growth percentages to identify trends, spikes, or slowdowns.

---

## Investor Insights
- The data shows notable growth trends in Two Wheeler registrations indicating increasing demand in this segment.
- Several manufacturers consistently outperform their competitors, signaling market leadership.
- Seasonal spikes and cyclical buying patterns are visible in the data — useful for investment timing.
- Quarterly data for 2025 allows granular monitoring of market shifts throughout the year.

---

## Video Walkthrough
Watch a quick demo of the dashboard's features, how to use filters, explore both annual and quarterly trends, and observe key investor insights:  
[Video Walkthrough Link](https://drive.google.com/file/d/1FwnDz8qi9Hfhyo6K49FK8bOZjZA1dlgx/view)

---

## Contact / Support
Feel free to reach out for questions, suggestions, or collaboration opportunities!

---

Thank you for exploring the Vehicle Registration Dashboard!
