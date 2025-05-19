import streamlit as st
from collections import defaultdict
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="공강 분석기", layout="wide")
st.title("🧠 사용자별 공강 시간 분석기")

# 🧠 세션 상태에 사용자별 시간표 저장 공간 초기화
if "schedules" not in st.session_state:
    st.session_state["schedules"] = {}

# 📆 요일 + 15분 단위 시간 생성
days = ["월", "화", "수", "목", "금"]
start_time = datetime.strptime("09:00", "%H:%M")
end_time = datetime.strptime("21:00", "%H:%M")
interval = timedelta(minutes=15)

time_slots = []
current = start_time
while current <= end_time:
    time_slots.append(current.strftime("%H:%M"))
    current += interval

# ⏳ 시작~종료 시간 리스트로 만들기
def get_time_range(start, end):
    start_dt = datetime.strptime(start, "%H:%M")
    end_dt = datetime.strptime(end, "%H:%M")
    times = []
    while start_dt < end_dt:
        times.append(start_dt.strftime("%H:%M"))
        start_dt += timedelta(minutes=15)
    return times

# 👤 사용자 시간표 입력 UI
st.markdown("### 📝 사용자별 시간표 등록")
name = st.text_input("사용자 이름")

if name:
    user_schedule = []
    for day in days:
        with st.expander(f"{day} 수업 추가"):
            count = st.number_input(f"{day} 수업 수", min_value=0, max_value=10, key=f"{name}_{day}_count")
            for i in range(count):
                col1, col2 = st.columns(2)
                with col1:
                    start = st.selectbox(f"{day} 수업 {i+1} 시작", time_slots, key=f"{name}_{day}_{i}_start")
                with col2:
                    end = st.selectbox(f"{day} 수업 {i+1} 끝", time_slots, key=f"{name}_{day}_{i}_end")
                user_schedule.append((day, start, end))

    if st.button("✅ 시간표 등록", key=f"submit_{name}"):
        st.session_state["schedules"][name] = user_schedule
        st.success(f"✅ {name}님의 시간표가 저장되었습니다!")

# 👀 등록된 사용자 목록 출력
if st.session_state["schedules"]:
    st.markdown("### 👥 등록된 사용자 목록")
    for uname in st.session_state["schedules"].keys():
        st.markdown(f"- {uname}")

# ✅ 공강 분석 대상 사용자 선택
st.markdown("### 📊 공강 분석할 사용자 선택")
selected_users = st.multiselect("분석 대상 선택", list(st.session_state["schedules"].keys()))

# 🔍 공강 분석 실행
if st.button("🚀 공강 시간 분석하기"):
    all_busy = defaultdict(set)
    for uname in selected_users:
        for day, start, end in st.session_state["schedules"][uname]:
            for t in get_time_range(start, end):
                all_busy[(day, t)].add(uname)

    # 표 생성
    data = []
    for t in time_slots:
        row = {"시간": t}
        for day in days:
            busy = all_busy.get((day, t), set())
            row[day] = "공강" if len(busy) == 0 else ""
        data.append(row)

    df_timetable = pd.DataFrame(data)

    # 셀 배경 초록색 강조 스타일
    def highlight_free(val):
        return "background-color: lightgreen" if val == "공강" else ""

    styled_df = df_timetable.style.applymap(highlight_free, subset=days)

    st.markdown("### ✅ 선택된 사용자들의 공강 시간표")
    st.dataframe(styled_df, height=700)
