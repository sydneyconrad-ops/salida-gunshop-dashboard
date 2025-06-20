import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(st.secrets["gcp_service_account"]),
    scope
)

client = gspread.authorize(creds)

# Sheet config
sheet_url = "https://docs.google.com/spreadsheets/d/1bD3IXAL3N8njmAxfCz6KHMy9TcFBX0Eh0V3HqLUrfkI/edit?usp=sharing"
sheet_id = sheet_url.split("/")[5]
inventory_sheet = client.open_by_key(sheet_id).sheet1
inventory_data = pd.DataFrame(inventory_sheet.get_all_records())

# Sample inquiries (replace with database or form data)
if "inquiries" not in st.session_state:
    st.session_state.inquiries = [
        {"name": "Mike", "message": "Do you have 9mm ammo?", "status": "New", "assigned": "Unassigned", "comments": "", "completed": False},
        {"name": "Rachel", "message": "Signing up for gun safety class", "status": "New", "assigned": "Jenna", "comments": "", "completed": False},
        {"name": "Terry", "message": "Looking for holsters for Glock 19", "status": "Follow-up", "assigned": "Adam", "comments": "", "completed": False}
    ]

# --- UI Styling ---
st.set_page_config(page_title="GunShop Dashboard", layout="wide")
st.markdown("## 🧭 Salida GunShop — Inquiry Dashboard")

st.markdown("### 🔥 NEEDS ATTENTION")
needs_attention = [i for i in st.session_state.inquiries if not i["completed"]]

if not needs_attention:
    st.success("All caught up! No outstanding messages.")
else:
    for i, item in enumerate(needs_attention):
        with st.expander(f"{item['name']} — {item['message'][:40]}..."):
            cols = st.columns([2, 2, 4, 2, 2])

            # Status
            item["status"] = cols[0].selectbox(
                "Status", ["New", "Follow-up", "Resolved"], index=["New", "Follow-up", "Resolved"].index(item["status"]), key=f"status_{i}"
            )

            # Staff
            staff_members = ["Unassigned", "Josiah", "Deryk", "Derek", "Cody", "Drew", "Adam", "Matty", "Jenna", "Gavin", "Kenny", "Jeff", "Phil"]
            item["assigned"] = cols[1].selectbox("Assign to", staff_members, index=staff_members.index(item["assigned"]), key=f"assign_{i}")

            # Comment box
            item["comments"] = cols[2].text_area("Comments", item["comments"], key=f"comment_{i}")

            # Inventory lookup
            product_match = inventory_data[inventory_data["product"].str.lower().str.contains(item["message"].lower())]
            inventory_msg = "Product not found."
            if not product_match.empty:
                row = product_match.iloc[0]
                inventory_msg = f"{row['product']} - {row['availability']} ({row['location']})"
            cols[3].markdown(f"**Stock Lookup:** {inventory_msg}")

            # Completion
            if cols[4].checkbox("Mark complete", key=f"complete_{i}"):
                item["completed"] = True
                item["status"] = "Resolved"

# --- Completed Tasks ---
st.markdown("---")
st.markdown("### ✅ COMPLETED INQUIRIES")
completed = [i for i in st.session_state.inquiries if i["completed"]]

if completed:
    for item in completed:
        st.markdown(f"- {item['name']} — {item['message']} *(Handled by {item['assigned']})*")

# --- Add new inquiry manually (optional) ---
with st.expander("➕ Add New Inquiry (Manual Entry)"):
    new_name = st.text_input("Name")
    new_msg = st.text_input("Message")
    if st.button("Add Inquiry"):
        st.session_state.inquiries.append({
            "name": new_name,
            "message": new_msg,
            "status": "New",
            "assigned": "Unassigned",
            "comments": "",
            "completed": False
        })
        st.success("Inquiry added!")

