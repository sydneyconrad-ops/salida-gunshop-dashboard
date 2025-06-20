import streamlit as st
import pandas as pd

# Sample message log
data = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New"},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "Follow-up"},
    {"Name": "Dave R.", "Category": "General Question", "Message": "What’s your return policy?", "Status": "Resolved"}
]

df = pd.DataFrame(data)

st.set_page_config(page_title="Salida Gun Shop | Staff View", layout="centered")
st.title("🔧 Staff Message Dashboard")

for i in df.index:
    st.write(f"**From:** {df.loc[i, 'Name']} | **Category:** {df.loc[i, 'Category']}")
    st.write(f"**Message:** {df.loc[i, 'Message']}")
    df.loc[i, 'Status'] = st.selectbox(
        f"Update Status for {df.loc[i, 'Name']}",
        options=["New", "Follow-up", "Resolved"],
        index=["New", "Follow-up", "Resolved"].index(df.loc[i, 'Status']),
        key=f"dropdown_{i}"
    )
    st.markdown("---")

st.subheader("📋 Updated Statuses")
st.dataframe(df)
