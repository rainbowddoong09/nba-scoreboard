import streamlit as st
import pandas as pd
from nba_api.live.nba.endpoints import scoreboard

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="NBA 실시간 스코어보드",
    page_icon="🏀",
    layout="centered"
)

# 2. 커스텀 CSS (빛나는 로고 + 말풍선 & 선수 프로필 스타일)
st.markdown("""
    <style>
    /* 팀 로고 스타일: 동그랗고 부드럽게 빛나는 효과 */
    .glowing-logo {
        width: 85px;
        height: 85px;
        border-radius: 50%;
        object-fit: contain;
        background: rgba(255, 255, 255, 0.05);
        padding: 8px;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.25),
                    0 0 30px rgba(255, 165, 0, 0.2); 
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
    }
    
    .glowing-logo:hover {
        transform: scale(1.08);
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.4),
                    0 0 40px rgba(255, 165, 0, 0.4);
    }

    /* 팀 카드 */
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
        margin-top: 8px;
    }
    
    .score-text {
        font-size: 2.3rem;
        font-weight: 900;
        color: #FF9F43;
    }

    /* 클릭 시 펼쳐지는 아코디언 */
    details {
        width: 100%;
        margin-top: 10px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 8px 10px;
    }
    
    summary {
        font-size: 0.85rem;
        color: #FF9F43;
        cursor: pointer;
        font-weight: bold;
        list-style: none;
        text-align: center;
    }
    
    summary::-webkit-details-marker {
        display: none;
    }

    /* 선수 프로필 및 말풍선 레이아웃 */
    .player-profile-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 10px;
        background: rgba(0, 0, 0, 0.25);
        padding: 12px;
        border-radius: 10px;
    }

    .player-headshot {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        object-fit: cover;
        background: #1e1e1e;
        border: 2px solid #FF9F43;
        margin-bottom: 6px;
    }

    /* 말풍선 디자인 */
    .speech-bubble {
        position: relative;
        background: #262730;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 0.82rem;
        color: #E0E0E0;
        text-align: center;
        margin-top: 6px;
        border: 1px solid rgba(255, 159, 67, 0.4);
        font-style: italic;
    }

    .speech-bubble:after {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        width: 0;
        height: 0;
        border: 6px solid transparent;
        border-bottom-color: #262730;
        border-top: 0;
        margin-left: -6px;
        margin-top: -6px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 헤더
st.title("🏀 NBA 경기 결과 및 스코어보드")
st.caption("팀 최다 득점자를 누르면 선수의 프로필 사진과 한마디 대사를 볼 수 있습니다.")

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

# 5. 최다 득점자 정보 및 사진/대사 생성 함수
def get_top_scorer_info(team_data):
    leaders = team_data.get('leaders')
    if leaders and 'points' in leaders and leaders['points']:
        player = leaders['points']
        name = player.get('name', '선수 정보 없음')
        pts = player.get('value', 0)
        person_id = player.get('personId')
        
        # 공식 NBA 헤드샷 이미지 URL (기본 프로필 대체 이미지 포함)
        if person_id:
            headshot_url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{person_id}.png"
        else:
            headshot_url = "https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png"
            
        # 득점에 따른 재밌는 선수 대사 생성
        if pts >= 30:
            quote = f"🔥 오늘 감 잡았어! 혼자서 {pts}점 폭격 중!"
        elif pts >= 20:
            quote = f"⚡ 내가 오늘 팀 득점 책임지는 중 ({pts}득점)"
        elif pts > 0:
            quote = f"🏀 오늘 팀에서 가장 많이 넣은 {pts}점 기록 중!"
        else:
            quote = "경기 준비 완료! 곧 코트를 지배해 줄게."
            
        return name, pts, headshot_url, quote
        
    return "경기 전 / 준비 중", 0, "https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png", "오늘도 승리를 위해 뛴다!"

# 6. 경기 정보 화면 표시
if not games:
    st.info("오늘 예정된 NBA 경기가 없거나 정보를 불러올 수 없습니다.")
else:
    st.subheader(f"📅 오늘 경기 목록 ({len(games)}경기)")
    
    for game in games:
        # 원정팀
        away_id = game['awayTeam']['teamId']
        away_name = game['awayTeam']['teamName']
        away_score = game['awayTeam']['score']
        away_logo = f"https://cdn.nba.com/logos/nba/{away_id}/global/L/logo.svg"
        away_p_name, away_p_pts, away_p_img, away_p_quote = get_top_scorer_info(game['awayTeam'])
        
        # 홈팀
        home_id = game['homeTeam']['teamId']
        home_name = game['homeTeam']['teamName']
        home_score = game['homeTeam']['score']
        home_logo = f"https://cdn.nba.com/logos/nba/{home_id}/global/L/logo.svg"
        home_p_name, home_p_pts, home_p_img, home_p_quote = get_top_scorer_info(game['homeTeam'])
        
        status = game['gameStatusText']
        
        # 경기 카드 구성
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 2])
            
            # 원정 팀 (Away)
            with col1:
                st.markdown(f"""
                <div class="team-box">
                    <img src="{away_logo}" class="glowing-logo" alt="{away_name}">
                    <div class="team-name">{away_name}</div>
                    <div class="score-text">{away_score}</div>
                    <span style="font-size: 0.75rem; color: #888;">AWAY</span>
                </div>
                <details>
                    <summary>🔥 팀 최다 득점자 보기</summary>
                    <div class="player-profile-container">
                        <img src="{away_p_img}" class="player-headshot" onerror="this.src='https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png'">
                        <div style="font-weight: bold; font-size: 0.9rem;">{away_p_name}</div>
                        <div style="color: #FF9F43; font-weight: bold; font-size: 0.85rem;">{away_p_pts} PTS</div>
                        <div class="speech-bubble">"{away_p_quote}"</div>
                    </div>
                </details>
                """, unsafe_allow_html=True)
                
            # 경기 상태 및 VS
            with col2:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="margin-top: 20px; font-weight: bold; color: #00D2D3;">`{status}`</div>
                    <div style="font-size: 1.1rem; font-weight: bold; color: #888; margin-top: 15px;">VS</div>
                </div>
                """, unsafe_allow_html=True)
                
            # 홈 팀 (Home)
            with col3:
                st.markdown(f"""
                <div class="team-box">
                    <img src="{home_logo}" class="glowing-logo" alt="{home_name}">
                    <div class="team-name">{home_name}</div>
                    <div class="score-text">{home_score}</div>
                    <span style="font-size: 0.75rem; color: #888;">HOME</span>
                </div>
                <details>
                    <summary>🔥 팀 최다 득점자 보기</summary>
                    <div class="player-profile-container">
                        <img src="{home_p_img}" class="player-headshot" onerror="this.src='https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png'">
                        <div style="font-weight: bold; font-size: 0.9rem;">{home_p_name}</div>
                        <div style="color: #FF9F43; font-weight: bold; font-size: 0.85rem;">{home_p_pts} PTS</div>
                        <div class="speech-bubble">"{home_p_quote}"</div>
                    </div>
                </details>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
