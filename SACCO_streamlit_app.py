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
        transaction_id TEXT,
        member_id TEXT
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
    ["About", "Member Management", "Savings & Deposits", "Loan Management", "Fees & Interest", "Notifications", "Summary"]
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
        c.execute("INSERT INTO savings_deposits (amount, date, transaction_id, member_id) VALUES (?, ?, ?, ?)",
                  (savings_amount, str(savings_date), transaction_id, member_id_selected))
        conn.commit()
        st.success(f"You have successfully added UGX {savings_amount} to member ID {member_id_selected} savings on {savings_date}. Transaction ID: {transaction_id}.")

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
        st.success(f"Loan Pending Approval for Member {member_id_selected}! Total repayment: UGX {total_repayment:.2f}, Monthly installment: UGX {monthly_installment:.2f}. Application Date: {loan_date}. Transaction ID: {loan_transaction_id}.")

# Summary Page
elif page == "Summary":
    st.header("Summary of All Transactions")

    # Fetch Registered Members
    c.execute("SELECT member_id, member_name FROM members")
    members = c.fetchall()
    member_choices = ["All Members"] + [f"{member[1]} (ID: {member[0]})" for member in members]

    # Member Selection
    selected_member = st.selectbox("Select a Member to View Transactions:", member_choices)

    if selected_member == "All Members":
        # Fetch All Savings & Deposits Transactions
        c.execute("SELECT * FROM savings_deposits")
        savings_data = c.fetchall()
        df_savings = pd.DataFrame(savings_data, columns=["ID", "Amount", "Date", "Transaction ID", "Member ID"])

        # Fetch All Loan Transactions
        c.execute("SELECT * FROM loans")
        loan_data = c.fetchall()
        df_loans = pd.DataFrame(loan_data, columns=["ID", "Loan Amount", "Loan Period", "Total Repayment", "Monthly Installment", "Loan Date", "Transaction ID", "Member ID"])

    else:
        # Extract Member ID from Selection
        selected_member_id = members[member_choices.index(selected_member) - 1][0]

        # Fetch Savings & Deposits for Selected Member
        c.execute("SELECT * FROM savings_deposits WHERE member_id = ?", (selected_member_id,))
        savings_data = c.fetchall()
        df_savings = pd.DataFrame(savings_data, columns=["ID", "Amount", "Date", "Transaction ID", "Member ID"])

         # Fetch Loans for Selected Member
        c.execute("SELECT * FROM loans WHERE member_id = ?", (selected_member_id,))
        loan_data = c.fetchall()
        df_loans = pd.DataFrame(loan_data, columns=["ID", "Loan Amount", "Loan Period", "Total Repayment", 
                                                    "Monthly Installment", "Loan Date", "Transaction ID", "Member ID"])

    # Display Savings Summary
    st.subheader("Savings & Deposits Summary")
    if df_savings.empty:
        st.write("No savings or deposit transactions found.")
    else:
        st.dataframe(df_savings)

    # Display Loan Summary
    st.subheader("Loan Transactions Summary")
    if df_loans.empty:
        st.write("No loan transactions found.")
    else:
        st.dataframe(df_loans)

# Notifications Page
elif page == "Notifications":
    st.header("Notifications")
    st.write("This feature is under development. Notifications will be available in future updates.")

# Fees & Interest Page
elif page == "Fees & Interest":
    st.header("Fees & Interest Calculator")

    # Inputs for Fees & Interest Calculation
    st.subheader("Calculate Interest")
    principal = st.number_input("Enter Principal Amount (UGX):", min_value=0, value=0)
    rate = st.number_input("Enter Annual Interest Rate (%):", min_value=0.0, value=0.0)
    time = st.number_input("Enter Time Period (Years):", min_value=0, value=0)

    if st.button("Calculate Interest"):
        interest = (principal * rate * time) / 100
        c.execute("INSERT INTO fees_interests (principal, rate, time, interest) VALUES (?, ?, ?, ?)",
                  (principal, rate, time, interest))
        conn.commit()
        st.success(f"Calculated Interest: UGX {interest:.2f}")

    # Display Recorded Interest Data
    st.subheader("Interest Records")
    c.execute("SELECT * FROM fees_interests")
    interest_records = c.fetchall()
    if interest_records:
        df_interest = pd.DataFrame(interest_records, columns=["ID", "Principal", "Rate (%)", "Time (Years)", "Interest"])
        st.dataframe(df_interest)
    else:
        st.write("No interest records found.")

# Closing the SQLite connection on app termination
conn.close()
