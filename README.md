# Climotion

A weather-aware workout planner for registered users. Enter a city to get current weather conditions and a recommendation on whether to work out indoors or outdoors. Create an account to get personalized exercise recommendations and save workouts with reflection notes.

## Tech Stack

- **Backend:** Python, Django, Django REST Framework, JWT (Simple JWT)
- **Frontend:** HTML, CSS
- **Database:** SQLite (development)
- **APIs:** OpenWeatherMap API, API Ninjas Exercises API
- **Testing:** Postman

## Features

- City-based weather lookup with current conditions, temperature, and daily high/low
- Indoor or outdoor workout recommendation based on live weather and temperature
- User registration and login with JWT authentication
- Personalized exercise recommendations based on workout type, difficulty, and target muscle groups (authenticated users only)                                                                  
- Save, view, update, and delete workouts with before and after reflection notes (authenticated users only)
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

   **Public**
   - `GET /weather/?city=London`
   - `GET /searched-cities/`
   - `POST /users/` - register
   - `POST /api/token/` - login
   - `POST /api/token/refresh/` - refresh access token
   
   **Authenticated**
   - `GET /workouts/?exercise-type=cardio&difficulty=beginner`
   - `GET/POST /saved-workouts/`
   - `GET/PATCH/DELETE /saved-workouts/<id>/`

## Roadmap

- [x] City-based weather lookup and indoor/outdoor workout recommendation
- [x] Exercise recommendations by workout type and difficulty level
- [x] Muscle group selector for strength training
- [x] Migrate backend to Django REST Framework
- [x] Searched Cities - save frequently searched cities
- [x] Saved Workouts - save and revisit previously generated workouts
- [x] User authentication
- [ ] Build React frontend
