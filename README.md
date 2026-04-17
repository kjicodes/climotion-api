## Climotion

A weather-aware workout planner. Enter your city to get current weather conditions and a recommendation on whether to work out indoors or outdoors. Select your workout type, target muscle groups, and preferred difficulty level to receive personalised exercise recommendations tailored to both your preferences and the weather.

## Tech Stack

- Python
- Django
- SQLite
- OpenWeatherMap API
- API Ninjas Exercises API

## Features

- City-based weather lookup using OpenWeatherMap geocoding
- Displays temperature, feels like, and daily high/low
- Suggests indoor or outdoor workout based on conditions and temperature
- Workout type selection (e.g. strength, cardio, flexibility)
- Muscle group targeting and difficulty level selection
- Exercise recommendations based on user preferences via API Ninjas

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
- [ ] Migrate backend to Django REST Framework
- [ ] Build React frontend
