import streamlit as st
from collections import defaultdict
from datetime import datetime, timedelta

st.set_page_config(page_title="공강 분석기", layout="wide")
st.title("🧠 공강 시간 자동 분석기")

days = ["월", "화", "수", "목", "금"]
time_slots = [f"{h:02}:00" for h in range(9, 22)]

def get_time_range(start, end):
    start_dt = datetime.strptime(start, "%H:%M")
    end_dt = datetime.strptime(end, "%H:%M")
    times = []
    while start_dt < end_dt:
        times.append(start_dt.strftime("%H:%M"))
        start_dt += timedelta(minutes=30)
    return times

st.markdown("### 👥 팀원 수를 입력하고, 각자 시간표를 입력하세요.")
num_members = st.number_input("팀원 수", min_value=1, max_value=10, value=2)

all_busy = defaultdict(set)

for i in range(num_members):
    st.subheader(f"🧍 팀원 {i+1} 시간표")
    for day in days:
        with st.expander(f"{day} 수업 추가"):
            class_count = st.number_input(f"{day} 수업 수", min_value=0, max_value=10, key=f"{i}_{day}_count")
            for j in range(class_count):
                col1, col2 = st.columns(2)
                with col1:
                    start = st.selectbox(f"{day} 수업 {j+1} 시작", time_slots, key=f"{i}_{day}_{j}_start")
                with col2:
                    end = st.selectbox(f"{day} 수업 {j+1} 끝", time_slots, key=f"{i}_{day}_{j}_end")
                for t in get_time_range(start, end):
                    all_busy[(day, t)].add(i)

if st.button("🚀 공강 시간 분석하기"):
    st.success("공강 시간 분석 완료!")
    st.markdown("### ✅ 공통 공강 시간 (모든 팀원이 가능한 시간)")
    result_table = []
    for day in days:
        row = []
        for t in time_slots:
            busy = all_busy.get((day, t), set())
            if len(busy) == 0:
                row.append("🟢")
            elif len(busy) < num_members:
                row.append("🟡")
            else:
                row.append("🔴")
        result_table.append(row)

    st.write("🟢 모두 공강 | 🟡 일부 공강 | 🔴 수업 있음")
    table_dict = {day: row for day, row in zip(days, result_table)}
    st.dataframe(table_dict, height=500)
