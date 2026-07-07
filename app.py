from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_career_advice(message, conversation_history):
    messages = [
        {
            "role": "system",
            "content": """You are a friendly and expert AI Career Advisor. Your job is to:
            1. Ask the user about their skills, interests, education, and experience level
            2. Based on their answers, suggest 2-3 specific career paths that match their profile
            3. For each career path, write the ACTUAL JOB TITLE (like "Conversational AI Engineer: 92%" or "Data Scientist: 90%") on its own line - NEVER write the literal words "Career Title"
            4. Follow with role description, skills to learn next, and salary range
            5. Be conversational, encouraging, and ask one question at a time
            6. Once you have enough information (skills + interests), provide career recommendations with the percentage format
            
            Example format:
            Conversational AI Engineer: 92%
            You'd design chatbots...
            
            Keep responses concise and friendly. Use emojis occasionally."""
        }
    ]
    
    for msg in conversation_history:
        messages.append({"role": msg["role"], "content": msg["text"]})
    
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )
    return response.choices[0].message.content

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Career Advisor AI</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --rose: #8EB69B;
  --rose-dark: #235347;
  --rose-light: #DAF1DE;
  --bg: #051F20;
  --bg2: #0B2B26;
  --bg3: #163832;
  --text: #DAF1DE;
  --text-muted: #8EB69B;
  --text-dim: #235347;
  --border: rgba(142,182,155,0.15);
}
html { scroll-behavior: smooth; }
body { font-family: 'Plus Jakarta Sans', sans-serif; background: var(--bg); color: var(--text); overflow: hidden; height: 100vh; display: flex; flex-direction: column; }
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: rgba(142,182,155,0.2); border-radius: 2px; }

.bg-blob { position: fixed; border-radius: 50%; filter: blur(100px); pointer-events: none; z-index: 0; animation: bFloat ease-in-out infinite; }
.bg-blob-1 { width: 600px; height: 600px; background: radial-gradient(circle, rgba(142,182,155,0.1), transparent); top: -200px; right: -100px; animation-duration: 16s; }
.bg-blob-2 { width: 400px; height: 400px; background: radial-gradient(circle, rgba(35,83,71,0.15), transparent); bottom: 0; left: -80px; animation-duration: 20s; animation-direction: reverse; }
@keyframes bFloat { 0%,100%{transform:translate(0,0)} 50%{transform:translate(15px,-25px)} }

