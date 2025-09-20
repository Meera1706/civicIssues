import streamlit as st
import pandas as pd
from database import init_db, insert_issue, get_issues, update_issue_status

init_db()
st.set_page_config(page_title="Citizen Issue Reporting", layout="wide")
st.title("🛠 Citizen Issue Reporting System")

menu = ["Citizen Web App", "Admin Dashboard", "Worker Dashboard", "Analytics"]
choice = st.sidebar.radio("Select View", menu)

# Example: Citizen Web App
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
