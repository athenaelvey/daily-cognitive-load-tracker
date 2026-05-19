# daily-cognitive-load-tracker
A Streamlit-based cognitive wellness tracker designed to analyze focus, stress, and energy trends through interactive visualizations.

---

## Features

- Daily logging of stress, energy, and focus levels  
- Time-stamped entries for tracking changes over time  
- One entry per day validation to prevent duplicates  
- Persistent data storage using a local CSV file  
- Interactive line charts for visualizing each metric  
- Trend visualization across days  
- Optional raw data viewer for transparency  

---

## Tech Stack

- Python  
- Streamlit  
- Pandas  
- Altair  
- Standard Python libraries (datetime, os)  

---

## How to Run

1. Clone the repository:
   git clone https://github.com/athenaelvey/daily-cognitive-load-tracker.git

2. Navigate into the project folder:
   cd daily-cognitive-load-tracker

3. Install dependencies:
   pip install streamlit pandas altair

4. Run the application:
   streamlit run app.py

---

## Future Improvements

- Add rolling averages to smooth trend analysis  
- Implement streak tracking for consistent daily logging  
- Introduce milestone badges for engagement (3, 7, 30 days)  
- Add alert system for unusual stress or focus patterns  
- Expand analytics with correlations between metrics  
- Add data export options (CSV / PDF reports)  
- Improve UI layout and visual design consistency  
- Deploy the app for public access via Streamlit Cloud  
