import streamlit as st
from datetime import datetime
import json
import os
import pytz

st.set_page_config(
    page_title="위치 안내 시스템",
    page_icon="👩‍💻📍",
    layout="wide"
)

DATA_FILE = "location_data.json"

def load_location():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # 기본값도 한국 시간
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    time_str = now.strftime("%p %I시 %M분 %S초")
    time_str = time_str.replace("AM", "오전").replace("PM", "오후")
    
    return {
        "floor": "2층", 
        "updated": now.strftime("%Y-%m-%d") + " " + time_str
    }

def save_location(floor):
    # 한국 시간대 설정
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    
    # 오전/오후 형식으로 변환
    time_str = now.strftime("%p %I시 %M분 %S초")
    time_str = time_str.replace("AM", "오전").replace("PM", "오후")
    
    data = {
        "floor": floor, 
        "updated": now.strftime("%Y-%m-%d") + " " + time_str
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data

def load_timetable():
    """시간표 불러오기"""
    TIMETABLE_FILE = "timetable_data.json"
    if os.path.exists(TIMETABLE_FILE):
        try:
            with open(TIMETABLE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    # 기본 빈 시간표
    return {
        "월": ["", "", "", "", "", "", "", ""],
        "화": ["", "", "", "", "", "", "", ""],
        "수": ["", "", "", "", "", "", "", ""],
        "목": ["", "", "", "", "", "", "", ""],
        "금": ["", "", "", "", "", "", "", ""],
        "토": ["", "", "", "", "", "", "", ""]
    }

def save_timetable(timetable_data):
    """시간표 저장"""
    TIMETABLE_FILE = "timetable_data.json"
    with open(TIMETABLE_FILE, 'w', encoding='utf-8') as f:
        json.dump(timetable_data, f, ensure_ascii=False, indent=2)

if 'location_data' not in st.session_state:
    st.session_state.location_data = load_location()

query_params = st.query_params
mode = query_params.get("mode", ["display"])[0] if isinstance(query_params.get("mode"), list) else query_params.get("mode", "display")

st.markdown("""
    <style>
    * {
        box-sizing: border-box;
    }
    
    /* 크롬 UI 회피 */
    .block-container {
        padding: 0.5vh 1vw !important;
        margin: 0 !important;
        background: #fef9f3;
        max-width: 100% !important;
        min-height: 100vh;
    }
    
    .main .block-container {
        padding-top: 0.5rem !important;
    }
    
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 헤더 - vw/vh 기준 */
    .app-header {
        text-align: center;
        padding: 1.5vh 2vw;
        background: linear-gradient(135deg, #b8c5f2 0%, #d4b5d4 100%);
        margin: 0 0 1vh 0;
    }
    
    .app-title {
        font-size: clamp(16px, 2.5vw, 32px);
        font-weight: bold;
        color: #5a5a8f;
        margin: 0;
        line-height: 1.2;
    }
    
    .app-subtitle {
        font-size: clamp(10px, 1.5vw, 16px);
        color: #6b6b9f;
        margin-top: 0.5vh;
        line-height: 1.2;
    }
    
    /* 위치 박스 - 최대 높이 제한 */
    .display-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 0 !important;
    background: linear-gradient(135deg, #ffe4f0 0%, #ffd4e8 100%);
    border-radius: 15px;
    height: 100%;
    min-height: 25vh;
    max-height: 75vh;
    }

/* ⭐ 이 부분 추가 ⭐ */
    .display-container > * {
        margin: 0 !important;
        padding: 0 !important;
    }

    .location-text {
        font-size: clamp(18px, 3.5vw, 45px);
        font-weight: bold;
        color: #ff6b9d;
        text-align: center;
        margin: 0 !important;
        padding: 0 !important;
    }

    .floor-text {
        font-size: clamp(45px, 10vw, 130px);
        font-weight: bold;
        color: #ff1493;
        text-align: center;
        margin: 0 !important;
        padding: 0 !important;
        text-shadow: 0.3vw 0.3vw 0.6vw rgba(255, 20, 147, 0.3);
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .update-time {
        font-size: clamp(13px, 1.8vw, 22px);
        color: #ff6b9d;
        text-align: center;
        margin: 0 !important;
        padding: 0 !important;
        font-weight: 500;
    }
    
    /* 버튼 */
    .stButton > button {
        height: clamp(70px, 12vh, 130px) !important;
        font-size: clamp(28px, 4.5vw, 55px) !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #ffd4e8 0%, #ffb4d4 100%) !important;
        color: #ff1493 !important;
        border: 0.2vw solid #ffb4d4 !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ffb4d4 0%, #ff94c4 100%) !important;
        transform: translateY(-0.3vh);
    }
    
    /* 시간표 - 최대 높이 제한 */
    .timetable-container {
        margin: 0;
        background: #fff9fc;
        padding: 1vh 0.8vw;
        border-radius: 12px;
        height: 100%;
        max-height: 77vh;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    
    .timetable-title {
        font-size: clamp(13px, 2.2vw, 22px);
        font-weight: bold;
        color: #b88bb8;
        text-align: center;
        margin-bottom: 0.8vh;
        flex-shrink: 0;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 0;
        flex-grow: 1;
        table-layout: fixed;
    }
    
    th, td {
        border: 1px solid #d4b5d4 !important;
        padding: clamp(0.2vh, 0.4vh, 0.8vh) clamp(0.2vw, 0.4vw, 0.8vw) !important;
        text-align: center !important;
        font-size: clamp(7px, 1.1vw, 13px) !important;
        vertical-align: middle !important;
        line-height: 1.1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    th {
        background: linear-gradient(135deg, #d4b5d4 0%, #c4a5c4 100%) !important;
        color: #5a5a8f !important;
        font-weight: bold !important;
        text-align: center !important;
    }

    td {
        background: #fff9fc !important;
        text-align: center !important;
        color: #7a7a9f !important;
    }

    table th {
        text-align: center !important;
    }

    table tr > *:first-child {
        text-align: center !important;
        font-weight: bold;
    }
    
    /* 컬럼 간격 */
    [data-testid="column"] {
        padding: 0 0.4vw !important;
    }
    
    /* Streamlit 탭 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #fef9f3;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #b88bb8 !important;
        font-size: clamp(14px, 2vw, 20px) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffe4f0 !important;
        color: #ff1493 !important;
    }
    
    /* 전체 화면 높이 제한 */
    .main {
        max-height: 100vh;
        overflow: auto;
    }
    
    /* 초소형 세로 화면 (작은 폰) */
    @media (max-width: 480px) and (orientation: portrait) {
        .app-title {
            font-size: 14px !important;
            white-space: normal !important;
        }
        
        .app-subtitle {
            font-size: 9px !important;
        }
        
        .floor-text {
            font-size: 40px !important;
        }
        
        .location-text {
            font-size: 16px !important;
        }
        
        th, td {
            font-size: 7px !important;
            padding: 0.1rem !important;
        }
    }
    
    /* 초소형 가로 화면 (작은 태블릿 가로) */
    @media (max-height: 500px) and (orientation: landscape) {
        .app-header {
            padding: 0.5vh 1vw !important;
        }
        
        .app-title {
            font-size: 14px !important;
        }
        
        .app-subtitle {
            font-size: 9px !important;
        }
        
        .display-container {
            padding: 0.8vh 0.5vw !important;
            min-height: 20vh !important;
        }
        
        .floor-text {
            font-size: 50px !important;
            margin: 0.3vh 0 !important;
        }
        
        .location-text {
            font-size: 18px !important;
        }
        
        .update-time {
            font-size: 12px !important;
        }
        
        th, td {
            font-size: 7px !important;
            padding: 0.1vh 0.2vw !important;
        }
        
        .timetable-title {
            font-size: 12px !important;
            margin-bottom: 0.3vh !important;
        }
    }
    
    /* 중형 태블릿 세로 */
    @media (min-width: 481px) and (max-width: 768px) and (orientation: portrait) {
        .floor-text {
            font-size: clamp(60px, 12vw, 100px) !important;
        }
    }
    
    /* 중형 태블릿 가로 */
    @media (min-width: 769px) and (max-width: 1024px) and (orientation: landscape) {
        .floor-text {
            font-size: clamp(70px, 10vw, 120px) !important;
        }
        
        th, td {
            font-size: clamp(9px, 1.2vw, 12px) !important;
        }
    }

    /* Streamlit markdown 기본 여백 제거 */
    .stMarkdown {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 컬럼 내부 여백 제거 */
    [data-testid="column"] > div {
        padding: 0 !important;
    }
    
    /* element-container 여백 제거 */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }

    </style>
""", unsafe_allow_html=True)

if mode == "control":
    st.markdown("""
        <div class="app-header">
            <div class="app-title">📍👩‍💻성아쌤은 지금 어디에?(관리자페이지)</div>
            <div class="app-subtitle">선생님의 현재 위치를 실시간으로 안내합니다.</div>
        </div>
    """, unsafe_allow_html=True)

    # 탭으로 위치/시간표 구분
    tab1, tab2 = st.tabs(["📍 위치 변경", "📅 시간표 수정"])
    
    # 탭1: 위치 변경
    with tab1:
        st.title("위치 변경 컨트롤")
        current_data = load_location()
        st.info(f"🏢 **현재 위치: {current_data['floor']}**  \n⏰ 마지막 업데이트: {current_data['updated']}")
        st.divider()

        col1, col2, col3, col4 = st.columns(4)
    
        with col1:
            if st.button("1️⃣\n\n1층", use_container_width=True, type="primary", key="btn1"):
                st.session_state.location_data = save_location("1층(컴퓨터실)")
                st.success("✅ 1층으로 변경!")
                st.balloons()
                st.rerun()
    
        with col2:
            if st.button("2️⃣\n\n2층", use_container_width=True, type="primary", key="btn2"):
                st.session_state.location_data = save_location("2층(본교무실)")
                st.success("✅ 2층으로 변경!")
                st.balloons()
                st.rerun()
    
        with col3:
            if st.button("3️⃣\n\n3층", use_container_width=True, type="primary", key="btn3"):
                st.session_state.location_data = save_location("3층(2학년 수업)")
                st.success("✅ 3층으로 변경!")
                st.balloons()
                st.rerun()

        with col4:
            if st.button("4️⃣\n\n4층", use_container_width=True, type="primary", key="btn4"):
                st.session_state.location_data = save_location("4층(1학년 교무실/2반)")
                st.success("✅ 4층으로 변경!")
                st.balloons()
                st.rerun()
    
    # 탭2: 시간표 수정
    with tab2:
        st.subheader("📝 시간표 수정")
        
        timetable_data = load_timetable()
        
        if 'temp_timetable' not in st.session_state:
            st.session_state.temp_timetable = timetable_data.copy()
        
        days = ["월", "화", "수", "목", "금", "토"]
        
        for day in days:
            with st.expander(f"📆 {day}요일", expanded=False):
                for i in range(8):
                    key = f"{day}_{i}"
                    st.session_state.temp_timetable[day][i] = st.text_input(
                        f"{i+1}교시", 
                        value=st.session_state.temp_timetable[day][i],
                        key=key
                    )
        
        col_save, col_reset = st.columns(2)
        
        with col_save:
            if st.button("💾 저장", use_container_width=True, type="primary"):
                save_timetable(st.session_state.temp_timetable)
                st.success("✅ 시간표가 저장되었습니다!")
                st.balloons()
        
        with col_reset:
            if st.button("🔄 초기화", use_container_width=True):
                st.session_state.temp_timetable = load_timetable()
                st.warning("⚠️ 시간표가 초기화되었습니다")
                st.rerun()
    
    with st.expander("ℹ️ 사용 방법"):
        st.markdown("""
        ### 사용 방법
        1. 이동할 층의 버튼을 누르세요
        2. 태블릿 화면이 자동으로 업데이트됩니다 (5초 이내)
        아
        ### 팁
        - 이 페이지를 휴대폰 홈 화면에 추가하세요
        """)

else:
    st.markdown("""
        <div class="app-header">
            <div class="app-title">📍👩‍💻성아쌤은 지금 어디에?</div>
            <div class="app-subtitle">위치 안내 주기: 최대 5초<br>💡동선이 겹치면 부재중일 수 있습니다.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2열 레이아웃: 위치(2) | 시간표(1)
    col_left, col_right = st.columns([2, 1])
    
    # 왼쪽: 현재 위치
    with col_left:
        current_data = load_location()
        # 안전한 시간 추출
        full_updated = current_data.get("updated", "")
        if full_updated and " " in full_updated:
            date_part, time_part = full_updated.split(" ", 1)
            update_time = time_part
        else:
            update_time = full_updated if full_updated else "시간 정보 없음"
    
         # 층별 색상
        floor_colors = {
            "1층": {"bg": "linear-gradient(135deg, #ffd4e8 0%, #ffc4d8 100%)", "main": "#ff1493", "sub": "#ff6b9d"},
            "2층": {"bg": "linear-gradient(135deg, #d4e8ff 0%, #c4d8ff 100%)", "main": "#1e90ff", "sub": "#4da6ff"},
            "3층": {"bg": "linear-gradient(135deg, #e8ffd4 0%, #d8ffc4 100%)", "main": "#32cd32", "sub": "#5ed65e"},
            "4층": {"bg": "linear-gradient(135deg, #ffe8d4 0%, #ffd8c4 100%)", "main": "#ff8c00", "sub": "#ffaa33"},
        }
    
        floor_key = current_data["floor"].split("(")[0] if "(" in current_data["floor"] else current_data["floor"]
        c = floor_colors.get(floor_key, {"bg": "linear-gradient(135deg, #ffe4f0 0%, #ffd4e8 100%)", "main": "#ff1493", "sub": "#ff6b9d"})
    
        # 층별 동적 CSS
        st.markdown(f"""
            <style>
            .current-floor-bg {{ background: {c["bg"]} !important; }}
            .current-floor-main {{ color: {c["main"]} !important; text-shadow: 0.3vw 0.3vw 0.6vw rgba(0,0,0,0.2) !important; }}
            .current-floor-sub {{ color: {c["sub"]} !important; }}
            </style>
        """, unsafe_allow_html=True)
    
        st.markdown(f'''
            <div class="display-container current-floor-bg">
                <div class="location-text current-floor-sub">현재 위치</div>
                <div class="floor-text current-floor-main">{current_data["floor"]}</div>
                <div class="update-time current-floor-sub">업데이트: {update_time}</div>
            </div>
        ''', unsafe_allow_html=True)
        
    # 오른쪽: 시간표
    # 오른쪽: 시간표 + 네트워크 상태
    with col_right:
        st.markdown('<div class="timetable-container">', unsafe_allow_html=True)
        st.markdown('<div class="timetable-title">📅 1학기 시간표</div>', unsafe_allow_html=True)
        
        timetable_data = load_timetable()
        
        # 시간표 HTML 생성
        table_html = """
        <table>
            <tr>
                <th>교시</th>
                <th>월</th>
                <th>화</th>
                <th>수</th>
                <th>목</th>
                <th>금</th>
                <th>토</th>
            </tr>
        """
        
        for i in range(8):
            table_html += f"<tr><th>{i+1}</th>"
            for day in ["월", "화", "수", "목", "금", "토"]:
                subject = timetable_data[day][i] if i < len(timetable_data[day]) else ""
                table_html += f"<td>{subject}</td>"
            table_html += "</tr>"
        
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)
        
         # 네트워크 상태
        st.markdown("""
            <div id="network-status-ok" style="text-align: center; margin-top: 0.5vh; padding: 0.8vh; background: #d4f4dd; color: #2d8659; border-radius: 8px; font-size: clamp(11px, 1.5vw, 14px); font-weight: bold;">
                ✅ 네트워크 원활
            </div>
            
            <div id="network-status-error" style="text-align: center; margin-top: 0.5vh; padding: 0.8vh; background: #ffe4e4; color: #ff1493; border-radius: 8px; display: none; font-size: clamp(11px, 1.5vw, 14px); font-weight: bold;">
                ⚠️ 네트워크 연결 안됨. 선생님께 문의
            </div>
            
            <script>
            function updateNetworkStatus() {
                const statusOk = document.getElementById('network-status-ok');
                const statusError = document.getElementById('network-status-error');
                
                if (navigator.onLine) {
                    statusOk.style.display = 'block';
                    statusError.style.display = 'none';
                } else {
                    statusOk.style.display = 'none';
                    statusError.style.display = 'block';
                }
            }
            
            // 1. 페이지 로드 시 체크
            updateNetworkStatus();
            
            // 2. 네트워크 상태 변경 시 즉시 반영
            window.addEventListener('online', updateNetworkStatus);
            window.addEventListener('offline', updateNetworkStatus);
            </script>
        """, unsafe_allow_html=True)

        import time
        time.sleep(5)
        st.rerun()
    
    st.markdown("""
        <script>
        setTimeout(function(){window.location.reload();}, 5000);
        </script>
    """, unsafe_allow_html=True)