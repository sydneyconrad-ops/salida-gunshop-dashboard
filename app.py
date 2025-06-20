import streamlit as st
import pandas as pd
import random

# ---------- FAKE DATA ----------
data = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New", "Assigned To": "Unassigned", "Comment": "", "Done": False},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "Follow-up", "Assigned To": "Unassigned", "Comment": "", "Done": False},
    {"Name": "Dave R.", "Category": "General Question", "Message": "What’s your return policy?", "Status": "Resolved", "Assigned To": "Unassigned", "Comment": "", "Done": False}
]
staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

df = pd.DataFrame(data)

# ---------- STREAMLIT UI SETTINGS ----------
st.set_page_config(page_title="Salida Gun Shop | Staff View", layout="centered")
st.title("🔧 Staff Message Dashboard")

# ---------- CLASS SIGNUP ALERT ----------
if any(df["Category"] == "Class Signup") and any(df["Status"] == "New"):
    st.markdown("<h3 style='color: red;'>🚨 New Class Signup Needs Follow-Up!</h3>", unsafe_allow_html=True)

# ---------- CATEGORY FILTER ----------
categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.selectbox("Filter by Category", categories)
if selected_category != "All":
    df = df[df["Category"] == selected_category]

