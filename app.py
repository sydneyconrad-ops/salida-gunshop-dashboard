import streamlit as st
import pandas as pd
from openai import OpenAI
import re

# 🧠 CONFIG
st.set_page_config("Salida Gun Shop | Staff View", layout="wide")
st.markdown("## 🔴 NEEDS ATTENTION")

# 🧾 Sample incoming messages
messages = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New", "Assigned To": "Unassigned", "Comment": "", "Complete": False},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "Follow-up", "Assigned To": "Unassigned", "Comment": "", "Complete": False},
    {"Name": "Dave R.", "Category": "General Question", "Message": "What’s your return policy?", "Status": "Resolved", "Assigned To": "Unassigned", "Comment": "", "Complete": True},
]

staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

df = pd.DataFrame(messages)

# 📦 INVENTORY LOOKUP
@st.cache_data(ttl=300)
def load_inventory():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTjTuYv6_hPYVcH-Yvtr9jI4SE8g0ZdQX4yluFpmgtnKu0P5T7IJVW5DQaGfPWZsQ/pub?output=csv"
    try:
        return pd.read_csv(url)
    except Exception:
        st.warning("⚠️ Couldn't load stock inventory.")
        return pd.DataFrame(columns=["Product", "Category", "Availability"])

inventory_df = load_inventory()

# 📣 Class Signup Alert
if any((df["Category"] == "Class Signup") & (df["Status"] != "Resolved")):
    st.error("🎓 NEW CLASS SIGNUP ALERT")

# 🔍 Filter by category
selected_category = st.selectbox("📂 Filter by Category", ["All"] + sorted(df["Category"].unique()))
if selected_category != "All":
    df = df[df["Category"] == selected_category]

st.markdown("### 📬 Incoming Messages")

# ✅ Helper: Inventory check
def check_inventory(message):
    for product in inventory_df["Product"]:
        if product.lower() in message.lower():
            availability = inventory_df[inventory_df["Product"] == product]["Availability"].values[0]
            return f"✅ Yes, we usually have those in stock. Can I confirm your pickup time?" if availability == "In Stock" else f"ℹ️ Item found: {availability}"
    return "💡 Suggestion: Thanks for your message! Let me check on that and get back to you."

# 🔁 Main Message Loop
for i in df.index:
    if df.at[i, "Complete"]:
        continue

    with st.expander(f"**From:** {df.at[i, 'Name']} | **Category:** {df.at[i, 'Category']}"):
        st.write(f"**Message:** {df.at[i, 'Message']}")
        
        suggestion = check_inventory(df.at[i, "Message"])
        st.info(f"💡 AI Suggestion: {suggestion}")
        
        df.at[i, "Assigned To"] = st.selectbox("Assign to:", staff_members, index=staff_members.index(df.at[i, "Assigned To"]), key=f"assign_{i}")
        df.at[i, "Status"] = st.selectbox("Status:", ["New", "Follow-up", "Resolved"], index=["New", "Follow-up", "Resolved"].index(df.at[i, "Status"]), key=f"status_{i}")
        df.at[i, "Comment"] = st.text_input("Comment:", value=df.at[i, "Comment"], key=f"comment_{i}")
        df.at[i, "Complete"] = st.checkbox("✅ Mark as Complete", value=df.at[i, "Complete"], key=f"complete_{i}")

# 🧾 Completed section
with st.expander("✅ Completed Messages"):
    st.dataframe(df[df["Complete"] == True][["Name", "Category", "Message", "Status", "Assigned To", "Comment"]], use_container_width=True)

# 🧃 Still active
with st.expander("📋 Updated Statuses"):
    st.dataframe(df[df["Complete"] == False][["Name", "Category", "Message", "Status", "Assigned To"]], use_container_width=True)
