import streamlit as st

def run_survey():
    # Page configuration
    st.set_page_config(
        page_title="SNV Four Domains Technical Expertise Benchmarking",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7fa;
        }
        .stButton>button {
            width: 100%;
            background-color: #0066cc;
            color: white;
            font-size: 18px;
            padding: 12px;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #0052a3;
        }
        .domain-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 10px; margin-bottom: 30px;'>
            <h1 style='color: white; margin: 0;'>📊 SNV Four Domains Technical Expertise</h1>
            <h2 style='color: white; margin: 10px 0;'>Country Benchmarking Exercise</h2>
            <p style='color: #f0f0f0; font-size: 16px;'>Self-scoring assessment across four key domains</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar with information
    with st.sidebar:
        st.markdown("### 🌍 Select Country")
        country = st.selectbox(
            "Choose your country:",
            ["Select a country", "Bangladesh", "Benin", "Bhutan", "Burkina Faso" ,"Burundi", "Cambodia", "Ethiopia", "Ghana", "Indonesia", "Kenya", "Lao PDR", "Mali", "Mozambique" , "Nepal" ,"Niger", "Nigeria", "Rwanda" , "South Sudan" , "Tanzania" , "Uganda" , "Vietnam" , "Zambia" , "Zimbabwe"],
            index=0
        )
        
        st.markdown("---")
        
        st.markdown("### 📋 About This Survey")
        st.write("""
        This benchmarking exercise evaluates your country portfolio across four interconnected domains 
        of Technical Expertise at SNV.
        """)
        
        st.markdown("### 🎯 The Four Domains")
        st.write("""
        1. **Positioning, Influencing & Strategic Collaboration**
        2. **Business Development & Partnerships**
        3. **Knowledge Development & Teams Capacity**
        4. **People & Project Management**
        """)
        
        st.markdown("### 📏 Rating Scale")
        st.write("""
        - **0** - Non-existent
        - **1** - Incipient
        - **2** - Basic
        - **3** - Advanced
        - **4** - Full-fledged
        """)

    # Define all survey data
    domains = {
        "Domain 1: Positioning, Influencing & Strategic Collaboration": [
            "1. Understand the overall Country/Sector system and Themes (key national development targets, policies and programmes, market dynamics, main challenges and opportunities, critical stakeholders, power issues, etc)?",
            "2. Have clear systems transformation ambitions (above and beyond projects), including on what issues to contribute to, what is the desired outcome, what processes are critical to influence and how?",
            "3. Follow up and intentionally contribute to key Country/Sector processes and debates (technical working groups, industry standards reviews, investment groups, planning cycles, policy and planning reviews, etc)?",
            "4. Have a good positioning (access, credibility and voice) in key platforms/debates/public forums relevant to its Systems Transformation agenda?",
            "5. Use robust evidence (projects data, track record, lessons learned, etc) in its Influencing efforts to relevant debates and processes?",
            "6. Go beyond the country footprint and uses also SNV's global footprint and expertise to strengthen its contribution to debates (global sector strategies, core themes position papers, knowledge documents, evidence from other countries, etc)?",
            "7. Strategically partner with like minded institutions, also informally, to amplify influencing efforts and pursue shared ambitions?",
            "8. Deliberately use its access and influence to facilitate the participation of local partners (including representatives of vulnerable groups), as opposed to speaking on their behalf?",
            "9. Monitors the progress it is making in moving towards its Systems Transformation ambitions, and aptly and timely adapts its positioning to remain relevant in an ever evolving context?",
            "10. Is intentionally seeking to fund positioning and influencing work in its project design and budgeting efforts (donor allowing)?"
        ],
        "Domain 2: Business Development & Partnerships": [
            "1. Strategically use its presence in relevant spaces and its relationships to strengthen its competitive edge (strong position and reputation, credibility to influence the donors' agenda, adequate showcase of its technical capacity, footprint and track record)?",
            "2. Have a deep understanding of the donor landscape in country and its trends -- including by nurturing (also informal) relationships with current and potential donors in country (including emerging ones)?",
            "3. Have the ability to capture donor intelligence timely, including 'unwritten' information?",
            "4. Have knowledge about key competitors/potential partners, including an understanding of their profiles and of their competitive advantage in relation to SNV and of SNV's competitive advantage in relation to them?",
            "5. Have strong relationships with local partners that enable it to easily mobilize them and closely work with them on BD opportunities (as opposed to reactively seeking partners when an opportunity arises)?",
            "6. Use an opportunity-cost/decision making mechanism to critically assess opportunities and decide on which ones to invest in in a focused and timely manner (as opposed to responding to any)?",
            "7. Have capacity to contextualize Global expertise (Sector Framework Approaches, Core Themes positioning papers, track records, lessons learned, etc) to the country's realities and to what the donors require - including the capacity to 'package' a proposal to fit with the terminology, priorities and preferred approaches of the donor?",
            "8. Have access to the Global Technical Expertise support it requires to complement/enhance the BD capacity in country (in addition to the technical quality of the proposals)?",
            "9. Have MEL systems (including staff) that are able to generate evidence of its capacity, track record, innovations/lessons learned to use in proposal development?",
            "10. Have a practice of consistently seeking feedback from donors - to learn from both successful and failed proposal submissions?"
        ],
        "Domain 3: Knowledge Development & Teams Capacity Enhancement": [
            "1. Have awareness of the Knowledge status (trends/hot topics, state of the art knowledge, key learning questions, main KD players), nationally and internationally, relevant for the sectors and themes work in its portfolio?",
            "2. Have an understanding of its portfolio strengths and gaps in relation to the current knowledge status on issues relevant to its work?",
            "3. Proactively seek to advance Knowledge relevant for its portfolio work (sectors AND themes) by engaging with Global Teams and learning from the practice and research of others (including academia) nationally, regionally and/or globally?",
            "4. Promote cross-sectorial learning and a deeper integration of core themes across the entire portfolio, in line with those broader Knowledge Development ambitions?",
            "5. Periodically assesses project results and team insights (data sense making, lessons learned, failures, etc) to critically interrogate approaches, technical solutions and/or methodologies used across the portfolio, so as to further develop and update them?",
            "6. Have a practice to identify, nurture, validate and document for sharing (also with Global teams) innovation emerging from its work practice?",
            "7. Deliberately seeks to learn from and to contribute to SNV's Global knowledge development (including through cross-country engagements/mechanisms)?",
            "8. Have a practice of deliberately engaging with Local Partners to jointly advance Knowledge, creating opportunities for mutual learning and expertise growth?",
            "9. Have a mechanism to identify and address the Technical Teams' learning needs (including soft skills)?",
            "10. Have a standard practice of integrating, to the extent possible (considering size, scope and budget), KD objectives and Teams capacity development objectives in project's design and budgeting?"
        ],
        "Domain 4: People & Project Management": [
            "1. Align projects with Sector Framework Approaches and Core Themes (as possible, considering the scope), or at the very least with their key principles, for enhanced coherence and branding of 'SNV's Technical Expertise and way of working'?",
            "2. Steer projects for quality, systems change, local partners empowerment, and sustainability (in addition to planned results and compliance with donor requirements)?",
            "3. Have MEL frameworks that track progress and evaluate outcome and impact achievements (as opposed to just outputs) and that have also (relevant) core themes indicators?",
            "4. Have capacity for sense making of MEL data (ability to identify the causal relationship between progress recorded and the work conducted by the project and/or contextual factors)?",
            "5. Use an adaptive management approach (fostering a mindset of critically interrogating projects' progress and the introduction of changes as relevant and possible, in dialogue with the donor when needed)?",
            "6. Have a practice of mobilizing Global Technical Expertise to support in country project delivery, as relevant?",
            "7. Recognize project implementation as a multi-pooling of capacities (not just the technical teams but also financial, procurement, logistics, HR) with lines of accountability established accordingly?",
            "8. Practice downward accountability of country management and technical leadership, with these accountable for how much teams feedback on projects' progress is considered and acted on, and on how much teams feel valued?",
            "9. Have a mechanism that acknowledges and strives to build diverse skill sets in the technical teams, in addition to 'pure' technical expertise, namely soft skills (facilitating, influencing, advocating, etc)?",
            "10. Manages for talent retention, including recognition of performance and a plan for the 'in between projects' gaps?"
        ]
    }

    rating_options = ["0 - Non-existent", "1 - Incipient", "2 - Basic", "3 - Advanced", "4 - Full-fledged"]
    
    # Store all responses
    all_responses = {}
    
    # Create tabs for each domain
    tabs = st.tabs(list(domains.keys()))
    
    for tab_idx, (domain_name, questions) in enumerate(domains.items()):
        with tabs[tab_idx]:
            st.markdown(f"<div class='domain-header'><h3>{domain_name}</h3></div>", unsafe_allow_html=True)
            
            domain_responses = {}
            for question in questions:
                response = st.radio(
                    question,
                    rating_options,
                    key=f"{domain_name}_{question}",
                    index=None,
                    horizontal=True
                )
                domain_responses[question] = response
            
            all_responses[domain_name] = domain_responses

    st.divider()

    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.button("📊 Submit Benchmarking Assessment", type="primary", use_container_width=True)

    if submit_button:
        # Check if country is selected
        if country == "Select a country":
            st.error("⚠️ Please select a country before submitting.")
            return
        
        # Check if all questions are answered
        all_answered = all(
            all(response is not None for response in domain_responses.values())
            for domain_responses in all_responses.values()
        )
        
        if not all_answered:
            st.error("⚠️ Please answer all questions in all domains before submitting.")
        else:
            # Calculate scores
            domain_scores = {}
            total_score = 0
            max_possible = len(domains) * 10 * 4  # 4 domains × 10 questions × 4 max points
            
            for domain_name, domain_responses in all_responses.items():
                domain_score = sum(int(response.split(" - ")[0]) for response in domain_responses.values())
                domain_scores[domain_name] = domain_score
                total_score += domain_score
            
            percentage = (total_score / max_possible) * 100

            # Display results
            st.success(f"✅ Benchmarking assessment for **{country}** submitted successfully!")
            st.markdown("---")
            
            # Overall results
            st.markdown(f"### 📊 Overall Results - {country}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Score", f"{total_score}/{max_possible}")
            with col2:
                st.metric("Percentage", f"{percentage:.1f}%")
            with col3:
                if percentage >= 75:
                    st.metric("Status", "Advanced", delta="Strong Performance")
                elif percentage >= 50:
                    st.metric("Status", "Developing", delta="Good Progress")
                else:
                    st.metric("Status", "Emerging", delta="Building Foundation")
            
            st.progress(percentage / 100)
            
            # Domain breakdown
            st.markdown("---")
            st.markdown("### 📈 Domain Breakdown")
            
            cols = st.columns(2)
            for idx, (domain_name, score) in enumerate(domain_scores.items()):
                with cols[idx % 2]:
                    domain_percentage = (score / 40) * 100
                    st.markdown(f"**{domain_name.split(':')[1].strip()}**")
                    st.metric("Score", f"{score}/40", f"{domain_percentage:.0f}%")
                    st.progress(domain_percentage / 100)
            
            # Detailed responses
            st.markdown("---")
            st.markdown("### 📝 Detailed Responses")
            
            for domain_name, domain_responses in all_responses.items():
                with st.expander(f"**{domain_name}**"):
                    for question, answer in domain_responses.items():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.write(question)
                        with col2:
                            st.write(f"**{answer.split(' - ')[0]}** - {answer.split(' - ')[1]}")
                        st.divider()
            
            # Recommendations
            st.markdown("---")
            st.markdown("### 💡 Recommendations")
            
            if percentage >= 75:
                st.success("""
                **Excellent Performance!** Your country portfolio demonstrates strong technical expertise across all domains. 
                Continue to maintain and build upon these strengths while identifying opportunities for innovation and leadership.
                """)
            elif percentage >= 50:
                st.info("""
                **Good Progress!** Your portfolio shows solid development across the domains. 
                Focus on strengthening areas with lower scores and sharing best practices from high-performing domains.
                """)
            else:
                st.warning("""
                **Building Foundation!** There are significant opportunities for growth. 
                Consider prioritizing capacity development and seeking support from Global Office teams and cross-country exchanges.
                """)
            
            # Download results
            st.markdown("---")
            results_text = f"""SNV Four Domains Technical Expertise Benchmarking Results
{'='*60}

Country: {country}
Overall Score: {total_score}/{max_possible} ({percentage:.1f}%)

Domain Scores:
"""
            for domain_name, score in domain_scores.items():
                results_text += f"\n{domain_name}: {score}/40 ({(score/40)*100:.0f}%)"
            
            results_text += "\n\nDetailed Responses:\n" + "="*60 + "\n"
            
            for domain_name, domain_responses in all_responses.items():
                results_text += f"\n\n{domain_name}\n{'-'*60}\n"
                for question, answer in domain_responses.items():
                    results_text += f"\n{question}\n→ {answer}\n"
            
            st.download_button(
                label="📥 Download Complete Results",
                data=results_text,
                file_name=f"snv_benchmarking_results_{country.lower()}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    run_survey()

