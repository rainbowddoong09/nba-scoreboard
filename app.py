import streamlit as st
import pandas as pd
from datetime import datetime
from nba_api.live.nba.endpoints import scoreboard

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="NBA 실시간 스코어보드",
    page_icon="🏀",
    layout="centered"
)

# 2. 헤더 및 제목
st.title("🏀 NBA 경기 결과 및 스코어보드")
st.caption("nba_api를 활용한 실시간 경기 정보 웹 앱")

# 3. 새로고침 버튼
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

# 5. 경기 정보 화면 표시
if not games:
    st.info("오늘 예정된 NBA 경기가 없거나 정보를 불러올 수 없습니다.")
else:
    st.subheader(f"📅 오늘 경기 목록 ({len(games)}경기)")
    
    for game in games:
        home_team = game['homeTeam']['teamName']
        home_score = game['homeTeam']['score']
        away_team = game['awayTeam']['teamName']
        away_score = game['awayTeam']['score']
        status = game['gameStatusText']
        
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                st.markdown(f"### {away_team}")
                st.markdown(f"# **{away_score}**")
                st.caption("원정 팀")
                
            with col2:
                st.write("")
                st.write("")
                st.markdown(f"**`{status}`**")
                st.write("VS")
                
            with col3:
                st.markdown(f"### {home_team}")
                st.markdown(f"# **{home_score}**")
                st.caption("홈 팀")
            
            st.markdown("---")
