import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Salida Gun Shop | Staff Dashboard", layout="wide")

# Title Section
st.markdown("""
    <h1 style='color:#e63946; font-size: 48px;'>🔧 STAFF DASHBOARD</h1>
    <hr style='border: 2px solid #e63946;'>
""", unsafe_allow_html=True)

# Fake message data
messages = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New", "Assigned": "Unassigned", "Complete": False, "Comment": ""},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "Follow-up", "Assigned": "Unassigned", "Complete": False, "Comment": ""},
    {"Name": "Dave R.", "Category": "General Question", "Message": "What’s your return policy?", "Status": "Resolved", "Assigned": "Unassigned", "Complete": True, "Comment": ""}
]

df = pd.DataFrame(messages)
staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

# Split into sectio
