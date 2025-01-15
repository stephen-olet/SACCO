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

    # Select member for summary
    selected_member = st.selectbox("Select Member:", [""] + [row[1] for row in c.execute("SELECT member_id FROM members")])

    # Summary of Members
    st.subheader("Member Summary")
    if selected_member:
        c.execute(f"SELECT * FROM members WHERE member_id = '{selected_member}'")
        members = c.fetchall()
        df_members = pd.DataFrame(members, columns=["ID", "Member ID", "Name", "Contact", "Registration Date"])
        st.dataframe(df_members)
    else:
        st.write("Please select a member to view summary.")

    # Summary of Savings & Deposits
    st.subheader("Savings & Deposits Summary")
    if selected_member:
        c.execute(f"SELECT * FROM savings_deposits WHERE member_id = '{selected_member}'")
        savings_deposits = c.fetchall()
        df_savings_deposits = pd.DataFrame(savings_deposits, columns=["ID", "Amount", "Date", "Transaction ID"])
        st.dataframe(df_savings_deposits)
    else:
        st.write("Please select a member to view savings & deposits summary.")

    # Summary of Loans
    st.subheader("Loan Summary")
    if selected_member:
        c.execute(f"SELECT * FROM loans WHERE member_id = '{selected_member}'")
        loans = c.fetchall()
        df_loans = pd.DataFrame(loans, columns=["ID", "Loan Amount", "Loan Period", "Total Repayment", "Monthly Installment", "Loan Date", "Transaction ID"])
        st.dataframe(df_loans)
    else:
        st.write("Please select a member to view loan summary.")
