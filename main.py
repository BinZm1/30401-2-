import streamlit as st
import random
import time
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

# 🤖 오토클릭 관련 세션 상태
if "auto_interval" not in st.session_state:
    st.session_state.auto_interval = 1.0  # 기본 1초
if "auto_per_sec" not in st.session_state:
    st.session_state.auto_per_sec = 1     # 기본 1회당 +1
if "auto_speed_cost" not in st.session_state:
    st.session_state.auto_speed_cost = 5000  # 속도 증가 초기 비용
if "auto_power_cost" not in st.session_state:
    st.session_state.auto_power_cost = 10000 # 클릭량 증가 초기 비용
if "last_auto_time" not in st.session_state:
    st.session_state.last_auto_time = time.time()

# 🎰 도박 횟수 및 쿨타임 초기화
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

# 2. 오토클릭 주기적 반영 로직
current_time = time.time()
elapsed = current_time - st.session_state.last_auto_time
if elapsed >= st.session_state.auto_interval:
    ticks = int(elapsed // st.session_state.auto_interval)
    st.session_state.count += ticks * st.session_state.auto_per_sec
    st.session_state.last_auto_time = current_time - (elapsed % st.session_state.auto_interval)

# 3. 쿨타임 및 리셋 체크 함수
def check_and_reset_limits():
    now = datetime.now()
    for amount, config in st.session_state.gamble_limits.items():
        if now >= config["reset_at"]:
            config["remaining"] = LIMIT_CONFIG[amount]
            config["reset_at"] = now + timedelta(hours=1)

check_and_reset_limits()

# 4. 로직 함수
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
        st.toast(f"🎉 클릭 강화 성공! (다음 비용 {chosen_multiplier}배 상승)")
    else:
        st.toast("❌ 카운트가 부족합니다!")

def buy_auto_speed():
    if st.session_state.count >= st.session_state.auto_speed_cost:
        if st.session_state.auto_interval <= 0.1:
            st.toast("⚡ 이미 최고 속도(0.1초)에 도달했습니다!")
            return
        st.session_state.count -= st.session_state.auto_speed_cost
        st.session_state.auto_interval = round(st.session_state.auto_interval - 0.1, 1)
        st.session_state.auto_speed_cost = int(st.session_state.auto_speed_cost * 1.5)
        st.toast(f"⚡ 오토클릭 속도 증가! (현재 주기: {st.session_state.auto_interval:.1f}초)")
    else:
        st.toast("❌ 카운트가 부족합니다!")

def buy_auto_power():
    if st.session_state.count >= st.session_state.auto_power_cost:
        st.session_state.count -= st.session_state.auto_power_cost
        st.session_state.auto_per_sec += 1
        st.session_state.auto_power_cost *= 2
        st.toast(f"🤖 오토클릭 수치 증가! (현재 자동 획득량: +{st.session_state.auto_per_sec:,})")
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
        limit_info["remaining"] -= 1
        
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

# 5. 키보드 이벤트 처리 (DOM 클릭 방식)
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

# 6. UI 구성
st.title("🔢 스페이스 카운터")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("현재 카운트", f"{st.session_state.count:,}")
with col2:
    st.metric("1회 클릭당", f"+{st.session_state.per_click:,}")
with col3:
    st.metric("오토 클릭", f"+{st.session_state.auto_per_sec:,} / {st.session_state.auto_interval:.1f}초")

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

# 7. 상점 UI
if st.session_state.show_shop:
    with st.expander("🛒 강화 상점", expanded=True):
        # 수동 클릭 강화
        st.markdown("**1. 클릭당 증가량 +1 강화**")
        st.write(f"- 필요 카운트: **{st.session_state.cost:,}**")
        st.write(f"- 구매 후 수치: **+{st.session_state.per_click + 1:,}**")
        st.caption("🎲 다음 비용이 랜덤 배율(2배/3배/5배/10배)로 상승합니다.")
        can_buy_click = st.session_state.count >= st.session_state.cost
        st.button(
            "클릭 강화 구매", 
            key="buy_click_btn",
            on_click=buy_upgrade, 
            disabled=not can_buy_click,
            use_container_width=True
        )

        st.write("---")

        # 오토클릭 속도 강화
        st.markdown("**2. ⚡ 오토클릭 속도 강화 (-0.1초)**")
        st.write(f"- 필요 카운트: **{st.session_state.auto_speed_cost:,}**")
        st.write(f"- 현재 주기: **{st.session_state.auto_interval:.1f}초** → 구매 후: **{max(0.1, round(st.session_state.auto_interval - 0.1, 1)):.1f}초**")
        st.caption("📈 구매 시마다 다음 비용이 50%씩 증가합니다. (최대 0.1초까지 단축 가능)")
        can_buy_speed = (st.session_state.count >= st.session_state.auto_speed_cost) and (st.session_state.auto_interval > 0.1)
        st.button(
            "속도 강화 구매", 
            key="buy_speed_btn",
            on_click=buy_auto_speed, 
            disabled=not can_buy_speed,
            use_container_width=True
        )

        st.write("---")

        # 오토클릭 클릭량 강화
        st.markdown("**3. 🤖 오토클릭 클릭량 강화 (+1)**")
        st.write(f"- 필요 카운트: **{st.session_state.auto_power_cost:,}**")
        st.write(f"- 현재 획득량: **+{st.session_state.auto_per_sec:,}** → 구매 후: **+{st.session_state.auto_per_sec + 1:,}**")
        st.caption("📈 구매 시마다 다음 비용이 2배씩 증가합니다.")
        can_buy_power = st.session_state.count >= st.session_state.auto_power_cost
        st.button(
            "클릭량 강화 구매", 
            key="buy_power_btn",
            on_click=buy_auto_power, 
            disabled=not can_buy_power,
            use_container_width=True
        )

# 8. 도박장 UI
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
