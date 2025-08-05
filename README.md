# Vehicle Registration Dashboard

## Overview
This project is an interactive dashboard built with Streamlit that visualizes vehicle registration data from the Vahan Dashboard. The focus is on providing investor-friendly insights into vehicle registration trends categorized by vehicle types (2W, 3W, 4W) and manufacturers.

The dashboard displays Year-over-Year (YoY) growth percentages alongside registration trends, enabling investors to track performance and identify promising opportunities in the automotive market.

---

## Features
- Interactive year range selection for filtering data
- Filters by vehicle category and manufacturer
- Visualizations include line charts for registrations and YoY growth
- Clean and intuitive UI designed for investor insights

---

## Data Source
- Public data originally sourced from the Vahan Dashboard
- This project includes the Excel data files directly in the repo for user convenience:
  - `Vehicle-Category-Wise-Calendar-Year-Data-For-All-State.xlsx`
  - `Maker-Wise-Calendar-Year-Data-For-All-State.xlsx`

---

## Setup Instructions

1. **Clone the repository:**
git clone <repo_url>
cd <repo_folder>

2. **Install dependencies:**
pip install -r requirements.txt


3. **Run the app:**
python -m streamlit run main.py


---

## Code Structure
- `app.py`: Streamlit dashboard app with UI and visualization logic
- `requirements.txt`: Python dependencies

---

## Data Assumptions
- Data accuracy relies on the original Vahan Dashboard source.
- Only yearly calendar data is available, so Quarter-over-Quarter (QoQ) growth is not shown.
- Numeric data is cleaned by removing commas before processing.
- Default selections filter to most recent years and a subset of manufacturers for performance.

---

## Feature Roadmap (if continued)
- Incorporate quarterly data if available in the future.
- Add more granular filters such as region or state-wise breakdown.
- Implement predictive analytics or investment risk indicators.
- Enhance UI responsiveness and add export options.
- Add user authentication and personalization features.

---

## Investor Insights
- Notable growth trends in 2W registrations signal rising demand.
- Some manufacturers consistently outperform competitors indicating market leadership.
- Seasonal spikes and trends point to possible cyclic buying behavior.

---

## Video Walkthrough
A short screen recording demonstrates:
- App functionality overview
- Using filters and exploring trends
- Key investor insights discovered in the data

[Insert YouTube unlisted or Drive link here]

---

Feel free to reach out for questions or suggestions!


