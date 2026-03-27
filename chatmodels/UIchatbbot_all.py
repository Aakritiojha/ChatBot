import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_mistralai import ChatMistralAI

PERSONAS = {
    "Beauty": {
        "system": "You are an experienced beauty guru with deep knowledge of skincare, makeup, haircare, and wellness trends.",
        "title": "Beauty Guru",
        "headline": "Your Beauty Advisor",
        "subtitle": "Skincare, makeup & wellness — honest advice, no filters.",
        "welcome_title": "What's on your mind?",
        "welcome_sub": "Ask about routines, products, ingredients, or anything beauty.",
        "placeholder": "Ask anything about beauty…",
        "suggestions": ["Morning skincare routine", "Ingredients to avoid", "Dewy makeup look", "Oily skin tips"],
        "accent": "#FF6EB4",
        "accent2": "#C2185B",
        "glow1": "rgba(255,110,180,0.55)",
        "glow2": "rgba(194,24,91,0.35)",
        "glow3": "rgba(255,64,129,0.25)",
        "orb1": "rgba(255,110,180,0.30)",
        "orb2": "rgba(194,24,91,0.20)",
        "orb3": "rgba(255,0,110,0.15)",
        "grad_a": "#FF6EB4",
        "grad_b": "#FF1493",
        "grad_c": "#C2185B",
        "aurora1": "rgba(255,110,180,0.18)",
        "aurora2": "rgba(194,24,91,0.12)",
        "aurora3": "rgba(255,64,129,0.10)",
        "text": "#FFE0F0",
        "muted": "#C9A0B8",
        "border": "rgba(255,110,180,0.25)",
        "user_bubble_a": "#FF6EB4",
        "user_bubble_b": "#C2185B",
        "bot_bg": "rgba(30,10,22,0.75)",
        "input_bg": "rgba(25,8,18,0.85)",
        "chip_bg": "rgba(255,110,180,0.10)",
        "chip_border": "rgba(255,110,180,0.30)",
        "chip_text": "#FF6EB4",
        "headline_grad": "linear-gradient(120deg, #FF6EB4 0%, #FF1493 50%, #C2185B 100%)",
    },
    "Finance": {
        "system": "You are a seasoned financial advisor with expertise in investments, budgeting, markets, and wealth management. Provide clear, actionable financial guidance.",
        "title": "Finance Advisor",
        "headline": "Your Finance Advisor",
        "subtitle": "Investments, budgeting & markets — clear thinking, plain language.",
        "welcome_title": "What would you like to explore?",
        "welcome_sub": "Ask about investing, saving, budgeting, or financial planning.",
        "placeholder": "Ask anything about finance…",
        "suggestions": ["How to start investing", "Build an emergency fund", "Understand index funds", "Budgeting basics"],
        "accent": "#00E5A0",
        "accent2": "#00796B",
        "glow1": "rgba(0,229,160,0.50)",
        "glow2": "rgba(0,121,107,0.30)",
        "glow3": "rgba(0,200,130,0.22)",
        "orb1": "rgba(0,229,160,0.28)",
        "orb2": "rgba(0,121,107,0.18)",
        "orb3": "rgba(0,255,160,0.12)",
        "grad_a": "#00E5A0",
        "grad_b": "#00BFA5",
        "grad_c": "#00796B",
        "aurora1": "rgba(0,229,160,0.15)",
        "aurora2": "rgba(0,121,107,0.10)",
        "aurora3": "rgba(0,200,130,0.08)",
        "text": "#C8FFF0",
        "muted": "#80C4B0",
        "border": "rgba(0,229,160,0.22)",
        "user_bubble_a": "#00E5A0",
        "user_bubble_b": "#00796B",
        "bot_bg": "rgba(4,22,18,0.75)",
        "input_bg": "rgba(2,16,12,0.85)",
        "chip_bg": "rgba(0,229,160,0.08)",
        "chip_border": "rgba(0,229,160,0.28)",
        "chip_text": "#00E5A0",
        "headline_grad": "linear-gradient(120deg, #00E5A0 0%, #00BFA5 50%, #00796B 100%)",
    },
    "Artist": {
        "system": "You are a versatile creative artist with expertise in painting, digital art, illustration, design principles, color theory, and artistic techniques across all mediums.",
        "title": "Creative Artist",
        "headline": "Your Creative Guide",
        "subtitle": "Painting, design & illustration — guidance for every level.",
        "welcome_title": "What are you creating?",
        "welcome_sub": "Ask about techniques, tools, colour theory, or getting unstuck.",
        "placeholder": "Ask anything about art…",
        "suggestions": ["Colour theory basics", "Improve my composition", "Digital vs traditional", "Overcome creative block"],
        "accent": "#B06EFF",
        "accent2": "#6A0DAD",
        "glow1": "rgba(176,110,255,0.55)",
        "glow2": "rgba(106,13,173,0.35)",
        "glow3": "rgba(200,64,255,0.22)",
        "orb1": "rgba(176,110,255,0.30)",
        "orb2": "rgba(106,13,173,0.20)",
        "orb3": "rgba(220,100,255,0.15)",
        "grad_a": "#B06EFF",
        "grad_b": "#9C27B0",
        "grad_c": "#6A0DAD",
        "aurora1": "rgba(176,110,255,0.18)",
        "aurora2": "rgba(106,13,173,0.12)",
        "aurora3": "rgba(200,64,255,0.10)",
        "text": "#EDD8FF",
        "muted": "#B090CC",
        "border": "rgba(176,110,255,0.25)",
        "user_bubble_a": "#B06EFF",
        "user_bubble_b": "#6A0DAD",
        "bot_bg": "rgba(16,4,28,0.75)",
        "input_bg": "rgba(10,2,20,0.85)",
        "chip_bg": "rgba(176,110,255,0.10)",
        "chip_border": "rgba(176,110,255,0.30)",
        "chip_text": "#B06EFF",
        "headline_grad": "linear-gradient(120deg, #B06EFF 0%, #9C27B0 50%, #6A0DAD 100%)",
    },
    "Philosopher": {
        "system": "You are a profound philosopher well-versed in classical and contemporary philosophy, ethics, metaphysics, epistemology, and existentialism. Guide thoughtful reflection and deep inquiry.",
        "title": "Philosopher",
        "headline": "The Examined Life",
        "subtitle": "Ethics, meaning & consciousness — no easy answers, good questions.",
        "welcome_title": "What are you thinking about?",
        "welcome_sub": "Bring any question — big, small, half-formed, uncertain.",
        "placeholder": "Ask anything…",
        "suggestions": ["What is consciousness?", "Do we have free will?", "Stoicism in modern life", "Ethics of AI"],
        "accent": "#78C8E0",
        "accent2": "#01579B",
        "glow1": "rgba(120,200,224,0.50)",
        "glow2": "rgba(1,87,155,0.30)",
        "glow3": "rgba(64,180,220,0.22)",
        "orb1": "rgba(120,200,224,0.28)",
        "orb2": "rgba(1,87,155,0.18)",
        "orb3": "rgba(80,200,240,0.12)",
        "grad_a": "#78C8E0",
        "grad_b": "#29B6F6",
        "grad_c": "#01579B",
        "aurora1": "rgba(120,200,224,0.15)",
        "aurora2": "rgba(1,87,155,0.10)",
        "aurora3": "rgba(64,180,220,0.08)",
        "text": "#D0F0FF",
        "muted": "#88B8CC",
        "border": "rgba(120,200,224,0.22)",
        "user_bubble_a": "#78C8E0",
        "user_bubble_b": "#01579B",
        "bot_bg": "rgba(2,12,22,0.75)",
        "input_bg": "rgba(1,8,16,0.85)",
        "chip_bg": "rgba(120,200,224,0.08)",
        "chip_border": "rgba(120,200,224,0.28)",
        "chip_text": "#78C8E0",
        "headline_grad": "linear-gradient(120deg, #78C8E0 0%, #29B6F6 50%, #01579B 100%)",
    },
    "Coach": {
        "system": "You are an elite fitness coach and sports nutritionist with expertise in strength training, cardio, flexibility, meal planning, and optimising athletic performance for all levels.",
        "title": "Fitness Coach",
        "headline": "Your Fitness Coach",
        "subtitle": "Training, nutrition & recovery — practical advice that actually works.",
        "welcome_title": "What's your goal?",
        "welcome_sub": "Ask about training, nutrition, recovery, or performance.",
        "placeholder": "Ask anything about fitness…",
        "suggestions": ["Build muscle at home", "High-protein meals", "Best cardio for fat loss", "Improve recovery"],
        "accent": "#FF6B35",
        "accent2": "#B71C1C",
        "glow1": "rgba(255,107,53,0.55)",
        "glow2": "rgba(183,28,28,0.35)",
        "glow3": "rgba(255,80,0,0.22)",
        "orb1": "rgba(255,107,53,0.30)",
        "orb2": "rgba(183,28,28,0.20)",
        "orb3": "rgba(255,50,0,0.15)",
        "grad_a": "#FF6B35",
        "grad_b": "#FF3D00",
        "grad_c": "#B71C1C",
        "aurora1": "rgba(255,107,53,0.18)",
        "aurora2": "rgba(183,28,28,0.12)",
        "aurora3": "rgba(255,80,0,0.10)",
        "text": "#FFE8DC",
        "muted": "#CC9070",
        "border": "rgba(255,107,53,0.25)",
        "user_bubble_a": "#FF6B35",
        "user_bubble_b": "#B71C1C",
        "bot_bg": "rgba(22,6,2,0.75)",
        "input_bg": "rgba(16,4,2,0.85)",
        "chip_bg": "rgba(255,107,53,0.10)",
        "chip_border": "rgba(255,107,53,0.30)",
        "chip_text": "#FF6B35",
        "headline_grad": "linear-gradient(120deg, #FF6B35 0%, #FF3D00 50%, #B71C1C 100%)",
    },
}

