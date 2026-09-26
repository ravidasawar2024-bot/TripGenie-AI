# TripGenie AI

TripGenie AI is an AI-powered travel planner built for the FFE TiE Entrepreneurship Program 2026.

## What it does

Users enter:
- Destination
- Number of days
- Number of travelers
- Budget
- Travel style
- Interests
- Trip pace
- Dietary preference

The AI generates:
- Personalized day-by-day itinerary
- Estimated budget allocation
- Must-try experiences
- Packing checklist
- Smart travel tips
- Alternative activities

## Technology

- Python
- Streamlit
- Google Gemini API
- Google GenAI Python SDK

## Run locally

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set `GEMINI_API_KEY` as an environment variable, or create `.streamlit/secrets.toml` from `secrets.toml.example`.

4. Run:

```bash
streamlit run app.py
```

## Security

Never commit a real API key to GitHub. Streamlit Community Cloud supports secrets for deployed applications.

## Disclaimer

The application generates planning estimates and suggestions. Users should verify current weather, opening hours, transport schedules, prices, availability, and local rules before making bookings.
