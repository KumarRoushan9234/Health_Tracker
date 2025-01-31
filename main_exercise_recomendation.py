def exercise_recomendation(name):
    import streamlit as st
    import pandas as pd
    import pickle

    with open('time_model.pkl', 'rb') as file:
        time_model = pickle.load(file)
    with open('aerobic_model.pkl', 'rb') as file:
        aerobic_model = pickle.load(file)
    with open('strength_model.pkl', 'rb') as file:
        strength_model = pickle.load(file)

    st.title("Fitness Recommendation App")
    nim="Hello "+name
    st.info(nim)

    age = st.number_input("Enter your age:", min_value=1, max_value=100)
    height = st.number_input("Enter your height (in cm):", min_value=1, max_value=300)
    weight = st.number_input("Enter your weight (in kg):", min_value=1, max_value=300)
    gender = st.radio("Select your gender:", ["Male", "Female"])
    goal = st.selectbox("Select your fitness goal:", ["Build Muscle", "Stay Fit", "Lose Weight"])

    gender_code = 1 if gender.lower() == "male" else 0

    goal_mapping = {"Build Muscle": 0, "Lose Weight": 1, "Stay Fit": 2}
    goal_code = goal_mapping.get(goal, 0)

    time_dt = pd.DataFrame({'age': [age], 'height': [height], 'weight': [weight]})
    fit_dt = pd.DataFrame({'age': [age], 'height': [height], 'weight': [weight], 'gender': [gender_code], 'goal': [goal_code]})

    time_pred = time_model.predict(time_dt)
    aerobic_pred = aerobic_model.predict(fit_dt)
    strength_pred = strength_model.predict(fit_dt)

    aerobic_activities = ["Cycling", "Dancing", "Jogging", "Running", "Swimming", "Weight Lifting"]
    strength_trainings = ["Bodyweight", "Resistance Band", "Weight Lifting", "Weight Machine"]

    aerobic = aerobic_activities[aerobic_pred[0]]
    strength = strength_trainings[strength_pred[0]]

    intensity=" "
    if 17 < age <= 30:
        intensity = "Intense"
    elif 30 < age <= 45:
        intensity = "Moderate"
    elif age > 45:
        intensity = "Low"

    if 18<age<35 and goal=="Build Muscle":
        strength="Weight Lifting"
    elif 18<age<35 and goal=="Lose Weight":
        strength="Bodyweight"
    elif 18<age<35 and goal=="Stay Fit":
        strength="Weight Machine"

    if st.button("submit"):
        st.header("Fitness Recommendations")
        st.write(f"Strength Training Recommended: {strength}")
        st.write(f"Aerobic Activity Recommended: {aerobic}")
        st.write(f"Duration of Activity: {time_pred[0]} minutes")
        st.write("Recommended Intensity: ",intensity)
        st.write("Recomended ",strength,"Exercises :")
        if strength == "Resistance Band":
            dt = pd.read_csv("resistance_band.csv")
            st.table(dt)
        elif strength == "Weight Machine":
            dt = pd.read_csv("machine.csv")
            st.table(dt)
        elif strength == "Weight Lifting":
            dt = pd.read_csv("weightlifting.csv")
            st.table(dt)
        elif strength == "Bodyweight":
            dt = pd.read_csv("bodyweight.csv")
            st.table(dt)
