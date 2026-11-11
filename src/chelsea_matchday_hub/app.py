
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_caching import Cache

load_dotenv()

app = Flask(__name__)

app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 900
cache = Cache(app)

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"

CHELSEA_ID = 61
TIMEZONE = ZoneInfo("Europe/London")


def fetch_data(endpoint):
    """Make an authenticated request to football-data.org."""
    if not API_KEY:
        raise ValueError("FOOTBALL_API_KEY is not configured")

    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        headers={"X-Auth-Token": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def format_match(match):
    """Transform an API match into data for our template."""
    match_date = datetime.fromisoformat(
        match["utcDate"].replace("Z", "+00:00")
    ).astimezone(TIMEZONE)

    score = match.get("score") or {}
    full_time = score.get("fullTime") or {}

    return {
        "home_team": match["homeTeam"]["shortName"],
        "away_team": match["awayTeam"]["shortName"],
        "home_crest": match["homeTeam"].get("crest"),
        "away_crest": match["awayTeam"].get("crest"),
        "date": match_date.strftime("%d %b %Y"),
        "time": match_date.strftime("%H:%M"),
        "home_score": full_time.get("home"),
        "away_score": full_time.get("away"),
        "status": match["status"],
	"home_team_id": match["homeTeam"]["id"],
	"away_team_id": match["awayTeam"]["id"],
    }


@cache.cached(timeout=900, key_prefix="chelsea_data")
def get_chelsea_data():
    """Fetch Chelsea fixtures, results and league standings."""

    matches_data = fetch_data("competitions/PL/matches")
    standings_data = fetch_data("competitions/PL/standings")

    all_matches = matches_data.get("matches", [])

    chelsea_matches = [
        match
        for match in all_matches
        if (
            match["homeTeam"]["id"] == CHELSEA_ID
            or match["awayTeam"]["id"] == CHELSEA_ID
        )
    ]

    finished = sorted(
        [
            m for m in chelsea_matches
            if m["status"] == "FINISHED"
        ],
        key=lambda m: m["utcDate"],
        reverse=True,
    )

    upcoming = sorted(
        [
            m for m in chelsea_matches
            if m["status"] in ("SCHEDULED", "TIMED")
        ],
        key=lambda m: m["utcDate"],
    )

    standings = next(
        (
            item["table"]
            for item in standings_data.get("standings", [])
            if item["type"] == "TOTAL"
        ),
        [],
    )

    chelsea = next(
        (
            row["team"]
            for row in standings
            if row["team"]["id"] == CHELSEA_ID
        ),
        {},
    )

    return {
        "team": chelsea,
        "upcoming": [format_match(m) for m in upcoming[:5]],
        "results": [format_match(m) for m in finished[:5]],
        "standings": standings,
    }


@app.route("/")
def index():
    error = None
    data = {
        "team": {},
        "upcoming": [],
        "results": [],
        "standings": [],
    }

    try:
        data = get_chelsea_data()
    except (requests.RequestException, ValueError) as exc:
        app.logger.error("Football API error: %s", exc)
        error = "Unable to load football data right now."

    return render_template(
        "index.html",
        **data,
        error=error,
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )

