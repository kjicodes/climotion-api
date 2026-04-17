# Climotion

A weather-aware workout planner. Enter your city to get current weather conditions and a recommendation on whether to work out indoors or outdoors. Select your workout type, target muscle groups, and preferred difficulty level to receive personalized exercise recommendations tailored to both your preferences and the weather.

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS
- **Database:** SQLite (development)
- **APIs:** OpenWeatherMap API, API Ninjas Exercises API

## Features

- City-based weather lookup with current conditions, temperature, and daily high/low
- Indoor or outdoor workout recommendation based on live weather and temperature
- Workout type — cardio, strength training, or stretching — and difficulty level selection
- Target muscle group selection for strength training
- Personalized exercise recommendations based on user preferences

## Running Locally

1. Clone the repo and create a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root
   ```
   SECRET_KEY=your_django_secret_key
   OPENWEATHER_API_KEY=your_openweathermap_key
   OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5/weather
   GEOCODING_BASE_URL=http://api.openweathermap.org/geo/1.0/direct
   ```

4. Run the development server
   ```bash
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000/api/home/`

## Roadmap

- [x] City-based weather lookup and indoor/outdoor workout recommendation
- [x] Exercise recommendations by workout type and difficulty level
- [x] Muscle group selector for strength training
- [ ] UI improvements and bug fixes
