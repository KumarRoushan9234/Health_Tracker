import streamlit as st
from main_exercise_recomendation import exercise_recomendation
from main_diertary_recomendation import dietary_recomendation
from main_calorie_tracker import calorie_tracker

def main():
    st.title("Health Recommendation App")

    page = st.sidebar.selectbox("Select a page", ["Home Page", "Calorie Tracker", "Dietary Recommendation","Exercise Recomendation"])
    if 'total_cal' not in st.session_state:
        st.session_state.name = ""

    if page == "Home Page":
        st.title("Fitness Future")
        st.write("Welcome to the Health Recommendation App!")
        st.session_state.name = st.text_input(f"Enter Name")
        age = st.text_input(f"Enter Age")
        gender = st.selectbox('Select Gender', ['Male','Female'])
        height = st.text_input(f"Enter Height")
        weight = st.text_input(f"Enter Weight")
        if st.button("Submit"):
            st.success("Information Added")
            st.write("Name: ",st.session_state.name)
            st.write("Age: ",age)
            st.write("Gender : ",gender)
            st.write("Height: ",height)
            st.write("Weight: ",weight)
        st.info("Choose a page from the sidebar to get started.")

    elif page == "Calorie Tracker":
        calorie_tracker(st.session_state.name)

    elif page == "Dietary Recommendation":
        dietary_recomendation(st.session_state.name)

    elif page == "Exercise Recomendation":
        exercise_recomendation(st.session_state.name)

if __name__ == "__main__":
    main()
