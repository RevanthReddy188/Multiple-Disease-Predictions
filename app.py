import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
if "users" not in st.session_state:
    st.session_state.users = {
        "revanth": {"password": "admin123", "name": "Revanth"}
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
    
def login_page():
    st.title("🔐 Login to Health Assistant")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid username or password")

    st.markdown("Don't have an account?")
    if st.button("Go to Signup"):
        st.session_state.show_signup = True

def signup_page():
    st.title("📝 Create an Account")

    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        if new_username in st.session_state.users:
            st.error("Username already exists")
        elif new_password != confirm:
            st.error("Passwords do not match")
        elif len(new_username.strip()) < 3 or len(new_password.strip()) < 4:
            st.warning("Username must be 3+ and password 4+ characters")
        else:
            st.session_state.users[new_username] = {"password": new_password, "name": new_username}
            st.success("Account created! You can now log in.")
            st.session_state.show_signup = False

    if st.button("Back to Login"):
        st.session_state.show_signup = False

# Page config
st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🧑‍⚕️")

# Load models
diabetes_model = pickle.load(open("diabetes_model.sav", "rb"))
heart_disease_model = pickle.load(open("heart_disease_model.sav", "rb"))
parkinsons_model = pickle.load(open("parkinsons_model.sav", "rb"))

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4344/4344647.png", width=80)
    selected = option_menu(
        'Multiple Disease Prediction System',
        ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction'],
        icons=['activity', 'heart', 'person'],
        menu_icon='hospital-fill',
        default_index=0
    )


if selected == 'Diabetes Prediction':
    st.title("🧠 Diabetes Prediction using ML")
    st.markdown("Enter the medical details below to predict the likelihood of diabetes.")

    with st.form("diabetes_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')

        with col2:
            Glucose = st.text_input('Glucose Level')

        with col3:
            BloodPressure = st.text_input('Blood Pressure value')

        with col1:
            SkinThickness = st.text_input('Skin Thickness value')

        with col2:
            Insulin = st.text_input('Insulin Level')

        with col3:
            BMI = st.text_input('BMI value')

        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

        with col2:
            Age = st.text_input('Age of the Person')

        submitted = st.form_submit_button("Diabetes Test Result")

    diab_diagnosis = ''
    if submitted:
        try:
            user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness,
                          Insulin, BMI, DiabetesPedigreeFunction, Age]
            user_input = [float(x) for x in user_input]

            diab_prediction = diabetes_model.predict([user_input])

            if diab_prediction[0] == 1:
                diab_diagnosis = '⚠️ The person is diabetic'
                st.error(diab_diagnosis)
                st.info("🔎 Consider consulting a healthcare provider for proper guidance.")
            else:
                diab_diagnosis = '✅ The person is not diabetic'
                st.success(diab_diagnosis)
                st.info("🎉 Keep maintaining a healthy lifestyle!")

        except:
            st.warning("❗ Please enter valid numeric values in all fields.")


if selected == 'Heart Disease Prediction':
    st.title("❤️ Heart Disease Prediction using ML")
    st.markdown("Fill out the following details to assess the risk of heart disease.")

    with st.form("heart_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input('Age')

        with col2:
            sex = st.text_input('Sex (1 = Male, 0 = Female)')

        with col3:
            cp = st.text_input('Chest Pain types (0-3)')

        with col1:
            trestbps = st.text_input('Resting Blood Pressure')

        with col2:
            chol = st.text_input('Serum Cholestoral in mg/dl')

        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl (1 = Yes, 0 = No)')

        with col1:
            restecg = st.text_input('Resting ECG (0, 1, 2)')

        with col2:
            thalach = st.text_input('Maximum Heart Rate achieved')

        with col3:
            exang = st.text_input('Exercise Induced Angina (1 = Yes, 0 = No)')

        with col1:
            oldpeak = st.text_input('ST depression')

        with col2:
            slope = st.text_input('Slope (0, 1, 2)')

        with col3:
            ca = st.text_input('Number of Major Vessels (0-4)')

        with col1:
            thal = st.text_input('Thal (0 = Normal, 1 = Fixed, 2 = Reversible)')

        submitted = st.form_submit_button("Heart Disease Test Result")

    heart_diagnosis = ''
    if submitted:
        try:
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                          exang, oldpeak, slope, ca, thal]
            user_input = [float(x) for x in user_input]

            heart_prediction = heart_disease_model.predict([user_input])

            if heart_prediction[0] == 1:
                heart_diagnosis = '⚠️ The person is likely to have heart disease'
                st.error(heart_diagnosis)
                st.info("💡 It's recommended to follow up with a cardiologist.")
            else:
                heart_diagnosis = '✅ The person does not have heart disease'
                st.success(heart_diagnosis)
                st.info("🎉 Keep taking care of your heart health!")

        except:
            st.warning("❗ Please enter valid numeric values in all fields.")


if selected == "Parkinsons Prediction":
    st.title("🧠 Parkinson's Disease Prediction using ML")
    st.markdown("Input the required voice measurements to check for Parkinson’s Disease.")

    with st.form("parkinsons_form"):
        inputs = []
        fields = ['MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)',
                  'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer',
                  'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ',
                  'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE']

        cols = st.columns(5)
        for i, field in enumerate(fields):
            with cols[i % 5]:
                val = st.text_input(field)
                inputs.append(val)

        submitted = st.form_submit_button("Parkinson's Test Result")

    parkinsons_diagnosis = ''
    if submitted:
        try:
            user_input = [float(x) for x in inputs]
            parkinsons_prediction = parkinsons_model.predict([user_input])

            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = "⚠️ The person has Parkinson's disease"
                st.error(parkinsons_diagnosis)
                st.info("🧠 Early detection is important. Please consult a neurologist.")
            else:
                parkinsons_diagnosis = "✅ The person does not have Parkinson's disease"
                st.success(parkinsons_diagnosis)
                st.info("🎉 No signs of Parkinson's disease detected.")

        except:
            st.warning("❗ Please enter valid numeric values in all fields.")
