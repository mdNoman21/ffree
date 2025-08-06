# Vehicle Registration Dashboard

## Overview
This project is an interactive dashboard built with Streamlit that visualizes vehicle registration data sourced from the [Vahan Dashboard](https://vahan.nic.in/). The focus is on providing investor-friendly insights into vehicle registration trends categorized by vehicle types (2W, 3W, 4W) and manufacturers.

The dashboard displays Year-over-Year (YoY) growth percentages alongside registration trends, enabling investors and analysts to track performance and identify promising opportunities in the automotive market.

You can access the **deployed live dashboard here:**  
[https://a82kpdsjpwvq86tdu9ntmu.streamlit.app/](https://a82kpdsjpwvq86tdu9ntmu.streamlit.app/)

---

## Features
- Interactive year range slider for filtering data dynamically
- Multi-select filters for vehicle category and manufacturer
- Visualizations include line charts representing registrations and YoY growth
- Clean and intuitive UI optimized for investor insights and decision-making

---

## Data Source
- Public datasets originally obtained from the Vahan Dashboard
- Excel data files included directly in the repository for user convenience:
  - `Vehicle-Category-Wise-Calendar-Year-Data-For-All-State.xlsx`
  - `Maker-Wise-Calendar-Year-Data-For-All-State.xlsx`

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
- `main.py` — The main Streamlit app script that contains all UI and visualization logic
- `requirements.txt` — Defines the Python dependencies for this project

---

## Data Assumptions
- The data accuracy relies on the original Vahan Dashboard source.
- Only annual (yearly) data is available; no quarterly data means Quarter-over-Quarter (QoQ) growth analysis is not included.
- Numeric data columns have been cleaned by removing commas before processing.
- Default filters usually show recent years and a subset of top manufacturers for optimal performance.

---

## Investor Insights
- The data shows notable growth trends in Two Wheeler registrations indicating increasing demand in this segment.
- Several manufacturers consistently outperform their competitors, signaling market leadership.
- Seasonal spikes and cyclical buying patterns are visible in the data — useful for investment timing.

---

## Video Walkthrough
Watch a quick demo of the dashboard's features and how to use filters to explore trends, along with key investor insights:  
[Video Walkthrough Link](https://drive.google.com/file/d/1FwnDz8qi9Hfhyo6K49FK8bOZjZA1dlgx/view)

---

## Contact / Support
Feel free to reach out for questions, suggestions, or collaboration opportunities!

---

Thank you for exploring the Vehicle Registration Dashboard!
