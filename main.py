import streamlit as st
import random

st.set_page_config(page_title="스페이스 카운터 & 상점", layout="centered")

# 1. 세션 상태 초기화
if "count" not in st.session_state:
    st.session_state.count = 0
if "per_click" not in st.session_state:
    st.session_state.per_click = 1  # 기본 증가량 1
if "cost" not in st.session_state:
    st.session_state.cost = 50      # 초기 필요 비용
if "show_shop" not in st.session_state:
    st.session_state.show_shop = False

# 2. 로직 함수
def increment():
    st.session_state.count += st.session_state.per_click

def toggle_shop():
    st.session_state.show_shop = not st.session_state.show_shop

def buy_upgrade():
    if st.session_state.count >= st.session_state.cost:
        st.session_state.count -= st.session_state.cost
        st.session_state.per_click += 1  # 클릭당 증가량 +1
        
        # 🎲 배율 확률 설정 (2배:10%, 3배:60%, 5배:30%, 10배:10%)
        multipliers = [2, 3, 5, 10]
        weights = [10, 60, 30, 10]
        
        # 확률에 따라 다음 배율 선택
        chosen_multiplier = random.choices(multipliers, weights=weights, k=1)[0]
        
        # 비용 인상 적용
        st.session_state.cost *= chosen_multiplier
        
        # 알림 메시지 출력
        st.toast(f"🎉 업그레이드 성공! (다음 비용 {chosen_multiplier}배 상승)")
    else:
        st.toast("❌ 카운트가 부족합니다!")

# 3. 키보드 이벤트 처리 (DOM 클릭 방식)
st.components.v1.html(
    """
    <script>
    const parentDoc = window.parent.document;
    
    function handleKeyDown(e) {
        if (['INPUT', 'TEXTAREA'].includes(parentDoc.activeElement.tagName)) return;
        
        if (e.code === 'Space') {
            e.preventDefault();
            const btns = parentDoc.querySelectorAll('button');
            for (let btn of btns) {
                if (btn.innerText.includes('숫자 올리기')) {
                    btn.click();
                    break;
                }
            }
        } else if (e.code === 'KeyE') {
            e.preventDefault();
            const btns = parentDoc.querySelectorAll('button');
            for (let btn of btns) {
                if (btn.innerText.includes('상점')) {
                    btn.click();
                    break;
                }
            }
        }
    }

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
    st.metric("1회당 증가량", f"+{st.session_state.per_click}")

# 숫자 올리기 버튼
st.button(
    f"숫자 올리기 (+{st.session_state.per_click}) (Space 키)", 
    on_click=increment, 
    use_container_width=True
)

st.write("---")

# 상점 버튼
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
        st.write(f"- 필요 카운트: **{st.session_state.cost:,}**")
        st.write(f"- 구매 후 증가 수치: **+{st.session_state.per_click + 1}**")
        st.caption("🎲 구매 시 다음 비용이 랜덤 배율(2배/3배/5배/10배)로 상승합니다.")
        
        can_buy = st.session_state.count >= st.session_state.cost
        st.button(
            "구매하기", 
            on_click=buy_upgrade, 
            disabled=not can_buy,
            use_container_width=True
        )