st.set_page_config(
    page_title="Chat",
    page_icon="—",
    layout="centered",
    initial_sidebar_state="collapsed",
)

@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506", temperature=1, max_tokens=500)

model = get_model()

if "active_persona" not in st.session_state:
    st.session_state.active_persona = "Beauty"
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=PERSONAS["Beauty"]["system"])]

p = PERSONAS[st.session_state.active_persona]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@500;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {{
    background: #050508 !important;
    font-family: 'Outfit', sans-serif !important;
    color: {p["text"]} !important;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
}}

/* ── Static dark base ── */
[data-testid="stApp"]::before {{
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 15%, {p["aurora1"]} 0%, transparent 60%),
        radial-gradient(ellipse 60% 80% at 90% 80%, {p["aurora2"]} 0%, transparent 60%),
        radial-gradient(ellipse 50% 50% at 50% 50%, {p["aurora3"]} 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: auroraShift 18s ease-in-out infinite alternate;
}}

@keyframes auroraShift {{
    0%   {{ opacity: 0.7; filter: blur(0px); }}
    50%  {{ opacity: 1.0; filter: blur(2px); }}
    100% {{ opacity: 0.8; filter: blur(0px); }}
}}

/* ── Floating orbs ── */
.orb {{
    position: fixed;
    border-radius: 50%;
    filter: blur(70px);
    pointer-events: none;
    z-index: 0;
    animation: orbFloat linear infinite;
}}
.orb1 {{
    width: 520px; height: 520px;
    background: radial-gradient(circle, {p["orb1"]} 0%, transparent 70%);
    top: -120px; left: -160px;
    animation-duration: 22s;
    animation-name: orbFloat1;
}}
.orb2 {{
    width: 400px; height: 400px;
    background: radial-gradient(circle, {p["orb2"]} 0%, transparent 70%);
    bottom: 80px; right: -120px;
    animation-duration: 28s;
    animation-name: orbFloat2;
}}
.orb3 {{
    width: 300px; height: 300px;
    background: radial-gradient(circle, {p["orb3"]} 0%, transparent 70%);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    animation-duration: 35s;
    animation-name: orbFloat3;
}}

