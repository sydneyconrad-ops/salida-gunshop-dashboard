import streamlit as st
import pandas as pd

# -------------------------------
# Fake Data Setup
# -------------------------------
data = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New", "Assigned To": "Unassigned"},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "Follow-up", "Assigned To": "Unassigned"},
    {"Name": "Dave R.", "Category": "General Question", "Message": "What’s your return policy?", "Status": "Resolved", "Assigned To": "Unassigned"}
]

staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

df = pd.DataFrame(data)

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Salida Gun Shop | Staff View", layout="centered")
st.title("🔧 Staff Message Dashboard")

# -------------------------------
# Message Filter by Category
# -------------------------------
all_categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.selectbox("📂 Filter by Category", options=all_categories)

if selected_category != "All":
    filtered_df = df[df["Category"] == selected_category].reset_index(drop=True)
else:
    filtered_df = df.copy()

# -------------------------------
# Visual Counters
# -------------------------------
new_count = (filtered_df["Status"] == "New").sum()
follow_up_count = (filtered_df["Status"] == "Follow-up").sum()
resolved_count = (filtered_df["Status"] == "Resolved").sum()

st.markdown(f"✅ **New:** {
