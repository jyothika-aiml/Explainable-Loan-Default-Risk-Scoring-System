import streamlit as st
import pandas as pd
import joblib

# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="Explainable Loan Default Risk Prediction",
    page_icon="💰",
    layout="wide"
)

# ---------------------------------
# Load Model and Preprocessing Files
# ---------------------------------

model = joblib.load("models/random_forest_model.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")
feature_names = joblib.load("models/feature_names.pkl")

# ---------------------------------
# Title
# ---------------------------------

st.title("💰 Explainable Loan Default Risk Prediction")

st.write("""
This web application predicts whether a customer is likely to default on a loan
using a trained Random Forest Machine Learning model.

Fill in the applicant's details and click **Predict**.
""")

st.divider()

# ---------------------------------
# Applicant Information
# ---------------------------------

st.header("Applicant Information")

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    income = st.number_input(
        "Annual Income",
        min_value=0,
        value=50000
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0,
        value=100000
    )

    credit_score = st.number_input(
        "Credit Score",
        min_value=300,
        max_value=850,
        value=650
    )

    months_employed = st.number_input(
        "Months Employed",
        min_value=0,
        value=24
    )

    num_credit_lines = st.number_input(
        "Number of Credit Lines",
        min_value=0,
        value=3
    )

    interest_rate = st.number_input(
        "Interest Rate (%)",
        min_value=0.0,
        value=10.5
    )

    loan_term = st.selectbox(
        "Loan Term",
        [12, 24, 36, 48, 60]
    )

with col2:

    dti_ratio = st.slider(
        "Debt-to-Income Ratio",
        0.0,
        1.0,
        0.30
    )

    education = st.selectbox(
        "Education",
        ["Bachelor's", "High School", "Master's", "PhD"]
    )

    employment_type = st.selectbox(
        "Employment Type",
        ["Full-time", "Part-time", "Self-employed", "Unemployed"]
    )

    marital_status = st.selectbox(
        "Marital Status",
        ["Single", "Married", "Divorced"]
    )

    has_mortgage = st.selectbox(
        "Has Mortgage",
        ["No", "Yes"]
    )

    has_dependents = st.selectbox(
        "Has Dependents",
        ["No", "Yes"]
    )

    loan_purpose = st.selectbox(
        "Loan Purpose",
        ["Auto", "Business", "Education", "Home", "Other"]
    )

    has_cosigner = st.selectbox(
        "Has Co-signer",
        ["No", "Yes"]
    )

st.divider()
# ---------------------------------
# Prediction
# ---------------------------------

if st.button("Predict Loan Default"):

    # Create input DataFrame with user inputs
    input_data = pd.DataFrame([{
        "Age": age,
        "Income": income,
        "LoanAmount": loan_amount,
        "CreditScore": credit_score,
        "MonthsEmployed": months_employed,
        "NumCreditLines": num_credit_lines,
        "InterestRate": interest_rate,
        "LoanTerm": loan_term,
        "DTIRatio": dti_ratio,
        "Education": education,
        "EmploymentType": employment_type,
        "MaritalStatus": marital_status,
        "HasMortgage": has_mortgage,
        "HasDependents": has_dependents,
        "LoanPurpose": loan_purpose,
        "HasCoSigner": has_cosigner
    }])

    # Encode categorical features using saved LabelEncoders
    categorical_columns = [
        "Education",
        "EmploymentType",
        "MaritalStatus",
        "HasMortgage",
        "HasDependents",
        "LoanPurpose",
        "HasCoSigner"
    ]

    for col in categorical_columns:
        input_data[col] = label_encoders[col].transform(input_data[col])

    # Ensure correct feature order
    input_data = input_data[feature_names]

    # Prediction
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    # Display results
    st.subheader("Prediction Result")

    if prediction == 1:
        st.error("⚠️ High Risk of Loan Default")
    else:
        st.success("✅ Low Risk of Loan Default")

    st.metric(
        label="Probability of Default",
        value=f"{probability:.2%}"
    )

    # Risk interpretation
    if probability < 0.30:
        st.success("🟢 Risk Level: Low")
    elif probability < 0.70:
        st.warning("🟡 Risk Level: Moderate")
    else:
        st.error("🔴 Risk Level: High")