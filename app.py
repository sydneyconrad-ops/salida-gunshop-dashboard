import streamlit as st
import pandas as pd
import random

# ---------------------------------------
# 1. CONFIGURE DASHBOARD
# ---------------------------------------
st.set_page_config(page_title="Salida Gun Shop | Staff Dashboard", layout="wide")
st.markdown("<h1 style='color:red;'>🔴 NEEDS ATTENTION</h1>", unsafe_allow_html=True)

# ---------------------------------------
# 2. LOAD DUMMY MESSAGE DATA
# ---------------------------------------
data = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New"},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "New"},
    {"Name": "Tom Davis", "Category": "Gear Inquiry", "Message": "Looking for 9mm ammo boxes.", "Status": "Follow-up"},
    {"Name": "Sandra C.", "Category": "General Question", "Message": "What are your holiday hours?", "Status": "Resolved"},
    {"Name": "Becky L.", "Category": "Class Signup", "Message": "Signing up for rifle course next month.", "Status": "New"}
]

df = pd.DataFrame(data)
df["Assigned To"] = "Unassigned"
df["Comment"] = ""
df["Completed"] = False

# ---------------------------------------
# 3. LOAD STOCK INVENTORY FROM GOOGLE SHEETS (as DataFrame)
# ---------------------------------------
@st.cache_data
def load_inventory():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTmnzBCJquVzOC_2YlRfWmT4-rUbsP9fXYBZYwn1Qbd82CBmQu2GF0h_wB0pNzC1pPIhK9Geq8_YACm/pub?gid=0&single=true&output=csv"
    return pd.read_csv(url)

try:
    stock_df = load_inventory()
except Exception as e:
    stock_df = pd.DataFrame(columns=["Product", "Category", "Availability"])
    st.warning("⚠️ Couldn't load stock inventory.")

# ---------------------------------------
# 4. FILTER OPTIONS
# ---------------------------------------
category_filter = st.selectbox("📂 Filter by Category", options=["All"] + sorted(df["Category"].unique().tolist()))

if category_filter != "All":
    df = df[df["Category"] == category_filter]

# ---------------------------------------
# 5. CLASS SIGNUP ALERT BANNER
# ---------------------------------------
if any(df["Category"] == "Class Signup"):
    st.markdown("<h3 style='color:orange;'>📣 NEW CLASS SIGNUP ALERT</h3>", unsafe_allow_html=True)

# ---------------------------------------
# 6. STAFF ASSIGNMENT, STATUS, COMMENTS, COMPLETION
# ---------------------------------------
staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

st.write("### 📬 Incoming Messages")

for i in df.index:
    with st.container():
        st.write(f"**From:** {df.loc[i, 'Name']} | **Category:** {df.loc[i, 'Category']}")
        st.write(f"**Message:** {df.loc[i, 'Message']}")

        # Simulated AI reply suggestion
        st.markdown(f"💡 *AI Suggestion:* {random.choice(['Thanks for your message! Let me check on that and get back to you.', 'Yes, we usually have those in stock. Can I confirm your pickup time?', 'We’d love to help you with that. I’ll pass this to the right staff member now.'])}")

        # Inventory check (basic keyword match)
        matched_items = stock_df[stock_df["Product"].str.lower().str.contains(df.loc[i, "Message"].lower())] if not stock_df.empty else pd.DataFrame()
        if not matched_items.empty:
            availability = matched_items.iloc[0]["Availability"]
            st.success(f"✅ Inventory Lookup: {matched_items.iloc[0]['Product']} is currently **{availability.upper()}**")
        else:
            st.info("🟡 No exact match found in inventory.")

        # Staff assignment
        df.loc[i, "Assigned To"] = st.selectbox("Assign to:", staff_members, index=0, key=f"assign_{i}")

        # Status update
        df.loc[i, "Status"] = st.selectbox("Status:", ["New", "Follow-up", "Resolved"], key=f"status_{i}")

        # Comment
        df.loc[i, "Comment"] = st.text_input("Comment:", key=f"comment_{i}")

        # Completion checkbox
        df.loc[i, "Completed"] = st.checkbox("Mark as Complete", key=f"complete_{i}")

        st.markdown("---")

# ---------------------------------------
# 7. DISPLAY STATUS SUMMARY TABLE
# ---------------------------------------
st.subheader("📊 Message Status Overview")
st.dataframe(df[["Name", "Category", "Status", "Assigned To", "Comment", "Completed"]])
