import streamlit as st
from datetime import datetime
import json
import os

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
    return {"floor": "2층", "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

def save_location(floor):
    data = {"floor": floor, "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
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
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        background: #fef9f3;
    }
    
    header[data-testid="stHeader"] {
        display: none;
    }
    
    .app-header {
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: linear-gradient(135deg, #b8c5f2 0%, #d4b5d4 100%);
        border-radius: 0;
        margin: 0;
        margin-bottom: 2rem;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .app-title {
        font-size: clamp(26px, 5vw, 36px);
        font-weight: bold;
        color: #5a5a8f;
        margin: 0;
        line-height: 1.5;
        padding: 0.5rem 1.5rem;
        white-space: nowrap;
    }
    
    .app-subtitle {
        font-size: clamp(14px, 3vw, 18px);
        color: #6b6b9f;
        margin-top: 0.5rem;
        line-height: 1.6;
        padding: 0.3rem 1.5rem;
    }
    
    .display-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #ffe4f0 0%, #ffd4e8 100%);
        border-radius: 20px;
    }
    
    .location-text {
        font-size: 60px;
        font-weight: bold;
        color: #ff6b9d;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .floor-text {
        font-size: 180px;
        font-weight: bold;
        color: #ff1493;
        text-align: center;
        margin: 1rem 0;
        text-shadow: 4px 4px 8px rgba(255, 20, 147, 0.3);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .update-time {
        font-size: 28px;
        color: #ff6b9d;
        text-align: center;
        margin-top: 1rem;
        font-weight: 500;
    }
    
    .stButton > button {
        height: 150px;
        font-size: 60px;
        font-weight: bold;
        border-radius: 15px;
        background: linear-gradient(135deg, #ffd4e8 0%, #ffb4d4 100%) !important;
        color: #ff1493 !important;
        border: 3px solid #ffb4d4 !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ffb4d4 0%, #ff94c4 100%) !important;
        transform: translateY(-3px);
    }
    
    /* 시간표 스타일 */
    .timetable-container {
        margin-top: 2rem;
        background: #fff9fc;
        padding: 1rem;
        border-radius: 15px;
    }
    
    .timetable-title {
        font-size: clamp(20px, 4vw, 28px);
        font-weight: bold;
        color: #b88bb8;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem auto;
    }
    
    th, td {
        border: 2px solid #d4b5d4 !important;
        padding: clamp(0.3rem, 1vw, 0.5rem) !important;
        text-align: center !important;
        font-size: clamp(10px, 2vw, 14px) !important;
        vertical-align: middle !important;
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

    /* 모든 테이블 헤더 강제 가운데 정렬 */
    table th {
        text-align: center !important;
    }

    /* 첫 번째 열(교시) 가운데 정렬 */
    table tr > *:first-child {
        text-align: center !important;
    }
    
    /* Streamlit 기본 스타일 오버라이드 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #fef9f3;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #b88bb8 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffe4f0 !important;
        color: #ff1493 !important;
    }
    
    /* 모바일 반응형 */
    @media (max-width: 768px) {
        .app-title {font-size: 28px;}
        .app-subtitle {font-size: 14px;}
        .floor-text {font-size: clamp(80px, 15vw, 120px) !important;}
        .location-text {font-size: clamp(30px, 6vw, 40px) !important;}
        .update-time {font-size: clamp(16px, 3vw, 20px) !important;}
        .stButton > button {height: 100px; font-size: 40px;}
        
        .timetable-title {
            font-size: clamp(18px, 4vw, 24px) !important;
        }
        
        th, td {
            font-size: clamp(8px, 1.5vw, 12px) !important;
            padding: clamp(0.2rem, 1vw, 0.3rem) !important;
        }
        
        table {
            font-size: clamp(8px, 1.5vw, 12px) !important;
        }
    }
    
    /* 태블릿 가로 모드 */
    @media (min-width: 769px) and (max-width: 1024px) {
        .floor-text {font-size: clamp(120px, 18vw, 160px) !important;}
        .location-text {font-size: clamp(40px, 7vw, 55px) !important;}
        .update-time {font-size: clamp(20px, 3.5vw, 26px) !important;}
        
        th, td {
            font-size: clamp(10px, 1.8vw, 13px) !important;
            padding: clamp(0.3rem, 1vw, 0.4rem) !important;
        }
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
        st.markdown('<div class="display-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="location-text">현재 위치</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="floor-text">{current_data["floor"]}</div>', unsafe_allow_html=True)
        update_time = current_data["updated"].split()[1] if " " in current_data["updated"] else current_data["updated"]
        st.markdown(f'<div class="update-time">업데이트: {update_time}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 오른쪽: 시간표
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
        st.markdown('</div>', unsafe_allow_html=True)

        import time
        time.sleep(5)
        st.rerun()
    
    st.markdown("""
        <script>
        setTimeout(function(){window.location.reload();}, 5000);
        </script>
    """, unsafe_allow_html=True)