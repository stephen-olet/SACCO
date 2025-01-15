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

    # Delete Member
    st.subheader("Delete Member")
    selected_member_for_deletion = st.selectbox("Select Member to Delete:", [""] + [row[1] for row in c.execute("SELECT member_id FROM members")])
    if selected_member_for_deletion:
        if st.button("Delete Member"):
            c.execute(f"DELETE FROM members WHERE member_id = '{selected_member_for_deletion}'")
            c.execute(f"DELETE FROM savings_deposits WHERE member_id = '{selected_member_for_deletion}'")
            c.execute(f"DELETE FROM loans WHERE member_id = '{selected_member_for_deletion}'")
            c.execute(f"DELETE FROM fees_interests WHERE member_id = '{selected_member_for_deletion}'")
            conn.commit()
            st.success(f"Member {selected_member_for_deletion} deleted successfully.")

    # Member List
    st.subheader("Registered Members")
    c.execute("SELECT * FROM members")
    members = c.fetchall()
    df_
