import os
import json
import urllib.request
import urllib.parse

import streamlit as st
from google import genai

def search_wikimedia_images(query, limit=3):
    params = urllib.parse.urlencode({
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
    })

    url = f"https://commons.wikimedia.org/w/api.php?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "TripGenieAI/1.0"
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode())

        images = []

        for page in data.get("query", {}).get("pages", {}).values():
            image_info = page.get("imageinfo", [])

            if image_info:
                images.append({
                    "title": page.get("title", ""),
                    "url": image_info[0].get("url", ""),
                })

        return images

    except Exception:
        return []

st.set_page_config(
    page_title="TripGenie AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f7fbff 0%, #ffffff 45%, #f7f9fc 100%);
    }

    /* Make generated markdown clearly readable */
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown strong, .stMarkdown em {
        color: #0f172a !important;
    }

    .hero {
        padding: 2.3rem 2.5rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #0f172a, #1d4ed8);
        color: white;
        margin-bottom: 1.4rem;
        box-shadow: 0 12px 35px rgba(15, 23, 42, 0.16);
    }

    .hero h1 {
        color: white !important;
        font-size: 3rem;
        margin: 0;
        letter-spacing: -1px;
    }

    .hero p {
        color: #e2e8f0 !important;
        font-size: 1.08rem;
        line-height: 1.6;
        margin-top: 0.6rem;
        max-width: 850px;
    }

    .intro-card {
        padding: 1.2rem 1.35rem;
        border: 1px solid #dbeafe;
        border-radius: 18px;
        background: white;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
        margin-bottom: 1.2rem;
    }

    .intro-card h3 {
        color: #0f172a;
        margin: 0 0 0.35rem 0;
    }

    .intro-card p {
        color: #475569;
        margin: 0;
    }

    .profile-card {
        padding: 1.2rem 1.3rem;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        background: #ffffff;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
    }

    .profile-card h3 {
        color: #0f172a;
        margin-top: 0;
    }

    .profile-card div {
        color: #334155;
        line-height: 1.9;
    }

    .ai-output {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 1.7rem 1.9rem;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    }

    .ai-output h1 {
        color: #0f172a !important;
        font-size: 2rem;
        margin-top: 0;
    }

    .ai-output h2 {
        color: #1d4ed8 !important;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 0.45rem;
        margin-top: 1.6rem;
    }

    .ai-output h3 {
        color: #0f172a !important;
    }

    .ai-output p, .ai-output li {
        color: #334155 !important;
        line-height: 1.65;
    }

    .ai-output strong {
        color: #0f172a !important;
    }

    .ai-output table {
        width: 100%;
        border-collapse: collapse;
        margin: 0.8rem 0 1.2rem 0;
    }

    .ai-output th {
        background: #eff6ff;
        color: #0f172a;
        text-align: left;
        padding: 0.65rem;
        border: 1px solid #dbeafe;
    }

    .ai-output td {
        color: #334155;
        padding: 0.65rem;
        border: 1px solid #e2e8f0;
    }

    .disclaimer {
        color: #64748b;
        font-size: 0.84rem;
        padding: 0.8rem 0;
    }

    div.stButton > button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>✈️ TripGenie AI</h1>
    <p>
        Your personal AI travel planner. Enter your destination, budget,
        interests and travel style to receive a practical, personalized
        itinerary in seconds.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🌍 Trip Details")

    destination = st.text_input(
        "Destination",
        placeholder="e.g. Goa, Manali, Jaipur",
    )

    col1, col2 = st.columns(2)
    with col1:
        days = st.number_input("Days", min_value=1, max_value=30, value=4, step=1)
    with col2:
        travelers = st.number_input("Travelers", min_value=1, max_value=20, value=2, step=1)

    budget = st.number_input(
        "Total budget (₹)",
        min_value=1000,
        max_value=10000000,
        value=20000,
        step=1000,
    )

    travel_style = st.selectbox(
        "Travel style",
        ["Budget", "Balanced", "Comfort", "Luxury"],
        index=1,
    )

    interests = st.multiselect(
        "Interests",
        [
            "Beaches",
            "Nature",
            "Adventure",
            "Food",
            "History & Culture",
            "Shopping",
            "Nightlife",
            "Photography",
            "Spiritual / Wellness",
            "Family activities",
        ],
        default=["Food", "Nature"],
    )

    pace = st.select_slider(
        "Trip pace",
        options=["Relaxed", "Balanced", "Packed"],
        value="Balanced",
    )

    dietary = st.text_input(
        "Dietary preferences (optional)",
        placeholder="e.g. vegetarian",
    )

    generate = st.button(
        "✨ Generate My Trip",
        type="primary",
        use_container_width=True,
    )

