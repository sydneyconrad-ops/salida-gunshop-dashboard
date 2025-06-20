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

# Split into sections
needs_attention = df[(df["Status"] != "Resolved") & (~df["Complete"])]
completed_tasks = df[df["Complete"]]

# 🔴 Needs Attention
st.markdown("<h2 style='color:#ff6b6b;'>🚨 NEEDS ATTENTION</h2>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px;'>These messages need review or staff assignment:</p>", unsafe_allow_html=True)

for i in needs_attention.index:
    with st.expander(f"📩 {df.loc[i, 'Name']} — {df.loc[i, 'Category']}"):
        st.markdown(f"**📝 Message:**<br><span style='font-size:18px'>{df.loc[i, 'Message']}</span>", unsafe_allow_html=True)
        df.loc[i, "Assigned"] = st.selectbox("👤 Assign to staff", staff_members, index=staff_members.index(df.loc[i, "Assigned"]), key=f"assign_{i}")
        df.loc[i, "Status"] = st.radio("📌 Update status", ["New", "Follow-up", "Resolved"], index=["New", "Follow-up", "Resolved"].index(df.loc[i, "Status"]), key=f"status_{i}", horizontal=True)
        df.loc[i, "Comment"] = st.text_area("💬 Add Comment", value=df.loc[i, "Comment"], key=f"comment_{i}")
        df.loc[i, "Complete"] = st.checkbox("✅ Mark Complete", value=df.loc[i, "Complete"], key=f"complete_{i}")

# ✅ Completed Tasks
with st.expander("🎉 View Completed Tasks"):
    st.markdown("<h3 style='color:green;'>✅ Completed Messages</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px;'>These have been handled and marked complete.</p>", unsafe_allow_html=True)
    st.dataframe(completed_tasks[["Name", "Category", "Message", "Assigned", "Comment"]], height=300)

# Optional footer
st.markdown("---")
st.markdown("<p style='text-align:center; font-size:14px;'>Built for <strong>Salida Gun Shop</strong> with ❤️</p>", unsafe_allow_html=True)
