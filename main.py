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

# 2. 로직 함수
def increment():
    st.session_state.count += 1

def toggle_shop():
    st.session_state.show_shop = not st.session_state.show_shop

def buy_upgrade():
    if st.session_state.count >= st.session_state.cost:
        st.session_state.count -= st.session_state.cost
        st.session_state.per_click += 1
        st.session_state.cost *= 2
        st.toast("🎉 업그레이드 성공!")
    else:
        st.toast("❌ 카운트가 부족합니다!")

# 3. 키보드 이벤트 처리 (강력한 DOM 클릭 방식)
st.components.v1.html(
    """
    <script>
    const parentDoc = window.parent.document;
    
    // 키 감지 함수
    function handleKeyDown(e) {
        if (['INPUT', 'TEXTAREA'].includes(parentDoc.activeElement.tagName)) return;
        
        if (e.code === 'Space') {
            e.preventDefault();
            // 첫 번째 일반 버튼(숫자 올리기) 클릭
            const btns = parentDoc.querySelectorAll('button');
            for (let btn of btns) {
                if (btn.innerText.includes('숫자 올리기')) {
                    btn.click();
                    break;
                }
            }
        } else if (e.code === 'KeyE') {
            e.preventDefault();
            // 상점 버튼 클릭
            const btns = parentDoc.querySelectorAll('button');
            for (let btn of btns) {
                if (btn.innerText.includes('상점')) {
                    btn.click();
                    break;
                }
            }
        }
    }

    // 부모 문서 및 iframe 둘 다에 키 이벤트 등록
    parentDoc.removeEventListener('keydown', handleKeyDown);
    parentDoc.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keydown', handleKeyDown);
    </script>
    """,
    height=0,
)

# 4. UI 구성
st.title("🔢 스페이스 카운터")

col1, col2 = st.columns(2)
with col1:
    st.metric("현재 카운트", st.session_state.count)
with col2:
    st.metric("상점 업그레이드 수치", f"+{st.session_state.per_click}")

# 숫자 올리기 버튼 (텍스트 검색 기반 클릭)
st.button(
    "숫자 올리기 (+1) (Space 키)", 
    on_click=increment, 
    use_container_width=True
)

st.write("---")

# 상점 버튼 (텍스트 검색 기반 클릭)
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
        st.write(f"- 구매 후 수치: **+{st.session_state.per_click + 1}**")
        
        can_buy = st.session_state.count >= st.session_state.cost
        st.button(
            "구매하기", 
            on_click=buy_upgrade, 
            disabled=not can_buy,
            use_container_width=True
        )