@keyframes orbFloat1 {{
    0%   {{ transform: translate(0px, 0px) scale(1);    opacity: 0.8; }}
    25%  {{ transform: translate(60px, 40px) scale(1.1); opacity: 1;   }}
    50%  {{ transform: translate(20px, 80px) scale(0.95); opacity: 0.7; }}
    75%  {{ transform: translate(-40px, 30px) scale(1.05); opacity: 0.9; }}
    100% {{ transform: translate(0px, 0px) scale(1);    opacity: 0.8; }}
}}
@keyframes orbFloat2 {{
    0%   {{ transform: translate(0px, 0px) scale(1);    opacity: 0.7; }}
    33%  {{ transform: translate(-50px, -30px) scale(1.08); opacity: 1; }}
    66%  {{ transform: translate(30px, -60px) scale(0.92); opacity: 0.8; }}
    100% {{ transform: translate(0px, 0px) scale(1);    opacity: 0.7; }}
}}
@keyframes orbFloat3 {{
    0%   {{ transform: translate(-50%, -50%) scale(1) rotate(0deg);   opacity: 0.5; }}
    25%  {{ transform: translate(-45%, -55%) scale(1.15) rotate(90deg); opacity: 0.8; }}
    50%  {{ transform: translate(-55%, -45%) scale(0.9) rotate(180deg); opacity: 0.5; }}
    75%  {{ transform: translate(-48%, -52%) scale(1.08) rotate(270deg); opacity: 0.7; }}
    100% {{ transform: translate(-50%, -50%) scale(1) rotate(360deg);  opacity: 0.5; }}
}}

