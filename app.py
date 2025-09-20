import streamlit as st
import pandas as pd
from database import init_db, insert_issue, get_issues, update_issue_status

# Initialize DB
init_db()

st.set_page_config(page_title="Citizen Issue Reporting", layout="wide")
st.title("🛠 Citizen Issue Reporting System")

menu = ["Citizen Web App", "Admin Dashboard", "Worker Dashboard", "Analytics"]
choice = st.sidebar.radio("Select View", menu)

# -------------------------
# Citizen Web App
# -------------------------
if choice == "Citizen Web App":
    st.header("📌 Submit a Report")
    name = st.text_input("Your Name")
    desc = st.text_area("Issue Description")
    photo = st.file_uploader("Upload a Photo", type=["jpg","jpeg","png"])

    if st.button("Submit Report"):
        if name and desc:
            photo_bytes = photo.read() if photo else None
            insert_issue(name, desc, photo_bytes)
            st.success("✅ Report submitted successfully!")
        else:
            st.error("Please enter name and description.")

    st.subheader("🔎 Track Issues")
    issues = get_issues()
    if issues:
        df = pd.DataFrame(issues, columns=["ID", "Citizen", "Description", "Photo", "Status", "Assigned To", "Proof"])
        st.dataframe(df[["ID","Citizen","Description","Status","Assigned To"]])

# -------------------------
# Admin Dashboard
# -------------------------
elif choice == "Admin Dashboard":
    st.header("👩‍💼 Admin Dashboard - Manage Issues")
    issues = get_issues()
    if issues:
        df = pd.DataFrame(issues, columns=["ID","Citizen","Description","Photo","Status","Assigned To","Proof"])
        st.dataframe(df)

        issue_id = st.number_input("Enter Issue ID to Assign", min_value=1, step=1)
        worker = st.text_input("Assign to Worker")
        if st.button("Assign Worker"):
            update_issue_status(issue_id, "Assigned", assigned_to=worker)
            st.success(f"Issue {issue_id} assigned to {worker}")

        verify_id = st.number_input("Enter Issue ID to Verify", min_value=1, step=1, key="verify")
        if st.button("Verify Task"):
            update_issue_status(verify_id, "Verified")
            st.success(f"Issue {verify_id} marked as Verified")

        approve_id = st.number_input("Enter Issue ID to Approve", min_value=1, step=1, key="approve")
        if st.button("Approve Resolution"):
            update_issue_status(approve_id, "Resolved")
            st.success(f"Issue {approve_id} approved as Resolved")

# -------------------------
# Worker Dashboard
# -------------------------
elif choice == "Worker Dashboard":
    st.header("👷 Worker Dashboard - Assigned Tasks")
    issues = get_issues()
    if issues:
        df = pd.DataFrame(issues, columns=["ID","Citizen","Description","Photo","Status","Assigned To","Proof"])
        st.dataframe(df[df["Status"]=="Assigned"])

        issue_id = st.number_input("Enter Issue ID to Update", min_value=1, step=1, key="worker")
        if st.button("Mark In Progress"):
            update_issue_status(issue_id, "In Progress")
            st.success(f"Issue {issue_id} marked as In Progress")

        proof = st.file_uploader("Upload Proof of Work", type=["jpg","jpeg","png"])
        if st.button("Upload Proof"):
            if proof:
                proof_bytes = proof.read()
                update_issue_status(issue_id, "Completed", proof=proof_bytes)
                st.success(f"Proof uploaded for Issue {issue_id}")

# -------------------------
# Analytics
# -------------------------
elif choice == "Analytics":
    st.header("📊 Analytics Dashboard")
    issues = get_issues()
    if issues:
        df = pd.DataFrame(issues, columns=["ID","Citizen","Description","Photo","Status","Assigned To","Proof"])
        st.dataframe(df)

        st.subheader("Status Distribution")
        st.bar_chart(df["Status"].value_counts())
