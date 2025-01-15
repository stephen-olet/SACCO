import streamlit as st
import pandas as pd
import sqlite3
import json
from google.cloud import storage
import os
from datetime import datetime

# Initialize SQLite database
conn = sqlite3.connect("sacco.db")
c = conn.cursor()

# Create tables if they do not exist (already covered previously)
# Create tables code here...

# Set Google Cloud Storage credentials (Make sure GOOGLE_APPLICATION_CREDENTIALS is set)
# For example, use os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account_file.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account_key.json"

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

# Define the Google Cloud bucket name
BUCKET_NAME = "your-cloud-bucket-name"
bucket = storage_client.get_bucket(BUCKET_NAME)

# Function to backup transaction data to Google Cloud Storage
def backup_to_cloud(data, file_name):
    """Back up the data to Google Cloud Storage"""
    # Convert data to JSON format
    json_data = json.dumps(data)
    
    # Create a blob object (file) in the cloud storage bucket
    blob = bucket.blob(file_name)
    
    # Upload data to Google Cloud Storage
    blob.upload_from_string(json_data, content_type="application/json")
    
    st.success(f"Backup successful: {file_name} uploaded to Google Cloud Storage!")

# App Title
st.title("INACAN SACCO App")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["About", "Member Management", "Savings & Deposits", "Loan Management", "Fees & Interest", "Notifications", "Summary"]
)

# Add new member functionality (already covered previously)

# Savings & Deposits Page
elif page == "Savings & Deposits":
    st.header("Savings & Deposits")

    # Select Member
    st.subheader("Select Member to Update Savings")
    c.execute("SELECT member_id, member_name FROM members")
    members = c.fetchall()
    member_choices = [f"{member[1]} (ID: {member[0]})" for member in members]
    member_selected = st.selectbox("Select a Member", member_choices)

    # Extract member_id from selected member
    member_id_selected = members[member_choices.index(member_selected)][0]

    # User Input for Savings
    st.subheader("Add to Savings")
    savings_amount = st.number_input("Enter amount to add to savings:", min_value=0, value=0)
    savings_date = st.date_input("Select date of transaction:", datetime.now().date())
    transaction_id = st.text_input("Enter transaction ID:")
    
    if st.button("Update Savings"):
        c.execute("INSERT INTO savings_deposits (amount, date, transaction_id, member_id) VALUES (?, ?, ?, ?)",
                  (savings_amount, str(savings_date), transaction_id, member_id_selected))
        conn.commit()

        # Prepare data for backup
        transaction_data = {
            "transaction_type": "Savings Deposit",
            "amount": savings_amount,
            "date": str(savings_date),
            "transaction_id": transaction_id,
            "member_id": member_id_selected
        }

        # Create a unique file name using the current timestamp
        file_name = f"savings_deposit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Backup to Google Cloud Storage
        backup_to_cloud(transaction_data, file_name)

        st.success(f"You have successfully added UGX {savings_amount} to member ID {member_id_selected} savings.")

# Loan Management Page
elif page == "Loan Management":
    st.header("Loan Management")

    # Select Member
    st.subheader("Select Member to Apply for Loan")
    c.execute("SELECT member_id, member_name FROM members")
    members = c.fetchall()
    member_choices = [f"{member[1]} (ID: {member[0]})" for member in members]
    member_selected = st.selectbox("Select a Member", member_choices)

    # Extract member_id from selected member
    member_id_selected = members[member_choices.index(member_selected)][0]

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
        c.execute("INSERT INTO loans (loan_amount, loan_period, total_repayment, monthly_installment, loan_date, loan_transaction_id, member_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (loan_amount, loan_period, total_repayment, monthly_installment, str(loan_date), loan_transaction_id, member_id_selected))
        conn.commit()

        # Prepare loan transaction data for backup
        loan_data = {
            "transaction_type": "Loan Application",
            "loan_amount": loan_amount,
            "loan_period": loan_period,
            "total_repayment": total_repayment,
            "monthly_installment": monthly_installment,
            "loan_date": str(loan_date),
            "loan_transaction_id": loan_transaction_id,
            "member_id": member_id_selected
        }

        # Create a unique file name for loan data backup
        file_name = f"loan_application_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Backup to Google Cloud Storage
        backup_to_cloud(loan_data, file_name)

        st.success(f"Loan Application Pending for Member ID {member_id_selected}. Total repayment: UGX {total_repayment:.2f}, Monthly installment: UGX {monthly_installment:.2f}. Application Date: {loan_date}.")

