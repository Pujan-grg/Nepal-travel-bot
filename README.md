# 🇳🇵 Nepal Travel AI Assistant

A comprehensive AI-powered chatbot that helps tourists plan their Nepal trip with real-time weather, tourist attractions, flight information, trekking routes, festivals, food guides, travel tips, and smart itinerary planning.

## Features

- 🌤️ **Real-time Weather** - Current weather for Kathmandu, Pokhara, and Lukla via OpenWeatherMap API with weather comparison
- 📍 **Tourist Attractions** - Detailed information about 10 popular destinations including temples, stupas, national parks, and historical squares
- ✈️ **Domestic Flights** - Mock flight search for Kathmandu, Pokhara, Lukla, and Bharatpur routes with real-time status
- 🏔️ **Trekking Routes** - 5 popular treks with duration, difficulty, altitude, permits, cost, and tips
- 🎉 **Festivals** - 6 major Nepali festivals with dates, descriptions, and tourist tips
- 🍛 **Food Guide** - 8 traditional Nepali dishes with vegetarian options and where to find them
- 💡 **Travel Tips** - Random Nepal travel advice and cultural etiquette
- 📅 **Smart Itineraries** - Auto-generated day-by-day plans for 3, 5, 7, and 10+ day trips
- 🙏 **Nepali Greetings** - Responds to Namaste, Dhanyabad, and common greetings
- 💬 **AI Chat** - Powered by Llama 3.1 (8B) for general Nepal travel questions
- 🎨 **Dark Mode UI** - Boxed chat messages with Nepal flag-inspired colors

## Demo

Try these commands:

- `weather in Pokhara`
- `compare weather Kathmandu and Pokhara`
- `tell me about monkey temple`
- `flights to Lukla`
- `everest base camp trek`
- `tell me about dashain festival`
- `what is momo`
- `give me a travel tip`
- `plan a 7 day trip`
- `best time to visit Nepal`

## Tech Stack

- **Frontend:** Streamlit
- **AI Model:** Llama 3.1 (8B) via Ollama
- **Weather API:** OpenWeatherMap
- **Language:** Python
- **Styling:** Custom CSS with Nepal flag colors (Crimson #DC143C & Blue #003893)

## Setup

### Prerequisites

- Python 3.8+
- Ollama installed with Llama 3.1

### Installation

1. Clone the repository
bash
git clone https://github.com/your-username/Nepal-travel-bot.git
cd Nepal-travel-bot

2. Create virtual environment
bash
python -m venv .venv

3. Activate virtual environment
Windows:
bash
.venv\Scripts\activate
Mac/Linux:
bash
source .venv/bin/activate

4. Install dependencies
bash
pip install -r requirements.txt

5. Set up environment variables
Create a .env file in the project folder:
OPENWEATHER_API_KEY=your_api_key_here

6. Pull Llama model
bash
ollama pull llama3.1:8b

7. Start Ollama (in a separate terminal)
bash
ollama serve

8. Run the app
bash
streamlit run app.py
The app will open at http://localhost:8501

Project Structure
text
Nepal-travel-bot/
├── .streamlit/
│   └── config.toml        # Dark theme configuration
├── app.py                 # Main application with all logic
├── data/
│   ├── attractions.txt    # 10 tourist attractions
│   ├── flights.json       # Mock domestic flight data
│   ├── trekking.txt       # 5 trekking routes
│   ├── festivals.txt      # 6 Nepali festivals
│   └── food.txt           # 8 traditional dishes
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not committed)
├── .gitignore
└── README.md              # Documentation

Attractions Covered:
Swayambhunath Stupa (Monkey Temple)
Boudhanath Stupa
Pashupatinath Temple
Pokhara Lakeside
Chitwan National Park
Lumbini
Bhaktapur Durbar Square
Sarangkot
Sagarmatha National Park
Patan Durbar Square

Trekking Routes:
Everest Base Camp
Annapurna Circuit
Ghorepani Poon Hill
Langtang Valley
Manaslu Circuit

Festivals Covered:
Dashain (September-October)
Tihar / Deepawali (October-November)
Holi (March)
Indra Jatra (September)
Buddha Jayanti (April-May)
Teej (August-September)

Food Guide:
Dal Bhat - National dish
Momo - Dumplings
Thukpa - Noodle soup
Sel Roti - Sweet rice bread
Newari Khaja Set - Traditional platter
Chatamari - Rice crepe
Juju Dhau - King yogurt
Yomari - Sweet dumpling

Flight Routes:
Kathmandu ↔ Pokhara
Kathmandu ↔ Lukla
Kathmandu → Bharatpur

Future Enhancements:
Real flight API integration
Live festival date calculator
Multi-language support (Nepali, Chinese, Japanese)
Accommodation recommendations
Budget calculator
Photo gallery integration
Voice input support

License:
This project is built for educational purposes.
