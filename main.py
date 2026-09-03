import streamlit as st

st.title("🔢 스페이스바 카운터")

# 카운트 상태 초기화
if "count" not in st.session_state:
    st.session_state.count = 0

# 카운트 증가 함수
def increment():
    st.session_state.count += 1

# 스페이스바 키 입력 감지 (Streamlit HTML/JS 주입)
st.components.v1.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.code === 'Space') {
            e.preventDefault();
            // 화면 내 버튼 찾아서 클릭 실행
            const btn = doc.querySelector('button[kind="primary"]');
            if (btn) btn.click();
        }
    });
    </script>
    """,
    height=0,
)

# UI 구성
st.metric(label="현재 카운트", value=st.session_state.count)
st.button("숫자 올리기 (Space 키 가능)", on_click=increment, type="primary")
