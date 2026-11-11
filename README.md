# Chelsea FC Matchday Hub ⚽

A Flask-based web application displaying Chelsea FC's upcoming Premier League fixtures, recent match results, and league standings using the [football-data.org](https://www.football-data.org/) API.

Built as a hands-on project to learn Flask, REST API integration, Jinja2 templating, API caching, and web application deployment.

### 🌐 Live Demo

**[View the deployed Chelsea FC Matchday Hub](https://chelsea-matchday-hub.onrender.com/)**

*Hosted on Render's free tier. The first request after inactivity may take longer while the service starts.*

## 📸 Screenshot

![Chelsea FC Matchday Hub](screenshots/dashboard.PNG)

## ✨ Features

- **Upcoming Fixtures:** Displays Chelsea's next five Premier League fixtures, including opponents, dates, and kickoff times.
- **Recent Results:** Shows the five most recent matches with color-coded results:
  - 🟢 Green — Win
  - 🔴 Red — Loss
  - ⚪ Grey — Draw
- **Premier League Standings:** Displays the league table, highlighting Chelsea's position.
- **Club Crests:** Displays team badges alongside fixtures and results.
- **Responsive Dashboard:** Three-column layout on desktop, adapting to smaller screens.
- **API Caching:** Caches football data for 15 minutes to reduce unnecessary requests.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend |
| Flask | Web framework |
| Jinja2 | HTML templating |
| HTML & CSS | Frontend |
| football-data.org | Football data provider |
| Requests | API integration |
| Flask-Caching | API response caching |
| uv | Dependency and environment management |
| Gunicorn | Production WSGI server |
| Render | Cloud deployment |
| GitHub | Version control and source hosting |

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- A free [football-data.org API key](https://www.football-data.org/client/register)

### 1. Clone the repository

```bash
git clone https://github.com/keerthan-m-shetty/chelsea-matchday-hub.git
cd chelsea-matchday-hub
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```dotenv
FOOTBALL_API_KEY=your_api_key_here
```

Replace the placeholder with your API key.

Never commit your `.env` file to GitHub.

### 4. Run locally

```bash
uv run python src/chelsea_matchday_hub/app.py
```

Visit http://127.0.0.1:5000 in your browser.

## ☁️ Deployment

The application is deployed on **Render** using Gunicorn.

**Build Command**

```bash
uv sync --locked --no-dev
```

**Start Command**

```bash
uv run --no-sync gunicorn chelsea_matchday_hub.app:app --bind 0.0.0.0:$PORT
```

Required Render environment variable: `FOOTBALL_API_KEY`.

The service uses Render's free instance, which can spin down during inactivity.

**Production URL:** https://chelsea-matchday-hub.onrender.com/

## 📁 Project Structure

```text
chelsea-matchday-hub/
├── screenshots/
│   └── dashboard.png
├── src/
│   └── chelsea_matchday_hub/
│       ├── __init__.py
│       ├── app.py
│       └── templates/
│           └── index.html
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

## 📊 Data Source

Football data is provided by [football-data.org](https://www.football-data.org/).

The application uses the Premier League matches and standings endpoints. Data availability and freshness depend on the API provider. This application does not provide real-time live scores.

## 🔮 Future Improvements

- Match detail pages
- Additional competitions, including the Champions League
- Home and away league tables
- Improved error handling and fallback caching
- Automated testing

## 📄 Disclaimer

This is an independent educational project and is not affiliated with or endorsed by Chelsea Football Club or the Premier League.
