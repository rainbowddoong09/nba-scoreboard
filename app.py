<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NBA 실시간 스코어보드</title>
  <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-color: #F5F2EB;
      --card-bg: #FAF8F5;
      --card-border: #E8E2D5;
      --text-main: #2C2A29;
      --text-muted: #7A7571;
      --accent-orange: #E65100;
      --accent-soft: #FFF3E0;
      --accent-green: #2E7D32;
      --shadow-sm: 0 4px 12px rgba(44, 42, 41, 0.05);
      --shadow-hover: 0 12px 28px rgba(230, 81, 0, 0.15);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }

    body {
      background-color: var(--bg-color);
      color: var(--text-main);
      padding: 30px 20px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .container {
      width: 100%;
      max-width: 680px;
    }

    header {
      text-align: center;
      margin-bottom: 25px;
    }

    header h1 {
      font-size: 2rem;
      font-weight: 900;
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }

    header p {
      color: var(--text-muted);
      font-size: 0.95rem;
      margin-top: 6px;
    }

    .controls {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }

    .status-badge {
      font-size: 0.85rem;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 20px;
      background: #EFECE6;
      color: var(--text-muted);
    }

    .refresh-btn {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 8px 16px;
      border-radius: 20px;
      font-weight: 700;
      font-size: 0.85rem;
      cursor: pointer;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .refresh-btn:hover {
      background: var(--accent-orange);
      color: #FFF;
      border-color: var(--accent-orange);
      transform: translateY(-2px);
    }

    .games-list {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .game-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
      box-shadow: var(--shadow-sm);
    }

    .matchup {
      display: grid;
      grid-template-columns: 1fr 100px 1fr;
      align-items: center;
      text-align: center;
    }

    .team-box {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .logo-wrapper {
      width: 85px;
      height: 85px;
      border-radius: 50%;
      background: #FFFFFF;
      border: 2px solid var(--card-border);
      padding: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow-sm);
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .logo-wrapper img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }

    .team-box:hover .logo-wrapper {
      transform: translateY(-6px) scale(1.05);
      border-color: var(--accent-orange);
      box-shadow: var(--shadow-hover);
    }

    .team-name {
      font-size: 1.1rem;
      font-weight: 800;
      margin-top: 10px;
    }

    .score {
      font-size: 2.2rem;
      font-weight: 900;
      color: var(--accent-orange);
      margin-top: 2px;
    }

    .team-type {
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-muted);
      letter-spacing: 1px;
    }

    .status-box {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
    }

    .game-status {
      font-size: 0.85rem;
      font-weight: 800;
      color: var(--accent-green);
      background: #E8F5E9;
      padding: 4px 10px;
      border-radius: 12px;
    }

    .vs-text {
      font-size: 1.2rem;
      font-weight: 900;
      color: var(--card-border);
    }

    details {
      margin-top: 18px;
      border-top: 1px dashed var(--card-border);
      padding-top: 14px;
    }

    summary {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--accent-orange);
      cursor: pointer;
      text-align: center;
      list-style: none;
    }

    summary::-webkit-details-marker {
      display: none;
    }

    .player-card {
      background: #FFFFFF;
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 14px;
      margin-top: 10px;
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .player-headshot {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      object-fit: cover;
      background: #F5F2EB;
      border: 2px solid var(--accent-orange);
      flex-shrink: 0;
    }

    .player-info {
      flex: 1;
      text-align: left;
    }

    .player-name {
      font-size: 0.95rem;
      font-weight: 800;
    }

    .player-stat {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--accent-orange);
      margin-bottom: 4px;
    }

    .speech-bubble {
      background: var(--accent-soft);
      border: 1px solid #FFE0B2;
      border-radius: 8px;
      padding: 6px 10px
