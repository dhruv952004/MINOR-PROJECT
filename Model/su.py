import pickle
from sklearn.metrics import PredictionErrorDisplay
from sklearn.tree import DecisionTreeClassifier
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import streamlit
import os
import pickle
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import plotly.graph_objects as go
import time
print("Current Working Directory:", os.getcwd())
print("Files:", os.listdir(os.getcwd()))


# loading the saved models
try:
    diabetes_model = pickle.load(open('Model/saved_models/diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open('Model/saved_models/heart_disease_model.sav','rb'))
    parkinsons_model = pickle.load(open('Model/saved_models/parkinsons_model.sav', 'rb'))
except FileNotFoundError:
    st.error("Error: Model files not found. Please ensure the model files are present in the Model/saved_models directory.")
    st.info("Required files: diabetes_model.sav, heart_disease_model.sav, parkinsons_model.sav")
    st.stop()


# Initialize session state for user management
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = None

# User data
USERS = {
    "doctor": {"password": "1234", "name": "Dr. Smith"},
    "patient": {"password": "1234", "name": "James Wilson"}
}

# Login page
def show_login():
    # Add custom CSS for centering and styling
    st.markdown("""
        <style>
        .main {
            padding: 0;
            margin: 0;
        }
        .main > div {
            padding: 1rem;
            max-width: 500px;
            margin: 0 auto;
        }
        .stApp {
            background: #f0f2f6;
        }
        .login-container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
        }
        .login-header {
            text-align: center;
            color: #1e3c72;
            margin-bottom: 2rem;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 2rem;
            font-weight: 600;
        }
        .role-selector {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            border-radius: 8px;
            background: #f8f9fa;
        }
        .demo-credentials {
            margin-top: 1.5rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
            text-align: center;
        }
        .demo-credentials p {
            color: #1e3c72;
            margin: 0;
        }
        .stButton > button {
            width: 100%;
            background: #1e3c72;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: 500;
            margin-top: 1rem;
        }
        .stButton > button:hover {
            background: #2a5298;
        }
        div[data-testid="stForm"] {
            background: transparent;
            border: none;
            padding: 1rem 0;
        }
        .stTextInput > div > div > input {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Single login container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="login-header">Welcome to AROGYAM</h1>', unsafe_allow_html=True)
    
    # Role selection
    st.markdown('<div class="role-selector">', unsafe_allow_html=True)
    role = st.radio("Select Role", ["patient", "doctor"], horizontal=True, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.user_role = role
                st.session_state.username = username
                st.success(f"Welcome, {USERS[username]['name']}!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    # Demo credentials
    st.markdown("""
        <div class="demo-credentials">
            <p>
                <strong>Demo credentials:</strong><br>
                Username: doctor/patient<br>
                Password: 1234
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# sidebar for navigation
with st.sidebar:
    if st.session_state.user_role:
        st.success(f"Welcome, {USERS[st.session_state.username]['name']}")
        
        if st.session_state.user_role == "doctor":
            selected = option_menu('Doctor Dashboard',
                                ['Patient List',
                                 'Diabetes Prediction',
                                 'Heart Disease Prediction',
                                 'Parkinsons Prediction',
                                 'Appointments',
                                 'Reports'],
                                icons=['people','activity','heart','person','calendar','file-text'],
                                default_index=0)
        else:
            selected = option_menu('Patient Dashboard',
                                ['Health Check',
                                 'Appointments',
                                 'Medical Records',
                                 'Test Results'],
                                icons=['activity','calendar','file-medical','clipboard-data'],
                                default_index=0)
        
        if st.button("Logout"):
            st.session_state.user_role = None
            st.session_state.username = None
            st.rerun()
    else:
        show_login()

if not st.session_state.user_role:
    st.stop()

# Doctor's Patient List
if selected == 'Patient List':
    st.title('Patient Management')
    
    patients = {
        'Name': ['James Wilson', 'Emily Brown', 'Michael Davis'],
        'Age': [35, 28, 45],
        'Last Visit': ['2024-03-01', '2024-02-28', '2024-03-02'],
        'Status': ['Stable', 'Follow-up needed', 'Under treatment']
    }
    st.dataframe(pd.DataFrame(patients))
    
    with st.expander("Add New Patient"):
        with st.form("new_patient"):
            name = st.text_input("Patient Name")
            age = st.number_input("Age", 0, 120)
            if st.form_submit_button("Add Patient"):
                st.success("Patient added successfully!")

# Patient Health Check
if selected == 'Health Check':
    st.title('Health Check')
    
    symptoms = st.multiselect(
        "Select your symptoms",
        ['Fever', 'Cough', 'Headache', 'Fatigue', 'Body ache']
    )
    
    if symptoms:
        severity = st.slider("Rate severity (1-10)", 1, 10, 5)
        duration = st.number_input("Duration (days)", 1, 30, 1)
        
        if st.button("Analyze"):
            with st.spinner("Analyzing symptoms..."):
                time.sleep(1)
                st.success("Analysis complete!")
                st.info("Possible condition: Common Cold")
                st.warning("Recommendation: Rest and hydration")

# Appointments (for both doctor and patient)
if selected == 'Appointments':
    st.title('Appointments')
    
    upcoming = {
        'Date': ['2024-03-15', '2024-03-16'],
        'Time': ['10:00 AM', '02:30 PM'],
        'Type': ['Check-up', 'Follow-up']
    }
    st.dataframe(pd.DataFrame(upcoming))
    
    with st.form("book_appointment"):
        date = st.date_input("Select Date")
        time = st.selectbox("Select Time", ["09:00 AM", "10:00 AM", "02:00 PM"])
        appointment_type = st.selectbox("Type", ["Check-up", "Follow-up", "Consultation"])
        if st.form_submit_button("Book Appointment"):
            st.success("Appointment booked successfully!")

# Medical Records (for patients)
if selected == 'Medical Records':
    st.title('Medical Records')
    
    # Vitals
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Blood Pressure", "120/80")
    with col2:
        st.metric("Heart Rate", "72 bpm")
    with col3:
        st.metric("Temperature", "98.6°F")
    
    # History
    st.subheader("Medical History")
    history = {
        'Date': ['2024-02-15', '2024-01-10'],
        'Type': ['Check-up', 'Blood Test'],
        'Notes': ['All vitals normal', 'Cholesterol slightly elevated']
    }
    st.dataframe(pd.DataFrame(history))
    
# Diabetes Prediction Page
if (selected == 'Diabetes Prediction'):
    st.title('Diabetes Prediction using ML')
    
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
    
    diab_diagnosis = ''
    
    if st.button('Diabetes Test Result'):
        try:
            diab_prediction = diabetes_model.predict([[float(Pregnancies), float(Glucose), float(BloodPressure), 
                                                     float(SkinThickness), float(Insulin), float(BMI), 
                                                     float(DiabetesPedigreeFunction), float(Age)]])
            
            if (diab_prediction[0] == 1):
                diab_diagnosis = 'The person is diabetic'
            else:
                diab_diagnosis = 'The person is not diabetic'
            
            st.success(diab_diagnosis)
            
            # Generate report
            if st.button("Generate Report"):
                report = f"""
                Diabetes Test Report
                Date: {datetime.now().strftime('%Y-%m-%d')}
                Result: {diab_diagnosis}
                
                Parameters:
                - Glucose Level: {Glucose}
                - Blood Pressure: {BloodPressure}
                - BMI: {BMI}
                - Age: {Age}
                """
                st.download_button("Download Report", report, "diabetes_report.txt")
        except ValueError:
            st.error("Please enter valid numeric values for all fields")

# Heart Disease Prediction Page
if (selected == 'Heart Disease Prediction'):
    st.title('Heart Disease Prediction using ML')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.text_input('Age')
        
    with col2:
        sex = st.text_input('Sex')
        
    with col3:
        cp = st.text_input('Chest Pain types')
        
    with col1:
        trestbps = st.text_input('Resting Blood Pressure')
        
    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')
        
    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
        
    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')
        
    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')
        
    with col3:
        exang = st.text_input('Exercise Induced Angina')
        
    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')
        
    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')
        
    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')
        
    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')
        
    heart_diagnosis = ''
    
    if st.button('Heart Disease Test Result'):
        try:
            heart_prediction = heart_disease_model.predict([[float(age), float(sex), float(cp), float(trestbps), 
                                                           float(chol), float(fbs), float(restecg), float(thalach),
                                                           float(exang), float(oldpeak), float(slope), float(ca), 
                                                           float(thal)]])                          
            
            if (heart_prediction[0] == 1):
                heart_diagnosis = 'The person is having heart disease'
            else:
                heart_diagnosis = 'The person does not have any heart disease'
            
            st.success(heart_diagnosis)
            
        except ValueError:
            st.error("Please enter valid numeric values for all fields")

# Parkinson's Prediction Page
if (selected == "Parkinsons Prediction"):
    
    st.title("Parkinson's Disease Prediction using ML")
    
    col1, col2, col3, col4, col5 = st.columns(5)  
    
    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')
        
    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')
        
    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')
        
    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')
        
    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')
        
    with col1:
        RAP = st.text_input('MDVP:RAP')
        
    with col2:
        PPQ = st.text_input('MDVP:PPQ')
        
    with col3:
        DDP = st.text_input('Jitter:DDP')
        
    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')
        
    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')
        
    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')
        
    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')
        
    with col3:
        APQ = st.text_input('MDVP:APQ')
        
    with col4:
        DDA = st.text_input('Shimmer:DDA')
        
    with col5:
        NHR = st.text_input('NHR')
        
    with col1:
        HNR = st.text_input('HNR')
        
    with col2:
        RPDE = st.text_input('RPDE')
        
    with col3:
        DFA = st.text_input('DFA')
        
    with col4:
        spread1 = st.text_input('spread1')
        
    with col5:
        spread2 = st.text_input('spread2')
        
    with col1:
        D2 = st.text_input('D2')
        
    with col2:
        PPE = st.text_input('PPE')
        
    parkinsons_diagnosis = ''
    
    if st.button("Parkinson's Test Result"):
        try:
            parkinsons_prediction = parkinsons_model.predict([[float(fo), float(fhi), float(flo), float(Jitter_percent),
                                                             float(Jitter_Abs), float(RAP), float(PPQ), float(DDP),
                                                             float(Shimmer), float(Shimmer_dB), float(APQ3), float(APQ5),
                                                             float(APQ), float(DDA), float(NHR), float(HNR), float(RPDE),
                                                             float(DFA), float(spread1), float(spread2), float(D2),
                                                             float(PPE)]])
            
            if (parkinsons_prediction[0] == 1):
                parkinsons_diagnosis = "The person has Parkinson's disease"
            else:
                parkinsons_diagnosis = "The person does not have Parkinson's disease"
            
            st.success(parkinsons_diagnosis)
        except ValueError:
            st.error("Please enter valid numeric values for all fields")

st.title('AROGYAM')