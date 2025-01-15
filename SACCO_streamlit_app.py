import streamlit as st
import pandas as pd
import numpy as np

# App Title
st.title("INACAN SACCO App")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Overview", "Savings & Deposits", "Loan Management", "Fees & Interest", "About"]
)

# Overview Page
if page == "Overview":
    st.header("INACAN SACCO App")
    st.write("Welcome to the INACAN SACCO App. Track your savings, deposits, loans, and fees.")

    # Example Summary Data
    summary = {
        "Category": ["Savings", "Deposits", "Loans", "Interest Earned", "Fees Paid"],
        "Amount (UGX)": [500000, 200000, 800000, 25000, 10000]
    }
    df_summary = pd.DataFrame(summary)

    st.subheader("Summary Table")
    st.dataframe(df_summary)

    # Pie Chart for Distribution
    st.subheader("Financial Distribution")
    st.write("Visualize how your funds are distributed.")
    pie_data = df_summary.set_index("Category")
    st.write(pie_data.plot.pie(y="Amount (UGX)", autopct="%1.1f%%", figsize=(5, 5)))
    st.pyplot()

# Savings & Deposits Page
elif page == "Savings & Deposits":
    st.header("Savings & Deposits")

    # User Input for Savings
    st.subheader("Add to Savings")
    savings_amount = st.number_input("Enter amount to add to savings:", min_value=0, value=0)
    if st.button("Update Savings"):
        st.success(f"You have successfully added UGX {savings_amount} to your savings.")

    # User Input for Deposits
    st.subheader("Add a Deposit")
    deposit_amount = st.number_input("Enter deposit amount:", min_value=0, value=0)
    if st.button("Update Deposits"):
        st.success(f"You have successfully added UGX {deposit_amount} as a deposit.")

# Loan Management Page
elif page == "Loan Management":
    st.header("Loan Management")

    # Current Loan Balance
    st.subheader("Loan Overview")
    loan_balance = 800000  # Example value
    st.write(f"Your current loan balance is: **UGX {loan_balance}**")

    # Loan Application
    st.subheader("Apply for a Loan")
    loan_amount = st.number_input("Enter loan amount:", min_value=0, value=0)
    loan_period = st.selectbox("Choose loan repayment period (months):", [6, 12, 24, 36])
    interest_rate = 0.1  # Example interest rate of 10%

    if st.button("Submit Loan Application"):
        total_repayment = loan_amount * (1 + interest_rate)
        monthly_installment = total_repayment / loan_period
        st.success(f"Loan Approved! Total repayment: UGX {total_repayment:.2f}, Monthly installment: UGX {monthly_installment:.2f}.")

# Fees & Interest Page
elif page == "Fees & Interest":
    st.header("Fees & Interest")

    # Interest Calculation
    st.subheader("Calculate Interest")
    principal = st.number_input("Enter the principal amount:", min_value=0, value=0)
    rate = st.number_input("Enter the annual interest rate (%):", min_value=0.0, value=10.0) / 100
    time = st.number_input("Enter time (in years):", min_value=1, value=1)

    if st.button("Calculate Interest"):
        interest = principal * rate * time
        st.write(f"The interest for UGX {principal} at {rate*100:.2f}% for {time} years is UGX {interest:.2f}.")

    # Fees Overview
    st.subheader("Fees Overview")
    fee_details = {
        "Fee Type": ["Loan Processing Fee", "Late Payment Penalty", "Account Maintenance Fee"],
        "Amount (UGX)": [20000, 5000, 10000]
    }
    df_fees = pd.DataFrame(fee_details)
    st.dataframe(df_fees)

# About Page
elif page == "About":
    st.header("About This App")
    st.write(
        """
        The SACCO Loan Management App helps members track their financial activity, including savings, 
        deposits, loans, interest, and fees. It is designed to provide transparency and ease of use.
        """
    )
    st.info("Developed by Stephen Olet.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit.")
