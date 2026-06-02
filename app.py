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
day = today

if len(logged_days) == 0:
    st.info("Welcome! Log your first entry to start a streak!")

last_3 = df2.sort_values("Date").tail(3)

alerts = []

if len(last_3) >= 3:

    stress = last_3["Stress"].tolist()
    focus = last_3["Focus"].tolist()
    energy = last_3["Energy"].tolist()

    stress_trend = stress[0] < stress[1] < stress[2]
    focus_trend = focus[0] > focus[1] > focus[2]
    energy_trend = energy[0] > energy[1] > energy[2]

    if stress_trend:
        alerts.append("Stress has been increasing over the last few days.")

    if focus_trend:
        alerts.append("Focus has been declining recently.")

    if energy_trend:
        alerts.append("Energy levels have been trending downward over recent days.")

if len(alerts) > 0:
    for alert in alerts:
        st.info(alert)

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

logged_days = sorted(df2["Date"].dt.date.unique())

streak = 0
day = today

while day in logged_days:
    streak += 1
    day = day - dt.timedelta(days = 1)

if streak == 0 and len(logged_days) > 0:
    st.info("No entry logged today... let's log an entry today to the streak back up!")
else:
    st.success(f"🔥 You’re on a **{streak}-day streak**! Amazing consistency!")

if streak >= 100:
    st.balloons()
    st.markdown("🏅 **100-Day Milestone Achieved**")
elif streak >= 30:
    st.markdown("🥇 **30-Day Streak**")
elif streak >= 7:
    st.markdown("🎉 **7-Day Streak**")

st.subheader("Wellness Trends")

col1, col2, col3 = st.columns(3)

week = df2[df2['Date'] >= (df2['Date'].max() - pd.Timedelta(days=6))]

df2['focus_rolling'] = df2['Focus'].rolling(7, min_periods = 1).mean()
df2['energy_rolling'] = df2['Energy'].rolling(7, min_periods = 1).mean()
df2['stress_rolling'] = df2['Stress'].rolling(7, min_periods = 1).mean()

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

stress_rolling_vis = alt.Chart(df2).mark_line().encode(
    x = 'Date:T',
    y = 'stress_rolling:Q',
    color = alt.value('#990000')

).properties(
    title="Stress Rolling"
)

stress_comb = stress_chart + stress_rolling_vis
avg_stress_week = week['Stress'].mean()
avg_stress_total = df2['Stress'].mean()

with col1:
    st.altair_chart(stress_comb, use_container_width=True)

    if avg_stress_week > avg_stress_total:
        st.info("Stress this week is higher than usual, take some time to relax.")
    elif avg_stress_week < avg_stress_total:
        st.success("Stress is decreasing this week, keep doing what you're doing!")
    else:
        st.info("Stress is constant this week, let's see if we can lower it.")


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

energy_rolling_vis = alt.Chart(df2).mark_line().encode(
    x = 'Date:T',
    y = 'energy_rolling:Q',
    color = alt.value('#c28a30')

).properties(
    title="Energy Rolling"

)

energy_comb = energy_chart + energy_rolling_vis
avg_energy_week = week['Energy'].mean()
avg_energy_total = df2['Energy'].mean()


with col2:
    st.altair_chart(energy_comb, use_container_width=True)

    if avg_energy_week > avg_energy_total:
        st.success("Energy is rocketing this week! See if you can do something productive with it.")
    elif avg_energy_week < avg_energy_total:
        st.info("Feeling a bit weary this week? That's alright, take a break and recharge.")
    else:
        st.info("Energy is staying stagnant, make sure you don't overdo it!")


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

focus_rolling_vis = alt.Chart(df2).mark_line().encode(
    x = 'Date:T',
    y = 'focus_rolling:Q',
    color = alt.value('#c95f00')

).properties(
    title="Focus Rolling"
)

focus_comb = focus_chart + focus_rolling_vis
avg_focus_week = week['Focus'].mean()
avg_focus_total = df2['Focus'].mean()


with col3:
    st.altair_chart(focus_comb, use_container_width=True)
    
    if avg_focus_week > avg_focus_total:
        st.success("Focus is high for this week! Why don't we work on a to-do list? Get some studying down?")
    elif avg_focus_week < avg_focus_total:
        st.info("Focus is down for now, clear your mind and try some relaxing exercises")
    else:
        st.info("Focus is steady this week, try not to fall behind on any work !")

st.markdown("---")

if st.checkbox("📄 Show raw data"):
    st.dataframe(df2)