/* ── Sparkle ring ── */
.ring {{
    position: fixed;
    border-radius: 50%;
    border: 1px solid {p["accent"]};
    opacity: 0;
    pointer-events: none;
    z-index: 0;
    animation: ringPulse 6s ease-in-out infinite;
}}
.ring1 {{ width: 300px; height: 300px; top: 10%; left: 5%; animation-delay: 0s; }}
.ring2 {{ width: 200px; height: 200px; bottom: 20%; right: 8%; animation-delay: 2s; }}
.ring3 {{ width: 160px; height: 160px; top: 60%; left: 70%; animation-delay: 4s; }}

@keyframes ringPulse {{
    0%   {{ transform: scale(0.85); opacity: 0;    }}
    30%  {{ opacity: 0.18; }}
    60%  {{ transform: scale(1.15); opacity: 0.08; }}
    100% {{ transform: scale(1.3);  opacity: 0;    }}
}}

/* ── Scan line ── */
.scanline {{
    position: fixed;
    left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {p["accent"]}, transparent);
    opacity: 0;
    z-index: 0;
    pointer-events: none;
    animation: scanDown 10s linear infinite;
}}
@keyframes scanDown {{
    0%   {{ top: -2px;   opacity: 0;    }}
    5%   {{ opacity: 0.25; }}
    95%  {{ opacity: 0.10; }}
    100% {{ top: 100vh;  opacity: 0;    }}
}}

/* ── Hide Streamlit chrome ── */
#MainMenu, header, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {{
    display: none !important;
    visibility: hidden !important;
}}

[data-testid="stMainBlockContainer"] {{
    max-width: 720px !important;
    margin: 0 auto !important;
    padding: 0 1.4rem 8rem !important;
    position: relative; z-index: 1;
}}

/* ── Tab buttons ── */
[data-testid="stHorizontalBlock"] .stButton > button {{
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    color: rgba(200,200,220,0.45) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 0.4rem 0.85rem !important;
    transition: color 0.25s, border-color 0.25s, text-shadow 0.25s !important;
    box-shadow: none !important;
    width: 100% !important;
    cursor: pointer !important;
}}
[data-testid="stHorizontalBlock"] .stButton > button:hover {{
    color: {p["accent"]} !important;
    background: transparent !important;
    border-bottom-color: {p["border"]} !important;
    text-shadow: 0 0 12px {p["glow1"]} !important;
    transform: none !important;
    box-shadow: none !important;
}}
[data-testid="stHorizontalBlock"] .stButton > button[kind="primary"] {{
    color: {p["accent"]} !important;
    border-bottom: 2px solid {p["accent"]} !important;
    font-weight: 700 !important;
    background: transparent !important;
    text-shadow: 0 0 18px {p["glow1"]}, 0 0 30px {p["glow2"]} !important;
    box-shadow: none !important;
    transform: none !important;
}}

/* ── Tab underline ── */
.tab-underline {{
    height: 1px;
    background: linear-gradient(90deg, transparent, {p["border"]}, transparent);
    margin-bottom: 2.8rem;
    margin-top: -2px;
}}

