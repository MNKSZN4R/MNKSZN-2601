import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="SNV Four Domains Benchmarking", layout="wide")

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# Title and introduction
st.title("🌍 SNV Four Domains Technical Expertise Benchmarking Exercise")

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

# Sector selection page
if st.session_state.current_page == 0:
    st.header("📋 Sector Selection")
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
        key="sector"
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
    
    st.header(f"Domain {domain_index + 1}: {current_domain}")
    st.subheader(f"Sector: {st.session_state.responses.get('sector', 'Not specified')}")
    
    # Progress indicator
    progress = (st.session_state.current_page) / 5
    st.progress(progress)
    st.write(f"Progress: {st.session_state.current_page}/5")
    
    st.markdown("---")
    st.markdown("**Rate each benchmark from 0 (Non-existent) to 4 (Full-fledged)**")
    st.markdown("---")
    
    # Display benchmarks for current domain
    for i, benchmark in enumerate(domains[current_domain]):
        st.markdown(f"**Benchmark {i+1}:**")
        st.write(benchmark)
        
        key = f"{current_domain}_{i}"
        rating = st.radio(
            "Rating:",
            options=list(rating_options.keys()),
            format_func=lambda x: f"{x} - {rating_options[x]}",
            key=key,
            index=st.session_state.responses.get(key, 0),
            horizontal=True
        )
        st.session_state.responses[key] = rating
        st.markdown("---")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Previous"):
            st.session_state.current_page -= 1
            st.rerun()
    with col3:
        if st.session_state.current_page < 4:
            if st.button("Next →", type="primary"):
                st.session_state.current_page += 1
                st.rerun()
        else:
            if st.button("View Results →", type="primary"):
                st.session_state.current_page = 5
                st.rerun()

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
    
    for domain_name, score in domain_scores.items():
        with st.expander(f"**{domain_name}**: {score}/40 ({score/40*100:.1f}%)"):
            st.progress(score/40)
            
            # Show individual benchmark scores
            st.markdown("**Individual Benchmarks:**")
            for i, benchmark in enumerate(domains[domain_name]):
                key = f"{domain_name}_{i}"
                rating = st.session_state.responses.get(key, 0)
                st.write(f"{i+1}. {benchmark}")
                st.write(f"   **Rating:** {rating} - {rating_options[rating]}")
                st.markdown("")
    
    st.markdown("---")
    
    # Download results
    st.markdown("### Export Results")
    
    # Prepare data for export
    export_data = []
    export_data.append(["SNV Four Domains Technical Expertise Benchmarking Results"])
    export_data.append(["Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    export_data.append(["Sector", st.session_state.responses.get('sector', 'Not specified')])
    export_data.append([])
    export_data.append(["Domain", "Benchmark", "Rating", "Rating Description"])
    
    for domain_name in domains.keys():
        for i, benchmark in enumerate(domains[domain_name]):
            key = f"{domain_name}_{i}"
            rating = st.session_state.responses.get(key, 0)
            export_data.append([domain_name, benchmark, rating, rating_options[rating]])
    
    export_data.append([])
    export_data.append(["Summary"])
    for domain_name, score in domain_scores.items():
        export_data.append([domain_name, f"{score}/40", f"{score/40*100:.1f}%"])
    
    df_export = pd.DataFrame(export_data)
    csv = df_export.to_csv(index=False, header=False)
    
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name=f"snv_benchmarking_{st.session_state.responses.get('sector', 'sector')}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
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