# ---------- Intro ----------
st.markdown("""
<div class="intro-card">
    <h3>🧭 Build a trip around you</h3>
    <p>
        TripGenie uses your preferences to organize activities logically,
        estimate a budget, and create a practical travel plan.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- Generate ----------
if generate:
    if not destination.strip():
        st.warning("Please enter a destination first.")
        st.stop()

    api_key = None

    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("Gemini API key not found.")
        st.info(
            "Add GEMINI_API_KEY to Streamlit secrets. Never put the key directly in GitHub."
        )
        st.stop()

    interests_text = ", ".join(interests) if interests else "General sightseeing"
    dietary_text = dietary.strip() if dietary.strip() else "No specific preference"

    prompt = f"""
You are TripGenie AI, a professional travel-planning assistant.

Create a polished, practical itinerary using these preferences:

Destination: {destination}
Days: {days}
Travelers: {travelers}
Total budget: ₹{budget:,}
Travel style: {travel_style}
Interests: {interests_text}
Trip pace: {pace}
Dietary preference: {dietary_text}

Write the response in Markdown using EXACTLY these sections:

# ✈️ {destination} — {days}-Day Personalized Trip

Start with a 2-3 sentence overview explaining why the itinerary fits the user's preferences.

## 📅 Day-by-Day Itinerary

For EACH day use this format:

### Day X — [short theme]
| Time | Plan |
|---|---|
| 🌅 Morning | activity + short practical note |
| 🍴 Afternoon | activity + food/local experience |
| 🌆 Evening | activity |
| 🌙 Night | activity / relaxed option |

Then add:
**Estimated day spend:** ₹X–₹Y

Do not overload a day. Group nearby activities together when possible.

## 💰 Budget Plan

Use a Markdown table:

| Category | Estimated Cost |
|---|---:|
| Accommodation | ₹X |
| Food | ₹X |
| Local transport | ₹X |
| Activities & entry fees | ₹X |
| Miscellaneous | ₹X |
| **Estimated Total** | **₹X** |

The estimated total should be reasonably consistent with the user's ₹{budget:,} budget.

## ⭐ Top 5 Experiences

Give five concise, destination-relevant experiences.

## 🎒 Packing Checklist

Give a practical checklist with 8-12 items.

## 💡 Smart Travel Tips

Give six concise tips covering transport, timing, local etiquette, safety and budgeting where relevant.

## 🔄 Alternative Activities

Give three replacement activities.

IMPORTANT:
- Make the itinerary useful rather than generic.
- Prefer realistic sequencing over listing famous places randomly.
- Clearly label prices as estimates.
- Do NOT claim live prices, opening hours, weather, transport schedules or availability.
- Do NOT invent booking confirmations.
- If a recommendation is seasonal, explicitly say it should be checked for the travel dates.
- Do not mention that you are an AI unless necessary.
"""

    try:
        with st.spinner("✨ TripGenie is creating your personalized itinerary..."):
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )

        answer = response.text

        images = search_wikimedia_images(destination, limit=3)

        if images:
            st.markdown("### 📸 Destination Highlights")

        image_cols = st.columns(len(images))

        for col, image in zip(image_cols, images):
            with col:
                st.image(
                    image["url"],
                    width="stretch"
                )

                title = image["title"].replace("File:", "").strip()

                st.caption(f"📷 {title}")

                st.markdown(
                    f"[View source on Wikimedia Commons]({image['url']})"
                )
                

        left, right = st.columns([3.4, 1], gap="large")

        with right:
            st.markdown(
                f"""
                <div class="profile-card">
                    <h3>🧳 Trip Profile</h3>
                    <div>
                        📍 <b>{destination}</b><br>
                        📅 {days} days<br>
                        👥 {travelers} traveler(s)<br>
                        💰 ₹{budget:,} budget<br>
                        🎒 {travel_style} style<br>
                        ⚡ {pace} pace
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with left:
            st.markdown('<div class="ai-output">', unsafe_allow_html=True)
            st.markdown(answer)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="disclaimer">⚠️ AI-generated planning draft. Verify current '
            'weather, opening hours, transport, prices, availability and local rules '
            'before booking.</div>',
            unsafe_allow_html=True,
        )

    except Exception as exc:
        error_text = str(exc)

        if "503" in error_text or "UNAVAILABLE" in error_text:
            st.error(
                "Gemini is temporarily busy. Please wait a few seconds and try again."
            )
        else:
            st.error("The AI request could not be completed.")
            st.code(error_text)

st.divider()
st.caption(
    "TripGenie AI • FFE TiE Entrepreneurship Program 2026 • "
    "AI-powered travel planning prototype"
)