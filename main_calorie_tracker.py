def calorie_tracker(name):
    import streamlit as st
    import pandas as pd
    from fuzzywuzzy import process

    df = pd.read_csv("Calorie_and_Nutrients.csv")
    df.drop(["Minerals.1", "Goals", "Preferences", "Restrictions"], axis=1, inplace=True)
    df["Sodium"] = df["Sodium"] / 1000
    df["Vitamins"] = df["Vitamins"] / 1000
    df["Minerals"] = df["Minerals"] / 1000
    df["Sodium"] = df["Sodium"].round(6)
    df["Vitamins"] = df["Vitamins"].round(6)
    df["Minerals"] = df["Minerals"].round(6)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    def match_food(x):
        match_food, similar_score = process.extractOne(x.capitalize(), df['food'].str.capitalize().values)
        if similar_score >= 80:
            row = df.loc[df['food'].str.capitalize() == match_food.capitalize()]
            
            cal = float(row['calorie'].values[0]),
            pro  = float(row['protein'].values[0]),
            carb = float(row['carbs'].values[0]),
            fat = float(row['fat'].values[0]),
            sugar = float(row['Sugar'].values[0]),
            fib = float(row['Fiber'].values[0]),
            sod = float(row['Sodium'].values[0]),
            vit = float(row['Vitamins'].values[0]),
            min = float(row['Minerals'].values[0])
            # nutrient_info = ()
            return cal,pro,carb,fat,sugar,fib,sod,vit,min,match_food
        else:
            st.write("Food not found. Please enter a valid food item.")
            return None
    st.title("Calorie and Nutrient Tracker")
    st.write()
    nim="Hello "+name
    st.info(nim)
    st.write("-------------------------------------------------------------------")

    if 'total_cal' not in st.session_state:
        st.session_state.total_cal = 0.0
        st.session_state.total_pro = 0.0
        st.session_state.total_carb = 0.0
        st.session_state.total_fat = 0.0
        st.session_state.total_sugar = 0.0
        st.session_state.total_fib = 0.0
        st.session_state.total_sod = 0.0
        st.session_state.total_vit = 0.0
        st.session_state.total_min = 0.0
        st.session_state.serv = 0

    if 'my_data' not in st.session_state:
        st.session_state.my_data = {}

    if 'final_df' not in st.session_state.my_data:
        final_df = pd.DataFrame(columns=["Serving","Total-Calorie","Total-Protein","Total-Carbs","Total-Fat","Total-Sugar","Total-Fiber","Total-Sodium","Total-Vitamin","Total-Mineral"])
        st.session_state.my_data['final_df'] = final_df

    # final_df = pd.DataFrame(columns=["Total-Calorie","Total-Protein","Total-Carbs","Total-Fat","Total-Sugar","Total-Fiber","Total-Sodium","Total-Vitamin","Total-Mineral"])
    # final_df = pd.DataFrame(columns=["Serving","Total-Calorie","Total-Protein","Total-Carbs","Total-Fat","Total-Sugar","Total-Fiber","Total-Sodium","Total-Vitamin","Total-Mineral"])
    st.subheader("Add Food Item")
    x = st.text_input(f"Enter Food")
    serv = st.number_input("No. of Servings (1 serving = 100g)", min_value=1, max_value=10, value=1, step=1)
    if st.button("Add Item"):
        cal,pro,carb,fat,sugar,fib,sod,vit,min,food = match_food(x)
        inp=food+" - has been added"
        st.success(inp)
        st.write("Nutriturional Information About",food)
        data = {
            "Calorie": cal,
            "Protein": pro,
            "Carbs": carb,
            "Fat": fat,
            "Sugar": sugar,
            "Fiber": fib,
            "Sodium": sod,     
            "Vitamin": vit,
            "Mineral": min
        }
        df = pd.DataFrame(data)
        st.table(df)
        st.session_state.total_cal += (float(cal[0])*serv)
        st.session_state.total_pro += (float(pro[0])*serv)
        st.session_state.total_carb += (float(carb[0])*serv)
        st.session_state.total_fat += (float(fat[0])*serv)
        st.session_state.total_sugar += (float(sugar[0])*serv)
        st.session_state.total_fib += (float(fib[0])*serv)
        st.session_state.total_sod += (float(sod[0])*serv)
        st.session_state.total_vit += (float(vit[0])*serv)
        st.session_state.total_min += (float(min)*serv)
        st.session_state.serv = int(serv)
        l1 = [int(st.session_state.serv),st.session_state.total_cal,st.session_state.total_pro,st.session_state.total_carb,st.session_state.total_fat,st.session_state.total_sugar,st.session_state.total_fib,st.session_state.total_sod,st.session_state.total_vit,st.session_state.total_min]
        final_df = st.session_state.my_data['final_df']
        
        final_df.loc[food] = l1
        st.write(final_df)
        st.session_state.my_data['final_df'] = final_df

        # st.session_state.serv += int(serv)

    if st.button("Final Result"):
        st.write("Total-Calorie :",st.session_state.total_cal)
        st.write("Total-Protien :",st.session_state.total_pro)
        st.write("Total-Carbs :",st.session_state.total_carb)
        st.write("Total-Fat :",st.session_state.total_fat)
        st.write("Total-Sugar :",st.session_state.total_sugar)
        st.write("Total-Fiber :",st.session_state.total_fib)
        st.write("Total-Sodium :",st.session_state.total_sod)
        st.write("Total-Vitamin :",st.session_state.total_vit)
        st.write("Total-Mineral :",st.session_state.total_min)
        st.subheader("Food-List")
        st.write(st.table(st.session_state.my_data['final_df']))
    else:
        pass

        

