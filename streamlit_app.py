import streamlit as st
import time
import random
import streamlit.components.v1 as components

# 1. 화면 기본 설정 (검은 배경, 모바일 최적화)
st.set_page_config(
    page_title="수면 패턴 분석기",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 디자인 (CSS): 검은 배경, 큰 글씨
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .big-emoji {
        font-size: 100px;
        text-align: center;
        margin-bottom: 20px;
    }
    .status-text {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        color: #4facfe;
    }
    .metric-label {
        font-size: 14px;
        color: #888;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 자바스크립트 센서 연결 (브라우저에서 센서 권한 요청)
# 참고: 실제 센서값 전송은 보안(HTTPS) 문제로 복잡하여, 여기서는 '센서가 작동 중'임만 확인합니다.
js_sensor_code = """
<script>
// 화면 꺼짐 방지 (Wake Lock)
let wakeLock = null;
async function requestWakeLock() {
  try {
    wakeLock = await navigator.wakeLock.request('screen');
    console.log('화면 켜짐 유지 중...');
  } catch (err) {
    console.log('Wake Lock Error:', err);
  }
}
requestWakeLock();

// 마이크/가속도 권한 요청 (작동 확인용)
navigator.mediaDevices.getUserMedia({ audio: true })
.then(function(stream) {
    console.log('마이크 권한 허용됨');
})
.catch(function(err) {
    console.log('마이크 권한 필요');
});
</script>
"""
components.html(js_sensor_code, height=0)

# 4. 메인 화면 로직 (깜빡임 방지 기능 적용)
# @st.fragment: 이 부분만 1초마다 새로고침 됩니다 (전체 화면 리로드 X)
@st.fragment(run_every=1)
def run_sleep_monitor():
    # --- [데이터 생성 파트] ---
    # 초보자를 위해 실제 센서 연결 대신, 실제처럼 보이는 '가짜 데이터'를 만듭니다.
    # 나중에 실력이 늘면 이 부분을 실제 센서 데이터로 바꾸면 됩니다!
    
    movement = random.uniform(0, 10)  # 움직임 (0~10)
    noise = random.uniform(20, 80)    # 소음 (20~80dB)
    
    # --- [수면 단계 분석 로직] ---
    status = ""
    emoji = ""
    status_color = ""
    
    if movement > 8:
        status = "기상 (Wake)"
        emoji = "👀"
        status_color = "#ff4b4b" # 빨강
    elif movement > 3:
        status = "얕은 잠 (Light)"
        emoji = "🛌"
        status_color = "#ffa500" # 주황
    else:
        if noise > 50:
            status = "렘 수면 (REM)"
            emoji = "🧠"
            status_color = "#bf00ff" # 보라
        else:
            status = "깊은 잠 (Deep)"
            emoji = "😴"
            status_color = "#00c853" # 초록

    # --- [화면 표시 파트] ---
    st.markdown(f'<div class="big-emoji">{emoji}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="status-text" style="color:{status_color}">{status}</div>', unsafe_allow_html=True)
    
    # 여백
    st.write("") 
    st.write("")

    # 데이터 그래프 (최근 상황)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-label">움직임 강도</div>', unsafe_allow_html=True)
        st.progress(min(movement / 10, 1.0)) # 게이지 바
    with col2:
        st.markdown('<div class="metric-label">주변 소음 (dB)</div>', unsafe_allow_html=True)
        st.progress(min(noise / 100, 1.0))   # 게이지 바

# 5. 앱 실행
st.title("🌙 Sleep AI Monitor")
st.caption("초보자용 프로토타입 (Simulation Mode)")

# 위에서 만든 화면 함수 실행
run_sleep_monitor()