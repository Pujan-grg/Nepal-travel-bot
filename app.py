# ============================================
# 🇳🇵 Nepal Travel AI Assistant
# A comprehensive travel chatbot for Nepal
# Dark mode only - Boxed chat messages
# ============================================

import streamlit as st
import requests
import os
import json
import random
from dotenv import load_dotenv

load_dotenv()

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Nepal Travel Assistant",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Nepal Travel AI Assistant - Your guide to Nepal"
    }
)

# ============================================
# FORCE DARK THEME - No light mode allowed
# ============================================

st.markdown("""
<style>
    /* Force dark on every possible element */
    html, body, [class*="css"], [class*="st-"], .stApp, .main, 
    [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"],
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        background-color: #0E1116 !important;
        color: #FFFFFF !important;
    }
    
    /* Kill any light mode remnants */
    @media (prefers-color-scheme: light) {
        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background-color: #0E1116 !important;
            color: #FFFFFF !important;
        }
    }
    
    /* Streamlit's theme toggle - hide it */
    [data-testid="baseButton-headerNoPadding"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CUSTOM CSS - Boxed chat bubbles
# ============================================

st.markdown("""
<style>
    /* ========== FONTS ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ========== CONTAINER ========== */
    .block-container {
        max-width: 850px !important;
        margin: 0 auto !important;
        padding: 2rem 1.5rem !important;
    }

    /* ========== HEADER ========== */
    .app-header {
        padding: 0.4rem 0 1.2rem 0;
        border-bottom: 2px solid #DC143C;
        margin-bottom: 1.5rem;
    }
    .app-header .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #2C5FA8;
        margin-bottom: 0.35rem;
    }
    .app-header h1 {
        font-size: 2rem;
        color: #FFFFFF;
        margin: 0;
    }
    .app-header .sub {
        color: rgba(255, 255, 255, 0.62);
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }

    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {
        background-color: #161A21 !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] h2 {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #2C5FA8 !important;
    }
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        text-align: left;
        background-color: rgba(255, 255, 255, 0.04) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-left: 3px solid #DC143C !important;
        border-radius: 6px !important;
        padding: 0.6rem 0.9rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
        margin: 3px 0 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(220, 20, 60, 0.15) !important;
        border-left: 3px solid #2C5FA8 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.1);
        margin: 1rem 0;
    }
    section[data-testid="stSidebar"] .stCaption {
        color: rgba(255, 255, 255, 0.62) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.68rem !important;
        line-height: 1.6;
    }

    /* ============================================
       CHAT CONTAINER
       ============================================ */
    [data-testid="stChatMessageContainer"] {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        width: 100%;
        padding: 0.5rem 0;
    }

    /* ============================================
       REMOVE DEFAULT STREAMLIT CHAT STYLING
       ============================================ */
    [data-testid="stChatMessage"] {
        display: flex !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
    }

    /* Hide default avatar icons */
    [data-testid="stChatMessage"] > div:first-child {
        display: none !important;
    }

    /* Remove default backgrounds from content wrappers */
    [data-testid="stChatMessage"] [data-testid="chat-message-content"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    /* ============================================
       USER MESSAGE BOX - RED BORDER - RIGHT SIDE
       ============================================ */
    [data-testid="stChatMessage"][data-testid="chat-message-user"] {
        justify-content: flex-end !important;
    }

    [data-testid="stChatMessage"][data-testid="chat-message-user"] > div:last-child {
        max-width: 72% !important;
        background: #1a1f2b !important;
        border: 2px solid #DC143C !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        box-shadow: 0 4px 12px rgba(220, 20, 60, 0.2) !important;
    }

    [data-testid="stChatMessage"][data-testid="chat-message-user"] p,
    [data-testid="stChatMessage"][data-testid="chat-message-user"] li,
    [data-testid="stChatMessage"][data-testid="chat-message-user"] span,
    [data-testid="stChatMessage"][data-testid="chat-message-user"] div {
        color: #FFFFFF !important;
        text-align: left;
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.55;
        background: transparent !important;
    }

    /* ============================================
       ASSISTANT MESSAGE BOX - BLUE BORDER - LEFT SIDE
       ============================================ */
    [data-testid="stChatMessage"][data-testid="chat-message-assistant"] {
        justify-content: flex-start !important;
    }

    [data-testid="stChatMessage"][data-testid="chat-message-assistant"] > div:last-child {
        max-width: 72% !important;
        background: #1a1f2b !important;
        border: 2px solid #2C5FA8 !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        margin-right: auto !important;
        margin-left: 0 !important;
        box-shadow: 0 4px 12px rgba(44, 95, 168, 0.2) !important;
    }

    [data-testid="stChatMessage"][data-testid="chat-message-assistant"] p,
    [data-testid="stChatMessage"][data-testid="chat-message-assistant"] li,
    [data-testid="stChatMessage"][data-testid="chat-message-assistant"] span,
    [data-testid="stChatMessage"][data-testid="chat-message-assistant"] div {
        color: rgba(255, 255, 255, 0.85) !important;
        text-align: left;
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.55;
        background: transparent !important;
    }

    /* Bold text */
    [data-testid="stChatMessage"] strong {
        color: #FFFFFF !important;
        font-weight: 600;
    }

    /* Links */
    [data-testid="stChatMessage"] a {
        color: #2C5FA8 !important;
    }

    /* Lists inside boxes */
    [data-testid="stChatMessage"] ul,
    [data-testid="stChatMessage"] ol {
        margin: 0.4rem 0;
        padding-left: 1.2rem;
    }

    /* ============================================
       CHAT INPUT BOX
       ============================================ */
    [data-testid="stChatInput"] {
        max-width: 850px;
        margin: 0 auto;
        padding: 0.8rem 0;
    }
    [data-testid="stChatInput"] textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #FFFFFF !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 14px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 12px 16px !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #2C5FA8 !important;
        box-shadow: 0 0 0 3px rgba(44, 95, 168, 0.2) !important;
    }
    [data-testid="stChatInput"] button {
        color: #FFFFFF !important;
        background: #DC143C !important;
        border-radius: 10px !important;
    }

    /* ============================================
       SPINNER
       ============================================ */
    .stSpinner > div {
        border-top-color: #2C5FA8 !important;
        border-left-color: #2C5FA8 !important;
    }

    /* ============================================
       SCROLLBAR
       ============================================ */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0E1116; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 3px; }

    /* ============================================
       RESPONSIVE
       ============================================ */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.6rem !important;
        }
        .app-header h1 {
            font-size: 1.5rem;
        }
        .app-header .sub {
            font-size: 0.8rem;
        }
        [data-testid="stChatMessage"][data-testid="chat-message-user"] > div:last-child,
        [data-testid="stChatMessage"][data-testid="chat-message-assistant"] > div:last-child {
            max-width: 85% !important;
            padding: 12px 14px !important;
        }
        [data-testid="stChatMessage"][data-testid="chat-message-user"] p,
        [data-testid="stChatMessage"][data-testid="chat-message-assistant"] p {
            font-size: 0.9rem;
        }
    }

    @media (max-width: 480px) {
        [data-testid="stChatMessage"][data-testid="chat-message-user"] > div:last-child,
        [data-testid="stChatMessage"][data-testid="chat-message-assistant"] > div:last-child {
            max-width: 90% !important;
            padding: 10px 12px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING FUNCTIONS
# ============================================

def _parse_blocks(path):
    """Shared block parser for text data files"""
    items = []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    for block in content.strip().split("\n\n"):
        info = {}
        for line in block.split("\n"):
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                info[key.strip().lower()] = value.strip()
        if info:
            items.append(info)
    return items

def load_attractions():
    return _parse_blocks("data/attractions.txt")

def load_flights():
    with open("data/flights.json", "r") as f:
        return json.load(f)

def load_trekking():
    return _parse_blocks("data/trekking.txt")

def load_festivals():
    return _parse_blocks("data/festivals.txt")

def load_food():
    return _parse_blocks("data/food.txt")

@st.cache_data
def load_all_data():
    """Cache data loads for performance"""
    return {
        "attractions": load_attractions(),
        "flights": load_flights(),
        "trekking": load_trekking(),
        "festivals": load_festivals(),
        "food": load_food(),
    }

try:
    _db = load_all_data()
    attractions_db = _db["attractions"]
    flights_db = _db["flights"]
    trekking_db = _db["trekking"]
    festivals_db = _db["festivals"]
    food_db = _db["food"]
except FileNotFoundError as e:
    st.error(f"⚠️ Missing data file: {e.filename}. Make sure the `data/` folder exists.")
    st.stop()

# ============================================
# WEATHER FUNCTIONS
# ============================================

def get_weather(city):
    """Get current weather for a city using OpenWeatherMap API"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "⚠️ Weather lookup needs an OPENWEATHER_API_KEY in your .env file."
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},NP&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=6)
    except requests.RequestException:
        return f"Couldn't reach the weather service for {city}. Check your connection."
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        feels = data["main"].get("feels_like", temp)
        desc = data["weather"][0]["description"]
        return f"**{city}**: {temp}°C (feels like {feels}°C), {desc}."
    return f"Couldn't fetch weather for {city}. Check the city name."

def compare_weather(city1, city2):
    """Compare weather between two cities"""
    w1 = get_weather(city1)
    w2 = get_weather(city2)
    return f"{w1}\n\n{w2}"

# ============================================
# SEARCH FUNCTIONS
# ============================================

def search_attractions(query):
    """Search attractions by name, location, or description"""
    query = query.lower().strip().replace("?", "").replace(".", "").replace("!", "")
    results = []
    for a in attractions_db:
        name = a.get("name", "").lower()
        location = a.get("location", "").lower()
        desc = a.get("description", "").lower()
        for word in query.split():
            if word in name or word in location or word in desc:
                results.append(a)
                break

    if not results:
        return "No attractions found. Try 'temples', 'Pokhara', or 'stupa'."

    if len(results) == 1:
        r = results[0]
        return (
            f"**{r.get('name', 'Unknown')}**\n\n"
            f"📍 Location: {r.get('location', 'Nepal')}\n\n"
            f"📝 {r.get('description', '')}\n\n"
            f"⏰ Best Time: {r.get('best time', 'N/A')}\n\n"
            f"💰 Entry Fee: {r.get('entry fee', 'N/A')}\n\n"
            f"💡 Tip: {r.get('tip', '')}"
        )

    reply = f"Found {len(results)} places:\n\n"
    for r in results[:5]:
        reply += f"**{r.get('name', 'Unknown')}**\n📍 {r.get('location', 'Nepal')}\n📝 {r.get('description', '')[:100]}...\n\n"
    return reply

def search_flights(from_city=None, to_city=None):
    """Search flights by origin and/or destination"""
    results = [f for f in flights_db 
               if (not from_city or from_city.lower() in f["from"].lower())
               and (not to_city or to_city.lower() in f["to"].lower())]

    if not results:
        return "No flights found for that route."

    reply = "✈️ **Flights found:**\n\n"
    for f in results:
        emoji = "✅" if f["status"] == "On Time" else "⚠️" if f["status"] == "Delayed" else "❌"
        reply += f"{emoji} **{f['flight_no']}** - {f['airline']}\n"
        reply += f"   {f['from']} → {f['to']}\n"
        reply += f"   Depart: {f['dep_time']} | Arrive: {f['arr_time']}\n"
        reply += f"   Status: {f['status']}\n\n"
    reply += "⚠️ *Mountain flights are weather dependent.*"
    return reply

def search_treks(query):
    """Search trekking routes by name or description"""
    query = query.lower().strip().replace("?", "").replace(".", "").replace("!", "")
    results = []
    for t in trekking_db:
        name = t.get("name", "").lower()
        desc = t.get("description", "").lower()
        for word in query.split():
            if word in name or word in desc:
                results.append(t)
                break

    if not results:
        results = trekking_db[:3]

    if len(results) == 1:
        t = results[0]
        return (
            f"**{t.get('name', 'Unknown')}**\n\n"
            f"⏱️ Duration: {t.get('duration', 'N/A')}\n"
            f"📊 Difficulty: {t.get('difficulty', 'N/A')}\n"
            f"🏔️ Max Altitude: {t.get('max altitude', 'N/A')}\n"
            f"📅 Best Season: {t.get('best season', 'N/A')}\n"
            f"📋 Permits: {t.get('permits', 'N/A')}\n"
            f"💰 Cost: {t.get('cost', 'N/A')}\n\n"
            f"📝 {t.get('description', '')}\n\n"
            f"💡 Tip: {t.get('tip', '')}"
        )

    reply = f"Found {len(results)} treks:\n\n"
    for t in results[:5]:
        reply += f"**{t.get('name', 'Unknown')}**\n⏱️ {t.get('duration', 'N/A')} | 📊 {t.get('difficulty', 'N/A')}\n📝 {t.get('description', '')[:100]}...\n\n"
    return reply

def search_festivals(query):
    """Search festivals by name, date, or description"""
    query = query.lower().strip().replace("?", "").replace(".", "").replace("!", "")
    results = []
    for f in festivals_db:
        name = f.get("name", "").lower()
        desc = f.get("description", "").lower()
        date = f.get("date", "").lower()
        for word in query.split():
            if word in name or word in desc or word in date:
                results.append(f)
                break

    if not results:
        results = festivals_db[:3]

    if len(results) == 1:
        f = results[0]
        return (
            f"**{f.get('name', 'Unknown')}**\n\n"
            f"📅 Date: {f.get('date', 'N/A')}\n"
            f"🏷️ Type: {f.get('type', 'N/A')}\n\n"
            f"📝 {f.get('description', '')}\n\n"
            f"💡 Tip: {f.get('tip', '')}"
        )

    reply = f"Found {len(results)} festivals:\n\n"
    for f in results[:5]:
        reply += f"**{f.get('name', 'Unknown')}**\n📅 {f.get('date', 'N/A')} | 🏷️ {f.get('type', 'N/A')}\n📝 {f.get('description', '')[:100]}...\n\n"
    return reply

def search_food(query):
    """Search Nepali foods by name, type, or description"""
    query = query.lower().strip().replace("?", "").replace(".", "").replace("!", "")
    results = []
    for f in food_db:
        name = f.get("name", "").lower()
        desc = f.get("description", "").lower()
        food_type = f.get("type", "").lower()
        for word in query.split():
            if word in name or word in desc or word in food_type:
                results.append(f)
                break

    if not results:
        results = food_db[:4]

    if len(results) == 1:
        f = results[0]
        return (
            f"**{f.get('name', 'Unknown')}**\n\n"
            f"🍽️ Type: {f.get('type', 'N/A')}\n"
            f"🥬 Vegetarian: {f.get('vegetarian', 'N/A')}\n\n"
            f"📝 {f.get('description', '')}\n\n"
            f"💡 Tip: {f.get('tip', '')}"
        )

    reply = f"Found {len(results)} foods:\n\n"
    for f in results[:5]:
        reply += f"**{f.get('name', 'Unknown')}**\n🍽️ {f.get('type', 'N/A')}\n📝 {f.get('description', '')[:100]}...\n\n"
    return reply

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_travel_tip():
    """Return a random Nepal travel tip"""
    tips = [
        "💡 Always carry cash. ATMs are limited outside Kathmandu and Pokhara.",
        "💡 Learn 'Namaste' - the traditional greeting with palms together.",
        "💡 Remove shoes before entering temples and homes.",
        "💡 Walk clockwise around Buddhist stupas and temples.",
        "💡 Don't drink tap water. Stick to bottled or filtered water.",
        "💡 Bargaining is common in local markets, but be respectful.",
        "💡 Dress modestly at religious sites - cover shoulders and knees.",
        "💡 Get a local SIM card (Ncell or NTC) for internet in remote areas.",
        "💡 Altitude sickness is real above 3000m. Ascend slowly and stay hydrated.",
        "💡 Tipping isn't mandatory but appreciated. 10% at restaurants is generous."
    ]
    return random.choice(tips)

def suggest_itinerary(days_query):
    """Generate a day-by-day Nepal itinerary"""
    try:
        days = int(''.join(filter(str.isdigit, days_query)))
    except ValueError:
        days = 5

    if days <= 3:
        return """**Quick 3-Day Nepal Trip:**\n
**Day 1:** Kathmandu - Swayambhunath and Boudhanath
**Day 2:** Pashupatinath and Patan Durbar Square
**Day 3:** Bhaktapur Durbar Square, fly out\n
💡 Tip: Stay in Thamel for easy access."""

    elif days <= 5:
        return """**5-Day Nepal Highlights:**\n
**Day 1:** Kathmandu - Swayambhunath, Boudhanath
**Day 2:** Pashupatinath, Patan Durbar Square
**Day 3:** Fly to Pokhara, Lakeside evening
**Day 4:** Sarangkot sunrise, Peace Pagoda
**Day 5:** Fly back, depart\n
💡 Tip: Book Pokhara flights in advance."""

    elif days <= 7:
        return """**1-Week Nepal Adventure:**\n
**Day 1:** Swayambhunath, Thamel
**Day 2:** Boudhanath, Pashupatinath, Patan
**Day 3:** Drive to Pokhara (6-7 hrs)
**Day 4:** Sarangkot sunrise, Lakeside
**Day 5:** Paragliding, boating
**Day 6:** Fly back, Bhaktapur Durbar Square
**Day 7:** Shopping, depart\n
💡 Tip: Add Chitwan if you skip some Kathmandu days."""

    else:
        return """**10+ Days Ultimate Nepal Trip:**\n
**Days 1-2:** Kathmandu valley temples
**Days 3-4:** Chitwan jungle safari
**Days 5-7:** Pokhara lakes & mountains
**Days 8-10:** Ghorepani Poon Hill trek
**Days 11-12:** Return, departure\n
💡 Tip: For EBC/Annapurna, add 12-16 days."""

# ============================================
# SESSION STATE
# ============================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! 🙏 I'm your Nepal travel guide.\n\n**I can help with:**\n🌤️ Weather\n📍 Attractions\n✈️ Flights\n🏔️ Trekking\n🎉 Festivals\n🍛 Food\n💡 Travel Tips\n📅 Itineraries\n\nWhat would you like to know?"}
    ]

def add_exchange(user_text, assistant_text):
    """Add a user-assistant exchange to chat history"""
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})

# ============================================
# UI HEADER
# ============================================

st.markdown(
    """
    <div class="app-header">
        <div class="eyebrow">Kathmandu · Pokhara · Everest · Annapurna</div>
        <h1>🏔️ Nepal Travel Assistant</h1>
        <div class="sub">Weather, attractions, flights, treks, festivals, and food — all in one trail.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.header("Quick Actions")

    if st.button("🌤️  Kathmandu weather"):
        add_exchange("Weather in Kathmandu?", get_weather("Kathmandu"))
        st.rerun()

    if st.button("🌤️  Pokhara weather"):
        add_exchange("Weather in Pokhara?", get_weather("Pokhara"))
        st.rerun()

    if st.button("📍  Top attractions"):
        add_exchange("Show me popular attractions", search_attractions(""))
        st.rerun()

    if st.button("✈️  Flights to Pokhara"):
        add_exchange("Flights to Pokhara?", search_flights(to_city="Pokhara"))
        st.rerun()

    if st.button("🏔️  Popular treks"):
        add_exchange("Show me popular treks", search_treks(""))
        st.rerun()

    if st.button("🎉  Festivals"):
        add_exchange("Tell me about Nepali festivals", search_festivals(""))
        st.rerun()

    if st.button("🍛  Nepali food"):
        add_exchange("What are popular Nepali foods?", search_food(""))
        st.rerun()

    if st.button("💡  Travel tip"):
        add_exchange("Give me a travel tip", get_travel_tip())
        st.rerun()

    st.divider()
    st.caption("Try: 'plan 5 days trip' · 'compare weather' · 'everest base camp trek' · 'momo' · 'dashain festival'")

# ============================================
# CHAT HISTORY DISPLAY
# ============================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# CHAT INPUT & ROUTING LOGIC
# ============================================

if prompt := st.chat_input("Ask me anything about traveling in Nepal..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Reading the trail map..."):
            prompt_lower = prompt.lower()

            # --- GREETINGS ---
            if prompt_lower in ["hi", "hello", "hey", "namaste"]:
                replies = [
                    "Namaste! 🙏 How can I help you explore Nepal?",
                    "Namaste! Ready for an adventure in Nepal?",
                    "Hello! Ask me about weather, places, treks, food, or flights!"
                ]
                reply = random.choice(replies)

            # --- THANK YOU ---
            elif prompt_lower in ["thanks", "thank you", "dhanyabad"]:
                reply = "Dhanyabad! 🙏 Happy to help. Enjoy your Nepal trip! 🏔️"

            # --- ITINERARY ---
            elif any(word in prompt_lower for word in ["itinerary", "plan", "trip", "days"]):
                reply = suggest_itinerary(prompt_lower)

            # --- WEATHER COMPARISON ---
            elif "compare" in prompt_lower and "weather" in prompt_lower:
                reply = compare_weather("Kathmandu", "Pokhara")

            # --- WEATHER ---
            elif "weather" in prompt_lower:
                if "pokhara" in prompt_lower:
                    reply = get_weather("Pokhara")
                elif "kathmandu" in prompt_lower:
                    reply = get_weather("Kathmandu")
                elif "lukla" in prompt_lower:
                    reply = get_weather("Lukla")
                else:
                    reply = get_weather("Kathmandu")

            # --- FLIGHTS ---
            elif any(word in prompt_lower for word in ["flight", "fly", "plane", "airline"]):
                if "pokhara" in prompt_lower:
                    reply = search_flights(to_city="Pokhara")
                elif "lukla" in prompt_lower:
                    reply = search_flights(to_city="Lukla")
                elif "bharatpur" in prompt_lower or "chitwan" in prompt_lower:
                    reply = search_flights(to_city="Bharatpur")
                elif "kathmandu" in prompt_lower:
                    reply = search_flights(to_city="Kathmandu")
                else:
                    reply = search_flights()

            # --- TREKKING ---
            elif any(word in prompt_lower for word in ["trek", "trekking", "everest", "annapurna", "base camp", "poon hill", "langtang", "manaslu"]):
                clean = prompt_lower.replace("tell me about", "").replace("what is", "").replace("how long", "").strip()
                reply = search_treks(clean)

            # --- FESTIVALS ---
            elif any(word in prompt_lower for word in ["festival", "dashain", "tihar", "holi", "jatra", "teej"]):
                reply = search_festivals(prompt_lower)

            # --- FOOD ---
            elif any(word in prompt_lower for word in ["food", "eat", "dish", "momo", "dal bhat", "thukpa", "sel roti", "yomari", "chatamari", "juju dhau", "newari"]):
                reply = search_food(prompt_lower)

            # --- TRAVEL TIPS ---
            elif any(word in prompt_lower for word in ["tip", "advice", "recommend"]):
                reply = get_travel_tip()

            # --- ATTRACTIONS ---
            elif any(word in prompt_lower for word in ["attraction", "temple", "stupa", "visit", "place", "park", "monkey", "buddha", "durbar", "square", "chitwan", "pokhara", "boudha", "pashupati", "swayambhu", "lumbini"]):
                clean = prompt_lower.replace("tell me about", "").replace("what is", "").replace("what's", "").replace("show me", "").strip()
                reply = search_attractions(clean)

            # --- LLAMA FALLBACK ---
            else:
                try:
                    response = requests.post(
                        'http://localhost:11434/api/chat',
                        json={
                            "model": "llama3.1:8b",
                            "messages": [
                                {"role": "system", "content": "You are a Nepal travel assistant. Answer in 1-3 short sentences. Be direct and brief."},
                                {"role": "user", "content": prompt}
                            ],
                            "stream": False,
                            "options": {"num_predict": 100}
                        },
                        timeout=20,
                    )
                    reply = response.json()['message']['content']
                except requests.RequestException:
                    reply = "Sorry, I'm having trouble. Try asking about weather, flights, treks, food, or attractions!"

            # Display and save response
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})