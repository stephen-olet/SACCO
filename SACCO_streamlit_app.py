import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import datetime
import os

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
# Backup transactions table
c.execute('''
    CREATE TABLE IF NOT EXISTS transactions_backup (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_type TEXT,
        data TEXT,
        timestamp TEXT
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

# Function to backup data to a JSON file
def backup_to_json(data, file_name):
    """Backup the data to a JSON file."""
    if not os.path.exists("backup"):
        os.makedirs("backup")
    
    file_path = os.path.join("backup", file_name)
    
    with open(file_path, "a") as json_file:
        json.dump(data, json_file)
        json_file.write("\n")  # Write each transaction on a new line

    st.success(f"Backup successful: {file_name} stored locally in 'backup' folder.")

# Function to backup data to SQLite transactions table
def backup_to_db(transaction_type, data):
    """Backup transaction data to the transactions_backup table."""
    timestamp = str(datetime.now())
    c.execute("INSERT INTO transactions_backup (transaction_type, data, timestamp) VALUES (?, ?, ?)",
              (transaction_type, json.dumps(data), timestamp))
    conn.commit()
    st.success(f"Backup successful: Transaction data stored in SQLite database.")

# Member Management Page (already covered previously)

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

        # Prepare transaction data for backup
        transaction_data = {
            "transaction_type": "Savings Deposit",
            "amount": savings_amount,
            "date": str(savings_date),
            "transaction_id": transaction_id,
            "member_id": member_id_selected
        }

        # Backup to JSON file
        file_name = f"savings_deposit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_to_json(transaction_data, file_name)

        # Backup to SQLite database
        backup_to_db("Savings Deposit", transaction_data)

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

        # Prepare loan data for backup
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

        # Backup to JSON file
        file_name = f"loan_application_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_to_json(loan_data, file_name)

        # Backup to SQLite database
        backup_to_db("Loan Application", loan_data)

        st.success(f"Loan Application Pending for Member ID {member_id_selected}. Total repayment: UGX {total_repayment:.2f}, Monthly installment: UGX {monthly_installment:.2f}. Application Date: {loan_date}.")

# Summary Page
elif page == "Summary":
    st.header("Summary of All Transactions")

    # Fetch and display savings and loans transaction summary
    c.execute("SELECT * FROM savings_deposits")
    savings_data = c.fetchall()
    c.execute("SELECT * FROM loans")
    loan_data = c.fetchall()

    # Combine both savings and loan data for the summary
    savings_df = pd.DataFrame(savings_data, columns=["ID", "Amount", "Date", "Transaction ID", "Member ID"])
    loan_df = pd.DataFrame(loan_data, columns=["ID", "Loan Amount", "Loan Period", "Total Repayment", "Monthly Installment", "Loan Date", "Loan Transaction ID", "Member ID"])

    st.subheader("Savings & Deposits Summary")
    st.dataframe(savings_df)

    st.subheader("Loan Applications Summary")
    st.dataframe(loan_df)

    st.subheader("Backup History")
    c.execute("SELECT * FROM transactions_backup")
    backup_data = c.fetchall()
    backup_df = pd.DataFrame(backup_data, columns=["ID", "Transaction Type", "Data", "Timestamp"])
    st.dataframe(backup_df)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit.")
