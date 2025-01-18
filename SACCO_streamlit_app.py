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
        member_id TEXT UNIQUE,
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
        transaction_id TEXT UNIQUE,
        member_id TEXT,
        FOREIGN KEY (member_id) REFERENCES members (member_id)
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
        loan_transaction_id TEXT UNIQUE,
        member_id TEXT,
        FOREIGN KEY (member_id) REFERENCES members (member_id)
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
    member_id = st.text_input("Enter Member ID:").strip()
    member_name = st.text_input("Enter Member Name:").strip()
    member_contact = st.text_input("Enter Contact Information:").strip()
    registration_date = st.date_input("Select Registration Date:", datetime.now().date())

    if st.button("Register Member"):
        if member_id and member_name and member_contact:
            try:
                c.execute(
                    "INSERT INTO members (member_id, member_name, member_contact, registration_date) VALUES (?, ?, ?, ?)",
                    (member_id, member_name, member_contact, str(registration_date))
                )
                conn.commit()
                st.success(f"Member {member_name} with ID {member_id} registered successfully on {registration_date}.")
            except sqlite3.IntegrityError:
                st.error("Member ID must be unique. Please use a different Member ID.")
        else:
            st.error("Please fill in all fields.")

    # Member List
    st.subheader("Registered Members")
    c.execute("SELECT * FROM members")
    members = c.fetchall()
    if members:
        df_members = pd.DataFrame(members, columns=["ID", "Member ID", "Name", "Contact", "Registration Date"])
        st.dataframe(df_members)

        # Delete Member
        st.subheader("Delete Member")
        member_to_delete = st.selectbox("Select a member to delete", df_members["Member ID"])

        if st.button("Delete Member"):
            c.execute("DELETE FROM members WHERE member_id = ?", (member_to_delete,))
            conn.commit()
            st.success(f"Member with ID {member_to_delete} has been successfully deleted.")
    else:
        st.write("No members found.")

# Savings & Deposits Page
elif page == "Savings & Deposits":
    st.header("Savings & Deposits")

    # Select Member
    st.subheader("Select Member to Update Savings")
    c.execute("SELECT member_id, member_name FROM members")
    members = c.fetchall()
    if members:
        member_choices = [f"{member[1]} (ID: {member[0]})" for member in members]
        member_selected = st.selectbox("Select a Member", member_choices)

        # Extract member_id from selected member
        member_id_selected = members[member_choices.index(member_selected)][0]

        # User Input for Savings
        st.subheader("Add to Savings")
        savings_amount = st.number_input("Enter amount to add to savings:", min_value=0, value=0)
        savings_date = st.date_input("Select date of transaction:", datetime.now().date())
        transaction_id = st.text_input("Enter transaction ID:").strip()

        if st.button("Update Savings"):
            if transaction_id:
                try:
                    c.execute(
                        "INSERT INTO savings_deposits (amount, date, transaction_id, member_id) VALUES (?, ?, ?, ?)",
                        (savings_amount, str(savings_date), transaction_id, member_id_selected)
                    )
                    conn.commit()
                    st.success(f"UGX {savings_amount} added to member ID {member_id_selected}'s savings on {savings_date}. Transaction ID: {transaction_id}.")
                except sqlite3.IntegrityError:
                    st.error("Transaction ID must be unique. Please use a different Transaction ID.")
            else:
                st.error("Please provide a Transaction ID.")
    else:
        st.write("No members found. Please register members first.")

# The remaining sections (Loan Management, Fees & Interest, Notifications, Summary) follow similar logic for handling inputs, validations, and database interactions.

# Closing the SQLite connection on app termination
conn.close()
