def dietary_recomendation(name):
    import streamlit as st
    import pandas as pd

    data = pd.read_csv("diertary_recomendation.csv")

    data.drop_duplicates(inplace=True)
    data.reset_index(drop=True, inplace=True)

    data['Restrictions'].fillna('No Restriction', inplace=True)

    data['Preferences'] = data['Preferences'].astype(str)

    unique_goals = data['Goals'].unique().tolist()
    unique_preferences = data['Preferences'].unique().tolist()
    unique_restrictions = data['Restrictions'].unique().tolist()

    st.title("Dietary Recommendation System")
    nim="Hello "+name
    st.info(nim)
    
    st.header("User Input")
    weight = st.number_input("Enter your weight (kg):", min_value=0.0)
    height = st.number_input("Enter your height (cm):", min_value=0.0)

    if height == 0.0:
        st.error("Height must be greater than zero.")
        st.stop()  

    gender = st.selectbox("Select your gender:", ("Male", "Female"))
    age = st.number_input("Select your age:", min_value=0.0)

    bmi = round(float(weight) / float(((height / 100) ** 2)), 2)
        
    st.write("BMI:",bmi)

    if bmi < 18.5:
        body_type = "Underweight"
    elif 18.5 <= bmi < 25:
        body_type = "Normal Weight"
    elif 25 <= bmi < 30:
        body_type = "Overweight"
    else:
        body_type = "Obese"

    st.write("Body Type:", body_type)

    if gender.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender.lower() == "female":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        st.warning("Invalid gender")

    st.write("Basal Metabolic Rate (BMR):", bmr)

    activity_level=st.selectbox(
        "Select your activity level:",
        ['Sedentary', 'Lightly_Active', 'Moderately_Active', 'Very_Active']
    )

    multiplier = {
        'Sedentary': 1.2,
        'Lightly_Active': 1.375,
        'Moderately_Active': 1.55,
        'Very_Active': 1.725
    }

    tdee = bmr * multiplier.get(activity_level, 1)

    st.write("Total Daily Energy Expenditure (TDEE):", tdee)
    st.header("Dietary Preferences")
    user_goals = st.multiselect("Select your goals:", unique_goals)
    user_preferences = st.multiselect("Select your preferences:", unique_preferences)
    user_restrictions = st.multiselect("Select your restrictions:", unique_restrictions)

    filtered_data = data[data['Goals'].isin(user_goals) &
                        data['Preferences'].apply(lambda x: any(pref in user_preferences for pref in str(x).split(','))) &
                        data['Restrictions'].apply(lambda x: any(rest in user_restrictions for rest in str(x).split(',')))]

    st.write("Filtered Data:")
    st.write(filtered_data)

    goal_weight = 3
    preference_weight = 2
    restriction_weight = 1

    filtered_data['Score'] = (
        filtered_data['Goals'].apply(lambda x: goal_weight if x in user_goals else 0) +
        filtered_data['Preferences'].apply(lambda x: preference_weight if any(pref in user_preferences for pref in x.split(',')) else 0) +
        filtered_data['Restrictions'].apply(lambda x: restriction_weight if any(rest in user_restrictions for rest in x.split(',')) else 0)
    )

    st.write("Scored Data:")
    st.write(filtered_data[['food', 'Score']])

    st.header("Top Recommendations:")
    recommended_food = filtered_data.sort_values(by='Score', ascending=False)[['food', 'Score']]
    st.table(recommended_food)
