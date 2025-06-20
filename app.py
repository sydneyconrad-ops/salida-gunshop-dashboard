import streamlit as st
import pandas as pd
import random

# ---------------------------------------
# CONFIGURE DASHBOARD
# ---------------------------------------
st.set_page_config(page_title="Salida Gun Shop | Staff Dashboard", layout="wide")
st.markdown("<h1 style='color:red;'>🔴 NEEDS ATTENTION</h1>", unsafe_allow_html=True)

# ---------------------------------------
# LOAD MESSAGE DATA
# ---------------------------------------
data = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New", "Assigned To": "Unassigned", "Comment": "", "Completed": False},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "New", "Assigned To": "Unassigned", "Comment": "", "Completed": False},
    {"Name": "Tom Davis", "Category": "Gear Inquiry", "Message": "Looking for 9mm ammo boxes.", "Status": "Follow-up", "Assigned To": "Unassigned", "Comment": "", "Completed": False},
    {"Name": "Sandra C.", "Category": "General Question", "Message": "What are your holiday hours?", "Status": "Resolved", "Assigned To": "Jenna", "Comment": "Emailed her.", "Completed": True}
]

df = pd.DataFrame(data)

# ---------------------------------------
# LOAD STOCK INVENTORY FROM GOOGLE SHEETS
# ---------------------------------------
@st.cache_data
def load_inventory():
    # Replace with your actual public CSV export link from your sheet
    url = "https://docs.google.com/spreadsheets/d/1PustzDWgFysPiMh_n7HUUVCoh2qNJmHOX78Y8i2gPRk/edit?usp=sharing"
    return pd.read_csv(url)

try:
    stock_df = load_inventory()
except Exception as e:
    stock_df = pd.DataFrame(columns=["Product", "Category", "Availability"])
    st.warning("⚠️ Couldn't load stock inventory.")

# ---------------------------------------
# FILTER OPTIONS
# ---------------------------------------
category_filter = st.selectbox("📂 Filter by Category", options=["All"] + sorted(df["Category"].unique().tolist()))

if category_filter != "All":
    df = df[df["Category"] == category_filter]

# ---------------------------------------
# CLASS SIGNUP BANNER
# ---------------------------------------
if any((df["Category"] == "Class Signup") & (df["Completed"] == False)):
    st.markdown("<h3 style='color:orange;'>📣 NEW CLASS SIGNUP ALERT</h3>", unsafe_allow_html=True)

# ---------------------------------------
# STAFF & OUTSTANDING TASKS
# ---------------------------------------
staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

st.write("### 📬 Incoming Messages")

for i in df[df["Completed"] == False].index:
    with st.container():
        st.write(f"**From:** {df.loc[i, 'Name']} | **Category:** {df.loc[i, 'Category']}")
        st.write(f"**Message:** {df.loc[i, 'Message']}")

        st.markdown(f"💡 *AI Suggestion:* {random.choice(['Thanks for your message! Let me check on that and get back to you.', 'Yes, we usually have those in stock. Can I confirm your pickup time?', 'We’d love to help you with that. I’ll pass this to the right staff member now.'])}")

        if not stock_df.empty:
            match = stock_df[stock_df["Product"].str.lower().str.contains(df.loc[i, "Message"].lower())]
            if not match.empty:
                st.success(f"✅ Inventory: {match.iloc[0]['Product']} is **{match.iloc[0]['Availability'].upper()}**")
            else:
                st.info("🟡 No exact match found in inventory.")
        else:
            st.warning("⚠️ Inventory not loaded.")

        df.loc[i, "Assigned To"] = st.selectbox("Assign to:", staff_members, index=staff_members.index(df.loc[i, "Assigned To"]), key=f"assign_{i}")
        df.loc[i, "Status"] = st.selectbox("Status:", ["New", "Follow-up", "Resolved"], index=["New", "Follow-up", "Resolved"].index(df.loc[i, "Status"]), key=f"status_{i}")
        df.loc[i, "Comment"] = st.text_input("Comment:", value=df.loc[i, "Comment"], key=f"comment_{i}")
        df.loc[i, "Completed"] = st.checkbox("Mark as Complete", value=df.loc[i, "Completed"], key=f"complete_{i}")

        st.markdown("---")

# ---------------------------------------
# COMPLETED TASKS (COLLAPSIBLE)
# ---------------------------------------
with st.expander("✅ View Completed Tasks"):
    completed = df[df["Completed"] == True]
    st.dataframe(completed[["Name", "Category", "Status", "Assigned To", "Comment"]])

# ---------------------------------------
# SUMMARY TABLE
# ---------------------------------------
st.subheader("📊 Message Status Summary")
st.dataframe(df[["Name", "Category", "Status", "Assigned To", "Comment", "Completed"]])
