# Climotion

A weather-aware workout planner. Enter a city to get current weather conditions and a recommendation on whether to work out indoors or outdoors. Select your workout type, target muscle groups, and preferred difficulty level to receive personalized exercise recommendations tailored to both your preferences and the weather.

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS
- **Database:** SQLite (development)
- **APIs:** OpenWeatherMap API, API Ninjas Exercises API
- **Testing:** Postman

## Features

- City-based weather lookup with current conditions, temperature, and daily high/low
- Indoor or outdoor workout recommendation based on live weather and temperature
- Personalized exercise recommendations based on workout type, difficulty, and target muscle groups                                                                  
- Save, view, update, and delete workouts with before and after reflection notes
- Previously searched cities saved for quick access

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

5. Visit api endpoints
   - `GET http://127.0.0.1:8000/weather/?city=London`
   - `GET http://127.0.0.1:8000/workouts/?exercise-type=cardio&difficulty=beginner`
   - `GET/POST http://127.0.0.1:8000/saved-workouts/`                                                                                                                         
   - `GET/PATCH/DELETE http://127.0.0.1:8000/saved-workouts/<id>/`
   - `GET http://127.0.0.1:8000/searched-cities/` 

## Roadmap

- [x] City-based weather lookup and indoor/outdoor workout recommendation
- [x] Exercise recommendations by workout type and difficulty level
- [x] Muscle group selector for strength training
- [x] Migrate backend to Django REST Framework
- [x] Searched Cities - save frequently searched cities
- [x] Saved Workouts - save and revisit previously generated workouts
- [ ] User authentication
- [ ] Build React frontend
