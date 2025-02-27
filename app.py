import streamlit as st
import requests
import os
from dotenv import load_dotenv

# ------------------ CONFIGURATION ------------------ #
st.set_page_config(page_title="🌱 Growth Mindset App", page_icon="🌿", layout="centered")

# Load environment variables
load_dotenv()

API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")  # Get API key from .env

# Check API Key
if not API_TOKEN:
    st.error("❌ API Key not found! Make sure you have a `.env` file.")
    st.stop()  # Stop execution if API key is missing

# ------------------ HUGGING FACE API ------------------ #
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Function to Query Hugging Face API
def query_huggingface(prompt: str):
    payload = {"inputs": prompt, "max_length": 100, "temperature": 0.8}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data[0].get("generated_text", "⚠️ No meaningful response from API.")
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ API Error: {str(e)}"

# ------------------ UI ELEMENTS ------------------ #
st.title("🌱 Growth Mindset Coach")
st.markdown("**Cultivate positivity, resilience, and unstoppable growth!**")

# User Input
mood = st.selectbox("How are you feeling today?", ["Motivated", "Neutral", "Down"])
goal = st.selectbox("What's your growth goal?", [
    "Build Resilience", "Enhance Focus", "Boost Confidence", 
    "Stay Consistent", "Develop Self-Discipline", "Practice Gratitude", 
    "Improve Emotional Intelligence", "Master Meditation", "Increase Productivity"
])

# ------------------ CONTENT GENERATION ------------------ #
if st.button("Get Growth Tip & Affirmation"):
    with st.spinner("Generating your personalized advice..."):
        prompt = f"Give me a motivational affirmation and tip for someone who feels {mood.lower()} and wants to {goal.lower()}."
        response = query_huggingface(prompt)
    st.markdown(f"**Your Growth Boost:**\n\n{response}")

# ------------------ EXTRA FEATURES ------------------ #
st.markdown("### 🧘 Mindfulness & Personal Growth")

topic = st.selectbox("Select a topic to learn more:", [
    "Daily Meditation Tips", "How to Build a Growth Mindset",
    "Overcoming Negative Thoughts", "How to Develop Self-Discipline",
    "The Science of Gratitude", "Habits for Success",
    "How to Improve Focus", "Morning Routines for Success"
])

if st.button("Get Insights"):
    with st.spinner("Fetching wisdom..."):
        prompt = f"Provide a short and powerful guide on {topic}."
        response = query_huggingface(prompt)
    st.markdown(f"**Insight:**\n\n{response}")

# ------------------ PROGRESS TRACKER ------------------ #
st.markdown("### 🌟 Track Your Progress")
progress = st.slider("How do you rate your progress today?", 0, 100, 50)
st.progress(progress)

if progress > 75:
    st.success("You're doing amazing! Keep up the great work! 🚀")
elif progress > 50:
    st.info("Great progress! Stay consistent! 💪")
else:
    st.warning("Every small step counts! Keep going! 🌻")

# Footer
st.markdown("<footer>Made with ❤️ by Almas | Powered by Hugging Face & Streamlit</footer>", unsafe_allow_html=True)