/* ── Hero ── */
.hero {{
    padding: 0 0 2rem;
    animation: fadeUp 0.7s cubic-bezier(.22,1,.36,1) both;
}}
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(28px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
.hero-eyebrow {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: {p["accent"]};
    margin-bottom: 0.8rem;
    display: block;
    text-shadow: 0 0 18px {p["glow1"]};
    animation: glowPulse 3s ease-in-out infinite;
}}
@keyframes glowPulse {{
    0%, 100% {{ text-shadow: 0 0 14px {p["glow1"]}, 0 0 28px {p["glow2"]}; opacity: 0.9; }}
    50%       {{ text-shadow: 0 0 28px {p["glow1"]}, 0 0 50px {p["glow2"]}; opacity: 1.0; }}
}}
.hero h1 {{
    font-family: 'Syne', sans-serif !important;
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    line-height: 1.08 !important;
    margin: 0 0 0.75rem !important;
    letter-spacing: -0.03em;
    background: {p["headline_grad"]};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    background-size: 200% 100%;
    animation: gradientShift 5s ease-in-out infinite alternate;
    filter: drop-shadow(0 0 24px {p["glow2"]});
}}
@keyframes gradientShift {{
    0%   {{ background-position: 0% 50%;   }}
    100% {{ background-position: 100% 50%; }}
}}
.hero p {{
    font-size: 1rem !important;
    color: {p["muted"]};
    font-weight: 300;
    line-height: 1.65;
}}

/* ── Divider ── */
.rule {{
    height: 1px;
    background: linear-gradient(90deg, transparent, {p["border"]}, transparent);
    margin: 0 0 2rem;
    animation: scaleIn 0.6s 0.15s ease both;
    transform-origin: center;
}}
@keyframes scaleIn {{
    from {{ transform: scaleX(0); opacity: 0; }}
    to   {{ transform: scaleX(1); opacity: 1; }}
}}

