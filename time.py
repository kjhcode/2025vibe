import streamlit as st
import time
import random
import hashlib
import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="미루지 말자!", layout="centered")

# ----------------------------
# ✅ 세션 상태 초기화
# ----------------------------
def init_session_state():
    defaults = {
        "checklist": [],
        "reward_categories": {},
        "selected_reward": None,
        "diary_entries": {},
        "start_time": None,
        "running": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
    if not isinstance(st.session_state.diary_entries, dict):
        st.session_state.diary_entries = {}

init_session_state()

# ----------------------------
# ✅ 체크리스트
# ----------------------------
st.title("✅ 체크리스트 + ⏱ 타이머 + 🎁 보상 + 📝 일기")
st.header("📋 오늘의 할 일")

task_input = st.text_input("할 일 입력", key="input_task")
if st.button("➕ 추가"):
    if task_input.strip():
        st.session_state.checklist.append({"text": task_input.strip(), "checked": False})
        st.success("할 일이 추가되었습니다!")

def get_safe_key(text, index):
    return f"task_{index}_" + hashlib.md5(text.encode()).hexdigest()

completed = 0
for i, item in enumerate(st.session_state.checklist):
    key = get_safe_key(item["text"], i)
    checked = st.checkbox(item["text"], value=item["checked"], key=key)
    st.session_state.checklist[i]["checked"] = checked
    if checked:
        completed += 1

total = len(st.session_state.checklist)
if total > 0:
    st.markdown(f"**완료: {completed} / {total}**")
    st.progress(completed / total)
else:
    st.info("할 일을 입력해보세요!")

# ----------------------------
# ✅ 보상 등록 + 랜덤 뽑기
# ----------------------------
st.header("🎁 카테고리별 보상 등록")

with st.form("reward_form_section"):
    category = st.text_input("카테고리 입력", placeholder="예: 음식, 휴식")
    reward = st.text_input("보상 내용", placeholder="예: 치킨 먹기")
    submit = st.form_submit_button("추가")
    if submit and category.strip() and reward.strip():
        st.session_state.reward_categories.setdefault(category, []).append(reward)
        st.success("보상이 추가되었습니다!")

if st.session_state.reward_categories:
    for cat, rewards in st.session_state.reward_categories.items():
        st.markdo
