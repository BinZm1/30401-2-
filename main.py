import streamlit as st

st.set_page_config(page_title="스페이스 카운터 & 상점", layout="centered")

# 1. 세션 상태 초기화
if "count" not in st.session_state:
    st.session_state.count = 0
if "per_click" not in st.session_state:
    st.session_state.per_click = 1
if "cost" not in st.session_state:
    st.session_state.cost = 50
if "show_shop" not in st.session_state:
    st.session_state.show_shop = False

# Query Parameter로 입력된 키 이벤트 처리
query_params = st.query_params
if "key" in query_params:
    pressed_key = query_params["key"]
    # URL 파라미터 초기화
    st.query_params.clear()
    
    if pressed_key == "space":
        st.session_state.count += st.session_state.per_click
    elif pressed_key in ["e", "E"]:
        st.session_state.show_shop = not st.session_state.show_shop
    st.rerun()

# 2. 로직 함수
def buy_upgrade():
    if st.session_state.count >= st.session_state.cost:
        st.session_state.count -= st.session_state.cost
        st.session_state.per_click += 1
        st.session_state.cost *= 2
        st.toast("🎉 업그레이드 성공!")
    else:
        st.toast("❌ 카운트가 부족합니다!")

# 3. 키보드 이벤트 감지 스크립트 (기본 HTML/JS 방식)
st.components.v1.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.repeat) return;
        
        if (e.code === 'Space') {
            e.preventDefault();
            window.parent.postMessage({type: 'KEY_PRESS', key: 'space'}, '*');
        } else if (e.code === 'KeyE') {
            e.preventDefault();
            window.parent.postMessage({type: 'KEY_PRESS', key: 'e'}, '*');
        }
    });

    window.addEventListener('message', function(event) {
        if (event.data.type === 'KEY_PRESS') {
            const url = new URL(window.parent.location.href);
            url.searchParams.set('key', event.data.key);
            window.parent.location.search = url.searchParams.toString();
        }
    });
    </script>
    """,
    height=0,
)

# 4. UI 화면 구성
st.title("🔢 스페이스 카운터")

col1, col2 = st.columns(2)
with col1:
    st.metric("현재 카운트", st.session_state.count)
with col2:
    st.metric("1회당 증가량", f"+{st.session_state.per_click}")

# 수동 클릭용 버튼
if st.button("숫자 올리기 (Space 키)", use_container_width=True):
    st.session_state.count += st.session_state.per_click
    st.rerun()

st.write("---")

if st.button(
    f"🏪 상점 {'닫기' if st.session_state.show_shop else '열기'} (E 키)", 
    type="primary" if not st.session_state.show_shop else "secondary",
    use_container_width=True
):
    st.session_state.show_shop = not st.session_state.show_shop
    st.rerun()

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
