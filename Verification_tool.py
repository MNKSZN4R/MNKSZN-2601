import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(page_title="WVU Outcome Story Verification", layout="wide")

# Password to access this tool (internal use only)
ACCESS_PASSWORD = "admin123"

# File to store verification records
RESPONSES_FILE = "verification_records.json"

# ---------- Session State ----------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# ---------- Storage functions ----------
def save_verification(data):
    try:
        if os.path.exists(RESPONSES_FILE):
            with open(RESPONSES_FILE, 'r') as f:
                all_records = json.load(f)
        else:
            all_records = []

        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['record_id'] = f"V{len(all_records) + 1:04d}"

        all_records.append(data)

        with open(RESPONSES_FILE, 'w') as f:
            json.dump(all_records, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving verification record: {e}")
        return False

def load_all_verifications():
    try:
        if os.path.exists(RESPONSES_FILE):
            with open(RESPONSES_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Error loading verification records: {e}")
        return []

# ==================================================================
# ACCESS GATE
# ==================================================================
if not st.session_state.authenticated:
    st.title("🔐 Outcome Story Verification Tool")
    st.caption("For SNV / NGO WASH Forum use only — not completed by the reporting CSO.")
    st.markdown("### Enter password to continue")

    password_input = st.text_input("Password:", type="password", key="access_password_input")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Login", type="primary"):
            if password_input == ACCESS_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")

# ==================================================================
# MAIN APP (authenticated)
# ==================================================================
else:
    with st.sidebar:
        st.title("🔧 Navigation")
        mode = st.radio("Select Mode:", ["Add Verification Record", "View All Records"])
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()

    # ---------- Banner ----------
    st.markdown(
        """
        <div style="background: linear-gradient(90deg, #1B6CA8 0%, #2E9E5B 100%);
                    padding: 20px 30px; border-radius: 8px; margin-bottom: 20px;">
            <div style="color:white; text-align:center;">
                <div style="font-size:26px; font-weight:800;">Water Voices United</div>
                <div style="font-size:13px; margin-top:4px;">
                    Strengthening CSOs capacities and collaboration for the realization of the
                    Human Right to Water and Sanitation in Zambia
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("✅ Outcome Story — Verification Tool")
    st.caption("For SNV / NGO WASH Forum use only — not completed by the reporting CSO.")
    st.markdown("---")

    # ==============================================================
    # ADD VERIFICATION RECORD
    # ==============================================================
    if mode == "Add Verification Record":

        related_story = st.text_input(
            "Related Outcome Story (Story ID or CSO name) *",
            placeholder="e.g. OS0001 or name of the CSO whose story this verifies"
        )

        col1, col2 = st.columns(2)
        with col1:
            verifier_name_role = st.text_input("Verified by (name & role) *")
        with col2:
            date_verified = st.date_input("Date verified *", value=None)

        verification_method = st.multiselect(
            "Verification method (tick all that apply) *",
            ["Desk review of evidence", "Call to a named source", "Field visit", "Triangulation of ≥2 sources"]
        )

        verification_status = st.radio(
            "Verification status *",
            ["Verified", "Partially verified", "More evidence needed", "Not verified"]
        )

        outcome_accurate = st.radio(
            "Is the outcome story accurate? *",
            ["Yes", "Partially", "Not accurate"]
        )

        verifier_comments = st.text_area(
            "Verifier comments",
            placeholder="Any additional notes on the verification process, findings, or concerns."
        )

        st.markdown("---")

        required_fields_ok = all([
            related_story, verifier_name_role, date_verified,
            verification_method, verification_status, outcome_accurate
        ])

        if not required_fields_ok:
            st.warning("⚠️ Please complete all fields marked with * before submitting.")

        if st.button("✅ Save Verification Record", type="primary", disabled=not required_fields_ok):
            record_data = {
                "related_story": related_story,
                "verifier_name_role": verifier_name_role,
                "date_verified": str(date_verified) if date_verified else "",
                "verification_method": verification_method,
                "verification_status": verification_status,
                "outcome_accurate": outcome_accurate,
                "verifier_comments": verifier_comments
            }

            if save_verification(record_data):
                st.session_state.submitted = True
                st.success("✅ Verification record saved successfully.")

        if st.session_state.submitted:
            if st.button("🔄 Add Another Record"):
                st.session_state.submitted = False
                st.rerun()

    # ==============================================================
    # VIEW ALL RECORDS
    # ==============================================================
    else:
        all_records = load_all_verifications()

        if len(all_records) == 0:
            st.info("No verification records saved yet.")
        else:
            st.success(f"Total Verification Records: {len(all_records)}")

            # Summary
            st.markdown("### 📊 Summary")
            status_count = {}
            accuracy_count = {}
            for r in all_records:
                st_ = r.get('verification_status', 'Unknown')
                status_count[st_] = status_count.get(st_, 0) + 1
                acc = r.get('outcome_accurate', 'Unknown')
                accuracy_count[acc] = accuracy_count.get(acc, 0) + 1

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**By Verification Status**")
                st.write(status_count)
            with col2:
                st.markdown("**By Accuracy**")
                st.write(accuracy_count)

            st.markdown("---")
            st.markdown("### 📋 Individual Verification Records")

            for r in reversed(all_records):
                title = f"{r.get('record_id','')} — {r.get('related_story','Unlinked')} — {r.get('timestamp','')}"
                with st.expander(title):
                    st.write(f"Related Outcome Story: {r.get('related_story','')}")
                    st.write(f"Verified by: {r.get('verifier_name_role','')}")
                    st.write(f"Date verified: {r.get('date_verified','')}")
                    st.write(f"Verification method: {', '.join(r.get('verification_method', []))}")
                    st.write(f"Verification status: {r.get('verification_status','')}")
                    st.write(f"Outcome accurate: {r.get('outcome_accurate','')}")
                    st.write(f"Verifier comments: {r.get('verifier_comments','')}")

            st.markdown("---")
            st.markdown("### 💾 Export All Records")
            if st.button("📥 Prepare CSV Export"):
                export_rows = []
                for r in all_records:
                    row = dict(r)
                    row['verification_method'] = ', '.join(r.get('verification_method', []))
                    export_rows.append(row)

                df = pd.DataFrame(export_rows)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"wvu_verification_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )