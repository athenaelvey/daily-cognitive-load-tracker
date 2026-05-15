import streamlit as st
import datetime as dt
import pandas as pd
import altair as alt
import os

st.set_page_config(
    page_title="Daily Cognitive Load Tracker",
    layout="wide",        
    initial_sidebar_state="auto"
)

st.title("Daily Cognitive Load Tracker")

csv_file = "daily_log.csv"

if os.path.exists(csv_file):
    df2 = pd.read_csv(csv_file)

else:
    df2 = pd.DataFrame(columns = ["Date", "Time", "Focus", "Energy", "Stress"])
    df2.to_csv(csv_file, index = False)

df2["Date"] = pd.to_datetime(df2["Date"])

logged_days = sorted(df2["Date"].dt.date.unique())

today = dt.date.today()
streak = 0
day = 0

while day in logged_days:
    streak += 1
    day = day - timedelta(days = 1)

if streak == 0:
    st.info("You lost your streak... let's log an entry today to get it back up!")
else:
    st.success(f"🔥 You’re on a **{streak}-day streak**! Amazing consistency!")

if streak >= 100:
    st.balloons()
    st.markdown("🏅 **100-Day Milestone Achieved**")
elif streak >= 30:
    st.markdown("🥇 **30-Day Streak**")
elif streak >= 7:
    st.markdown("🎉 **7-Day Streak**")

st.subheader("Check-In")

focus = st.slider("How are your focus levels today?", 1, 10)

st.write("Focus Levels: ", focus)

st.markdown("---");

energy = st.slider("How energized do you feel today?", 1, 10)

st.write("Energy Levels: ", energy)

st.markdown("---");

stress = st.slider("How stressed are you today?", 1, 10)

st.write("Stress Levels: ", stress)

st.markdown("---");

current_time = dt.datetime.now().strftime("%I:%M %p")

entry = [dt.date.today(), current_time, focus, energy, stress]
df = pd.DataFrame([entry], columns = ["Date", "Time", "Focus", "Energy", "Stress"])

today = dt.date.today()

if st.button("💾 Save Entry"):
    st.caption("Entries are saved once a day.")
    
    if today in df2["Date"].values:
        st.warning("You’ve already logged an entry for today! ✅")

    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)
        st.success("✅ Your entry was saved!")

df2 = pd.read_csv(csv_file)
df2["Date"] = pd.to_datetime(df2["Date"])

df2 = df2.drop_duplicates(subset=["Date"], keep="first")

df2.to_csv(csv_file, index=False)

st.subheader("Wellness Trends")

col1, col2, col3 = st.columns(3)

week = df2[df2['Date'] >= (df2['Date'].max() - pd.Timedelta(days=6))]

stress_chart = alt.Chart(df2).mark_line(point=True).encode(
    x = 'Date:T',
    y = 'Stress:Q',
    color = alt.Color('Stress:Q',
                    scale=alt.Scale(domain=[df2['Stress'].min(),df2['Stress'].max()],
                                    range=['#ffd6d6','#ff0000']),
                    legend=None)
).properties(
    title="Stress"
)

avg_stress_week = week['Stress'].mean()
avg_stress_total = df2['Stress'].mean()

with col1:
    st.altair_chart(stress_chart, use_container_width=True)

    if avg_stress_week > avg_stress_total:
        st.info("Stress this week is higher than usual, take some time to relax.")
    elif avg_stress_week < avg_stress_total:
        st.success("Stress is decreasing this week, keep doing what you're doing!")
    else:
        st.write("Stress is constant this week, let's see if we can lower it.")


energy_chart = alt.Chart(df2).mark_line(point=True).encode(
    x = 'Date:T',
    y = 'Energy:Q',
    color = alt.Color('Energy:Q',
                    scale=alt.Scale(domain=[df2['Energy'].min(),df2['Energy'].max()],
                                    range=['#ebe5d5','#ffd59a']),
                    legend=None)
).properties(
    title="Energy"
)

avg_energy_week = week['Energy'].mean()
avg_energy_total = df2['Energy'].mean()


with col2:
    st.altair_chart(energy_chart, use_container_width=True)

    if avg_energy_week > avg_energy_total:
        st.info("Energy is rocketing this week! See if you can do something productive with it.")
    elif avg_energy_week < avg_energy_total:
        st.success("Feeling a bit weary this week? That's alright, take a break and recharge.")
    else:
        st.write("Energy is staying stagnant, make sure you don't overdo it!")


focus_chart = alt.Chart(df2).mark_line(point=True).encode(
    x = 'Date:T',
    y = 'Focus:Q',
    color = alt.Color('Focus:Q',
                    scale=alt.Scale(domain=[df2['Focus'].min(),df2['Focus'].max()],
                                    range=['#f9e076','#fa8128']),
                    legend=None)
).properties(
    title="Focus"
)

avg_focus_week = week['Focus'].mean()
avg_focus_total = df2['Focus'].mean()


with col3:
    st.altair_chart(focus_chart, use_container_width=True)
    
    if avg_focus_week > avg_focus_total:
        st.info("Focus is high for this week! Why don't we work on a to-do list? Get some studying down?")
    elif avg_focus_week < avg_focus_total:
        st.success("Focus is down for now, clear your mind and try some relaxing exercises")
    else:
        st.write("Focus is steady this week, try not to fall behind on any work !")

st.markdown("---")

if st.checkbox("📄 Show raw data"):
    st.dataframe(df2)

df2['Focus'].rolling(window = 7).mean()
df2['Energy'].rolling(window = 7).mean()
df2['Stress'].rolling(window = 7).mean()

df2['focus_rolling'] = df2['Focus'].rolling(7, min_periods = 1).mean()
df2['energy_rolling'] = df2['Energy'].rolling(7, min_periods = 1).mean()
df2['stress_rolling'] = df2['Stress'].rolling(7, min_periods = 1).mean()
