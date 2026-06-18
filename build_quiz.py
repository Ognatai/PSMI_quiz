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
  .review-list {{
    text-align: left;
    margin-top: 24px;
  }}
  .review-item {{
    padding: 14px 0;
    border-bottom: 1px solid var(--border);
  }}
  .review-item:last-child {{ border-bottom: none; }}
  .review-q {{
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 6px;
    white-space: pre-wrap;
  }}
  .review-status {{
    font-size: 0.85rem;
    font-weight: 600;
  }}
  .review-status.ok {{ color: var(--correct); }}
  .review-status.fail {{ color: var(--wrong); }}

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
      <div class="big-title">Ready to Practice?</div>
      <div class="tagline">30 random questions from the full question bank</div>
      <div class="stats">
        <div class="stat"><div class="stat-num">270</div><div class="stat-label">Total Questions</div></div>
        <div class="stat"><div class="stat-num">30</div><div class="stat-label">Per Session</div></div>
        <div class="stat"><div class="stat-num">85%</div><div class="stat-label">Passing Score</div></div>
      </div>
      <button class="btn-primary" onclick="startQuiz()">Start Quiz (30 random)</button>

      <div class="divider">or choose a custom range</div>

      <div class="range-section">
        <div class="range-title">Custom Range</div>
        <div class="range-subtitle">Pick a subset of questions by number (1–270)</div>
        <div class="range-inputs">
          <div class="range-field">
            <label>From Q#</label>
            <input type="number" id="range-from" min="1" max="270" value="1">
            <span class="field-hint">start</span>
          </div>
          <div class="range-field">
            <label>To Q#</label>
            <input type="number" id="range-to" min="1" max="270" value="50">
            <span class="field-hint">end (inclusive)</span>
          </div>
          <div class="range-field">
            <label>Count</label>
            <input type="number" id="range-count" min="1" max="270" value="10">
            <span class="field-hint">how many to pick</span>
          </div>
        </div>
        <div class="range-error" id="range-error"></div>
        <button class="btn-secondary" onclick="startCustomQuiz()">Start Custom Quiz</button>
      </div>
    </div>
  </div>

  <!-- Quiz screen -->
  <div id="quiz-screen" style="display:none">
    <div class="progress-bar-wrap">
      <div class="progress-bar" id="progress-bar" style="width:0%"></div>
    </div>
    <div class="progress-text" id="progress-text">Question 1 of 30</div>
    <div class="card">
      <div class="question-text" id="question-text"></div>
      <div class="options" id="options"></div>
      <div class="feedback" id="feedback"></div>
      <div class="btn-row">
        <button class="btn-secondary" id="btn-submit" onclick="submitAnswer()" disabled>Check Answer</button>
        <button class="btn-primary" id="btn-next" onclick="nextQuestion()" disabled>Next</button>
      </div>
    </div>
  </div>

  <!-- Results screen -->
  <div id="results-screen" style="display:none">
    <div class="card results">
      <div class="score-circle" id="score-circle">
        <div class="score-num" id="score-num"></div>
        <div class="score-label" id="score-total">/ 30</div>
      </div>
      <div class="score-pct" id="score-pct"></div>
      <div class="score-msg" id="score-msg"></div>
      <div class="btn-row" style="justify-content:center">
        <button class="btn-secondary" onclick="showReview()">Review Answers</button>
        <button class="btn-primary" onclick="location.reload()">New Quiz</button>
      </div>
      <div class="review-list" id="review-list" style="display:none"></div>
    </div>
  </div>
</div>

<script>
const ALL_QUESTIONS = {questions_json};

let sessionQuestions = [];
let sessionCount = 30;
let currentIdx = 0;
let score = 0;
let selected = new Set();
let answered = false;
let history = [];

function shuffle(arr) {{
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }}
  return a;
}}

function startQuiz() {{
  sessionCount = 30;
  sessionQuestions = shuffle(ALL_QUESTIONS).slice(0, 30);
  beginSession();
}}

function startCustomQuiz() {{
  const errEl = document.getElementById("range-error");
  errEl.textContent = "";

  const from = parseInt(document.getElementById("range-from").value, 10);
  const to   = parseInt(document.getElementById("range-to").value, 10);
  const count = parseInt(document.getElementById("range-count").value, 10);

  if (isNaN(from) || isNaN(to) || isNaN(count)) {{
    errEl.textContent = "Please fill in all three fields.";
    return;
  }}
  if (from < 1 || to > ALL_QUESTIONS.length || from > to) {{
    errEl.textContent = `Q# must be between 1 and ${{ALL_QUESTIONS.length}}, and From ≤ To.`;
    return;
  }}
  const pool = ALL_QUESTIONS.slice(from - 1, to); // convert to 0-based
  if (count < 1 || count > pool.length) {{
    errEl.textContent = `Count must be between 1 and ${{pool.length}} (the size of your range).`;
    return;
  }}

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
  document.getElementById("feedback").textContent = "";
  document.getElementById("btn-submit").disabled = true;
  document.getElementById("btn-next").disabled = true;
  document.getElementById("btn-next").textContent = currentIdx === sessionCount - 1 ? "See Results" : "Next";
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

  document.getElementById("btn-submit").disabled = selected.size === 0;
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

function nextQuestion() {{
  if (currentIdx === sessionCount - 1) {{
    showResults();
    return;
  }}
  currentIdx++;
  renderQuestion();
}}

function showResults() {{
  document.getElementById("quiz-screen").style.display = "none";
  document.getElementById("results-screen").style.display = "block";
  document.getElementById("review-list").style.display = "none";

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

function showReview() {{
  const listEl = document.getElementById("review-list");
  if (listEl.style.display !== "none") {{
    listEl.style.display = "none";
    return;
  }}

  listEl.innerHTML = "<h3 style='margin-bottom:16px;font-size:1rem'>Answer Review</h3>";
  history.forEach((entry, i) => {{
    const div = document.createElement("div");
    div.className = "review-item";
    const statusClass = entry.correct ? "ok" : "fail";
    const statusText = entry.correct ? "Correct" : "Incorrect";
    const correctLetters = [...entry.question.correct].join(", ");
    const selectedLetters = [...entry.selected].join(", ") || "—";
    const expHtml = entry.question.explanation
      ? `<div class="review-explanation">${{entry.question.explanation}}</div>`
      : "";
    div.innerHTML = `
      <div class="review-q">Q${{i + 1}}: ${{entry.question.question}}</div>
      <div class="review-status ${{statusClass}}">${{statusText}}</div>
      <div style="font-size:.85rem;color:var(--subtext);margin-top:4px">
        Your answer: <strong>${{selectedLetters}}</strong> &nbsp;|&nbsp;
        Correct: <strong>${{correctLetters}}</strong>
      </div>
      ${{expHtml}}
    `;
    listEl.appendChild(div);
  }});
  listEl.style.display = "block";
}}
</script>
</body>
</html>
"""

with open("quiz.html", "w", encoding="utf-8") as f:
    f.write(html)

print("quiz.html created successfully!")
