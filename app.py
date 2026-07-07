import streamlit as st
import datetime as dt
import pandas as pd
import altair as alt
import numpy as np
import os

st.set_page_config(
    page_title="Daily Cognitive Load Tracker",
    layout="wide",        
    initial_sidebar_state="auto"
)

st.title("Daily Cognitive Load Tracker")

csv_file = "daily_log.csv"

backup_folder = "backups"

if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)

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

if len(last_3) == 3:

    stress = last_3["Stress"].tolist()
    focus = last_3["Focus"].tolist()
    energy = last_3["Energy"].tolist()

    stress_trend = stress[0] < stress[1] < stress[2]
    focus_trend = focus[0] > focus[1] > focus[2]
    energy_trend = energy[0] > energy[1] > energy[2]

    if stress_trend:
        alerts.append("Take a breather! Stress has been increasing over the last few days.")

    if focus_trend:
        alerts.append("Try something new, Focus has been declining recently.")

    if energy_trend:
        alerts.append("Spend some time resetting. Energy levels have been trending downward over recent days.")

if alerts:
    for alert in alerts:
        st.info(alert)

st.subheader("Check-In")

focus = st.slider("How are your focus levels today?", 1, 10)

st.write("Focus Levels: ", focus)

st.markdown("---")

energy = st.slider("How energized do you feel today?", 1, 10)

st.write("Energy Levels: ", energy)

st.markdown("---")

stress = st.slider("How stressed are you today?", 1, 10)

st.write("Stress Levels: ", stress)

st.markdown("---")

current_time = dt.datetime.now().strftime("%I:%M %p")

entry = [dt.date.today(), current_time, focus, energy, stress]
df = pd.DataFrame([entry], columns = ["Date", "Time", "Focus", "Energy", "Stress"])

if st.button("💾 Save Entry"):
    st.caption("Entries are saved once a day")
    
    if today in df2["Date"].dt.date.values:
        st.warning("You’ve already logged an entry for today! ✅")

    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)
        
        backup_name = f"daily_log_{today}.csv"
        backup_path = os.path.join(backup_folder, backup_name)

        df2.to_csv(backup_path, index = False)

        st.success("✅ Your entry was saved!")

df2 = pd.read_csv(csv_file)
df2["Date"] = pd.to_datetime(df2["Date"])

data_count = len(df2)
has_trend = data_count >= 2

df2['day_num'] = range(len(df2))

if data_count >= 2:
    stress_fit = np.polyfit(df2['day_num'], df2['Stress'],1)

    stress_slope = stress_fit[0]
    stress_intercept = stress_fit[1]

    df2['stress_trend'] = stress_slope * df2['day_num'] + stress_intercept

    energy_fit = np.polyfit(df2['day_num'], df2['Energy'],1)

    energy_slope = energy_fit[0]
    energy_intercept = energy_fit[1]

    df2['energy_trend'] = energy_slope * df2['day_num'] + energy_intercept

    focus_fit = np.polyfit(df2['day_num'], df2['Focus'], 1)

    focus_slope = focus_fit[0]
    focus_intercept = focus_fit[1]

    df2['focus_trend'] = focus_slope * df2['day_num'] + focus_intercept

df2 = df2.drop_duplicates(subset=["Date"], keep="first")

df2.to_csv(csv_file, index=False)

logged_days = sorted(df2["Date"].dt.date.unique())

streak = 0
day = today

while day in logged_days:
    streak += 1
    day = day - dt.timedelta(days = 1)

if len(logged_days) == 0:
    pass
elif streak == 0:
    st.info("No entry logged today... let's log an entry today to get the streak back up!")
else:
    st.success(f"🔥 You’re on a **{streak}-day streak**! Amazing consistency!")

if streak >= 100:
    st.balloons()
    st.markdown("🏅 **100-Day Milestone Achieved**")
elif streak >= 30:
    st.markdown("🥇 **30-Day Streak**")
