import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(page_title="SNV Four Domains Benchmarking", layout="wide")

# Admin password - Change this to your desired password
ADMIN_PASSWORD = "admin123"

# File to store responses
RESPONSES_FILE = "survey_responses.json"

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

# Functions to save and load responses
def save_response(response_data):
    """Save a completed survey response to file"""
    try:
        # Load existing responses
        if os.path.exists(RESPONSES_FILE):
            with open(RESPONSES_FILE, 'r') as f:
                all_responses = json.load(f)
        else:
            all_responses = []
        
        # Add timestamp and unique ID
        response_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_data['response_id'] = f"R{len(all_responses) + 1:04d}"
        
        # Append new response
        all_responses.append(response_data)
        
        # Save back to file
        with open(RESPONSES_FILE, 'w') as f:
            json.dump(all_responses, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving response: {e}")
        return False

def load_all_responses():
    """Load all saved responses"""
    try:
        if os.path.exists(RESPONSES_FILE):
            with open(RESPONSES_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Error loading responses: {e}")
        return []

# Define the four domains and their benchmarks
domains = {
    "Positioning, Influencing & Strategic Collaboration": [
        "Have a Global overview for Sector and Core Themes (main trends, key development agendas, ambitions, challenges) and of how these are playing out in different SNV Countries/regions?",
        "Have clear Global Systems Transformations ambitions -- including on what to contribute to/how to influence, what key players to work with, and where to position accordingly?",
        "Periodically reflect on the relevance and appropriateness of Systems Transformation ambitions for Sector and Themes (given that trends evolve), globally, also considering countries' feedback?",
        "Regularly and systematically (documenting and following up) engage with countries to remain updated on national and regional contexts dynamics and trends of SNV countries/regions on sector and the core themes?",
        "Regularly and systematically (documenting and following up) engage with countries to provide updates on Global trends and guidance on global Systems Transformations ambitions for Sector and Core Themes?",
        "Have a position (access, credibility and voice) in the key platforms/forums/technical working groups, from which it can then contribute to advancing the global development agenda for sector and the core themes?",
        "Use robust and up to date evidence, also from the countries (project data & results, track records, relationships, people) to strengthen positioning and ability to contribute/influence in global platforms/fora/events?",
        "Have a consistent lead for the different technical issues in the relevant Influencing spaces (following the 'be consistent to be recognizable' principle)?",
        "Collaborate with like minded institutions, also informally; and connect with global and regional partners to advance shared agendas on Sectors and on Themes?",
        "Assess progress and adjustments needed to move towards the achievement of Systems Transformation ambitions regularly through Global Technical Team meetings?"
    ],
    "Business Development & Partnerships": [
        "Have a consistent practice of deliberately using SNV's relationships and presence in relevant spaces to strengthen its profile for BD purposes (positioning, building reputation, deepen/expanding connections) and also to influence the donors' agenda?",
        "Intentionally enhances SNV's reputation as a 'partner of choice' -- not just by showcasing technical and institutional capacity but also by investing in building networks, and personalised and responsive relationships?",
        "Have knowledge about key competitors and potential partners, including a partnerships vision/strategy (with whom to partner and for what)?",
        "Proactively engage and establish/build relationships with (also emerging) donors, while involving targeted countries in these efforts to showcase the availability of contextualized expertise, country footprint and relationships?",
        "Have an effective mechanism in place to lead/organize multi-country proposal development (including the facilitation of multi-country collaboration, gathering of country track records and evidence, organization of the Technical Expertise, etc)?",
        "Have communication mechanisms with countries to share/receive donor intelligence timely (so as to also allow to anticipate and pro-actively position and prepare for BD opportunities)?",
        "Have an overview of the Technical Expertise available in country for proposal development and of how the Global Technical Team can best enhance/complement it?",
        "Have a mechanism in place to ensure timely, well coordinated and high quality support to proposal development in countries?",
        "Have a practice for proposal review that ensures suitability to donor requirements AND overall alignment with SNVs 'Technical Excellence branding and ways of working'?",
        "Seeks to improve proposal development by deliberately learning from (successful and failed) submissions?"
    ],
    "Knowledge Development & Teams Capacity": [
        "Have an overview of the Global Knowledge Development status (trends/hot topics, state of the art knowledge, key learning questions, main KD players)?",
        "Have a global Learning Agenda aligned with Systems Transformation ambitions - that seeks to bridge the gap between the current Knowledge status and the level of Knowledge required to maintain SNV's relevance?",
        "Have a mechanism to identify, nurture, validate and document countries experiences, best practices, innovations and ideas (including from local partners) to enable dissemination, scaling up and replication?",
        "Use project's results and feedback from countries to critically interrogate framework approaches, themes positioning papers, technical solutions and/or methodologies used, so as to further develop and update them?",
        "Have a streamlined mechanism to share Global knowledge advancements and lessons learned across countries back with countries to develop their Knowledge and support the contextualization of its use to their context?",
        "Have strategic partnerships with knowledge/research institutions that complement, deepen and/or validate SNV's technical expertise?",
        "Strategically mobilize SNV's Knowledge (Countries & Global) to contribute to relevant Global debates and advance the Global Knowledge base, also in relation to the Core Themes?",
        "Have a clear understanding of what particular issue/approach/methodology SNV is a thought leader/frontrunner on, and on how to maintain that profile/competitive advantage?",
        "Have a mechanism to identify and address the Global Technical Teams' learning needs (including soft skills)?",
        "Deliberately integrate KD objectives and Teams capacity development objectives in project's design and budgeting (donor allowing)?"
    ],
    "People & Project Management": [
        "Align multi-country projects with Sector Framework Approaches and Core Themes (as possible, considering the donors' scope), or at the very least with their key principles?",
        "Have a mechanism to manage multi-country projects effectively (including steering for quality, systems change, local partners empowerment, and sustainability)?",
        "Have an overview of the Technical Expertise available in country for project delivery and of how the Global Technical Team can best build it (in addition to backstopping it only)?",
        "Have MEL frameworks for all Framework approaches in Sector -- including ToCs and core theme indicators, as these support project design & delivery, and facilitate the easier aggregation of results across countries?",
        "Have a practice of supporting country teams in project monitoring reflections/data sense making and learning exercises?",
        "Uses an adaptive management approach: fostering a mindset of critically interrogating projects' progress and the introduction of changes as relevant and possible?",
        "Have communication/feedback loop mechanisms with Countries to timely identify (or even anticipate) bottlenecks in project implementation (in addition to the quarterly PRRs)?",
        "Have a strategy to timely support projects facing challenges in implementation?",
        "Have a mechanism that acknowledges and strives to build diverse skill sets in the technical teams, in addition to 'pure' technical expertise?",
        "Manages for talent retention, including recognition of performance and a plan for the 'in between projects' gaps?"
    ]
}

rating_options = {
    0: "Non-existent",
    1: "Incipient",
    2: "Basic",
    3: "Advanced",
    4: "Full-fledged"
}

# Sidebar for admin panel
with st.sidebar:
    st.title("🔧 Navigation")
    
    mode = st.radio("Select Mode:", ["Survey", "Admin Panel"])
    
    if mode == "Admin Panel":
        st.session_state.admin_mode = True
    else:
        st.session_state.admin_mode = False
        st.session_state.admin_authenticated = False  # Reset authentication when leaving admin mode
    
    st.markdown("---")
    
    if not st.session_state.admin_mode:
        st.info(f"**Current Page:** {st.session_state.current_page}/5")
        if st.session_state.current_page > 0:
            st.success(f"**Sector:** {st.session_state.responses.get('sector', 'Not selected')}")

# ADMIN PANEL
if st.session_state.admin_mode:
    # Check if authenticated
    if not st.session_state.admin_authenticated:
        st.title("🔐 Admin Login")
        st.markdown("### Enter admin password to access responses")
        
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
        st.info("💡 Default password: admin123 (Change this in the code for security)")
    
    else:
        # Authenticated - Show admin panel
        st.title("🔐 Admin Panel - Survey Responses")
        
        # Logout button
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.admin_authenticated = False
            st.rerun()
        
        st.markdown("---")
        
        all_responses = load_all_responses()
        
        if len(all_responses) == 0:
            st.info("No survey responses recorded yet.")
        else:
            st.success(f"Total Responses: {len(all_responses)}")
            
            # Summary statistics
            st.markdown("### 📊 Summary Statistics")
            col1, col2, col3 = st.columns(3)
            
            # Count responses by sector
            sectors_count = {}
            for resp in all_responses:
                sector = resp.get('sector', 'Unknown')
                sectors_count[sector] = sectors_count.get(sector, 0) + 1
            
            with col1:
                st.metric("Water", sectors_count.get('Water', 0))
            with col2:
                st.metric("Energy", sectors_count.get('Energy', 0))
            with col3:
                st.metric("Agri Food Systems", sectors_count.get('Agri Food Systems', 0))
            
            st.markdown("---")
            
            # Display individual responses
            st.markdown("### 📋 Individual Responses")
            
            for i, response in enumerate(reversed(all_responses)):
                with st.expander(f"Response {response.get('response_id', f'R{i+1}')} - {response.get('sector', 'Unknown')} - {response.get('timestamp', 'N/A')}"):
                    
                    # Calculate total score
                    domain_scores = {}
                    question_num = 1
                    
                    for domain_name in domains.keys():
                        domain_score = 0
                        st.markdown(f"**{domain_name}**")
                        
                        for j in range(len(domains[domain_name])):
                            key = f"{domain_name}_{j}"
                            rating = response.get(key, 0)
                            domain_score += rating
                            
                            st.write(f"Q{question_num}. Rating: {rating} - {rating_options.get(rating, 'N/A')}")
                            question_num += 1
                        
                        domain_scores[domain_name] = domain_score
                        st.write(f"**Domain Score: {domain_score}/40**")
                        st.markdown("---")
                    
                    total_score = sum(domain_scores.values())
                    st.metric("Total Score", f"{total_score}/160 ({total_score/160*100:.1f}%)")
            
            st.markdown("---")
            
            # Export all responses
            st.markdown("### 💾 Export All Responses")
            
            if st.button("📥 Download All Responses as CSV"):
                # Prepare comprehensive export
                export_rows = []
                
                for response in all_responses:
                    row = {
                        'Response ID': response.get('response_id', ''),
                        'Timestamp': response.get('timestamp', ''),
                        'Sector': response.get('sector', '')
                    }
                    
                    # Add all question responses
                    question_num = 1
                    for domain_name in domains.keys():
                        for j in range(len(domains[domain_name])):
                            key = f"{domain_name}_{j}"
                            rating = response.get(key, 0)
                            row[f'Q{question_num}'] = rating
                            row[f'Q{question_num}_Description'] = rating_options.get(rating, '')
                            question_num += 1
                    
                    # Add domain scores
                    for domain_name in domains.keys():
                        domain_score = sum([response.get(f"{domain_name}_{j}", 0) for j in range(len(domains[domain_name]))])
                        row[f'{domain_name}_Score'] = domain_score
                    
                    # Add total score
                    total = sum([response.get(f"{dn}_{j}", 0) for dn in domains.keys() for j in range(len(domains[dn]))])
                    row['Total_Score'] = total
                    
                    export_rows.append(row)
                
                df = pd.DataFrame(export_rows)
                csv = df.to_csv(index=False)
                
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"all_survey_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

# SURVEY MODE
else:
    # Sector selection page
    if st.session_state.current_page == 0:
        st.title("🌍 SNV Four Domains Technical Expertise Benchmarking Exercise")
        
        st.markdown("""
        Welcome to the Four Domains Technical Expertise Benchmarking Exercise!
        
        This tool helps Global Technical Expertise Teams assess their practices across four critical domains:
        - **Positioning, Influencing & Strategic Collaboration**
        - **Business Development & Partnerships**
        - **Knowledge Development & Teams Capacity**
        - **People & Project Management**
        
        Please select your sector to begin the assessment.
        """)
        
        sector = st.selectbox(
            "Select your sector:",
            ["", "Water", "Energy", "Agri Food Systems"],
            key="sector_select"
        )
        
        if sector:
            st.session_state.responses['sector'] = sector
            if st.button("Begin Assessment →", type="primary"):
                st.session_state.current_page = 1
                st.rerun()

    # Domain assessment pages
    elif 1 <= st.session_state.current_page <= 4:
        domain_index = st.session_state.current_page - 1
        domain_names = list(domains.keys())
        current_domain = domain_names[domain_index]
        
        # Calculate question numbering offset
        questions_before = sum([len(domains[domain_names[i]]) for i in range(domain_index)])
        
        st.header(f"Domain {domain_index + 1}: {current_domain}")
        st.subheader(f"Sector: {st.session_state.responses.get('sector', 'Not specified')}")
        
        # Progress indicator
        progress = (st.session_state.current_page) / 5
        st.progress(progress)
        st.write(f"Progress: Domain {st.session_state.current_page} of 4")
        
        st.markdown("---")
        st.markdown("**Rate each benchmark from 0 (Non-existent) to 4 (Full-fledged)**")
        st.markdown("---")
        
        # Display benchmarks for current domain
        for i, benchmark in enumerate(domains[current_domain]):
            question_number = questions_before + i + 1
            
            st.markdown(f"### Question {question_number}")
            st.write(benchmark)
            
            key = f"{current_domain}_{i}"
            
            # Check if this question has been answered before
            default_index = None if key not in st.session_state.responses else st.session_state.responses[key]
            
            rating = st.radio(
                "Rating:",
                options=list(rating_options.keys()),
                format_func=lambda x: f"{x} - {rating_options[x]}",
                key=key,
                index=default_index,
                horizontal=True
            )
            st.session_state.responses[key] = rating
            st.markdown("---")
        
        # Check if all questions in current domain are answered
        all_answered = True
        for i in range(len(domains[current_domain])):
            key = f"{current_domain}_{i}"
            if key not in st.session_state.responses:
                all_answered = False
                break
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous"):
                st.session_state.current_page -= 1
                st.rerun()
        with col3:
            if st.session_state.current_page < 4:
                if all_answered:
                    if st.button("Next →", type="primary"):
                        st.session_state.current_page += 1
                        st.rerun()
                else:
                    st.button("Next →", type="primary", disabled=True)
                    st.warning("⚠️ Please answer all questions before proceeding to the next domain.")
            else:
                if all_answered:
                    if st.button("View Results →", type="primary"):
                        st.session_state.current_page = 5
                        st.rerun()
                else:
                    st.button("View Results →", type="primary", disabled=True)
                    st.warning("⚠️ Please answer all questions before viewing results.")

    # Results page
    elif st.session_state.current_page == 5:
        st.header("📊 Assessment Results")
        st.subheader(f"Sector: {st.session_state.responses.get('sector', 'Not specified')}")
        
        # Calculate scores for each domain
        domain_scores = {}
        for domain_name in domains.keys():
            total_score = 0
            for i in range(len(domains[domain_name])):
                key = f"{domain_name}_{i}"
                total_score += st.session_state.responses.get(key, 0)
            domain_scores[domain_name] = total_score
        
        # Display overall summary
        st.markdown("### Overall Summary")
        total_possible = 40 * 4  # 40 points per domain, 4 domains
        total_achieved = sum(domain_scores.values())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Score", f"{total_achieved}/{total_possible}")
        with col2:
            st.metric("Overall Percentage", f"{(total_achieved/total_possible*100):.1f}%")
        with col3:
            avg_score = total_achieved / 4
            st.metric("Average per Domain", f"{avg_score:.1f}/40")
        
        st.markdown("---")
        
        # Display domain-by-domain results
        st.markdown("### Results by Domain")
        
        question_num = 1
        for domain_name, score in domain_scores.items():
            with st.expander(f"**{domain_name}**: {score}/40 ({score/40*100:.1f}%)"):
                st.progress(score/40)
                
                # Show individual benchmark scores
                st.markdown("**Individual Benchmarks:**")
                for i, benchmark in enumerate(domains[domain_name]):
                    key = f"{domain_name}_{i}"
                    rating = st.session_state.responses.get(key, 0)
                    st.write(f"**Q{question_num}.** {benchmark}")
                    st.write(f"**Rating:** {rating} - {rating_options[rating]}")
                    st.markdown("")
                    question_num += 1
        
        st.markdown("---")
        
        # Save response button
        st.markdown("### 💾 Save Your Response")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Save Response to Database", type="primary"):
                if save_response(dict(st.session_state.responses)):
                    st.success("✅ Response saved successfully!")
                else:
                    st.error("❌ Failed to save response. Please try again.")
        
        st.markdown("---")
        
        # Download individual results
        st.markdown("### 📥 Export Your Results")
        
        # Prepare data for export
        export_data = []
        export_data.append(["SNV Four Domains Technical Expertise Benchmarking Results"])
        export_data.append(["Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        export_data.append(["Sector", st.session_state.responses.get('sector', 'Not specified')])
        export_data.append([])
        export_data.append(["Question #", "Domain", "Benchmark", "Rating", "Rating Description"])
        
        question_num = 1
        for domain_name in domains.keys():
            for i, benchmark in enumerate(domains[domain_name]):
                key = f"{domain_name}_{i}"
                rating = st.session_state.responses.get(key, 0)
                export_data.append([f"Q{question_num}", domain_name, benchmark, rating, rating_options[rating]])
                question_num += 1
        
        export_data.append([])
        export_data.append(["Summary"])
        for domain_name, score in domain_scores.items():
            export_data.append([domain_name, f"{score}/40", f"{score/40*100:.1f}%"])
        
        export_data.append([])
        export_data.append(["Total Score", f"{total_achieved}/160", f"{total_achieved/160*100:.1f}%"])
        
        df_export = pd.DataFrame(export_data)
        csv = df_export.to_csv(index=False, header=False)
        
        st.download_button(
            label="📄 Download Your Results as CSV",
            data=csv,
            file_name=f"snv_benchmarking_{st.session_state.responses.get('sector', 'sector')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Assessment"):
                st.session_state.current_page = 4
                st.rerun()
        with col2:
            if st.button("🔄 Start New Assessment"):
                st.session_state.clear()
                st.rerun()
