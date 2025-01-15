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
        member_id TEXT,
        amount INTEGER,
        date TEXT,
        transaction_id TEXT
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
        loan_amount INTEGER,
        loan_period INTEGER,
        total_repayment REAL,
        monthly_installment REAL,
        loan_date TEXT,
        loan_transaction_id TEXT
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS fees_interests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
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
    ["About", "Summary", "Member Management", "Savings & Deposits", "Loan Management", "Fees & Interest", "Notifications"]
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

# Summary Page
elif page == "Summary":
    st.header("Summary")

    summary_option = st.radio("View summary for:", ["All Members", "Individual Member"])
    
    if summary_option == "Individual Member":
        member_id = st.text_input("Enter Member ID:")
    
    if summary_option == "All Members" or (summary_option == "Individual Member" and member_id):
        # Summary of Members
        st.subheader("Member Summary")
        if summary_option == "All Members":
            c.execute("SELECT * FROM members")
        else:
            c.execute("SELECT * FROM members WHERE member_id=?", (member_id,))
        members = c.fetchall()
        df_members = pd.DataFrame(members, columns=["ID", "Member ID", "Name", "Contact", "Registration Date"])
        st.dataframe(df_members)
        
        # Summary of Savings & Deposits
        st.subheader("Savings & Deposits Summary")
        if summary_option == "All Members":
            c.execute("SELECT * FROM savings_deposits")
        else:
            c.execute("SELECT * FROM savings_deposits WHERE member_id=?", (member_id,))
        savings_deposits = c.fetchall()
        df_savings_deposits = pd.DataFrame(savings_deposits, columns=["ID", "Member ID", "Amount", "Date", "Transaction ID"])
        st.dataframe(df_savings_deposits)
        
        # Summary of Loans
        st.subheader("Loan Summary")
        if summary_option == "All Members":
            c.execute("SELECT * FROM loans")
        else:
            c.execute("SELECT * FROM loans WHERE member_id=?", (member_id,))
        loans = c.fetchall()
        df_loans = pd.DataFrame(loans, columns=["ID", "Member ID", "Loan Amount", "Loan Period", "Total Repayment", "Monthly Installment", "Loan Date", "Transaction ID"])
        st.dataframe(df_loans)
        
        # Summary of Fees & Interests
        st.subheader("Fees & Interests Summary")
        if summary_option == "All Members":
            c.execute("SELECT * FROM fees_interests")
        else:
            c.execute("SELECT * FROM fees_interests WHERE member_id=?", (member_id,))
        fees_interests = c.fetchall()
        df_fees_interests = pd.DataFrame(fees_interests, columns=["ID", "Member ID", "Principal", "Rate", "Time", "Interest"])
        st.dataframe(df_fees_interests)

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

# Savings & Deposits Page
elif page == "Savings & Deposits":
    st.header("Savings & Deposits")

    view_option = st.radio("View for:", ["All Members", "Individual Member"])
    
    if view_option == "Individual Member":
        member_id = st.text_input("Enter Member ID:")
    
    # User Input for Savings
    st.subheader("Add to Savings")
    savings_amount = st.number_input("Enter amount to add to savings:", min_value=0, value=0)
    savings_date = st.date_input("Select date of transaction:", datetime.now().date())
    transaction_id = st.text_input("Enter transaction ID:")
    if st.button("Update Savings"):
        c.execute("INSERT INTO savings_deposits (member_id, amount, date, transaction_id) VALUES (?, ?, ?, ?)",
                  (member_id, savings_amount, str(savings_date), transaction_id))
        conn.commit()
        st.success(f"You have successfully added UGX {savings_amount} to your savings on {savings_date}. Transaction ID: {transaction_id}.")

    # User Input for Deposits
    st.subheader("Add a Deposit")
    deposit_amount = st.number_input("Enter deposit amount:", min_value=0, value=0)
    deposit_date = st.date_input("Select date of deposit:", datetime.now().date())
    deposit_transaction_id = st.text_input("Enter deposit transaction ID:")
    if st.button("Update Deposits"):
        c.execute("INSERT INTO savings_deposits (member_id, amount, date, transaction_id) VALUES (?, ?, ?, ?)",
                  (member_id, deposit_amount, str(deposit_date), deposit_transaction_id))
        conn.commit()
        st.success(f"You have successfully added UGX {deposit_amount} as a deposit on {deposit_date}. Transaction ID: {deposit_transaction_id}.")

    if view_option == "All Members" or (view_option == "Individual Member" and member_id):
        # Savings & Deposits Summary
        st.subheader("Savings & Deposits Summary")
        if view_option == "All Members":
            c.execute("SELECT * FROM savings_deposits")
        else:
            c.execute("SELECT * FROM savings_deposits WHERE member_id=?", (member_id,))
        savings_deposits = c.fetchall()
        df_savings_deposits = pd.DataFrame(savings_deposits, columns=["ID", "Member ID", "Amount", "Date", "Transaction ID"])
        st.dataframe(df_savings_deposits)

# Loan Management Page
elif page == "Loan Management":
    st.header("Loan Management")

    view_option = st.radio("View for:", ["All Members", "Individual Member"])
    
    if view_option == "Individual Member":
        member_id = st.text_input("Enter Member ID:")

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
        c.execute("INSERT INTO loans (member_id, loan_amount, loan_period, total_repayment, monthly_installment, loan_date, loan_transaction_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (member_id, loan_amount, loan_period, total_repayment, monthly_installment, str(loan_date), loan_transaction_id))
        conn.commit()
        st.success(f"Loan Pending Approval! Total repayment: UG
