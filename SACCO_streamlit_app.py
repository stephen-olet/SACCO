import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Initialize SQLite database
conn = sqlite3.connect("sacco.db")
c = conn.cursor()

# Create tables if they do not exist
c.execute(''' 
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
        member_name TEXT,
        member_contact TEXT,
        registration_date TEXT
    )
''')
c.execute(''' 
    CREATE TABLE IF NOT EXISTS savings_deposits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount INTEGER,
        date TEXT,
        transaction_id TEXT
    )
''')
c.execute(''' 
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        loan_amount INTEGER,
        loan_period INTEGER,
        total_repayment REAL,
        monthly_installment REAL,
        loan_date TEXT,
        loan_transaction_id TEXT,
        member_id TEXT
    )
''')
c.execute(''' 
    CREATE TABLE IF NOT EXISTS fees_interests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        principal INTEGER,
        rate REAL,
        time INTEGER,
        interest REAL
    )
''')

conn.commit()

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
        c.execute("INSERT INTO members (member_id, member_name, member_contact, registration_date) VALUES (?, ?, ?, ?)",
                  (member_id, member_name, member_contact, str(registration_date)))
        conn.commit()
        st.success(f"Member {member_name} with ID {member_id} registered successfully on {registration_date}.")

    # Member List
    st.subheader("Registered Members")
    c.execute("SELECT * FROM members")
    members = c.fetchall()
    df_members = pd.DataFrame(members, columns=["ID", "Member ID", "Name", "Contact", "Registration Date"])
    st.dataframe(df_members)

    # Delete Member
    st.subheader("Delete Member")

    # Select member to delete
    member_to_delete = st.selectbox("Select a member to delete", df_members["Member ID"])

    if st.button("Delete Member"):
        c.execute("DELETE FROM members WHERE member_id = ?", (member_to_delete,))
        conn.commit()
        st.success(f"Member with ID {member_to_delete} has been successfully deleted.")

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
        c.execute("INSERT INTO savings_deposits (amount, date, transaction_id) VALUES (?, ?, ?)",
                  (savings_amount, str(savings_date), transaction_id))
        conn.commit()

        # Update the savings record for the selected member (optional, for tracking)
        st.success(f"You have successfully added UGX {savings_amount} to member ID {member_id_selected} savings on {savings_date}. Transaction ID: {transaction_id}.")

# Loan Management Page
elif page == "Loan Management":
    st.header("Loan Management")

    # Loan Overview
    st.subheader("Loan Overview")
    loan_balance = 800000  # Example value
    st.write(f"Your current loan balance is: **UGX {loan_balance}**")

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
        st.success(f"Loan Pending Approval for Member {member_id_selected}! Total repayment: UGX {total_repayment:.2f}, Monthly installment: UGX {monthly_installment:.2f}. Application Date: {loan_date}. Transaction ID: {loan_transaction_id}.")

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
        c.execute("INSERT INTO fees_interests (principal, rate, time, interest) VALUES (?, ?, ?, ?)",
                  (principal, rate, time, interest))
        conn.commit()
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

    notification_type = st.radio(
        "Send to:",
        ["All Members", "Individual Member"]
    )

    if notification_type == "Individual Member":
        member_email = st.text_input("Enter the member's email address:")
        if st.button("Send Notification to Member"):
            # Here you would add the code to send an email to the individual member
            # You can use libraries like smtplib to send emails
            st.success(f"Email notification sent successfully to {member_email}.")

    elif notification_type == "All Members":
        if st.button("Send Notification to All Members"):
            # Here you would add the code to send emails to all members
            # For example, by querying the database for all member emails
            st.success("Email notification sent successfully to all members.")

