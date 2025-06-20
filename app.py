import streamlit as st
import pandas as pd
import openai
from datetime import datetime

# --- CONFIGURATION ---
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"  # ← Replace this!

# --- SAMPLE DATA ---
data = [
    {
        "Name": "John Smith",
        "Category": "Gear Inquiry",
        "Message": "Do you have any Magpul stocks?",
        "Status": "New",
        "Assigned To": "Unassigned",
        "Comments": "",
        "Comment History": [],
        "Suggested Reply": ""
    },
    {
        "Name": "Megan Lee",
        "Category": "Class Signup",
        "Message": "Is there a pistol training this weekend?",
        "Status": "Follow-up",
        "Assigned To": "Unassigned",
        "Comments": "",
        "Comment History": [],
        "Suggested Reply": ""
    },
    {
        "Name": "Dave R.",
        "Category": "General Question",
        "Message": "What’s your return policy?",
        "Status": "Resolved",
        "Assigned To": "Unassigned",
        "Comments": "",
        "Comment History": [],
        "Suggested Reply": ""
    }
]

staff_members = [
    "Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew",
    "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"
]

df = pd.DataFrame(data)

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="Salida Gun Shop | Staff View", layout="centered")
st.title("🔧 Staff Message Dashboard")

# --- CATEGORY FILTER ---
categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.selectbox("Filter by Category", categories)

if selected_category != "All":
    filtered_df = df[df["Category"] == selected_category].copy()
else:
    filtered_df = df.copy()

# --- ALERT FOR CLASS SIGNUPS ---
if any((df["Category"] == "Class Signup") & (df["Status"].isin(["New", "Follow-up"]))):
    st.markdown("### :rotating_light: **New Class Signup Needs Follow-Up!**", unsafe_allow_html=True)

# --- MAIN LOOP ---
for i in filtered_df.index:
    with st.expander(f"From: {filtered_df.loc[i, 'Name']} | Category: {filtered_df.loc[i, 'Category']}"):
        st.write(f"**Message:** {filtered_df.loc[i, 'Message']}")

        # Status Dropdown
        filtered_df.loc[i, 'Status'] = st.selectbox(
            f"Update Status for {filtered_df.loc[i, 'Name']}",
            options=["New", "Follow-up", "Resolved"],
            index=["New", "Follow-up", "Resolved"].index(filtered_df.loc[i, 'Status']),
            key=f"status_{i}"
        )

        # Assign Staff
        filtered_df.loc[i, 'Assigned To'] = st.selectbox(
            "Assign to Staff",
            options=staff_members,
            index=staff_members.index(filtered_df.loc[i, 'Assigned To']),
            key=f"assign_{i}"
        )

        # Add Comment
        new_comment = st.text_input(
            "Comment or Note:",
            value=filtered_df.loc[i, 'Comments'],
            key=f"comment_{i}"
        )

        if new_comment != filtered_df.loc[i, 'Comments']:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            history = filtered_df.loc[i, "Comment History"]
            history.append(f"[{timestamp}] {new_comment}")
            filtered_df.loc[i, 'Comment History'] = history
            filtered_df.loc[i, 'Comments'] = new_comment

        # View Comment History
        if filtered_df.loc[i, 'Comment History']:
            st.markdown("**🕒 Comment History:**")
            for entry in filtered_df.loc[i, 'Comment History']:
                st.markdown(f"- {entry}")

        # Generate GPT reply suggestion
        if st.button(f"💡 Suggest Auto-Reply for {filtered_df.loc[i, 'Name']}", key=f"gpt_{i}"):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant at a gun shop."},
                        {"role": "user", "content": filtered_df.loc[i, "Message"]}
                    ]
                )
                reply = response.choices[0].message.content.strip()
                filtered_df.loc[i, "Suggested Reply"] = reply
            except Exception as e:
                st.error(f"Error generating reply: {e}")

        # Show reply
        if filtered_df.loc[i, "Suggested Reply"]:
            st.markdown(f"**💬 Suggested Reply:** {filtered_df.loc[i, 'Suggested Reply']}")

# --- FINAL TABLE + EXPORT ---
st.subheader("📋 Updated Statuses")
st.dataframe(filtered_df.drop(columns=["Comment History", "Suggested Reply"]), use_container_width=True)

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📤 Export Daily Report", data=csv, file_name="daily_report.csv", mime="text/csv")
