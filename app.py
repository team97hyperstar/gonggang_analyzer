import streamlit as st
from collections import defaultdict
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="공강 분석기", layout="wide")
st.title("🧠 공강 시간 자동 분석기")

# 요일 및 15분 단위 시간 생성
days = ["월", "화", "수", "목", "금"]
start_time = datetime.strptime("09:00", "%H:%M")
end_time = datetime.strptime("21:00", "%H:%M")
interval = timedelta(minutes=15)

time_slots = []
current = start_time
while current <= end_time:
    time_slots.append(current.strftime("%H:%M"))
    current += interval

# 시작-종료 시간 범위 생성 함수
def get_time_range(start, end):
    start_dt = datetime.strptime(start, "%H:%M")
    end_dt = datetime.strptime(end, "%H:%M")
    times = []
    while start_dt < end_dt:
        times.append(start_dt.strftime("%H:%M"))
        start_dt += timedelta(minutes=15)
    return times

# 팀원 수 입력
st.markdown("### 👥 팀원 수를 입력하고, 각자 시간표를 입력하세요.")
num_members = st.number_input("팀원 수", min_value=1, max_value=10, value=2)

all_busy = defaultdict(set)

# 시간표 입력
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

# 분석 및 표 출력
if st.button("🚀 공강 시간 분석하기"):
    st.success("공강 시간 분석 완료!")
    st.markdown("### ✅ 모두 공강인 시간만 표시된 시간표")

    data = []
    for t in time_slots:
        row = {"시간": t}
        for day in days:
            busy = all_busy.get((day, t), set())
            row[day] = "공강" if len(busy) == 0 else ""
        data.append(row)

    df_timetable = pd.DataFrame(data)
    st.dataframe(df_timetable, height=700)
