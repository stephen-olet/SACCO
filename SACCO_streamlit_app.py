# Loan Management Page
elif page == "Loan Management":
    st.header("Loan Management")

    # Select a member from the list of registered members
    c.execute("SELECT * FROM members")
    members = c.fetchall()
    member_options = [f"{member[1]} - {member[2]}" for member in members]
    selected_member = st.selectbox("Select Member to Update Loan Details", member_options)

    if selected_member:
        member_id = selected_member.split(" - ")[0]  # Extracting member ID

        # Loan Overview
        st.subheader(f"Loan Overview for {selected_member.split(' - ')[1]}")

        # Display member's loan details
        c.execute("SELECT * FROM loans WHERE member_id = ?", (member_id,))
        loans = c.fetchall()

        if loans:
            loan_data = loans[0]  # Assuming one loan per member for simplicity
            loan_amount = loan_data[1]
            loan_period = loan_data[2]
            total_repayment = loan_data[3]
            monthly_installment = loan_data[4]
            loan_date = loan_data[5]
            loan_transaction_id = loan_data[6]
            st.write(f"Loan Amount: UGX {loan_amount}")
            st.write(f"Repayment Period: {loan_period} months")
            st.write(f"Total Repayment: UGX {total_repayment}")
            st.write(f"Monthly Installment: UGX {monthly_installment}")
            st.write(f"Loan Application Date: {loan_date}")
            st.write(f"Loan Transaction ID: {loan_transaction_id}")
        else:
            st.warning("No loan data found for this member.")

        # Loan Application (Update Existing Loan)
        st.subheader("Update Loan Application")
        loan_amount_input = st.number_input("Enter new loan amount:", min_value=0, value=loan_amount)
        loan_period_input = st.selectbox("Choose new loan repayment period (months):", [6, 12, 24, 36], index=[6, 12, 24, 36].index(loan_period))
        interest_rate = 0.1  # Example interest rate of 10%
        total_repayment_input = loan_amount_input * (1 + interest_rate)
        monthly_installment_input = total_repayment_input / loan_period_input
        loan_date_input = st.date_input("Select loan application date:", datetime.now().date())
        loan_transaction_id_input = st.text_input("Enter loan transaction ID:", value=loan_transaction_id)

        if st.button("Update Loan"):
            c.execute("""
                UPDATE loans 
                SET loan_amount = ?, loan_period = ?, total_repayment = ?, monthly_installment = ?, loan_date = ?, loan_transaction_id = ? 
                WHERE member_id = ?""",
                      (loan_amount_input, loan_period_input, total_repayment_input, monthly_installment_input, str(loan_date_input), loan_transaction_id_input, member_id))
            conn.commit()
            st.success(f"Loan details updated successfully for {selected_member.split(' - ')[1]}.")

        # Loan Repayment Tracking (Placeholder Example)
        st.subheader("Repayment History")
        repayment_data = {
            "Date": ["2025-01-01", "2025-02-01"],
            "Amount Paid (UGX)": [50000, 50000],
            "Transaction ID": ["TXN001", "TXN002"]
        }
        df_repayments = pd.DataFrame(repayment_data)
        st.dataframe(df_repayments)
