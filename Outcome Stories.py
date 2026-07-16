import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(page_title="WVU Outcome Story", layout="wide")

# Admin password - Change this to your desired password
ADMIN_PASSWORD = "admin123"

# File to store responses
RESPONSES_FILE = "outcome_stories.json"

# ---------- Session State ----------
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# ---------- Storage functions ----------
def save_story(data):
    try:
        if os.path.exists(RESPONSES_FILE):
            with open(RESPONSES_FILE, 'r') as f:
                all_stories = json.load(f)
        else:
            all_stories = []

        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['story_id'] = f"OS{len(all_stories) + 1:04d}"

        all_stories.append(data)

        with open(RESPONSES_FILE, 'w') as f:
            json.dump(all_stories, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving story: {e}")
        return False

def load_all_stories():
    try:
        if os.path.exists(RESPONSES_FILE):
            with open(RESPONSES_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Error loading stories: {e}")
        return []

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🔧 Navigation")
    mode = st.radio("Select Mode:", ["Submit Outcome Story", "Admin Panel"])
    if mode == "Admin Panel":
        st.session_state.admin_mode = True
    else:
        st.session_state.admin_mode = False
        st.session_state.admin_authenticated = False

# ==================================================================
# ADMIN PANEL
# ==================================================================
if st.session_state.admin_mode:

    if not st.session_state.admin_authenticated:
        st.title("🔐 Admin Login")
        st.markdown("### Enter admin password to access outcome stories")
        password_input = st.text_input("Password:", type="password", key="admin_password_input")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Login", type="primary"):
                if password_input == ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect password. Please try again.")
        st.markdown("---")
        st.info("💡 Default password: admin123 (change in code for security)")

    else:
        st.title("🔐 Admin Panel — Outcome Stories")
        if st.button("🚪 Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()

        st.markdown("---")
        all_stories = load_all_stories()

        if len(all_stories) == 0:
            st.info("No outcome stories submitted yet.")
        else:
            st.success(f"Total Outcome Stories: {len(all_stories)}")

            # Summary
            st.markdown("### 📊 Summary")
            level_count = {}
            consent_count = {}
            for s in all_stories:
                lvl = s.get('level_of_change', 'Unknown')
                level_count[lvl] = level_count.get(lvl, 0) + 1
                cons = s.get('consent', 'Unknown')
                consent_count[cons] = consent_count.get(cons, 0) + 1

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**By Level of Change**")
                st.write(level_count)
            with col2:
                st.markdown("**By Consent**")
                st.write(consent_count)

            st.markdown("---")
            st.markdown("### 📋 Individual Outcome Stories")

            for s in reversed(all_stories):
                title = f"{s.get('story_id','')} — {s.get('cso_name','Unnamed CSO')} — {s.get('timestamp','')}"
                with st.expander(title):
                    st.markdown("**PART A — Snapshot**")
                    st.write(f"CSO Name: {s.get('cso_name','')}")
                    st.write(f"Contact person: {s.get('contact_person','')}")
                    st.write(f"CSO location: {s.get('cso_location','')}")
                    st.write(f"Month & year of change: {s.get('change_period','')}")
                    st.write(f"Thematic area(s): {', '.join(s.get('thematic_areas', []))}")
                    st.write(f"Level of change: {s.get('level_of_change','')}")
                    st.write(f"Type of change: {', '.join(s.get('type_of_change', []))}")

                    st.markdown("**PART B — Describe the Change**")
                    st.write(f"Outcome statement: {s.get('outcome_statement','')}")
                    st.write(f"Why it matters: {s.get('why_matters','')}")

                    st.markdown("**PART C — The Story Behind the Change**")
                    st.write(f"Before: {s.get('before','')}")
                    st.write(f"What changed: {s.get('what_changed','')}")
                    st.write(f"Sustainability: {s.get('sustainability','')}")
                    st.write(f"A voice / quote: {s.get('voice_quote','')}")
                    st.write(f"Surprises: {s.get('surprises','')}")

                    st.markdown("**PART D — Our Contribution**")
                    st.write(f"What you did: {s.get('what_you_did','')}")
                    st.write(f"Strength of role: {s.get('role_strength','')}")
                    st.write(f"Other contributors: {s.get('other_contributors','')}")

                    st.markdown("**PART E — Link with Water Voices United Project**")
                    st.write(f"Support received: {', '.join(s.get('wvu_support', []))}")
                    st.write(f"How support helped: {s.get('support_helped','')}")
                    st.write(f"Relevance of support: {s.get('support_relevance','')}")

                    st.markdown("**PART F — Evidence & Verification**")
                    st.write(f"Evidence available: {', '.join(s.get('evidence', []))}")
                    st.write("Independent confirmers:")
                    for c in s.get('confirmers', []):
                        st.write(f"  - {c.get('name','')} | {c.get('role','')} | {c.get('contact','')}")

                    st.markdown("**PART G — Consent & Next Steps**")
                    st.write(f"Consent: {s.get('consent','')}")
                    st.write(f"Follow-up plans: {s.get('next_steps','')}")
                    st.write(f"Lesson learned: {s.get('lesson_learned','')}")
                    st.write(f"Completed by: {s.get('completed_by','')}")
                    st.write(f"Date: {s.get('completion_date','')}")

            st.markdown("---")
            st.markdown("### 💾 Export All Stories")
            if st.button("📥 Prepare CSV Export"):
                export_rows = []
                for s in all_stories:
                    row = dict(s)
                    # Flatten list fields
                    row['thematic_areas'] = ', '.join(s.get('thematic_areas', []))
                    row['type_of_change'] = ', '.join(s.get('type_of_change', []))
                    row['wvu_support'] = ', '.join(s.get('wvu_support', []))
                    row['evidence'] = ', '.join(s.get('evidence', []))
                    confirmers = s.get('confirmers', [])
                    for idx, c in enumerate(confirmers):
                        row[f'confirmer_{idx+1}_name'] = c.get('name', '')
                        row[f'confirmer_{idx+1}_role'] = c.get('role', '')
                        row[f'confirmer_{idx+1}_contact'] = c.get('contact', '')
                    row.pop('confirmers', None)
                    export_rows.append(row)

                df = pd.DataFrame(export_rows)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"wvu_outcome_stories_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

# ==================================================================
# SUBMISSION FORM
# ==================================================================
else:
    # ---------- Banner (placeholder for logos) ----------
    st.markdown(
        """
        <div style="background: linear-gradient(90deg, #1B6CA8 0%, #2E9E5B 100%);
                    padding: 25px 30px; border-radius: 8px; margin-bottom: 20px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="color:white; font-size:14px; font-weight:600; letter-spacing:1px;">
                    SNV
                </div>
                <div style="color:white; text-align:center;">
                    <div style="font-size:26px; font-weight:800;">Water Voices United</div>
                    <div style="font-size:13px; margin-top:4px;">
                        Strengthening CSOs capacities and collaboration for the realization of the
                        Human Right to Water and Sanitation in Zambia
                    </div>
                </div>
                <div style="color:white; font-size:14px; font-weight:600; letter-spacing:1px;">
                    NGO WASH FORUM
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # NOTE: Replace the text placeholders above with st.image() calls once you
    # have the actual logo files, e.g.:
    # col1, col2, col3 = st.columns([1,2,1])
    # with col1: st.image("snv_logo.png")
    # with col3: st.image("ngo_wash_forum_logo.png")

    st.title("📖 Outcome Story")
    st.markdown("**Capturing CSO-driven change — for visibility, influence and donor credibility**")

    with st.expander("ℹ️ What's in it for you / How to use this tool", expanded=False):
        st.markdown("""
        **Get seen and celebrated** — best stories are featured on SNV and NGO WASH Forum channels,
        with an annual award and possible photo/video coverage of your work.

        **Grow your influence** — verified stories feed into national policy dialogues, Government
        and donor briefings (including the EU), and may lead to speaking invitations.

        **Build your credibility with donors** — build a documented, verified track record for future
        funding proposals, backed by SNV reference letters.

        ---
        **What is an outcome?** A change in what a specific group or institution *does, decides,
        changes or commits to* — that your CSO helped create. It is **not** an activity
        (e.g. "we held 3 meetings") but the **change that followed**
        (e.g. "Chongwe District Council approved a ZMW 200,000 budget line for borehole repairs
        in March 2026").

        **Tips for a strong story:**
        - **Be specific** — name who changed, what, roughly when and where.
        - **Describe your contribution honestly** — it's fine to say others helped too.
        - **Show proof** — one good piece of evidence beats a long description.

        ⏱ About 30 minutes • No special skills needed • One story per change
        """)

    st.markdown("---")

    # ================= PART A =================
    st.header("PART A — Snapshot: the basics")

    col1, col2 = st.columns(2)
    with col1:
        cso_name = st.text_input("Name of your CSO *")
        cso_location = st.text_input("CSO location *")
    with col2:
        contact_person = st.text_input("Contact person & phone / email *")
        change_period = st.text_input("Month & year (or period) the change happened *")

    st.caption("Contact details are for internal verification only and will not be published.")

    thematic_areas = st.multiselect(
        "Thematic area (tick all that apply) *",
        ["Right to Water", "Right to Sanitation", "Hygiene", "WASH in Schools",
         "WASH in Health Facilities", "IWRM", "Climate resilience", "Gender & inclusion", "Other"]
    )
    thematic_other = ""
    if "Other" in thematic_areas:
        thematic_other = st.text_input("Please detail 'Other' thematic area")

    level_of_change = st.radio(
        "Level at which the change happened *",
        ["Community / ward", "District / sub-national", "Provincial", "National"]
    )

    type_of_change = st.multiselect(
        "Type of change (tick all that apply) *",
        ["Policy/regulation/by-law change", "Budgetary change", "Institutional practice change",
         "Government-community relation change", "Service Provision change",
         "Evidence based decision making change", "Other"]
    )
    type_other = ""
    if "Other" in type_of_change:
        type_other = st.text_input("Please detail 'Other' type of change")

    st.markdown("---")

    # ================= PART B =================
    st.header("PART B — Describe the change")

    outcome_statement = st.text_area(
        "Outcome statement — describe the single change in 1–2 sentences *",
        placeholder="[Who changed] did / decided / committed to [what change] in [place] in [month, year]."
    )

    why_matters = st.text_area(
        "Why does this change matter, and for whom? *",
        placeholder="Who benefits, and how does it advance the right to water and sanitation, "
                    "inclusion or climate resilience? Highlight specific benefits for vulnerable "
                    "groups (women, girls, people with disabilities, remote/underserved communities) if applicable."
    )

    st.markdown("---")

    # ================= PART C =================
    st.header("PART C — The story behind the change")

    before = st.text_area("BEFORE — what was the situation?",
                           placeholder="What problem or gap existed before the change?")

    what_changed = st.text_area("WHAT CHANGED — what happened as a result?",
                                 placeholder="Describe the shift in decision, behaviour, practice, policy or resources.")

    sustainability = st.text_area("SUSTAINABILITY",
                                   placeholder="How likely is the change you created to be maintained over time?")

    voice_quote = st.text_area("A VOICE — a short quote",
                                placeholder="A quote from a CSO member, community member, traditional leader "
                                            "or government official. Note their first name / role.")

    surprises = st.text_area("SURPRISES — any unexpected results?",
                              placeholder="Both positive and negative surprises are important learning points.")

    st.markdown("---")

    # ================= PART D =================
    st.header("PART D — Our contribution: what was your role?")

    what_you_did = st.text_area(
        "WHAT YOU DID — your CSO's actions",
        placeholder="e.g. evidence gathered, dialogue, campaign, community mobilization or awareness, meeting, media engagement."
    )

    role_strength = st.radio(
        "How strong was the role of your CSO?",
        ["We were the main driver", "One of several contributors", "Mostly, a supporting role"]
    )

    other_contributors = st.text_area(
        "Did anyone else contribute?",
        placeholder="Other CSOs, the Forum, media, government, communities, other projects."
    )

    st.markdown("---")

    # ================= PART E =================
    st.header("PART E — Link with Water Voices United project (if applicable)")

    wvu_support = st.multiselect(
        "What support or learning from Water Voices United supported the change you achieved?",
        ["Training / workshop", "Coaching or mentoring", "M&E or tools & templates",
         "A Water Voices United grant", "Evidence/research support",
         "Networking via the NGO WASH Forum", "Joint activity with the Forum or other CSOs", "Other"]
    )
    wvu_support_other = ""
    if "Other" in wvu_support:
        wvu_support_other = st.text_input("Please detail 'Other' support")

    support_helped = st.text_area(
        "How did this support or learning help you achieve the change?",
        placeholder="Connect the dots. e.g. 'The advocacy training helped us prepare the evidence "
                    "brief we presented to the council.'"
    )

    support_relevance = st.radio(
        "To what extent was the Water Voices United support relevant to achieve this outcome?",
        ["Not very relevant", "A bit relevant", "Very relevant", "Essential"]
    )

    st.markdown("---")

    # ================= PART F =================
    st.header("PART F — Evidence & verification: how we can confirm it")
    st.caption("This is the part that turns your story into a verified result. Please complete it.")

    evidence = st.multiselect(
        "What evidence can you attach or point to?",
        ["Photos", "Meeting minutes", "Official letter / policy document", "Budget line / plan",
         "Media article", "Attendance list", "Video / audio", "Testimony", "Other"]
    )
    evidence_other = ""
    if "Other" in evidence:
        evidence_other = st.text_input("Please detail 'Other' evidence")

    st.markdown("**Who can independently confirm this change?**")
    st.caption("Give at least one person outside your CSO (e.g. an official, a partner, private sector, or community leader).")

    confirmers = []
    conf_col1, conf_col2, conf_col3 = st.columns(3)
    with conf_col1:
        c1_name = st.text_input("Name (Confirmer 1)")
    with conf_col2:
        c1_role = st.text_input("Role / organisation (Confirmer 1)")
    with conf_col3:
        c1_contact = st.text_input("Phone or email (Confirmer 1)")
    if c1_name or c1_role or c1_contact:
        confirmers.append({"name": c1_name, "role": c1_role, "contact": c1_contact})

    conf_col4, conf_col5, conf_col6 = st.columns(3)
    with conf_col4:
        c2_name = st.text_input("Name (Confirmer 2)")
    with conf_col5:
        c2_role = st.text_input("Role / organisation (Confirmer 2)")
    with conf_col6:
        c2_contact = st.text_input("Phone or email (Confirmer 2)")
    if c2_name or c2_role or c2_contact:
        confirmers.append({"name": c2_name, "role": c2_role, "contact": c2_contact})

    st.markdown("---")

    # ================= PART G =================
    st.header("PART G — Consent & what's next")

    consent = st.radio(
        "May the project share this story (with names / photos) in its communications? *",
        ["Yes, freely", "Yes, but anonymise people", "No — for project reporting purposes only"]
    )

    next_steps = st.text_area("What happens next?", placeholder="Any follow-up planned?")

    lesson_learned = st.text_area("What did you learn?", placeholder="Any lesson worth sharing with other CSOs?")

    col1, col2 = st.columns(2)
    with col1:
        completed_by = st.text_input("Completed by (name & signature) *")
    with col2:
        completion_date = st.date_input("Date *", value=None)

    st.markdown("---")

    # ================= SUBMIT =================
    required_fields_ok = all([
        cso_name, contact_person, cso_location, change_period,
        thematic_areas, type_of_change, outcome_statement, why_matters,
        consent, completed_by, completion_date
    ])

    if not required_fields_ok:
        st.warning("⚠️ Please complete all fields marked with * before submitting.")

    if st.button("✅ Submit Outcome Story", type="primary", disabled=not required_fields_ok):
        story_data = {
            "cso_name": cso_name,
            "contact_person": contact_person,
            "cso_location": cso_location,
            "change_period": change_period,
            "thematic_areas": thematic_areas + ([f"Other: {thematic_other}"] if thematic_other else []),
            "level_of_change": level_of_change,
            "type_of_change": type_of_change + ([f"Other: {type_other}"] if type_other else []),
            "outcome_statement": outcome_statement,
            "why_matters": why_matters,
            "before": before,
            "what_changed": what_changed,
            "sustainability": sustainability,
            "voice_quote": voice_quote,
            "surprises": surprises,
            "what_you_did": what_you_did,
            "role_strength": role_strength,
            "other_contributors": other_contributors,
            "wvu_support": wvu_support + ([f"Other: {wvu_support_other}"] if wvu_support_other else []),
            "support_helped": support_helped,
            "support_relevance": support_relevance,
            "evidence": evidence + ([f"Other: {evidence_other}"] if evidence_other else []),
            "confirmers": confirmers,
            "consent": consent,
            "next_steps": next_steps,
            "lesson_learned": lesson_learned,
            "completed_by": completed_by,
            "completion_date": str(completion_date) if completion_date else ""
        }

        if save_story(story_data):
            st.session_state.submitted = True
            st.success("✅ Thank you! Your outcome story has been submitted successfully.")
            st.balloons()

    if st.session_state.submitted:
        if st.button("🔄 Submit Another Story"):
            st.session_state.submitted = False
            st.rerun()