elif streak >= 7:
    st.markdown("🎉 **7-Day Streak**")

title_col, filter_col = st.columns([4,1])

with title_col:
    st.subheader("Wellness Trends")

with filter_col:
    date_filter = st.selectbox(
        "View",
        ["Default", "Last 30 Days", "Last 90 Days", "All Time"]
    )

if date_filter == "Default":
    chart_data = df2.tail(20)

elif date_filter == "Last 30 Days":
    chart_data = df2[df2['Date'] >= (dt.datetime.now() - pd.Timedelta(days=30))]

elif date_filter == "Last 90 Days":
    chart_data = df2[df2['Date'] >= (dt.datetime.now() - pd.Timedelta(days = 90))]

else:
    chart_data = df2

if data_count == 0:
    st.info("Log your first entry to start seeing trends!")

else:
    col1, col2, col3 = st.columns(3)

    week = df2[df2['Date'] >= (df2['Date'].max() - pd.Timedelta(days=6))]

    stress_chart = alt.Chart(chart_data).mark_line(point=True).encode(
    x='Date:T',
    y=alt.Y(
        'Stress:Q',
        scale=alt.Scale(domain=[0, 15])
    ),
    color=alt.Color(
        'Stress:Q',
        scale=alt.Scale(
            domain=[1, 10],
            range=['#ffd6d6', '#ff0000']
        ),
        legend=None
    )
).properties(
    title="Stress"
)

    stress_trend_vis = alt.Chart(chart_data).mark_line().encode(
        x = 'Date:T',
        y = alt.Y(
        'stress_trend:Q',
        title='Stress',
        scale=alt.Scale(domain=[0, 15])
    ),
        color = alt.value('#990000')
    )

    if has_trend:
        stress_comb = (stress_chart + stress_trend_vis).resolve_scale(
            y='shared'
        )
        avg_stress_week = week['Stress'].mean()
        avg_stress_total = df2['Stress'].mean()
    
    else:
        stress_comb = stress_chart

    with col1:
        st.altair_chart(stress_comb, use_container_width=True)

        if has_trend:
            if avg_stress_week > avg_stress_total:
                st.info("Stress this week is higher than usual, take some time to relax.")
            elif avg_stress_week < avg_stress_total:
                st.success("Stress is decreasing this week, keep doing what you're doing!")
            else:
                st.info("Stress is constant this week, let's see if we can lower it.")
        else:
            st.info("Log at least 2 entries to see weekly comparisons.")

    energy_chart = alt.Chart(chart_data).mark_line(point = True).encode(
        x = 'Date:T',
        y=alt.Y(
        'Energy:Q',
        scale=alt.Scale(domain=[0,15])
    ),
        color=alt.Color(
        'Energy:Q',
        scale=alt.Scale(
            domain=[1, 10],
            range=['#ebe5d5', '#ffd59a']
        ),
        legend=None
    )
    ).properties(
        title="Energy"
    )

    energy_trend_vis = alt.Chart(chart_data).mark_line().encode(
        x = 'Date:T',
        y=alt.Y(
        'energy_trend:Q',
        title = 'Energy',
        scale=alt.Scale(domain=[0,15])
    ),
        color = alt.value('#c28a30')
    )

    if has_trend:
        energy_comb = (energy_chart + energy_trend_vis).resolve_scale(
            y='shared'
        )
        avg_energy_week = week['Energy'].mean()
        avg_energy_total = df2['Energy'].mean()

    else:
        energy_comb = energy_chart

    with col2:
        st.altair_chart(energy_comb, use_container_width=True)

        if has_trend:
            if avg_energy_week > avg_energy_total:
                st.success("Energy is rocketing this week! See if you can do something productive with it.")
            elif avg_energy_week < avg_energy_total:
                st.info("Feeling a bit weary this week? That's alright, take a break and recharge.")
            else:
                st.info("Energy is staying stagnant, make sure you don't overdo it!")
        else:
            st.info("Log at least 2 entries to see weekly comparisons.")

    focus_chart = alt.Chart(chart_data).mark_line(point = True).encode(
        x = 'Date:T',
        y=alt.Y(
        'Focus:Q',
        scale=alt.Scale(domain=[0,15])
    ),
        color=alt.Color(
        'Focus:Q',
        scale=alt.Scale(
            domain=[1, 10],
            range=['#f9e076', '#fa8128']
        ),
        legend=None
    )
    ).properties(
        title="Focus"
    )

    focus_trend_vis = alt.Chart(chart_data).mark_line().encode(
        x = 'Date:T',
        y=alt.Y(
        'focus_trend:Q',
        title = 'Focus',
        scale=alt.Scale(domain=[0,15])
    ),
        color = alt.value('#c95f00')
    )

    if has_trend: 
        focus_comb = (focus_chart + focus_trend_vis).resolve_scale(
            y='shared'
        )
        avg_focus_week = week['Focus'].mean()
        avg_focus_total = df2['Focus'].mean()

    else:
        focus_comb = focus_chart

    with col3:
        st.altair_chart(focus_comb, use_container_width=True)
    
        if has_trend:
            if avg_focus_week > avg_focus_total:
                st.success("Focus is high for this week! Why don't we work on a to-do list? Get some studying down?")
            elif avg_focus_week < avg_focus_total:
                st.info("Focus is down for now, clear your mind and try some relaxing exercises.")
            else:
                st.info("Focus is steady this week, try not to fall behind on any work !")
        else:
            st.info("Log at least 2 entries to see weekly comparisons.")

