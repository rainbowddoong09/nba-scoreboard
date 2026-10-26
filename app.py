import streamlit as st
import pandas as pd
from nba_api.live.nba.endpoints import scoreboard

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="NBA 실시간 스코어보드",
    page_icon="🏀",
    layout="centered"
)

# 2. 커스텀 CSS (부드럽게 빛나는 둥근 팀 로고 및 카드 스타일)
st.markdown("""
    <style>
    /* 팀 로고 스타일: 동그랗고 부드럽게 빛나는 효과 */
    .glowing-logo {
        width: 90px;
        height: 90px;
        border-radius: 50%; /* 완전한 원형 */
        object-fit: contain;
        background: rgba(255, 255, 255, 0.05); /* 은은한 배경 */
        padding: 8px;
        
        /* 둥글고 부드럽게 빛나는 그림자 효과 (Glow) */
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.25),
                    0 0 30px rgba(255, 165, 0, 0.2); 
        
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    /* 마우스 호버 시 살짝 확대되며 더 밝게 빛남 */
    .glowing-logo:hover {
        transform: scale(1.08);
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.4),
                    0 0 40px rgba(255, 165, 0, 0.4);
    }

    /* 팀 카드 레이아웃 정렬 */
    .team-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    
    .team-name {
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 2px;
    }
    
    .score-text {
        font-size: 2.5rem;
        font-weight: 900;
        color: #FF9F43;
    }
    
    .vs-text {
        font-size: 1.1rem;
        font-weight: bold;
        color: #888;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 헤더
st.title("🏀 NBA 경기 결과 및 스코어보드")
st.caption("실시간 스코어와 부드럽게 빛나는 팀 로고")

if st.button("🔄 스코어 새로고침"):
    st.rerun()

st.markdown("---")

# 4. 데이터 불러오기 함수
@st.cache_data(ttl=60)
def fetch_nba_scores():
    try:
        board = scoreboard.ScoreBoard()
        games = board.games.get_dict()
        return games
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return []

games = fetch_nba_scores()

# 5. 경기 정보 및 로고 화면 표시
if not games:
    st.info("오늘 예정된 NBA 경기가 없거나 정보를 불러올 수 없습니다.")
else:
    st.subheader(f"📅 오늘 경기 목록 ({len(games)}경기)")
    
    for game in games:
        # 팀 정보 및 로고 URL 생성 (NBA 공식 CDN)
        home_id = game['homeTeam']['teamId']
        home_name = game['homeTeam']['teamName']
        home_score = game['homeTeam']['score']
        home_logo = f"https://cdn.nba.com/logos/nba/{home_id}/global/L/logo.svg"
        
        away_id = game['awayTeam']['teamId']
        away_name = game['awayTeam']['teamName']
        away_score = game['awayTeam']['score']
        away_logo = f"https://cdn.nba.com/logos/nba/{away_id}/global/L/logo.svg"
        
        status = game['gameStatusText']
        
        # 경기 카드 구성 (3개의 컬럼)
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 2])
            
            # 원정 팀 (Away)
            with col1:
                st.markdown(f"""
                <div class="team-box">
                    <img src="{away_logo}" class="glowing-logo" alt="{away_name}">
                    <div class="team-name">{away_name}</div>
                    <div class="score-text">{away_score}</div>
                    <span style="font-size: 0.8rem; color: #888;">AWAY</span>
                </div>
                """, unsafe_allow_html=True)
                
            # 경기 상태 및 VS
            with col2:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="margin-top: 15px; font-weight: bold; color: #00D2D3;">`{status}`</div>
                    <div class="vs-text">VS</div>
                </div>
                """, unsafe_allow_html=True)
                
            # 홈 팀 (Home)
            with col3:
                st.markdown(f"""
                <div class="team-box">
                    <img src="{home_logo}" class="glowing-logo" alt="{home_name}">
                    <div class="team-name">{home_name}</div>
                    <div class="score-text">{home_score}</div>
                    <span style="font-size: 0.8rem; color: #888;">HOME</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