/* ── Welcome ── */
.welcome {{
    padding: 0.4rem 0 1.4rem;
    animation: fadeUp 0.6s 0.1s cubic-bezier(.22,1,.36,1) both;
}}
.welcome h3 {{
    font-family: 'Syne', sans-serif;
    font-size: 1.45rem;
    font-weight: 600;
    color: {p["text"]};
    margin: 0 0 0.45rem;
    line-height: 1.3;
}}
.welcome p {{
    font-size: 0.92rem;
    color: {p["muted"]};
    margin: 0 0 1.4rem;
    line-height: 1.65;
    font-weight: 300;
}}
.chips {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
.chip {{
    font-size: 0.82rem;
    font-weight: 500;
    color: {p["chip_text"]};
    background: {p["chip_bg"]};
    border: 1px solid {p["chip_border"]};
    padding: 6px 16px;
    border-radius: 999px;
    font-family: 'Outfit', sans-serif;
    cursor: default;
    transition: background 0.2s, box-shadow 0.2s;
    box-shadow: 0 0 0 0 transparent;
}}
.chip:hover {{
    background: rgba(255,255,255,0.06);
    box-shadow: 0 0 16px {p["glow2"]};
}}

/* ── Messages ── */
.chat-wrap {{
    display: flex;
    flex-direction: column;
    gap: 1.6rem;
    padding-bottom: 0.5rem;
}}
.msg-row-user {{
    display: flex;
    justify-content: flex-end;
    animation: slideRight 0.38s cubic-bezier(.22,1,.36,1) both;
}}
@keyframes slideRight {{
    from {{ opacity: 0; transform: translateX(26px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}
.bubble-user {{
    background: linear-gradient(135deg, {p["user_bubble_a"]} 0%, {p["user_bubble_b"]} 100%);
    color: #fff;
    padding: 0.85rem 1.25rem;
    border-radius: 20px 20px 4px 20px;
    max-width: 74%;
    font-size: 0.95rem;
    line-height: 1.55;
    font-weight: 400;
    font-family: 'Outfit', sans-serif;
    box-shadow: 0 0 28px {p["glow2"]}, 0 8px 32px rgba(0,0,0,0.4);
    position: relative;
}}
.bubble-user::after {{
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: 20px 20px 4px 20px;
    background: linear-gradient(135deg, {p["glow1"]}, transparent);
    opacity: 0.35;
    z-index: -1;
    filter: blur(6px);
}}
.msg-row-bot {{
    display: flex;
    justify-content: flex-start;
    gap: 0.8rem;
    align-items: flex-start;
    animation: slideLeft 0.38s cubic-bezier(.22,1,.36,1) both;
}}
@keyframes slideLeft {{
    from {{ opacity: 0; transform: translateX(-26px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}
.bot-mark {{
    width: 36px; height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, {p["user_bubble_a"]} 0%, {p["user_bubble_b"]} 100%);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
    font-size: 0.68rem;
    font-weight: 700;
    color: white;
    letter-spacing: 0.06em;
    font-family: 'Outfit', sans-serif;
    box-shadow: 0 0 18px {p["glow2"]}, 0 3px 12px rgba(0,0,0,0.4);
    animation: botMarkGlow 3s ease-in-out infinite;
}}
@keyframes botMarkGlow {{
    0%, 100% {{ box-shadow: 0 0 12px {p["glow2"]}, 0 3px 12px rgba(0,0,0,0.4); }}
    50%       {{ box-shadow: 0 0 28px {p["glow1"]}, 0 3px 18px rgba(0,0,0,0.5); }}
}}
.bubble-bot {{
    background: {p["bot_bg"]};
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid {p["border"]};
    color: {p["text"]};
    padding: 0.85rem 1.25rem;
    border-radius: 4px 20px 20px 20px;
    max-width: 74%;
    font-size: 0.95rem;
    line-height: 1.68;
    font-weight: 300;
    font-family: 'Outfit', sans-serif;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04);
}}

/* ── Typing dots ── */
.typing {{
    display: flex;
    gap: 5px;
    align-items: center;
    padding: 0.3rem 0.2rem;
}}
.typing span {{
    width: 7px; height: 7px;
    background: {p["accent"]};
    border-radius: 50%;
    box-shadow: 0 0 8px {p["glow1"]};
    animation: dotPulse 1.3s infinite ease-in-out;
}}
.typing span:nth-child(2) {{ animation-delay: 0.2s; }}
.typing span:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes dotPulse {{
    0%, 80%, 100% {{ transform: scale(0.65); opacity: 0.35; box-shadow: 0 0 4px {p["glow2"]}; }}
    40%            {{ transform: scale(1.2);  opacity: 1.0;  box-shadow: 0 0 14px {p["glow1"]}; }}
}}

/* ── Clear button ── */
div[data-testid="stVerticalBlock"] > div .stButton > button {{
    background: transparent !important;
    border: 1px solid {p["border"]} !important;
    color: {p["muted"]} !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 5px 20px !important;
    border-radius: 999px !important;
    letter-spacing: 0.04em !important;
    transition: all 0.22s !important;
    text-transform: none !important;
}}
div[data-testid="stVerticalBlock"] > div .stButton > button:hover {{
    border-color: {p["accent"]} !important;
    color: {p["accent"]} !important;
    background: {p["chip_bg"]} !important;
    box-shadow: 0 0 16px {p["glow2"]} !important;
    transform: none !important;
}}

/* ── Chat input ── */
[data-testid="stChatInput"] {{
    position: fixed !important;
    bottom: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(720px, 100vw) !important;
    padding: 1rem 1.4rem 1.3rem !important;
    background: linear-gradient(to top, rgba(5,5,8,0.98) 0%, rgba(5,5,8,0.85) 65%, transparent 100%) !important;
    backdrop-filter: blur(28px) !important;
    -webkit-backdrop-filter: blur(28px) !important;
    border-top: none !important;
    box-shadow: none !important;
    z-index: 9999 !important;
}}
[data-testid="stChatInput"] textarea {{
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 400 !important;
    border-radius: 16px !important;
    background: {p["input_bg"]} !important;
    border: 1px solid {p["border"]} !important;
    color: {p["text"]} !important;
    padding: 0.8rem 1.15rem !important;
    box-shadow: 0 0 0 0 transparent, inset 0 1px 0 rgba(255,255,255,0.04) !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
    line-height: 1.55 !important;
}}
[data-testid="stChatInput"] textarea:focus {{
    border-color: {p["accent"]} !important;
    outline: none !important;
    box-shadow: 0 0 0 3px {p["chip_bg"]}, 0 0 24px {p["glow2"]} !important;
    background: {p["input_bg"]} !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{
    color: {p["muted"]} !important;
    opacity: 0.55 !important;
}}
[data-testid="stChatInput"] button {{
    background: linear-gradient(135deg, {p["user_bubble_a"]} 0%, {p["user_bubble_b"]} 100%) !important;
    border-radius: 12px !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 0 20px {p["glow2"]}, 0 4px 16px rgba(0,0,0,0.3) !important;
    transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s !important;
}}
[data-testid="stChatInput"] button:hover {{
    opacity: 0.88 !important;
    transform: scale(1.06) !important;
    box-shadow: 0 0 32px {p["glow1"]}, 0 4px 20px rgba(0,0,0,0.4) !important;
}}
</style>

<!-- Ambient orbs & effects injected into the DOM -->
<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>
<div class="ring ring1"></div>
<div class="ring ring2"></div>
<div class="ring ring3"></div>
<div class="scanline"></div>
""", unsafe_allow_html=True)

# ── Persona tabs ───────────────────────────────────────────────────────────────
st.markdown('<div style="padding-top:2rem;"></div>', unsafe_allow_html=True)
cols = st.columns(len(PERSONAS))
for i, name in enumerate(PERSONAS.keys()):
    with cols[i]:
        is_active = st.session_state.active_persona == name
        if st.button(
            PERSONAS[name]["title"],
            key=f"p_{name}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            if not is_active:
                st.session_state.active_persona = name
                st.session_state.messages = [SystemMessage(content=PERSONAS[name]["system"])]
                st.rerun()

st.markdown(f'<div class="tab-underline"></div>', unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <span class="hero-eyebrow">{p["title"]}</span>
    <h1>{p["headline"]}</h1>
    <p>{p["subtitle"]}</p>
</div>
<div class="rule"></div>
""", unsafe_allow_html=True)

# ── Welcome card ───────────────────────────────────────────────────────────────
chat_history = [m for m in st.session_state.messages if not isinstance(m, SystemMessage)]

if not chat_history:
    chips_html = "".join(f'<span class="chip">{s}</span>' for s in p["suggestions"])
    st.markdown(f"""
<div class="welcome">
    <h3>{p["welcome_title"]}</h3>
    <p>{p["welcome_sub"]}</p>
    <div class="chips">{chips_html}</div>
</div>
""", unsafe_allow_html=True)

# ── Messages ───────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

for msg in chat_history:
    if isinstance(msg, HumanMessage):
        st.markdown(
            f'<div class="msg-row-user"><div class="bubble-user">{msg.content}</div></div>',
            unsafe_allow_html=True,
        )
    elif isinstance(msg, AIMessage):
        label = p["title"][:2].upper()
        st.markdown(
            f'<div class="msg-row-bot">'
            f'<div class="bot-mark">{label}</div>'
            f'<div class="bubble-bot">{msg.content}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# ── Clear ──────────────────────────────────────────────────────────────────────
if chat_history:
    col1, col2, col3 = st.columns([4, 1.4, 4])
    with col2:
        if st.button("Clear chat"):
            st.session_state.messages = [SystemMessage(content=p["system"])]
            st.rerun()

# ── Input ──────────────────────────────────────────────────────────────────────
if prompt := st.chat_input(p["placeholder"]):
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.markdown(
        f'<div class="msg-row-user"><div class="bubble-user">{prompt}</div></div>',
        unsafe_allow_html=True,
    )

    label = p["title"][:2].upper()
    typing_ph = st.empty()
    typing_ph.markdown(
        f'<div class="msg-row-bot">'
        f'<div class="bot-mark">{label}</div>'
        f'<div class="bubble-bot"><div class="typing"><span></span><span></span><span></span></div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    response = model.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response.content))

    typing_ph.markdown(
        f'<div class="msg-row-bot">'
        f'<div class="bot-mark">{label}</div>'
        f'<div class="bubble-bot">{response.content}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )