import streamlit as st
import pandas as pd

# -----------------------------
# Sample message log (editable fake data)
# -----------------------------
data = [
    {"Name": "John Smith", "Category": "Gear Inquiry", "Message": "Do you have any Magpul stocks?", "Status": "New", "Assigned To": "Unassigned"},
    {"Name": "Megan Lee", "Category": "Class Signup", "Message": "Is there a pistol training this weekend?", "Status": "New", "Assigned To": "Unassigned"},
    {"Name": "Dave R.", "Category": "General Question", "Message": "What’s your return policy?", "Status": "Resolved", "Assigned To": "Unassigned"},
    {"Name": "Nina C.", "Category": "Class Signup", "Message": "Do you teach rifle classes?", "Status": "Follow-up", "Assigned To": "Ethan"}
]

# -----------------------------
# Updated Staff Members
# -----------------------------
staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]

df = pd.DataFrame(data)

# Streamlit page settings
st.set_page_config(page_title="Salida Gun Shop | Staff View", layout="centered")
st.title("🔧 Staff Message Dashboard")

# -----------------------------
# 🚨 Next Task Banner (First "New")
# -----------------------------
next_task = df[df["Status"] == "New"].head(1)

if not next_task.empty:
    st.markdown("### 🔔 Next Task")
    st.markdown(f"**From:** {next_task.iloc[0]['Name']} | **Category:** {next_task.iloc[0]['Category']}")
    st.markdown(f"**Message:** {next_task.iloc[0]['Message']}")
else:
    st.markdown("### ✅ All caught up!")

# -----------------------------
# 🚨 Alert if "Class Signup" messages are still New
# -----------------------------
urgent_class_signups = df[(df["Category"] == "Class Signup") & (df["Status"] == "New")]
if not urgent_class_signups.empty:
    st.error(f"🚨 {len(urgent_class_signups)} new Class Signup request(s) need attention!")

# -----------------------------
# Dropdown Filter by Category
# -----------------------------
selected_category = st.selectbox(
    "📂 Filter by Category",
    options=["All"] + df["Category"].unique().tolist()
)

if selected_category != "All":
    filtered_df = df[df["Category"] == selected_category]
else:
    filtered_df = df

# -----------------------------
# Message Cards with Dropdowns
# -----------------------------
for i in filtered_df.index:
    with st.expander(f"{filtered_df.loc[i, 'Name']} - {filtered_df.loc[i, 'Category']}"):
        st.write(f"**Message:** {filtered_df.loc[i, 'Message']}")

        # Status Dropdown
        filtered_df.loc[i, 'Status'] = st.selectbox(
            f"Update Status for {filtered_df.loc[i, 'Name']}",
            options=["New", "Follow-up", "Resolved"],
            index=["New", "Follow-up", "Resolved"].index(filtered_df.loc[i, 'Status']),
            key=f"status_{i}"
        )

        # Assign To Dropdown
        filtered_df.loc[i, 'Assigned To'] = st.selectbox(
            f"Assign to Staff",
            options=staff_members,
            index=staff_members.index(filtered_df.loc[i, 'Assigned To']) if filtered_df.loc[i, 'Assigned To'] in staff_members else 0,
            key=f"assign_{i}"
        )

# -----------------------------
# Visual Counters Summary
# -----------------------------
st.markdown("### 📊 Status Overview")
status_counts = df['Status'].value_counts()
for status in ["New", "Follow-up", "Resolved"]:
    count = status_counts.get(status, 0)
    st.markdown(f"- **{status}:** {count}")

# -----------------------------
# Display Updated Table
# -----------------------------
st.subheader("📋 Updated Message Log")
st.dataframe(filtered_df)

# -----------------------------
# Export CSV Button
# -----------------------------
st.download_button(
    label="⬇️ Export Daily Report",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='daily_report.csv',
    mime='text/csv'
)
