import streamlit as st
import pandas as pd

st.set_page_config(page_title="Salida Gun Shop | Staff Dashboard", layout="wide")
st.title("🔧 STAFF DASHBOARD")

# Sample messages (replace this with real input system later)
messages = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New", "Assigned": "Unassigned", "Complete": False, "Comment": ""},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "Follow-up", "Assigned": "Unassigned", "Complete": False, "Comment": ""},
    {"Name": "Dave R.", "Category": "General Question", "Message": "What’s your return policy?", "Status": "Resolved", "Assigned": "Unassigned", "Complete": True, "Comment": ""}
]

df = pd.DataFrame(messages)
staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

# Filter logic
needs_attention = df[(df["Status"] != "Resolved") & (~df["Complete"])]
completed_tasks = df[df["Complete"]]

# Needs attention
st.subheader("🔴 NEEDS ATTENTION")
for i in needs_attention.index:
    with st.expander(f"{df.loc[i, 'Name']} — {df.loc[i, 'Category']}"):
        st.write(f"**Message:** {df.loc[i, 'Message']}")
        df.loc[i, "Assigned"] = st.selectbox("Assign to staff", staff_members, index=staff_members.index(df.loc[i, "Assigned"]), key=f"assign_{i}")
        df.loc[i, "Status"] = st.selectbox("Update status", ["New", "Follow-up", "Resolved"], index=["New", "Follow-up", "Resolved"].index(df.loc[i, "Status"]), key=f"status_{i}")
        df.loc[i, "Comment"] = st.text_area("Comment", value=df.loc[i, "Comment"], key=f"comment_{i}")
        df.loc[i, "Complete"] = st.checkbox("Mark Complete", value=df.loc[i, "Complete"], key=f"complete_{i}")

# Completed section
with st.expander("✅ Completed Tasks"):
    st.dataframe(completed_tasks[["Name", "Category", "Message", "Assigned", "Comment"]])
