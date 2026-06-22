import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Nepal Travel Assistant",
    page_icon="🏔️"
)

# Load attractions data
def load_attractions():
    attractions = []
    with open("data/attractions.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    blocks = content.strip().split("\n\n")
    
    for block in blocks:
        info = {}
        for line in block.split("\n"):
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                info[key.strip().lower()] = value.strip()
        if info:
            attractions.append(info)
    return attractions

attractions_db = load_attractions()

# Weather function
def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},NP&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Current weather in {city}: {temp}°C, {desc}."
    return f"Couldn't fetch weather for {city}."

# Search attractions
def search_attractions(query):
    # Clean the query
    query = query.lower().strip().replace("?", "").replace(".", "").replace("!", "")
    
    results = []
    for a in attractions_db:
        name = a.get("name", "").lower()
        location = a.get("location", "").lower()
        desc = a.get("description", "").lower()
        
        # Check each word in query
        query_words = query.split()
        for word in query_words:
            if word in name or word in location or word in desc:
                results.append(a)
                break
    
    if not results:
        return "No attractions found. Try searching for 'temples', 'Pokhara', or 'stupa'."
    
    # If only one result, return detailed info
    if len(results) == 1:
        r = results[0]
        reply = f"**{r.get('name', 'Unknown')}**\n\n"
        reply += f"📍 Location: {r.get('location', 'Nepal')}\n\n"
        reply += f"📝 {r.get('description', '')}\n\n"
        reply += f"⏰ Best Time: {r.get('best time', 'N/A')}\n\n"
        reply += f"💰 Entry Fee: {r.get('entry fee', 'N/A')}\n\n"
        reply += f"💡 Tip: {r.get('tip', '')}"
        return reply
    
    # Multiple results
    reply = f"Found {len(results)} places:\n\n"
    for r in results[:5]:
        reply += f"**{r.get('name', 'Unknown')}**\n"
        reply += f"📍 {r.get('location', 'Nepal')}\n"
        reply += f"📝 {r.get('description', '')[:100]}...\n\n"
    return reply

st.title("🇳🇵 Nepal Travel AI Assistant")
st.caption("Ask me about weather, attractions, and more!")

# Sidebar
with st.sidebar:
    st.header("Quick Actions")
    if st.button("🌤️ Kathmandu Weather"):
        weather = get_weather("Kathmandu")
        st.session_state.messages.append({"role": "user", "content": "Weather in Kathmandu?"})
        st.session_state.messages.append({"role": "assistant", "content": weather})
        st.rerun()
    
    if st.button("🌤️ Pokhara Weather"):
        weather = get_weather("Pokhara")
        st.session_state.messages.append({"role": "user", "content": "Weather in Pokhara?"})
        st.session_state.messages.append({"role": "assistant", "content": weather})
        st.rerun()
    
    if st.button("📍 Top Attractions"):
        reply = search_attractions("")
        st.session_state.messages.append({"role": "user", "content": "Show me popular attractions"})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
    
    st.divider()
    st.caption("Try: 'weather in Pokhara' or 'tell me about temples'")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! 🙏 I'm your Nepal travel guide.\n\nI can help with:\n🌤️ Real-time weather\n📍 Tourist attractions\n💬 General Nepal questions\n\nWhat would you like to know?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about traveling in Nepal..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            prompt_lower = prompt.lower()
            
            # Check for weather requests
            if "weather" in prompt_lower:
                if "pokhara" in prompt_lower:
                    reply = get_weather("Pokhara")
                elif "kathmandu" in prompt_lower:
                    reply = get_weather("Kathmandu")
                elif "lukla" in prompt_lower:
                    reply = get_weather("Lukla")
                else:
                    reply = get_weather("Kathmandu")
            
            # Check for attraction requests
            elif any(word in prompt_lower for word in ["attraction", "temple", "stupa", "visit", "place", "park", "monkey", "buddha", "durbar", "square", "chitwan", "pokhara", "boudha", "pashupati", "swayambhu", "lumbini"]):
                clean_prompt = prompt_lower.replace("tell me about", "").replace("what is", "").replace("what's", "").replace("show me", "").strip()
                reply = search_attractions(clean_prompt)
            
            # Everything else goes to Llama
            else:
                try:
                    response = requests.post(
                        'http://localhost:11434/api/chat',
                        json={
                            "model": "llama3.1:8b",
                            "messages": [
                                {"role": "system", "content": "You are a helpful Nepal travel assistant. You know about Nepali culture, food, trekking, festivals, transportation, and travel tips. Keep answers concise (2-4 sentences) and friendly."},
                                {"role": "user", "content": prompt}
                            ],
                            "stream": False
                        }
                    )
                    reply = response.json()['message']['content']
                except:
                    reply = "Sorry, I'm having trouble connecting to my knowledge base. Try asking about weather or attractions!"
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})