# daily-cognitive-load-tracker
A Streamlit-based cognitive wellness tracker designed to analyze focus, stress, and energy trends through interactive visualizations.

---

## Live Demo

https://daily-cognitive-load-tracker.streamlit.app/

## Features

- Daily logging of stress, energy, and focus levels  
- Time-stamped entries for tracking changes over time  
- One entry per day validation to prevent duplicates  
- Persistent data storage using a local CSV file  
- Interactive line charts for visualizing each metric  
- Linear trend lines generated using NumPy regression
- Optional raw data viewer for transparency  
- Streak tracking for consistent daily logging
- Alert system for uncommon patterns 
- Adaptive warning and encouraging messages

---

## Tech Stack

- Python
- Streamlit  
- Pandas  
- Altair  
- Numpy
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
  
- User authentication
- Mood tracking 
- Mobile optimization
