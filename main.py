import streamlit as st
import random
from datetime import datetime, timedelta

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
if "show_casino" not in st.session_state:
    st.session_state.show_casino = False

# 🎰 도박 횟수 및 쿨타임 초기화
# [최대 횟수, 잔여 횟수, 다음 리셋 시각]
LIMIT_CONFIG = {
    100: 10,
    1000: 5,
    10000: 50
}

if "gamble_limits" not in st.session_state:
    now = datetime.now()
    reset_time = now + timedelta(hours=1)
    st.session_state.gamble_limits = {
        100: {"remaining": 10, "reset_at": reset_time},
        1000: {"remaining": 5, "reset_at": reset_time},
        10000: {"remaining": 50, "reset_at": reset_time}
    }

# 2. 쿨타임 및 리셋 체크 함수
def check_and_reset_limits():
    now = datetime.now()
    for amount, config in st.session_state.gamble_limits.items():
        if now >= config["reset_at"]:
            config["remaining"] = LIMIT_CONFIG[amount]
            config["reset_at"] = now + timedelta(hours=1)

check_and_reset_limits()

# 3. 로직 함수
def increment():
    st.session_state.count += st.session_state.per_click

def toggle_shop():
    st.session_state.show_shop = not st.session_state.show_shop
    if st.session_state.show_shop:
        st.session_state.show_casino = False

def toggle_casino():
    st.session_state.show_casino = not st.session_state.show_casino
    if st.session_state.show_casino:
        st.session_state.show_shop = False

def buy_upgrade():
    if st.session_state.count >= st.session_state.cost:
        st.session_state.count -= st.session_state.cost
        st.session_state.per_click += 1
        
        multipliers = [2, 3, 5, 10]
        weights = [10, 60, 30, 10]
        chosen_multiplier = random.choices(multipliers, weights=weights, k=1)[0]
        
        st.session_state.cost *= chosen_multiplier
        st.toast(f"🎉 업그레이드 성공! (다음 비용 {chosen_multiplier}배 상승)")
    else:
        st.toast("❌ 카운트가 부족합니다!")

def gamble(amount):
    check_and_reset_limits()
    limit_info = st.session_state.gamble_limits[amount]
    
    if limit_info["remaining"] <= 0:
        st.toast("❌ 이번 시간대의 배팅 횟수를 모두 소진했습니다!")
        return
        
    if st.session_state.count >= amount:
        st.session_state.count -= amount
        limit_info["remaining"] -= 1  # 횟수 차감
        
        # 0.5배:60%, 2배:29%, 5배:10%, 10배:1%
        multipliers = [0.5, 2, 5, 10]
        weights = [60, 29, 10, 1]
        
        chosen_multiplier = random.choices(multipliers, weights=weights, k=1)[0]
        winnings = int(amount * chosen_multiplier)
        
        st.session_state.count += winnings
        
        if chosen_multiplier >= 1:
            st.toast(f"🎰 대박! {chosen_multiplier}배 당첨! (+{winnings:,} 획득)", icon="🎉")
        else:
            st.toast(f"💀 꽝! {chosen_multiplier}배... ({winnings:,}만 환급)", icon="😭")
    else:
        st.toast("❌ 배팅할 카운트가 부족합니다!")

# 4. 키보드 이벤트 처리 (DOM 클릭 방식)
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

# 5. UI 구성
st.title("🔢 스페이스 카운터")

col1, col2 = st.columns(2)
with col1:
    st.metric("현재 카운트", f"{st.session_state.count:,}")
with col2:
    st.metric("1회당 증가량", f"+{st.session_state.per_click:,}")

st.button(
    f"숫자 올리기 (+{st.session_state.per_click:,}) (Space 키)", 
    on_click=increment, 
    use_container_width=True
)

st.write("---")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    st.button(
        f"🏪 상점 {'닫기' if st.session_state.show_shop else '열기'} (E 키)", 
        on_click=toggle_shop, 
        type="primary" if st.session_state.show_shop else "secondary",
        use_container_width=True
    )
with col_btn2:
    st.button(
        f"🎰 도박장 {'닫기' if st.session_state.show_casino else '열기'}", 
        on_click=toggle_casino, 
        type="primary" if st.session_state.show_casino else "secondary",
        use_container_width=True
    )

# 6. 상점 UI
if st.session_state.show_shop:
    with st.expander("🛒 강화 상점", expanded=True):
        st.markdown(f"**클릭당 증가량 +1 강화**")
        st.write(f"- 필요 카운트: **{st.session_state.cost:,}**")
        st.write(f"- 구매 후 증가 수치: **+{st.session_state.per_click + 1:,}**")
        st.caption("🎲 구매 시 다음 비용이 랜덤 배율(2배/3배/5배/10배)로 상승합니다.")
        
        can_buy = st.session_state.count >= st.session_state.cost
        st.button(
            "구매하기", 
            on_click=buy_upgrade, 
            disabled=not can_buy,
            use_container_width=True
        )

# 7. 도박장 UI
if st.session_state.show_casino:
    with st.expander("🎰 행운의 도박장", expanded=True):
        st.markdown("**배팅 금액 및 남아있는 횟수**")
        st.caption("🎲 확률: 0.5배 (60%) | 2배 (29%) | 5배 (10%) | 10배 (1%) (1시간마다 횟수 리셋)")
        
        now = datetime.now()
        c1, c2, c3 = st.columns(3)
        
        for idx, amount in enumerate([100, 1000, 10000]):
            info = st.session_state.gamble_limits[amount]
            rem = info["remaining"]
            max_cnt = LIMIT_CONFIG[amount]
            
            # 리셋까지 남은 시간 계산
            time_left = info["reset_at"] - now
            minutes_left = int(time_left.total_seconds() // 60)
            
            target_col = [c1, c2, c3][idx]
            with target_col:
                st.write(f"**{amount:,} 배팅**")
                st.caption(f"남은 횟수: **{rem}/{max_cnt}**")
                if rem == 0:
                    st.caption(f"⏳ 리셋: {minutes_left}분 후")
                
                can_gamble = (st.session_state.count >= amount) and (rem > 0)
                st.button(
                    f"{amount:,} 배팅", 
                    key=f"gamble_btn_{amount}",
                    on_click=gamble, 
                    args=(amount,),
                    disabled=not can_gamble,
                    use_container_width=True
                )
