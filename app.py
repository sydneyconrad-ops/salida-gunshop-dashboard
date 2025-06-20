import streamlit as st
import pandas as pd
import random

# --------- Sample Fake Data ---------
data = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New", "Assigned": "Unassigned", "Comment": ""},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "Follow-up", "Assigned": "Unassigned", "Comment": ""},
    {"Name": "Dave R.", "Category": "General Question", "Message": "What’s your return policy?", "Status": "Resolved", "Assigned": "Unassigned", "Comment": ""}
]

staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

df = pd.DataFrame(data)

# --------- Sort Messages by Status Priority ---------
status_priority = {"New": 0, "Follow-up": 1, "Resolved": 2}
df["Priority"] = df["Status"].map(status_priority)
df = df.sort_values(by="Priority")

# --------- Sidebar Filters ---------
st.set_page_config(page_title="Salida Gun Shop | Staff View", layout="wide")
st.title("🔧 STAFF DASHBOARD - Salida Gun Shop")

st.sidebar.header("📂 Filter Messages")
categories = ["All"] + sorted(df["Category"].unique())
selected_category = st.sidebar.selectbox("View by Category", categories)

if selected_category != "All":
    df = df[df["Category"] == selected_category]

# --------- NEEDS ATTENTION Banner ---------
if any(df["Status"].isin(["New", "Follow-up"])):
    st.markdown("### 🚨 **NEEDS ATTENTION:** You have unresolved messages!")

# --------- Visual Counters ---------
col1, col2, col3 = st.columns(3)
col1.metric("🆕 New", sum(df["Status"] == "New"))
col2.metric("📍 Follow-up", sum(df["Status"] == "Follow-up"))
col3.metric("✅ Resolved", sum(df["Status"] == "Resolved"))

st.markdown("---")

# --------- AI Reply Suggestion Function ---------
def get_ai_reply(message):
    suggestions = [
        "Thanks for reaching out! We’ll check inventory and get back to you ASAP.",
        "Yes! We have upcoming classes—I'll send you the details shortly.",
        "Great question! Let me get you that info.",
        "Thanks for the message—we're checking now and will follow up soon."
    ]
    return random.choice(suggestions)

# --------- Message Loop ---------
for i, row in df.iterrows():
    st.markdown(f"#### 📨 From: **{row['Name']}** | Category: _{row['Category']}_")
    st.markdown(f"**Message:** {row['Message']}")

    df.at[i, "Status"] = st.selectbox(
        "Update Status",
        ["New", "Follow-up", "Resolved"],
        index=["New", "Follow-up", "Resolved"].index(row["Status"]),
        key=f"status_{i}"
    )

    df.at[i, "Assigned"] = st.selectbox(
        "Assign to Staff",
        staff_members,
        index=staff_members.index(row["Assigned"]),
        key=f"assign_{i}"
    )

    df.at[i, "Comment"] = st.text_input(
        "Comment / Internal Notes",
        value=row["Comment"],
        key=f"comment_{i}"
    )

    st.markdown("**💬 Suggested Reply:**")
    st.code(get_ai_reply(row["Message"]), language="markdown")

    st.markdown("---")

# --------- Final Table ---------
st.subheader("📋 Summary Table (Internal)")
st.dataframe(df.drop(columns=["Priority"]))
