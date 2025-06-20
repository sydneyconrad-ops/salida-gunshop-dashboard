import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---- GOOGLE SHEETS AUTH ----
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("vivid-talent-438714-s8-e09e9578ac83.json", scope)
client = gspread.authorize(credentials)

# ---- CONFIG ----
st.set_page_config(page_title="Salida Gun Shop | Dashboard", layout="wide")
st.title("🔧 Salida Gun Shop — Task Dashboard")

sheet_url = "https://docs.google.com/spreadsheets/d/1bD3IXAL3N8njmAxfCz6KHMy9TcFBX0Eh0V3HqLUrfkI/edit#gid=0"
stock_sheet = client.open_by_url(sheet_url).sheet1
stock_data = stock_sheet.get_all_records()
stock_df = pd.DataFrame(stock_data)

# ---- SAMPLE DATA ----
data = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New", "Assigned": "Unassigned", "Complete": False, "Comment": ""},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "Follow-up", "Assigned": "Unassigned", "Complete": False, "Comment": ""},
    {"Name": "Dave R.", "Category": "General Question", "Message": "What’s your return policy?", "Status": "Resolved", "Assigned": "Unassigned", "Complete": True, "Comment": ""}
]
df = pd.DataFrame(data)

staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

# ---- FUNCTIONS ----
def lookup_stock(message):
    for keyword in stock_df['Product']:
        if keyword.lower() in message.lower():
            row = stock_df[stock_df['Product'] == keyword].iloc[0]
            if row['In Stock'].lower() == "yes":
                return f"✅ In stock: {row['Product']} — ${row['Price']} | {row['Details']}"
            else:
                return f"❌ Not in stock: {row['Product']}"
    return "🤖 I'm checking on that for you—our staff will confirm shortly."

# ---- DISPLAY ----
needs_attention = df[(df["Status"] != "Resolved") & (~df["Complete"])]
completed = df[df["Complete"]]

# ---- PRIORITY SECTION ----
st.header("🚨 NEEDS ATTENTION")
for i in needs_attention.index:
    with st.expander(f"{df.loc[i, 'Name']} — {df.loc[i, 'Category']}"):
        st.write(f"**Message:** {df.loc[i, 'Message']}")
        ai_reply = lookup_stock(df.loc[i, "Message"])
        st.info(f"**AI Reply Suggestion:** {ai_reply}")

        df.loc[i, "Assigned"] = st.selectbox("Assign to staff", staff_members, index=staff_members.index(df.loc[i, "Assigned"]), key=f"assign_{i}")
        df.loc[i, "Status"] = st.selectbox("Update status", ["New", "Follow-up", "Resolved"], index=["New", "Follow-up", "Resolved"].index(df.loc[i, "Status"]), key=f"status_{i}")
        df.loc[i, "Comment"] = st.text_area("Comment", value=df.loc[i, "Comment"], key=f"comment_{i}")
        df.loc[i, "Complete"] = st.checkbox("Mark Complete", value=df.loc[i, "Complete"], key=f"complete_{i}")

# ---- COMPLETED SECTION ----
with st.expander("✅ Completed Tasks"):
    st.dataframe(completed[["Name", "Category", "Message", "Assigned", "Comment"]])
