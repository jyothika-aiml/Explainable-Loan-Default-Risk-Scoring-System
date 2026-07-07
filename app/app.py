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
# Load Trained Model
# ---------------------------------

model = joblib.load("models/random_forest_model.pkl")

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

st.header("Applicant Information")

# ======================================================
# FORM STARTS HERE
# ======================================================

with st.form("loan_prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1
        )

        income = st.number_input(
            "Annual Income",
            min_value=0,
            value=50000,
            step=1000
        )

        loan_amount = st.number_input(
            "Loan Amount",
            min_value=0,
            value=100000,
            step=1000
        )

        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=850,
            value=650,
            step=1
        )

        months_employed = st.number_input(
            "Months Employed",
            min_value=0,
            value=24,
            step=1
        )

        num_credit_lines = st.number_input(
            "Number of Credit Lines",
            min_value=0,
            value=3,
            step=1
        )

        interest_rate = st.number_input(
            "Interest Rate (%)",
            min_value=0.0,
            value=10.5,
            step=0.1,
            format="%.2f"
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

    submitted = st.form_submit_button("Predict Loan Default")

# ======================================================
# PREDICTION
# ======================================================

if submitted:

    education_map = {
        "Bachelor's": 0,
        "High School": 1,
        "Master's": 2,
        "PhD": 3
    }

    employment_map = {
        "Full-time": 0,
        "Part-time": 1,
        "Self-employed": 2,
        "Unemployed": 3
    }

    marital_map = {
        "Divorced": 0,
        "Married": 1,
        "Single": 2
    }

    yes_no = {
        "No": 0,
        "Yes": 1
    }

    purpose_map = {
        "Auto": 0,
        "Business": 1,
        "Education": 2,
        "Home": 3,
        "Other": 4
    }

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
        "Education": education_map[education],
        "EmploymentType": employment_map[employment_type],
        "MaritalStatus": marital_map[marital_status],
        "HasMortgage": yes_no[has_mortgage],
        "HasDependents": yes_no[has_dependents],
        "LoanPurpose": purpose_map[loan_purpose],
        "HasCoSigner": yes_no[has_cosigner]
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.divider()
    st.subheader("Prediction Result")

    if prediction == 1:
        st.error("⚠️ High Risk of Loan Default")
    else:
        st.success("✅ Low Risk of Loan Default")

    st.metric(
        "Probability of Default",
        f"{probability:.2%}"
    )

    if prediction == 1:
        st.error("🔴 Risk Level: High")
    else:
        st.success("🟢 Risk Level: Low")