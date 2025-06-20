import streamlit as st
import pandas as pd
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- SETTINGS ---
spreadsheet_id = "1bD3IXAL3N8njmAxfCz6KHMy9TcFBX0Eh0V3HqLUrfkI"  # Your Sheet ID
sheet_name = "sgs_inventory_sample"

openai.api_key = st.secrets["openai_api_key"]  # Set in Streamlit Secrets

# --- Connect to Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
data = sheet.get_all_records()
inventory_df = pd.DataFrame(data)

# Normalize column headers
inventory_df.columns = [col.strip().lower() for col in inventory_df.columns]

# --- Sample Message Log ---
messages = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New", "Assigned To": "Unassigned", "Comment": "", "Completed": False},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "Follow-up", "Assigned To": "Unassigned", "Comment": "", "Completed": False},
    {"Name": "Dave R.", "Category": "General Question", "Message": "What’s your return policy?", "Status": "Resolved", "Assigned To": "Unassigned", "Comment": "", "Completed": True},
]

df = pd.DataFrame(messages)
staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

st.set_page_config(page_title="Salida Gun Shop | Staff View", layout="centered")

# --- Priority Header ---
st.markdown("## 🔴 NEEDS ATTENTION")

# --- Category Filter ---
selected_category = st.selectbox("📂 Filter by Category", ["All"] + df["Category"].unique().tolist())
filtered_df = df if selected_category == "All" else df[df["Category"] == selected_category]

# --- Class Signup Alert ---
if any((df["Category"] == "Class Signup") & (df["Status"] != "Resolved") & (~df["Completed"])):
    st.markdown("### 🥳 **NEW CLASS SIGNUP ALERT**")

# --- Message Card Renderer ---
st.markdown("### 📨 Incoming Messages")

for i in filtered_df.index:
    if df.loc[i, "Completed"]:
        continue  # Skip completed messages in main view

    with st.expander(f"From: {df.loc[i, 'Name']} | Category: {df.loc[i, 'Category']}"):
        st.markdown(f"**Message:** {df.loc[i, 'Message']}")

        # AI Suggestion
        try:
            prompt = f"A customer asked: {df.loc[i, 'Message']}\nReply politely and helpfully:"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60
            )
            suggestion = response["choices"][0]["message"]["content"]
        except:
            suggestion = "⚠️ Could not generate suggestion."

        st.markdown(f"💡 **AI Suggestion:** {suggestion}")

        # Stock Lookup
        try:
            msg_lower = df.loc[i, "Message"].lower()
            inventory_df["product_lower"] = inventory_df["product"].str.lower()
            match = inventory_df[inventory_df["product_lower"].str.contains(msg_lower)]
            if not match.empty:
                availability = match.iloc[0]["availability"]
                st.success(f"✅ Item in stock: {match.iloc[0]['product']} → {availability}")
            else:
                st.info("🟡 No exact match found in inventory.")
        except Exception as e:
            st.warning("⚠️ Couldn't load stock inventory.")

        # Assignment
        df.loc[i, "Assigned To"] = st.selectbox("Assign to:", staff_members, index=staff_members.index(df.loc[i, "Assigned To"]), key=f"assign_{i}")

        # Status
        df.loc[i, "Status"] = st.selectbox("Status:", ["New", "Follow-up", "Resolved"], index=["New", "Follow-up", "Resolved"].index(df.loc[i, "Status"]), key=f"status_{i}")

        # Comments
        df.loc[i, "Comment"] = st.text_input("Comment:", value=df.loc[i, "Comment"], key=f"comment_{i}")

        # Completion
        df.loc[i, "Completed"] = st.checkbox("✅ Mark as Complete", value=df.loc[i, "Completed"], key=f"complete_{i}")

# --- Completed Messages ---
if any(df["Completed"]):
    st.markdown("### ✅ Completed Tasks")
    for i in df.index:
        if df.loc[i, "Completed"]:
            with st.expander(f"✅ {df.loc[i, 'Name']} | {df.loc[i, 'Category']}"):
                st.markdown(f"**Message:** {df.loc[i, 'Message']}")
                st.markdown(f"**Status:** {df.loc[i, 'Status']}")
                st.markdown(f"**Assigned To:** {df.loc[i, 'Assigned To']}")
                st.markdown(f"**Comment:** {df.loc[i, 'Comment']}")