st.markdown("---")

raw, weekly, download = st.columns(3)

with raw:
    if st.checkbox("📄 Show raw data"):
        st.dataframe(df2)

with weekly:
    if st.button("📊 Generate Weekly Report"):

        if has_trend:
            st.write("Weekly Report")
        
            avg_focus = week['Focus'].mean()
            avg_energy = week['Energy'].mean()
            avg_stress = week['Stress'].mean()

            st.write(f"Average Focus: {avg_focus:.1f}")
            st.write(f"Average Energy: {avg_energy:.1f}")
            st.write(f"Average Stress: {avg_stress:.1f}")

            focus_pos = False
            stress_pos = False
            energy_pos = False

            if avg_focus > avg_focus_total:
                st.write("Focus vs Overall: ↑")
                focus_pos = True
            else:
                st.write("Focus vs Overall: ↓")
        
            if avg_energy > avg_energy_total:
                st.write("Energy vs Overall: ↑")
                energy_pos = True
            else:
                st.write("Energy vs Overall: ↓")

            if avg_stress < avg_stress_total:
                st.write("Stress vs Overall: ↓")
                stress_pos = True
            else:
                st.write("Stress vs Overall: ↑")

            if focus_pos and energy_pos and stress_pos:
                st.success("Excellent week! Focus and energy were above your usual levels while stress remained lower than normal.")

            elif focus_pos and energy_pos:
                st.success("Strong week! Focus and energy both improved compared to your overall averages.")

            elif focus_pos and stress_pos:
                st.success("Nice work! Focus improved while stress stayed lower than your usual levels.")

            elif energy_pos and stress_pos:
                st.success("Nice work! Energy was higher than usual and stress was kept under control.")

            elif focus_pos:
                st.info("Focus was stronger than usual this week. Try that strategy more often!")

            elif energy_pos:
                st.info("Energy levels were above your normal average this week. Ample sleep and hydration can maintain that!")

            elif stress_pos:
                st.info("Stress was lower than your typical level this week. Take advantage of this tranquility")

            else:
                st.warning("This week appears to have been more challenging than usual. Focus and energy were lower while stress was higher than your typical averages. Next week is a fresh start.")

    else:
        if data_count < 2:
            st.info("Log at least two entries to generate a weekly report.")

with download:
    csv_data = df2.to_csv(index=False)

    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name="daily_log.csv",
        mime="text/csv"
    )