import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# App Title
st.title("INACAN SACCO App")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["About", "Member Management", "Savings & Deposits", "Loan Management", "Fees & Interest", "Notifications"]
)

# About Page
if page == "About":
    st.header("About This App")
    st.write(
        """
        The SACCO Loan Management App helps members track their financial activity, including savings, 
        deposits, loans, interest, and fees. It is designed to provide transparency and ease of use.
        """
    )
    st.info("Developed by Stephen Olet.")

# Member Management Page
elif page == "Member Management":
    st.header("Member Management")

    # Add New Member
    st.subheader("Add New Member")
    member_id = st.text_input("Enter Member ID:")
    member_name = st.text_input("Enter Member Name:")
    member_contact = st.text_input("Enter Contact Information:")
    registration_date = st.date_input("Select Registration Date:", datetime.now().date())

    if st.button("Register Member"):
        st.success(f"Member {member_name} with ID {member_id} registered successfully on {registration_date}.")

    # Member List (Placeholder Example)
    st.subheader("Registered Members")
    member_data = {
        "Member ID": [],
        "Name": [],
        "Contact": [],
        "Registration Date": []
    }
    df_members = pd.DataFrame(member_data)
    st.dataframe(df_members)

# Savings & Deposits Page
elif page == "Savings & Deposits":
    st.header("Savings & Deposits")

    # User Input for Savings
    st.subheader("Add to Savings")
    savings_amount = st.number_input("Enter amount to add to savings:", min_value=0, value=0)
    savings_date = st.date_input("Select date of transaction:", datetime.now().date())
    transaction_id = st.text_input("Enter transaction ID:")
    if st.button("Update Savings"):
        st.success(f"You have successfully added UGX {savings_amount} to your savings on {savings_date}. Transaction ID: {transaction_id}.")

    # User Input for Deposits
    st.subheader("Add a Deposit")
    deposit_amount = st.number_input("Enter deposit amount:", min_value=0, value=0)
    deposit_date = st.date_input("Select date of deposit:", datetime.now().date())
    deposit_transaction_id = st.text_input("Enter deposit transaction ID:")
    if st.button("Update Deposits"):
        st.success(f"You have successfully added UGX {deposit_amount} as a deposit on {deposit_date}. Transaction ID: {deposit_transaction_id}.")

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
    loan_date = st.date_input("Select loan application date:", datetime.now().date())
    loan_transaction_id = st.text_input("Enter loan transaction ID:")

    if st.button("Submit Loan Application"):
        total_repayment = loan_amount * (1 + interest_rate)
        monthly_installment = total_repayment / loan_period
        st.success(f"Loan Pending Approval! Total repayment: UGX {total_repayment:.2f}, Monthly installment: UGX {monthly_installment:.2f}. Application Date: {loan_date}. Transaction ID: {loan_transaction_id}.")

    # Loan Repayment Tracking (Placeholder Example)
    st.subheader("Repayment History")
    repayment_data = {
        "Date": ["2025-01-01", "2025-02-01"],
        "Amount Paid (UGX)": [50000, 50000],
        "Transaction ID": ["TXN001", "TXN002"]
    }
    df_repayments = pd.DataFrame(repayment_data)
    st.dataframe(df_repayments)

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

# Notifications Page
elif page == "Notifications":
    st.header("Notifications")

    # Send Email Notifications
    st.subheader("Send Email Notification to Members")
    notification_message = st.text_area("Enter your message:")

    if st.button("Send Notification"):
        st.success("Email notification sent successfully.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit.")
