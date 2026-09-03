import streamlit as st
from streamlit_keyboard_event import keyboard_event

st.set_page_config(page_title="스페이스 카운터 & 상점", layout="centered")

# 1. 세션 상태(변수) 초기화
if "count" not in st.session_state:
    st.session_state.count = 0
if "per_click" not in st.session_state:
    st.session_state.per_click = 1
if "cost" not in st.session_state:
    st.session_state.cost = 50
if "show_shop" not in st.session_state:
    st.session_state.show_shop = False

# 2. 로직 함수 정의
def increment():
    st.session_state.count += st.session_state.per_click

def toggle_shop():
    st.session_state.show_shop = not st.session_state.show_shop

def buy_upgrade():
    if st.session_state.count >= st.session_state.cost:
        st.session_state.count -= st.session_state.cost
        st.session_state.per_click += 1
        st.session_state.cost *= 2
        st.toast("🎉 업그레이드 성공!")
    else:
        st.toast("❌ 카운트(점수)가 부족합니다!")

# 3. 키보드 감지 컴포넌트 실행 (Space, e, E)
key_event = keyboard_event(
    key_list=["Space", "e", "E"],
    key=st.session_state.get("key_listen_id", "kb_event")
)

# 키 입력 이벤트 처리
if key_event:
    pressed_key = key_event.get("key")
    if pressed_key == "Space":
        increment()
    elif pressed_key in ["e", "E"]:
        toggle_shop()

# 4. Main UI
st.title("그냥 스페이스바")

col1, col2 = st.columns(2)
with col1:
    st.metric("현재 카운트", st.session_state.count)
with col2:
    st.metric("1회당 증가량", f"+{st.session_state.per_click}")

# 기본 카운트 버튼
st.button("숫자 올리기 (Space 키)", on_click=increment, use_container_width=True)

st.write("---")

# 상점 토글 버튼
st.button(
    f"🏪 상점 {'닫기' if st.session_state.show_shop else '열기'} (E 키)", 
    on_click=toggle_shop, 
    type="primary" if not st.session_state.show_shop else "secondary",
    use_container_width=True
)

# 5. 상점 UI
if st.session_state.show_shop:
    with st.expander("🛒 강화 상점", expanded=True):
        st.markdown(f"**클릭당 증가량 +1 강화**")
        st.write(f"- 필요 카운트: **{st.session_state.cost}**")
        st.write(f"- 구매 후 증가량: **+{st.session_state.per_click + 1}**")
        
        can_buy = st.session_state.count >= st.session_state.cost
        st.button(
            "구매하기", 
            on_click=buy_upgrade, 
            disabled=not can_buy,
            use_container_width=True
        )
