"""Generates quiz.html by embedding questions.json into a self-contained HTML file."""
import json

with open("questions.json", encoding="utf-8") as f:
    questions = json.load(f)

questions_json = json.dumps(questions, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>PSM I Quiz</title>
<style>
  :root {{
    --bg: #f0f4f8;
    --card: #ffffff;
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --correct: #16a34a;
    --correct-bg: #dcfce7;
    --wrong: #dc2626;
    --wrong-bg: #fee2e2;
    --neutral: #64748b;
    --border: #e2e8f0;
    --text: #1e293b;
    --subtext: #64748b;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 24px 16px;
  }}
  .container {{
    max-width: 760px;
    margin: 0 auto;
  }}
  header {{
    text-align: center;
    margin-bottom: 28px;
  }}
  header h1 {{
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--primary);
  }}
  header p {{
    color: var(--subtext);
    margin-top: 4px;
    font-size: 0.95rem;
  }}
  .progress-bar-wrap {{
    background: var(--border);
    border-radius: 99px;
    height: 8px;
    margin-bottom: 20px;
    overflow: hidden;
  }}
  .progress-bar {{
    height: 100%;
    background: var(--primary);
    border-radius: 99px;
    transition: width 0.3s ease;
  }}
  .progress-text {{
    text-align: right;
    font-size: 0.85rem;
    color: var(--subtext);
    margin-bottom: 16px;
  }}
  .card {{
    background: var(--card);
    border-radius: 12px;
    padding: 28px 28px 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,.08), 0 4px 16px rgba(0,0,0,.04);
    margin-bottom: 20px;
  }}
  .question-text {{
    font-size: 1.08rem;
    font-weight: 600;
    line-height: 1.55;
    margin-bottom: 20px;
    white-space: pre-wrap;
  }}
  .multi-hint {{
    font-size: 0.82rem;
    font-weight: 400;
    color: var(--primary);
    background: #eff6ff;
    border-radius: 4px;
    padding: 2px 8px;
    margin-left: 8px;
    vertical-align: middle;
  }}
  .options {{
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .option {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border: 2px solid var(--border);
    border-radius: 8px;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
    user-select: none;
  }}
  .option:hover:not(.disabled) {{
    border-color: var(--primary);
    background: #eff6ff;
  }}
  .option.selected {{
    border-color: var(--primary);
    background: #eff6ff;
  }}
  .option.correct {{
    border-color: var(--correct);
    background: var(--correct-bg);
  }}
  .option.wrong {{
    border-color: var(--wrong);
    background: var(--wrong-bg);
  }}
  .option.missed {{
    border-color: var(--correct);
    background: var(--correct-bg);
    opacity: 0.75;
  }}
  .option.disabled {{ cursor: default; }}
  .letter-badge {{
    min-width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-top: 1px;
    transition: background 0.15s;
  }}
  .option.selected .letter-badge {{ background: var(--primary); color: #fff; }}
  .option.correct .letter-badge {{ background: var(--correct); color: #fff; }}
  .option.wrong .letter-badge {{ background: var(--wrong); color: #fff; }}
  .option.missed .letter-badge {{ background: var(--correct); color: #fff; }}
  .option-text {{
    font-size: 0.97rem;
    line-height: 1.5;
  }}
  .feedback {{
    margin-top: 16px;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 0.92rem;
    display: none;
  }}
  .feedback.show {{ display: block; }}
  .feedback.correct-fb {{ background: var(--correct-bg); color: var(--correct); border: 1px solid #bbf7d0; }}
  .feedback.wrong-fb {{ background: var(--wrong-bg); color: var(--wrong); border: 1px solid #fecaca; }}
  .explanation {{
    margin-top: 10px;
    padding: 10px 14px;
    border-radius: 6px;
    background: #f8fafc;
    border: 1px solid var(--border);
    font-size: 0.9rem;
    color: var(--text);
    line-height: 1.55;
  }}
  .explanation-label {{
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--subtext);
    margin-bottom: 4px;
  }}
  .review-explanation {{
    margin-top: 6px;
    font-size: 0.84rem;
    color: var(--text);
    line-height: 1.5;
    font-style: italic;
  }}
  .btn-row {{
    display: flex;
    gap: 12px;
    justify-content: flex-end;
    margin-top: 20px;
    flex-wrap: wrap;
  }}
  button {{
    padding: 10px 24px;
    border-radius: 8px;
    border: none;
    font-size: 0.97rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s, transform 0.1s;
  }}
  button:active {{ transform: scale(0.97); }}
  .btn-primary {{
    background: var(--primary);
    color: #fff;
  }}
  .btn-primary:hover {{ background: var(--primary-dark); }}
  .btn-secondary {{
    background: var(--border);
    color: var(--text);
  }}
  .btn-secondary:hover {{ background: #cbd5e1; }}
  button:disabled {{
    opacity: 0.4;
    cursor: not-allowed;
    transform: none;
  }}

  /* Results screen */
  .results {{
    text-align: center;
  }}
  .score-circle {{
    width: 140px;
    height: 140px;
    border-radius: 50%;
    border: 8px solid var(--primary);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto 24px;
  }}
  .score-num {{
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--primary);
    line-height: 1;
  }}
  .score-label {{
    font-size: 0.82rem;
    color: var(--subtext);
  }}
  .score-pct {{
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 6px;
  }}
  .score-msg {{
    color: var(--subtext);
    margin-bottom: 28px;
  }}
  /* Review tabs */
  .review-tabs {{
    display: none;
    margin-top: 28px;
    text-align: left;
  }}
  .review-tabs.show {{ display: block; }}
  .tab-bar {{
    display: flex;
    gap: 2px;
    border-bottom: 2px solid var(--border);
    margin-bottom: 20px;
  }}
  .tab-btn {{
    padding: 9px 20px;
    border: none;
    background: none;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--subtext);
    cursor: pointer;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;
    border-radius: 0;
    transition: color 0.15s;
  }}
  .tab-btn:hover {{ color: var(--text); }}
  .tab-btn:active {{ transform: none; }}
  .tab-btn.active {{
    color: var(--primary);
    border-bottom-color: var(--primary);
  }}
  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}
  .review-card {{
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 22px;
    margin-bottom: 16px;
  }}
  .review-card-q {{
    font-weight: 600;
    font-size: 0.97rem;
    line-height: 1.5;
    margin-bottom: 14px;
    white-space: pre-wrap;
  }}
  .review-options {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 12px;
  }}
  .review-opt {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 9px 13px;
    border: 2px solid var(--border);
    border-radius: 7px;
    font-size: 0.93rem;
    line-height: 1.45;
  }}
  .review-opt.r-correct {{
    border-color: var(--correct);
    background: var(--correct-bg);
  }}
  .review-opt.r-correct .letter-badge {{ background: var(--correct); color: #fff; }}
  .review-opt.r-wrong {{
    border-color: var(--wrong);
    background: var(--wrong-bg);
  }}
  .review-opt.r-wrong .letter-badge {{ background: var(--wrong); color: #fff; }}
  .review-opt.r-missed {{
    border-color: var(--correct);
    background: var(--correct-bg);
    opacity: 0.6;
  }}
  .review-opt.r-missed .letter-badge {{ background: var(--correct); color: #fff; }}
  .empty-tab {{
    text-align: center;
    padding: 40px 0;
    color: var(--subtext);
    font-size: 0.95rem;
  }}

  /* Start screen */
  #start-screen {{ text-align: center; }}
  #start-screen .card {{ padding: 40px; }}
  .big-title {{ font-size: 2rem; font-weight: 800; color: var(--primary); margin-bottom: 8px; }}
  .tagline {{ color: var(--subtext); margin-bottom: 28px; font-size: 1rem; }}
  .stats {{ display: flex; gap: 24px; justify-content: center; margin-bottom: 32px; flex-wrap: wrap; }}
  .stat {{ text-align: center; }}
  .stat-num {{ font-size: 1.8rem; font-weight: 800; color: var(--primary); }}
  .stat-label {{ font-size: 0.82rem; color: var(--subtext); }}

  /* Custom range */
  .divider {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0 24px;
    color: var(--subtext);
    font-size: 0.85rem;
  }}
  .divider::before, .divider::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }}
  .range-section {{
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
  }}
  .range-title {{
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
  }}
  .range-subtitle {{
    font-size: 0.83rem;
    color: var(--subtext);
    margin-bottom: 16px;
  }}
  .range-inputs {{
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 16px;
  }}
  .range-field {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
  }}
  .range-field label {{
    font-size: 0.75rem;
    color: var(--subtext);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}
  .range-field input {{
    width: 80px;
    padding: 8px;
    border: 2px solid var(--border);
    border-radius: 6px;
    font-size: 1.05rem;
    text-align: center;
    color: var(--text);
    background: #fff;
    outline: none;
    transition: border-color 0.15s;
  }}
  .range-field input:focus {{ border-color: var(--primary); }}
  .range-field .field-hint {{
    font-size: 0.72rem;
    color: var(--subtext);
  }}
  .range-error {{
    color: var(--wrong);
    font-size: 0.85rem;
    margin-bottom: 12px;
    min-height: 18px;
  }}
  .range-inputs.dimmed {{
    opacity: 0.35;
    pointer-events: none;
  }}
  .range-or-divider {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 14px 0 12px;
    color: var(--subtext);
    font-size: 0.82rem;
  }}
  .range-or-divider::before, .range-or-divider::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }}

  /* Browse screen */
  .browse-header {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
  }}
  .browse-header h2 {{
    font-size: 1.1rem;
    font-weight: 700;
    flex: 1;
  }}
  .search-input {{
    width: 100%;
    padding: 10px 14px;
    border: 2px solid var(--border);
    border-radius: 8px;
    font-size: 0.97rem;
    color: var(--text);
    background: #fff;
    outline: none;
    margin-bottom: 14px;
    transition: border-color 0.15s;
  }}
  .search-input:focus {{ border-color: var(--primary); }}
  .cat-filters {{
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-bottom: 16px;
  }}
  .cat-chip {{
    padding: 5px 13px;
    border-radius: 99px;
    border: 2px solid var(--border);
    background: #fff;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s, color 0.15s;
    color: var(--text);
  }}
  .cat-chip:hover {{ border-color: var(--primary); color: var(--primary); }}
  .cat-chip.active {{ border-color: var(--primary); background: var(--primary); color: #fff; }}
  .browse-count {{
    font-size: 0.83rem;
    color: var(--subtext);
    margin-bottom: 16px;
  }}
  .browse-card {{
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 14px;
  }}
  .browse-card-top {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 12px;
  }}
  .browse-card-q {{
    font-weight: 600;
    font-size: 0.97rem;
    line-height: 1.5;
    white-space: pre-wrap;
    flex: 1;
  }}
  .cat-tag {{
    font-size: 0.73rem;
    font-weight: 700;
    color: var(--primary);
    background: #eff6ff;
    border-radius: 4px;
    padding: 3px 8px;
    white-space: nowrap;
    flex-shrink: 0;
  }}
  .browse-opts {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .browse-opt {{
    display: flex;
    align-items: flex-start;
    gap: 9px;
    padding: 7px 11px;
    border-radius: 6px;
    font-size: 0.9rem;
    line-height: 1.4;
    border: 1.5px solid transparent;
  }}
  .browse-opt.b-correct {{
    border-color: var(--correct);
    background: var(--correct-bg);
    font-weight: 600;
  }}
  .browse-opt.b-correct .letter-badge {{ background: var(--correct); color: #fff; }}

  /* Mode selection buttons */
  .mode-select {{
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }}
  .mode-btn {{
    flex: 1;
    min-width: 180px;
    padding: 16px 18px;
    text-align: left;
    height: auto;
    border-radius: 10px;
  }}
  .mode-title {{
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .mode-desc {{
    font-size: 0.8rem;
    font-weight: 400;
    opacity: 0.85;
    line-height: 1.4;
  }}

  /* Start screen redesign */
  .count-row {{
    margin: 22px 0 20px;
    text-align: center;
  }}
  .count-label {{
    display: block;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--subtext);
    margin-bottom: 10px;
  }}
  .count-input-row {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }}
  .count-big {{
    width: 88px;
    padding: 10px;
    border: 2px solid var(--border);
    border-radius: 8px;
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
    color: var(--text);
    background: #fff;
    outline: none;
    transition: border-color 0.15s;
  }}
  .count-big:focus {{ border-color: var(--primary); }}
  .count-of {{
    font-size: 0.95rem;
    color: var(--subtext);
  }}
  .filter-toggle {{
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    background: var(--bg);
    border: 1.5px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
    margin-bottom: 0;
  }}
  .filter-toggle:hover {{ background: #e2e8f0; }}
  .filter-toggle:active {{ transform: none; }}
  .filter-toggle.open {{ border-radius: 8px 8px 0 0; border-bottom-color: transparent; }}
  .filter-chevron {{ font-size: 0.7rem; transition: transform 0.2s; display: inline-block; }}
  .filter-chevron.open {{ transform: rotate(180deg); }}
  .filter-panel {{
    display: none;
    border: 1.5px solid var(--border);
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 16px;
    background: #f8fafc;
    margin-bottom: 12px;
  }}
  .filter-panel.open {{ display: block; }}
  .active-filters-hint {{
    font-size: 0.8rem;
    color: var(--primary);
    font-weight: 600;
  }}
  .cat-checkbox-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 16px;
  }}
  .cat-check-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 6px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.1s;
    font-size: 0.88rem;
    color: var(--text);
  }}
  .cat-check-item:hover {{ background: #e8edf2; }}
  .cat-check-item input[type="checkbox"] {{
    width: 15px;
    height: 15px;
    accent-color: var(--primary);
    cursor: pointer;
    flex-shrink: 0;
  }}
  .cat-count {{
    font-size: 0.75rem;
    color: var(--subtext);
  }}
  .start-actions {{
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
  }}

  /* Timer */
  .timer-bar {{
    text-align: center;
    font-size: 1.7rem;
    font-weight: 800;
    color: var(--primary);
    margin-bottom: 10px;
    font-variant-numeric: tabular-nums;
    letter-spacing: 0.06em;
    transition: color 0.3s;
  }}
  .timer-bar.warning {{ color: var(--wrong); }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>PSM I Certification Quiz</h1>
    <p>Professional Scrum Master I — Practice Exam</p>
  </header>

  <!-- Start screen -->
  <div id="start-screen">
    <div class="card">
      <div class="big-title">PSM I Practice Quiz</div>
      <div class="stats">
        <div class="stat"><div class="stat-num">268</div><div class="stat-label">Questions</div></div>
        <div class="stat"><div class="stat-num">85%</div><div class="stat-label">Passing Score</div></div>
      </div>

      <!-- Count — always visible -->
      <div class="count-row">
        <span class="count-label">Questions per session</span>
        <div class="count-input-row">
          <input class="count-big" type="number" id="range-count" min="1" max="268" value="30">
          <span class="count-of" id="count-of-label">of 268</span>
        </div>
      </div>

      <!-- Filter by Category -->
      <button class="filter-toggle" id="filter-toggle-cat" onclick="toggleFilter('cat')">
        <span>Filter by Category <span class="active-filters-hint" id="filter-hint-cat"></span></span>
        <span class="filter-chevron" id="filter-chevron-cat">&#9660;</span>
      </button>
      <div class="filter-panel" id="filter-panel-cat">
        <div class="cat-checkbox-grid" id="start-cat-filters"></div>
      </div>

      <!-- Filter by Question Range -->
      <button class="filter-toggle" id="filter-toggle-range" onclick="toggleFilter('range')" style="margin-top:8px">
        <span>Filter by Question Number <span class="active-filters-hint" id="filter-hint-range"></span></span>
        <span class="filter-chevron" id="filter-chevron-range">&#9660;</span>
      </button>
      <div class="filter-panel" id="filter-panel-range">
        <div class="range-inputs" id="range-inputs">
          <div class="range-field">
            <label>From Q#</label>
            <input type="number" id="range-from" min="1" max="268" value="1">
            <span class="field-hint">start</span>
          </div>
          <div class="range-field">
            <label>To Q#</label>
            <input type="number" id="range-to" min="1" max="268" value="268">
            <span class="field-hint">end</span>
          </div>
        </div>
      </div>

      <div class="range-error" id="range-error"></div>

      <!-- Actions -->
      <div class="start-actions">
        <div class="mode-select" style="margin-bottom:0">
          <button class="mode-btn btn-secondary" onclick="startQuiz('normal')">
            <div class="mode-title">Normal</div>
            <div class="mode-desc">Check each answer immediately · Explanations shown</div>
          </button>
          <button class="mode-btn btn-primary" onclick="startQuiz('timed')">
            <div class="mode-title">&#9200; Timed</div>
            <div class="mode-desc">45 sec / question · Submit all at end · No explanations</div>
          </button>
        </div>
        <button class="btn-secondary" onclick="showBrowse()" style="width:100%">&#128270; Browse All Questions &amp; Answers</button>
      </div>
    </div>
  </div>

  <!-- Quiz screen -->
  <div id="quiz-screen" style="display:none">
    <div class="timer-bar" id="timer" style="display:none"></div>
    <div class="progress-bar-wrap">
      <div class="progress-bar" id="progress-bar" style="width:0%"></div>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <div class="progress-text" id="progress-text" style="margin-bottom:0">Question 1 of 30</div>
      <button class="btn-secondary" onclick="confirmHome()" style="font-size:0.8rem;padding:5px 12px">&#8962; Home</button>
    </div>
    <div class="card">
      <div class="question-text" id="question-text"></div>
      <div class="options" id="options"></div>
      <div class="feedback" id="feedback"></div>
      <div class="btn-row">
        <button class="btn-secondary" id="btn-back" onclick="backQuestion()" disabled>← Back</button>
        <button class="btn-secondary" id="btn-submit" onclick="submitAnswer()" disabled>Check Answer</button>
        <button class="btn-primary" id="btn-next" onclick="nextQuestion()" disabled>Next</button>
      </div>
    </div>
  </div>

  <!-- Browse screen -->
  <div id="browse-screen" style="display:none">
    <div class="card" style="margin-bottom:16px;padding:20px 24px">
      <div class="browse-header">
        <button class="btn-secondary" onclick="showStart()" style="padding:7px 16px;font-size:0.9rem">&#8592; Back</button>
        <h2>Browse Questions &amp; Answers</h2>
      </div>
      <div style="display:flex;gap:8px;margin-bottom:14px">
        <input class="search-input" id="browse-search" type="text" placeholder="Search questions or answers..." style="margin-bottom:0;flex:1" oninput="filterBrowse()" onkeydown="if(event.key==='Enter')filterBrowse()">
        <button class="btn-primary" onclick="filterBrowse()" style="white-space:nowrap;padding:10px 20px">Search</button>
      </div>
      <button class="filter-toggle" id="filter-toggle-browse-cat" onclick="toggleFilter('browse-cat')" style="margin-bottom:0">
        <span>Filter by Category <span class="active-filters-hint" id="filter-hint-browse-cat"></span></span>
        <span class="filter-chevron" id="filter-chevron-browse-cat">&#9660;</span>
      </button>
      <div class="filter-panel" id="filter-panel-browse-cat" style="margin-bottom:12px">
        <div class="cat-checkbox-grid" id="cat-filters"></div>
      </div>
      <div class="browse-count" id="browse-count"></div>
    </div>
    <div id="browse-list"></div>
  </div>

  <!-- Results screen -->
  <div id="results-screen" style="display:none">
    <div class="card results">
      <div class="score-circle" id="score-circle">
        <div class="score-num" id="score-num"></div>
        <div class="score-label" id="score-total"></div>
      </div>
      <div class="score-pct" id="score-pct"></div>
      <div class="score-msg" id="score-msg"></div>
      <div class="btn-row" style="justify-content:center">
        <button class="btn-secondary" id="btn-review" onclick="toggleReview()">Review Answers</button>
        <button class="btn-primary" onclick="goHome()">&#8962; New Quiz</button>
      </div>
      <div class="review-tabs" id="review-tabs">
        <div class="tab-bar">
          <button class="tab-btn active" data-tab="all" onclick="switchTab('all')">All</button>
          <button class="tab-btn" data-tab="correct" onclick="switchTab('correct')">Correct</button>
          <button class="tab-btn" data-tab="wrong" onclick="switchTab('wrong')">Wrong</button>
        </div>
        <div class="tab-content active" id="tab-all"></div>
        <div class="tab-content" id="tab-correct"></div>
        <div class="tab-content" id="tab-wrong"></div>
      </div>
    </div>
  </div>
</div>

<script>
const ALL_QUESTIONS = {questions_json};

let sessionQuestions = [];
let sessionCount = 0;
let currentIdx = 0;
let score = 0;
let selected = new Set();
let answered = false;
let history = [];
let quizMode = 'normal';
let timedAnswers = [];
let timerInterval = null;
let timeLeft = 0;
let selectedCats = new Set();

// Render category chips on the start screen
(function initStartCats() {{
  const catCounts = {{}};
  ALL_QUESTIONS.forEach(q => {{ if (q.category) catCounts[q.category] = (catCounts[q.category] || 0) + 1; }});
  const cats = Object.keys(catCounts).sort();
  document.getElementById("start-cat-filters").innerHTML = cats.map(c =>
    `<label class="cat-check-item">
      <input type="checkbox" value="${{c}}" onchange="toggleStartCat(this,'${{c}}')">
      <span>${{c}} <span class="cat-count">(${{catCounts[c]}})</span></span>
    </label>`
  ).join("");
}})();

function shuffle(arr) {{
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }}
  return a;
}}

function startQuiz(mode) {{
  const errEl = document.getElementById("range-error");
  errEl.textContent = "";

  const count = parseInt(document.getElementById("range-count").value, 10);
  if (isNaN(count) || count < 1) {{
    errEl.textContent = "Please enter a valid Count.";
    return;
  }}

  let pool;
  if (selectedCats.size > 0) {{
    pool = ALL_QUESTIONS.filter(q => selectedCats.has(q.category));
    if (pool.length === 0) {{
      errEl.textContent = "No questions found for the selected categories.";
      return;
    }}
  }} else {{
    const from = parseInt(document.getElementById("range-from").value, 10);
    const to   = parseInt(document.getElementById("range-to").value, 10);
    if (isNaN(from) || isNaN(to)) {{
      errEl.textContent = "Please fill in From and To, or select a category.";
      return;
    }}
    if (from < 1 || to > ALL_QUESTIONS.length || from > to) {{
      errEl.textContent = `Q# must be between 1 and ${{ALL_QUESTIONS.length}}, and From ≤ To.`;
      return;
    }}
    pool = ALL_QUESTIONS.slice(from - 1, to);
  }}

  if (count > pool.length) {{
    errEl.textContent = `Count must be at most ${{pool.length}} (questions available in this selection).`;
    return;
  }}

  quizMode = mode;
  sessionCount = count;
  sessionQuestions = shuffle(pool).slice(0, count);
  beginSession();
}}

function beginSession() {{
  currentIdx = 0;
  score = 0;
  history = [];
  selected = new Set();
  answered = false;

  if (quizMode === 'timed') {{
    timedAnswers = sessionQuestions.map(() => new Set());
    timeLeft = sessionCount * 45;
    document.getElementById("timer").style.display = "block";
    startTimer();
  }} else {{
    stopTimer();
    document.getElementById("timer").style.display = "none";
  }}

  document.getElementById("start-screen").style.display = "none";
  document.getElementById("results-screen").style.display = "none";
  document.getElementById("quiz-screen").style.display = "block";
  renderQuestion();
}}

function renderQuestion() {{
  const q = sessionQuestions[currentIdx];
  const isMulti = q.correct.length > 1;

  document.getElementById("progress-bar").style.width = ((currentIdx / sessionCount) * 100) + "%";
  document.getElementById("progress-text").textContent = `Question ${{currentIdx + 1}} of ${{sessionCount}}`;

  const qText = document.getElementById("question-text");
  qText.textContent = q.question;
  if (isMulti) {{
    const badge = document.createElement("span");
    badge.className = "multi-hint";
    badge.textContent = `Select ${{q.correct.length}}`;
    qText.appendChild(badge);
  }}

  const optionsEl = document.getElementById("options");
  optionsEl.innerHTML = "";
  selected = new Set();
  answered = false;

  q.options.forEach(opt => {{
    const div = document.createElement("div");
    div.className = "option";
    div.dataset.letter = opt.letter;
    div.innerHTML = `<div class="letter-badge">${{opt.letter}}</div><div class="option-text">${{opt.text}}</div>`;
    div.addEventListener("click", () => toggleOption(div, opt.letter));
    optionsEl.appendChild(div);
  }});

  document.getElementById("feedback").className = "feedback";
  document.getElementById("feedback").innerHTML = "";
  document.getElementById("btn-back").disabled = currentIdx === 0;

  const isLast = currentIdx === sessionCount - 1;

  if (quizMode === 'timed') {{
    // Restore any previously selected answers for this question
    selected = new Set(timedAnswers[currentIdx]);
    document.querySelectorAll(".option").forEach(div => {{
      if (selected.has(div.dataset.letter)) div.classList.add("selected");
    }});
    document.getElementById("btn-submit").style.display = "none";
    document.getElementById("btn-next").disabled = false;
    document.getElementById("btn-next").textContent = isLast ? "Finish Quiz" : "Next";
  }} else {{
    document.getElementById("btn-submit").style.display = "";
    document.getElementById("btn-submit").disabled = true;
    document.getElementById("btn-next").disabled = true;
    document.getElementById("btn-next").textContent = isLast ? "See Results" : "Next";

    // Restore answered state when navigating back to an already-answered question
    if (currentIdx < history.length) {{
      const entry = history[currentIdx];
      const correctSet = new Set(q.correct);
      answered = true;
      selected = new Set(entry.selected);

      document.querySelectorAll(".option").forEach(div => {{
        const letter = div.dataset.letter;
        div.classList.add("disabled");
        if (correctSet.has(letter) && entry.selected.has(letter)) {{
          div.classList.add("correct");
        }} else if (entry.selected.has(letter) && !correctSet.has(letter)) {{
          div.classList.add("wrong");
        }} else if (correctSet.has(letter) && !entry.selected.has(letter)) {{
          div.classList.add("missed");
        }}
      }});

      const fb = document.getElementById("feedback");
      fb.className = "feedback show " + (entry.correct ? "correct-fb" : "wrong-fb");
      if (entry.correct) {{
        fb.innerHTML = "<strong>Correct!</strong>";
      }} else {{
        const correctLabels = q.correct.map(l => {{
          const opt = q.options.find(o => o.letter === l);
          return `${{l}}) ${{opt ? opt.text : ""}}`;
        }}).join("; ");
        fb.innerHTML = `<strong>Incorrect.</strong> Correct answer${{q.correct.length > 1 ? "s" : ""}}: ${{correctLabels}}`;
      }}
      if (q.explanation) {{
        fb.innerHTML += `<div class="explanation"><div class="explanation-label">Why?</div>${{q.explanation}}</div>`;
      }}
      document.getElementById("btn-submit").disabled = true;
      document.getElementById("btn-next").disabled = false;
    }}
  }}
}}

function toggleOption(div, letter) {{
  if (answered) return;
  const q = sessionQuestions[currentIdx];
  const isMulti = q.correct.length > 1;

  if (isMulti) {{
    if (selected.has(letter)) {{
      selected.delete(letter);
      div.classList.remove("selected");
    }} else {{
      selected.add(letter);
      div.classList.add("selected");
    }}
  }} else {{
    document.querySelectorAll(".option").forEach(o => o.classList.remove("selected"));
    selected.clear();
    selected.add(letter);
    div.classList.add("selected");
  }}

  if (quizMode === 'timed') {{
    timedAnswers[currentIdx] = new Set(selected);
  }} else {{
    document.getElementById("btn-submit").disabled = selected.size === 0;
  }}
}}

function submitAnswer() {{
  if (answered) return;
  answered = true;

  const q = sessionQuestions[currentIdx];
  const correctSet = new Set(q.correct);
  const isCorrect = selected.size === correctSet.size && [...selected].every(l => correctSet.has(l));

  if (isCorrect) score++;

  history.push({{ question: q, selected: new Set(selected), correct: isCorrect }});

  document.querySelectorAll(".option").forEach(div => {{
    const letter = div.dataset.letter;
    div.classList.add("disabled");
    if (correctSet.has(letter) && selected.has(letter)) {{
      div.classList.remove("selected");
      div.classList.add("correct");
    }} else if (selected.has(letter) && !correctSet.has(letter)) {{
      div.classList.remove("selected");
      div.classList.add("wrong");
    }} else if (correctSet.has(letter) && !selected.has(letter)) {{
      div.classList.add("missed");
    }}
  }});

  const fb = document.getElementById("feedback");
  fb.className = "feedback show " + (isCorrect ? "correct-fb" : "wrong-fb");
  if (isCorrect) {{
    fb.innerHTML = "<strong>Correct!</strong>";
  }} else {{
    const correctLabels = q.correct.map(l => {{
      const opt = q.options.find(o => o.letter === l);
      return `${{l}}) ${{opt ? opt.text : ""}}`;
    }}).join("; ");
    fb.innerHTML = `<strong>Incorrect.</strong> Correct answer${{q.correct.length > 1 ? "s" : ""}}: ${{correctLabels}}`;
  }}

  if (q.explanation) {{
    fb.innerHTML += `<div class="explanation"><div class="explanation-label">Why?</div>${{q.explanation}}</div>`;
  }}

  document.getElementById("btn-submit").disabled = true;
  document.getElementById("btn-next").disabled = false;
}}

function backQuestion() {{
  if (currentIdx === 0) return;
  currentIdx--;
  renderQuestion();
}}

function nextQuestion() {{
  if (currentIdx === sessionCount - 1) {{
    if (quizMode === 'timed') finishTimedQuiz();
    else showResults();
    return;
  }}
  currentIdx++;
  renderQuestion();
}}

function showResults() {{
  document.getElementById("quiz-screen").style.display = "none";
  document.getElementById("results-screen").style.display = "block";

  const pct = Math.round((score / sessionCount) * 100);
  const color = pct >= 85 ? "var(--correct)" : (pct >= 60 ? "var(--primary)" : "var(--wrong)");

  const circle = document.getElementById("score-circle");
  circle.style.borderColor = color;
  document.getElementById("score-num").textContent = score;
  document.getElementById("score-num").style.color = color;
  document.getElementById("score-total").textContent = `/ ${{sessionCount}}`;
  document.getElementById("score-pct").textContent = pct + "%";

  let msg;
  if (pct >= 85) msg = "Excellent! You would pass the PSM I exam.";
  else if (pct >= 70) msg = "Good progress! Keep studying to reach the 85% passing threshold.";
  else if (pct >= 50) msg = "Decent start. Review the missed questions and try again.";
  else msg = "Keep studying! Review the Scrum Guide and practice more.";
  document.getElementById("score-msg").textContent = msg;
}}

function buildReviewCard(entry, i) {{
  const correctSet = new Set(entry.question.correct);
  let optsHtml = "";
  entry.question.options.forEach(opt => {{
    const sel = entry.selected.has(opt.letter);
    const cor = correctSet.has(opt.letter);
    let cls = "";
    if (sel && cor)  cls = "r-correct";
    else if (sel && !cor) cls = "r-wrong";
    else if (!sel && cor) cls = "r-missed";
    optsHtml += `<div class="review-opt ${{cls}}">
      <div class="letter-badge">${{opt.letter}}</div>
      <div class="option-text">${{opt.text}}</div>
    </div>`;
  }});
  const expHtml = (quizMode === 'normal' && entry.question.explanation)
    ? `<div class="explanation"><div class="explanation-label">Why?</div>${{entry.question.explanation}}</div>`
    : "";
  return `<div class="review-card">
    <div class="review-card-q">Q${{i + 1}}: ${{entry.question.question}}</div>
    <div class="review-options">${{optsHtml}}</div>
    ${{expHtml}}
  </div>`;
}}

function toggleReview() {{
  const tabsEl = document.getElementById("review-tabs");
  const btn = document.getElementById("btn-review");
  if (tabsEl.classList.contains("show")) {{
    tabsEl.classList.remove("show");
    btn.textContent = "Review Answers";
    return;
  }}

  const correctEntries = history.filter(e => e.correct);
  const wrongEntries   = history.filter(e => !e.correct);

  document.getElementById("tab-all").innerHTML =
    history.map((e, i) => buildReviewCard(e, i)).join("");

  document.getElementById("tab-correct").innerHTML = correctEntries.length
    ? correctEntries.map((e, i) => buildReviewCard(e, i)).join("")
    : "<div class='empty-tab'>No correct answers yet.</div>";

  document.getElementById("tab-wrong").innerHTML = wrongEntries.length
    ? wrongEntries.map((e, i) => buildReviewCard(e, i)).join("")
    : "<div class='empty-tab'>No wrong answers — perfect score!</div>";

  // Update tab labels with counts
  document.querySelector('[data-tab="all"]').textContent    = `All (${{history.length}})`;
  document.querySelector('[data-tab="correct"]').textContent = `Correct (${{correctEntries.length}})`;
  document.querySelector('[data-tab="wrong"]').textContent   = `Wrong (${{wrongEntries.length}})`;

  tabsEl.classList.add("show");
  switchTab("all");
  btn.textContent = "Hide Review";
}}

function switchTab(name) {{
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.toggle("active", b.dataset.tab === name));
  document.querySelectorAll(".tab-content").forEach(c => c.classList.toggle("active", c.id === "tab-" + name));
}}

// ── Start screen filters ────────────────────────────────────────
function toggleFilter(name) {{
  const panel  = document.getElementById("filter-panel-" + name);
  const toggle = document.getElementById("filter-toggle-" + name);
  const chev   = document.getElementById("filter-chevron-" + name);
  const open   = panel.classList.toggle("open");
  toggle.classList.toggle("open", open);
  chev.classList.toggle("open", open);
}}

function toggleStartCat(checkbox, cat) {{
  if (checkbox.checked) selectedCats.add(cat);
  else selectedCats.delete(cat);

  const hasCats = selectedCats.size > 0;
  document.getElementById("range-inputs").classList.toggle("dimmed", hasCats);

  if (hasCats) {{
    const available = ALL_QUESTIONS.filter(q => selectedCats.has(q.category)).length;
    document.getElementById("count-of-label").textContent = `of ${{available}}`;
    document.getElementById("filter-hint-cat").textContent = `· ${{selectedCats.size}} selected`;
  }} else {{
    document.getElementById("count-of-label").textContent = `of ${{ALL_QUESTIONS.length}}`;
    document.getElementById("filter-hint-cat").textContent = "";
  }}
  document.getElementById("range-error").textContent = "";
}}

// ── Browse screen ──────────────────────────────────────────────
let browseCategories = new Set();

function showBrowse() {{
  document.getElementById("start-screen").style.display = "none";
  document.getElementById("browse-screen").style.display = "block";
  browseCategories = new Set();

  // Build category checkboxes
  const catCounts = {{}};
  ALL_QUESTIONS.forEach(q => {{ if (q.category) catCounts[q.category] = (catCounts[q.category] || 0) + 1; }});
  document.getElementById("cat-filters").innerHTML = Object.keys(catCounts).sort().map(c =>
    `<label class="cat-check-item">
      <input type="checkbox" value="${{c}}" onchange="toggleBrowseCat(this,'${{c}}')">
      <span>${{c}} <span class="cat-count">(${{catCounts[c]}})</span></span>
    </label>`
  ).join("");

  filterBrowse();
}}

function goHome() {{
  stopTimer();
  ["quiz-screen", "results-screen", "browse-screen"].forEach(id =>
    document.getElementById(id).style.display = "none"
  );
  document.getElementById("start-screen").style.display = "block";
}}

function confirmHome() {{
  if (confirm("Leave the quiz? Your progress will be lost.")) goHome();
}}

function showStart() {{
  document.getElementById("browse-screen").style.display = "none";
  document.getElementById("start-screen").style.display = "block";
}}

function toggleBrowseCat(checkbox, cat) {{
  if (checkbox.checked) browseCategories.add(cat);
  else browseCategories.delete(cat);
  const n = browseCategories.size;
  document.getElementById("filter-hint-browse-cat").textContent = n > 0 ? `· ${{n}} selected` : "";
  filterBrowse();
}}

function filterBrowse() {{
  const term = document.getElementById("browse-search").value.trim().toLowerCase();
  const filtered = ALL_QUESTIONS.filter(q => {{
    const matchCat = browseCategories.size === 0 || browseCategories.has(q.category);
    if (!matchCat) return false;
    if (!term) return true;
    const haystack = (q.question + " " + q.options.map(o => o.text).join(" ")).toLowerCase();
    return haystack.includes(term);
  }});

  document.getElementById("browse-count").textContent =
    `Showing ${{filtered.length}} of ${{ALL_QUESTIONS.length}} questions`;

  document.getElementById("browse-list").innerHTML = filtered.map((q, i) => {{
    const cs = new Set(q.correct);
    const correctOptsHtml = q.options
      .filter(o => cs.has(o.letter))
      .map(o => `<div class="browse-opt b-correct">
        <div class="letter-badge">${{o.letter}}</div>
        <div class="option-text">${{o.text}}</div>
      </div>`).join("");
    const expHtml = q.explanation
      ? `<div class="explanation" style="margin-top:10px"><div class="explanation-label">Why?</div>${{q.explanation}}</div>`
      : "";
    return `<div class="browse-card">
      <div class="browse-card-top">
        <div class="browse-card-q">${{q.question}}</div>
        <div class="cat-tag">${{q.category || ""}}</div>
      </div>
      <div class="browse-opts">${{correctOptsHtml}}</div>
      ${{expHtml}}
    </div>`;
  }}).join("");
}}

// ── Timer ──────────────────────────────────────────────────────
function startTimer() {{
  updateTimerDisplay();
  timerInterval = setInterval(tick, 1000);
}}

function stopTimer() {{
  if (timerInterval) {{ clearInterval(timerInterval); timerInterval = null; }}
}}

function tick() {{
  timeLeft--;
  updateTimerDisplay();
  if (timeLeft <= 0) {{
    stopTimer();
    finishTimedQuiz();
  }}
}}

function updateTimerDisplay() {{
  const el = document.getElementById("timer");
  const min = Math.floor(timeLeft / 60);
  const sec = timeLeft % 60;
  el.textContent = String(min).padStart(2, '0') + ':' + String(sec).padStart(2, '0');
  el.className = 'timer-bar' + (timeLeft < 120 ? ' warning' : '');
}}

function finishTimedQuiz() {{
  stopTimer();
  document.getElementById("timer").style.display = "none";
  history = [];
  score = 0;
  sessionQuestions.forEach((q, i) => {{
    const sel = timedAnswers[i];
    const correctSet = new Set(q.correct);
    const isCorrect = sel.size === correctSet.size && [...sel].every(l => correctSet.has(l));
    if (isCorrect) score++;
    history.push({{ question: q, selected: sel, correct: isCorrect }});
  }});
  showResults();
}}
</script>
</body>
</html>
"""

with open("quiz.html", "w", encoding="utf-8") as f:
    f.write(html)

print("quiz.html created successfully!")
