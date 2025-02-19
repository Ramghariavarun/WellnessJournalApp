import streamlit as st
from datetime import datetime, time
import pandas as pd


def init_session_state():
    if 'meals' not in st.session_state:
        st.session_state.meals = []
    if 'water_intake' not in st.session_state:
        st.session_state.water_intake = []
    if 'mood_entries' not in st.session_state:
        st.session_state.mood_entries = []
    if 'time_format' not in st.session_state:
        st.session_state.time_format = "24-hour"


def format_timestamp(dt):
    if st.session_state.time_format == "12-hour":
        return dt.strftime("%Y-%m-%d %I:%M %p")
    return dt.strftime("%Y-%m-%d %H:%M")


def get_meal_type():
    current_time = datetime.now().time()
    meal_windows = {
        "Breakfast": (time(6, 0), time(9, 0)),
        "Lunch": (time(12, 0), time(15, 0)),
        "Dinner": (time(18, 0), time(22, 0))
    }

    for meal, (start, end) in meal_windows.items():
        if start <= current_time <= end:
            # Check if another meal exists in the same window today
            for m in st.session_state.meals:
                meal_time = datetime.strptime(m['timestamp'], "%Y-%m-%d %H:%M")
                if meal_time.date() == datetime.today().date() and start <= meal_time.time() <= end:
                    return "Snacking"
            return meal
    return "Snacking"


def main():
    st.title("Wellness Journal App")
    init_session_state()

    menu = st.sidebar.radio("Navigation", ["Meals", "Water Intake", "Mood Entry", "Summary"])
    time_format = st.sidebar.radio("Select Time Format", ["24-hour", "12-hour"])
    st.session_state.time_format = time_format

    if menu == "Meals":
        st.header("Log a Meal")
        meal_type = get_meal_type()
        meal_options = ["Roti with Sabzi", "Rice with Dal", "Paratha", "Idli Sambhar", "Dosa", "Pulao", "Khichdi",
                        "Chole Bhature", "Poha", "Upma", "Paneer Bhurji", "Salad", "Fruits", "Curd Rice",
                        "Egg Omelette", "Chicken Curry", "Fish Fry"]
        meal_name = st.selectbox("Select Meal", options=meal_options, index=0)
        meal_description = f"{meal_type} meal: {meal_name}"
        meal_image = st.camera_input("Take a picture of your meal")

        if st.button("Add Meal"):
            entry = {
                "type": meal_type,
                "description": meal_description,
                "timestamp": format_timestamp(datetime.now()),
                "image": meal_image
            }
            st.session_state.meals.append(entry)
            st.success(f"{meal_type} added!")

        if st.session_state.meals:
            st.subheader("Logged Meals")
            for meal in st.session_state.meals:
                st.write(f"{meal['timestamp']}: *{meal['type']}* - {meal['description']}")
                if meal['image']:
                    st.image(meal['image'], caption="Meal Image", use_column_width=True)

    elif menu == "Water Intake":
        st.header("Log Water Intake")
        water = st.number_input("Amount of water (ml)", min_value=0, step=50)
        if st.button("Add Water Intake"):
            st.session_state.water_intake.append({"amount": water, "timestamp": format_timestamp(datetime.now())})
            st.success("Water intake logged!")

        if st.session_state.water_intake:
            st.subheader("Logged Water Intake")
            total_water = sum(entry["amount"] for entry in st.session_state.water_intake)
            st.write(f"**Total Water Intake:** {total_water} ml")
            for entry in st.session_state.water_intake:
                st.write(f"{entry['timestamp']}: {entry['amount']} ml")

    elif menu == "Mood Entry":
        st.header("Log Mood Entry")
        mood_options = {5: "😁 Very Happy", 4: "😊 Happy", 3: "😐 Neutral", 2: "☹️ Sad", 1: "😢 Very Sad"}
        mood_rating = st.selectbox("Rate your mood", options=list(mood_options.keys()),
                                   format_func=lambda x: mood_options[x])
        symptoms = st.text_input("Any symptoms?")
        if st.button("Add Mood Entry"):
            entry = {
                "rating": mood_rating,
                "symptoms": symptoms,
                "timestamp": format_timestamp(datetime.now())
            }
            st.session_state.mood_entries.append(entry)
            st.success("Mood entry added!")

        if st.session_state.mood_entries:
            st.subheader("Mood Entries")
            for entry in st.session_state.mood_entries:
                st.write(f"{entry['timestamp']}: {mood_options[entry['rating']]} - Symptoms: {entry['symptoms']}")

    elif menu == "Summary":
        st.header("Generate Summary")
        if not st.session_state.meals and not st.session_state.water_intake and not st.session_state.mood_entries:
            st.warning("No data available for summary.")
        else:
            total_meals = len(st.session_state.meals)
            total_water = sum(entry["amount"] for entry in st.session_state.water_intake)
            avg_mood = sum(entry['rating'] for entry in st.session_state.mood_entries) / len(
                st.session_state.mood_entries) if st.session_state.mood_entries else "No mood data"
            st.subheader("Health Summary")
            st.write(f"**Total Meals Logged:** {total_meals}")
            st.write(f"**Total Water Intake:** {total_water} ml")
            st.write(f"**Average Mood Rating:** {avg_mood}")


if __name__ == '__main__':
    main()