nav { position: relative; z-index: 100; display: flex; align-items: center; justify-content: center; padding: 16px 48px; background: rgba(5,31,32,0.85); backdrop-filter: blur(24px); border-bottom: 1px solid var(--border); flex-shrink: 0; }
.nav-user-block { position: absolute; left: 48px; display: flex; align-items: center; gap: 10px; }
.nav-user-avatar { width: 36px; height: 36px; background: linear-gradient(135deg, #8EB69B, #235347); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px; box-shadow: 0 4px 12px rgba(142,182,155,0.3); }
.nav-user-name { font-family: 'Playfair Display', serif; font-size: 14px; font-weight: 600; color: var(--text); }
.nav-user-role { font-size: 10px; color: var(--text-muted); font-weight: 500; }
.nav-logo-block { text-align: center; }
.nav-logo { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 600; color: var(--rose-light); display: flex; align-items: center; gap: 10px; justify-content: center; }
.nav-logo-sub { font-size: 11px; color: var(--text-muted); font-weight: 400; margin-top: 2px; }
.nav-right { position: absolute; right: 48px; }
.status-pill { display: flex; align-items: center; gap: 7px; padding: 7px 16px; background: rgba(142,182,155,0.08); border: 1px solid rgba(142,182,155,0.18); border-radius: 20px; font-size: 12px; font-weight: 600; color: var(--rose); }
.rose-dot { width: 7px; height: 7px; background: var(--rose); border-radius: 50%; box-shadow: 0 0 6px var(--rose); animation: roseDot 2s infinite; }
@keyframes roseDot { 0%,100%{opacity:1} 50%{opacity:0.3} }

.layout { display: flex; flex: 1; overflow: hidden; position: relative; z-index: 1; }

.sidebar { width: 300px; background: rgba(5,31,32,0.5); backdrop-filter: blur(20px); border-right: 1px solid var(--border); display: flex; flex-direction: column; overflow: hidden; flex-shrink: 0; }

.sidebar-progress { padding: 22px; border-bottom: 1px solid var(--border); }
.sidebar-label { font-size: 10px; font-weight: 700; color: var(--text-dim); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 14px; }
.prog-item { margin-bottom: 12px; }
.prog-top { display: flex; justify-content: space-between; margin-bottom: 5px; }
.prog-top span { font-size: 12px; color: var(--text-muted); }
.prog-top strong { font-size: 12px; color: var(--rose); font-weight: 700; }
.prog-bar { height: 4px; background: rgba(255,255,255,0.04); border-radius: 2px; }
.prog-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #8EB69B, #DAF1DE); transition: width 0.6s ease; }

.sidebar-matches { padding: 22px; flex: 1; overflow-y: auto; }
.match-item { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border-radius: 12px; margin-bottom: 8px; border: 1px solid transparent; cursor: pointer; transition: all 0.2s; }
.match-item:hover, .match-item.active { background: rgba(142,182,155,0.06); border-color: rgba(142,182,155,0.15); }
.match-icon { width: 36px; height: 36px; background: rgba(142,182,155,0.1); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.match-info { flex: 1; }
.match-title { font-size: 13px; font-weight: 600; color: var(--text); margin-bottom: 2px; }
.match-pct { font-size: 11px; color: var(--rose); font-weight: 600; }

.chat-main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

.messages { flex: 1; overflow-y: auto; padding: 28px 36px; display: flex; flex-direction: column; gap: 22px; }

.msg-row { display: flex; gap: 14px; align-items: flex-start; max-width: 75%; }
.msg-row.user { align-self: flex-end; flex-direction: row-reverse; }

.avatar { width: 40px; height: 40px; border-radius: 12px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.ai-av { background: linear-gradient(135deg, #8EB69B, #235347); box-shadow: 0 4px 14px rgba(142,182,155,0.3); border: 1px solid rgba(255,255,255,0.1); }
.user-av { background: rgba(255,255,255,0.04); border: 1px solid var(--border); }

.msg-content { display: flex; flex-direction: column; gap: 5px; }
.msg-label { font-size: 10px; font-weight: 700; color: var(--text-dim); letter-spacing: 0.8px; text-transform: uppercase; }
.user .msg-label { text-align: right; color: var(--rose); }

.bubble { padding: 14px 20px; font-size: 14px; line-height: 1.8; font-weight: 400; }
.ai-bubble { background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 4px 18px 18px 18px; color: #c9e0d0; backdrop-filter: blur(10px); white-space: pre-wrap; }
.user-bubble { background: linear-gradient(135deg, rgba(142,182,155,0.25), rgba(35,83,71,0.2)); border: 1px solid rgba(142,182,155,0.3); border-radius: 18px 4px 18px 18px; color: var(--text); }

.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.chip { padding: 6px 16px; background: rgba(142,182,155,0.08); border: 1px solid rgba(142,182,155,0.2); border-radius: 20px; font-size: 12px; font-weight: 500; color: var(--rose-light); cursor: pointer; transition: all 0.2s; }
.chip:hover { background: rgba(142,182,155,0.15); color: var(--text); border-color: rgba(142,182,155,0.35); }

.input-section { padding: 14px 36px 18px; background: rgba(5,31,32,0.5); backdrop-filter: blur(20px); border-top: 1px solid var(--border); flex-shrink: 0; }
.input-wrap { display: flex; gap: 10px; align-items: center; background: rgba(255,255,255,0.02); border: 1px solid rgba(142,182,155,0.18); border-radius: 28px; padding: 5px 5px 5px 22px; transition: all 0.3s; }
.input-wrap:focus-within { border-color: rgba(142,182,155,0.4); box-shadow: 0 0 0 3px rgba(142,182,155,0.08); }
.input-wrap input { flex: 1; background: transparent; border: none; font-size: 14px; color: var(--text); outline: none; font-family: inherit; font-weight: 400; padding: 9px 0; }
.input-wrap input::placeholder { color: var(--text-dim); }
.send-btn { padding: 11px 24px; background: linear-gradient(135deg, #8EB69B, #235347); border: none; border-radius: 22px; font-size: 14px; font-weight: 600; color: white; cursor: pointer; font-family: inherit; box-shadow: 0 4px 14px rgba(142,182,155,0.25); transition: all 0.2s; white-space: nowrap; }
.send-btn:hover { transform: scale(1.04); box-shadow: 0 6px 22px rgba(142,182,155,0.4); }
.input-hint { font-size: 11px; color: var(--text-dim); text-align: center; margin-top: 8px; }

.loading-dots { display: flex; gap: 4px; padding: 14px 20px; }
.loading-dots span { width: 6px; height: 6px; background: var(--rose); border-radius: 50%; animation: loadBounce 1.4s infinite ease-in-out; }
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes loadBounce { 0%,80%,100%{transform:scale(0.6);opacity:0.4} 40%{transform:scale(1);opacity:1} }
</style>
</head>
<body>

<div class="bg-blob bg-blob-1"></div>
<div class="bg-blob bg-blob-2"></div>

<nav>
  <div class="nav-user-block">
    <div class="nav-user-avatar">🎯</div>
    <div>
      <div class="nav-user-name" id="userName">Welcome!</div>
      <div class="nav-user-role">Career Explorer</div>
    </div>
  </div>
  <div class="nav-logo-block">
    <div class="nav-logo">🎯 Career Advisor AI</div>
    <div class="nav-logo-sub">Your Personalized AI Career Guidance</div>
  </div>
  <div class="nav-right">
    <div class="status-pill"><div class="rose-dot"></div> Always Available</div>
  </div>
</nav>

<div class="layout">
  <div class="sidebar">
    <div class="sidebar-progress">
      <div class="sidebar-label">Conversation Progress</div>
      <div class="prog-item">
        <div class="prog-top"><span>Messages Sent</span><strong id="msgCount">0</strong></div>
        <div class="prog-bar"><div class="prog-fill" id="msgProgress" style="width:0%"></div></div>
      </div>
    </div>

    <div class="sidebar-matches">
      <div class="sidebar-label">Your Career Matches</div>
      <div id="careerMatches">
        <div class="match-item">
          <div class="match-icon">💭</div>
          <div class="match-info">
            <div class="match-title">No matches yet</div>
            <div class="match-pct">Chat to discover careers</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="chat-main">
    <div class="messages" id="messages">
      <div class="msg-row">
        <div class="avatar ai-av">🎯</div>
        <div class="msg-content">
          <div class="msg-label">Career Advisor AI</div>
          <div class="bubble ai-bubble">Hello! 🌿 I'm your AI Career Advisor.

I'll help you discover the perfect career path based on your unique skills and interests. Let's start — what are your main technical skills?</div>
          <div class="chip-row">
            <div class="chip">Python & AI</div>
            <div class="chip">Web Development</div>
            <div class="chip">Data Science</div>
            <div class="chip">Automation</div>
          </div>
        </div>
      </div>
    </div>

    <div class="input-section">
      <div class="input-wrap">
        <input type="text" id="userInput" placeholder="Tell me about your skills and interests...">
        <button class="send-btn" id="sendBtn">Send ✦</button>
      </div>
      <div class="input-hint">✦ Powered by LLaMA 3.3 · 70B — Your personal career guide</div>
    </div>
  </div>
</div>

<script>
let conversationHistory = [];
let messageCount = 0;
let userName = '';

window.onload = function() {
  userName = prompt("👋 Welcome! What's your name?") || "Guest";
  document.getElementById('userName').textContent = userName;
};

document.querySelectorAll('.chip').forEach(function(chip) {
  chip.addEventListener('click', function() {
    document.getElementById('userInput').value = chip.textContent;
    sendMessage();
  });
});

document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('userInput').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
  const input = document.getElementById('userInput');
  const message = input.value.trim();
  if (!message) return;

  addMessage('user', message);
  conversationHistory.push({role: 'user', text: message});
  input.value = '';
  messageCount++;
  updateProgress();

  const loadingId = addLoading();

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        message: message,
        history: conversationHistory.slice(0, -1)
      })
    });
    const data = await response.json();
    removeLoading(loadingId);
    addMessage('ai', data.reply);
    conversationHistory.push({role: 'assistant', text: data.reply});
    updateCareerMatches(data.reply);
  } catch(e) {
    removeLoading(loadingId);
    addMessage('ai', 'Sorry, something went wrong. Please try again.');
  }
}

function addMessage(role, text) {
  const messages = document.getElementById('messages');
  const row = document.createElement('div');
  row.className = 'msg-row' + (role === 'user' ? ' user' : '');
  
  const avatar = role === 'user' ? '👤' : '🎯';
  const avClass = role === 'user' ? 'user-av' : 'ai-av';
  const label = role === 'user' ? 'You' : 'Career Advisor AI';
  const bubbleClass = role === 'user' ? 'user-bubble' : 'ai-bubble';
  const labelClass = role === 'user' ? 'user' : '';

  row.innerHTML = '<div class="avatar ' + avClass + '">' + avatar + '</div>' +
    '<div class="msg-content">' +
    '<div class="msg-label ' + labelClass + '">' + label + '</div>' +
    '<div class="bubble ' + bubbleClass + '">' + text + '</div>' +
    '</div>';
  messages.appendChild(row);
  messages.scrollTop = messages.scrollHeight;
}

function addLoading() {
  const messages = document.getElementById('messages');
  const row = document.createElement('div');
  const id = 'loading-' + Date.now();
  row.id = id;
  row.className = 'msg-row';
  row.innerHTML = '<div class="avatar ai-av">🎯</div>' +
    '<div class="msg-content">' +
    '<div class="msg-label">Career Advisor AI</div>' +
    '<div class="bubble ai-bubble loading-dots"><span></span><span></span><span></span></div>' +
    '</div>';
  messages.appendChild(row);
  messages.scrollTop = messages.scrollHeight;
  return id;
}

function removeLoading(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function updateProgress() {
  document.getElementById('msgCount').textContent = messageCount;
  const pct = Math.min(messageCount * 15, 100);
  document.getElementById('msgProgress').style.width = pct + '%';
}

function updateCareerMatches(aiReply) {
  const careerIcons = ['🤖','🌐','⚡','📊','💼','🎨','🔬','📱'];
  const regex = /(?:^|\\n)#{0,3}\\s*\\**([A-Z][A-Za-z\\s\\/]+?(?:Engineer|Developer|Scientist|Designer|Analyst|Specialist|Manager))\\**[:\\s-]*(\\d{1,3})%/gm;
  let matches = [...aiReply.matchAll(regex)];
  
  if (matches.length === 0) return;

  const container = document.getElementById('careerMatches');
  container.innerHTML = '';
  
  matches.slice(0, 4).forEach(function(m, i) {
    const title = m[1].trim();
    const pct = m[2];
    const div = document.createElement('div');
    div.className = 'match-item';
    div.innerHTML = '<div class="match-icon">' + careerIcons[i % careerIcons.length] + '</div>' +
      '<div class="match-info">' +
      '<div class="match-title">' + title + '</div>' +
      '<div class="match-pct">' + pct + '% Match</div>' +
      '</div>';
    container.appendChild(div);
  });
}
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        history = data.get('history', [])
        
        reply = get_career_advice(message, history)
        return jsonify({'reply': reply})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)