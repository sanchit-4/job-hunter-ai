# # # # import streamlit as st
# # # # import requests
# # # # import time
# # # # import json

# # # # # --- CONFIG ---
# # # # API_URL = "http://127.0.0.1:8000/api/v1"
# # # # st.set_page_config(page_title="JobHunterAI", page_icon="🚀", layout="wide")

# # # # # --- CUSTOM CSS ---
# # # # st.markdown("""
# # # # <style>
# # # #     /* Global Font & Colors */
# # # #     .stApp {
# # # #         background-color: #f8f9fa;
# # # #         color: #212529;
# # # #     }
    
# # # #     /* Header Styling */
# # # #     .main-header {
# # # #         font-size: 2.5rem;
# # # #         font-weight: 700;
# # # #         color: #1a73e8;
# # # #         margin-bottom: 0.5rem;
# # # #     }
# # # #     .sub-header {
# # # #         font-size: 1.1rem;
# # # #         color: #6c757d;
# # # #         margin-bottom: 2rem;
# # # #     }

# # # #     /* Card Styling */
# # # #     .result-card {
# # # #         background-color: white;
# # # #         padding: 20px;
# # # #         border-radius: 10px;
# # # #         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
# # # #         margin-bottom: 20px;
# # # #         border-left: 5px solid #1a73e8;
# # # #     }

# # # #     /* Skill Tags */
# # # #     .skill-badge {
# # # #         display: inline-block;
# # # #         background-color: #e8f0fe;
# # # #         color: #1a73e8;
# # # #         padding: 5px 12px;
# # # #         border-radius: 15px;
# # # #         font-size: 0.9em;
# # # #         font-weight: 600;
# # # #         margin: 4px;
# # # #         border: 1px solid #d2e3fc;
# # # #     }

# # # #     /* Status Indicators */
# # # #     .status-box {
# # # #         padding: 15px;
# # # #         border-radius: 8px;
# # # #         margin-bottom: 20px;
# # # #         font-weight: bold;
# # # #     }
# # # #     .status-success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
# # # #     .status-error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
# # # #     .status-processing { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }

# # # # </style>
# # # # """, unsafe_allow_html=True)

# # # # # --- SIDEBAR ---
# # # # with st.sidebar:
# # # #     st.title("⚡ JobHunterAI")
# # # #     st.markdown("Your autonomous career agent.")
# # # #     st.markdown("---")
    
# # # #     with st.expander("📝 Your Master Resume", expanded=True):
# # # #         default_resume = """Sanchit
# # # # Python Backend Engineer | 5 Years Experience

# # # # Skills: Python, Django, FastAPI, Docker, Kubernetes, AWS, PostgreSQL, Redis.

# # # # Experience:
# # # # - Senior Engineer at TechCorp: Built microservices handling 10k RPS. Optimized SQL queries reducing load by 40%.
# # # # - Developer at StartupX: Implemented CI/CD pipelines and automated scraping tools using Playwright.
# # # # """
# # # #         resume_text = st.text_area("Edit Resume", value=default_resume, height=300)
    
# # # #     st.markdown("---")
# # # #     st.caption("v1.0.0 | Powered by Gemini Pro")


# # # # # --- MAIN CONTENT ---
# # # # st.markdown('<div class="main-header">Job Application Agent</div>', unsafe_allow_html=True)
# # # # st.markdown('<div class="sub-header">Paste a job link below. I will scrape it, analyze it, and write your application.</div>', unsafe_allow_html=True)

# # # # # Input Section
# # # # col1, col2 = st.columns([3, 1])
# # # # with col1:
# # # #     job_url = st.text_input("Job Posting URL", placeholder="https://www.ycombinator.com/jobs/...", label_visibility="collapsed")
# # # # with col2:
# # # #     apply_btn = st.button("🚀 Generate Application", use_container_width=True, type="primary")

# # # # # --- APP LOGIC ---
# # # # if apply_btn:
# # # #     if not job_url:
# # # #         st.toast("⚠️ Please enter a valid URL")
# # # #     else:
# # # #         # 1. Start Application
# # # #         with st.status("🤖 AI Agent Working...", expanded=True) as status:
# # # #             st.write("🌐 Connecting to Server...")
# # # #             try:
# # # #                 payload = {"url": job_url, "original_resume_text": resume_text}
# # # #                 response = requests.post(f"{API_URL}/apply", json=payload)
                
# # # #                 if response.status_code == 200:
# # # #                     job_id = response.json()['id']
# # # #                     st.write("🕷️ Scraping Job Description...")
                    
# # # #                     # 2. Polling Loop
# # # #                     progress_bar = st.progress(0)
# # # #                     for i in range(60): # 60 seconds timeout
# # # #                         time.sleep(1)
# # # #                         res = requests.get(f"{API_URL}/jobs/{job_id}")
# # # #                         data = res.json()
# # # #                         state = data['status']
                        
# # # #                         if state == "SUCCESS":
# # # #                             progress_bar.progress(100)
# # # #                             status.update(label="✅ Application Ready!", state="complete", expanded=False)
# # # #                             break
# # # #                         elif "FAILED" in state:
# # # #                             status.update(label="❌ Application Failed", state="error")
# # # #                             st.error(f"Error: {state}")
# # # #                             st.stop()
# # # #                         else:
# # # #                             # Fake progress for visual feedback
# # # #                             prog = min(90, i * 5)
# # # #                             progress_bar.progress(prog)
# # # #                             if i == 5: st.write("🧠 Analyzing requirements...")
# # # #                             if i == 15: st.write("✍️ Drafting cover letter...")
# # # #                             if i == 25: st.write("🎨 Formatting PDF...")

# # # #                     # --- RESULTS DISPLAY ---
                    
# # # #                     # A. Cover Letter Tab
# # # #                     tab1, tab2, tab3 = st.tabs(["📄 Cover Letter", "📊 Resume Strategy", "📥 Downloads"])
                    
# # # #                     with tab1:
# # # #                         st.markdown('<div class="result-card">', unsafe_allow_html=True)
# # # #                         st.markdown(data.get('cover_letter', 'No cover letter generated.'))
# # # #                         st.markdown('</div>', unsafe_allow_html=True)

# # # #                     # B. Strategy Tab (Visualized, NO JSON)
# # # #                     with tab2:
# # # #                         content = data.get('tailored_resume_content', {})
                        
# # # #                         # Summary
# # # #                         st.subheader("🎯 Tailored Summary")
# # # #                         st.info(content.get('professional_summary', ''))
                        
# # # #                         # Skills (Badges)
# # # #                         st.subheader("🔑 Keywords Matched")
# # # #                         skills = content.get('skills', [])
# # # #                         if skills:
# # # #                             skill_html = "".join([f'<span class="skill-badge">{s}</span>' for s in skills])
# # # #                             st.markdown(f"<div>{skill_html}</div>", unsafe_allow_html=True)
                        
# # # #                         # Experience (Expanders)
# # # #                         st.subheader("💼 Experience Rewrite")
# # # #                         for company, bullets in content.get('experience_bullets', {}).items():
# # # #                             with st.expander(f"**{company}**", expanded=True):
# # # #                                 for b in bullets:
# # # #                                     st.markdown(f"- {b}")

# # # #                     # C. Download Tab
# # # #                     with tab3:
# # # #                         col_d1, col_d2 = st.columns(2)
# # # #                         with col_d1:
# # # #                             st.success("PDF Generated Successfully")
# # # #                             # In a real deployed app, you'd serve the file via API. 
# # # #                             # For local, we just tell them where it is.
# # # #                             st.markdown(f"**File Location:**")
# # # #                             st.code(f"generated_applications/{job_id}.pdf")
                        
# # # #                         with col_d2:
# # # #                             # Show Raw Data only if requested
# # # #                             with st.expander("View Raw JSON Data"):
# # # #                                 st.json(data)

# # # #                 else:
# # # #                     st.error(f"Server Error: {response.text}")
# # # #             except Exception as e:
# # # #                 st.error(f"Connection Error: {e}")



# # # import streamlit as st
# # # import requests
# # # import time
# # # import json

# # # # --- CONFIG ---
# # # API_URL = "http://127.0.0.1:8000/api/v1"
# # # st.set_page_config(
# # #     page_title="JobHunter",
# # #     page_icon="⚡",
# # #     layout="wide",
# # #     initial_sidebar_state="auto"
# # # )

# # # # --- CUSTOM CSS (DARK MODE & RESPONSIVE) ---
# # # st.markdown("""
# # # <style>
# # #     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

# # #     /* --- BASE THEME --- */
# # #     .stApp {
# # #         background-color: #0F172A; /* Slate 900 */
# # #         font-family: 'Inter', sans-serif;
# # #         color: #E2E8F0; /* Slate 200 */
# # #     }
    
# # #     /* HIDE BLOAT */
# # #     #MainMenu {visibility: hidden;}
# # #     footer {visibility: hidden;}
# # #     header {visibility: hidden;}
    
# # #     /* --- HERO --- */
# # #     .hero-container {
# # #         text-align: center;
# # #         padding: 40px 0 30px 0;
# # #     }
# # #     .hero-title {
# # #         font-size: 3.5rem;
# # #         font-weight: 800;
# # #         background: -webkit-linear-gradient(45deg, #818CF8, #38BDF8);
# # #         -webkit-background-clip: text;
# # #         -webkit-text-fill-color: transparent;
# # #         margin-bottom: 10px;
# # #     }
# # #     .hero-subtitle {
# # #         font-size: 1.1rem;
# # #         color: #94A3B8;
# # #         font-weight: 400;
# # #     }

# # #     /* --- INPUTS --- */
# # #     div[data-testid="stTextInput"] input {
# # #         background-color: #1E293B;
# # #         color: #F8FAFC;
# # #         border-radius: 12px;
# # #         border: 1px solid #334155;
# # #         padding: 16px;
# # #         font-size: 1rem;
# # #     }
# # #     div[data-testid="stTextInput"] input:focus {
# # #         border-color: #818CF8;
# # #     }

# # #     /* --- BUTTONS --- */
# # #     div.stButton > button {
# # #         background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
# # #         color: white;
# # #         font-weight: 600;
# # #         padding: 18px 25px;
# # #         border-radius: 12px;
# # #         border: none;
# # #         width: 100%;
# # #         margin-top: 2px;
# # #     }
# # #     div.stButton > button:hover {
# # #         transform: translateY(-2px);
# # #         color: white;
# # #     }

# # #     /* --- RESULTS CARD (FIXED) --- */
# # #     /* This was the source of the weird box. We now style the container properly */
# # #     .paper-card {
# # #         background: #1E293B;
# # #         border-radius: 16px;
# # #         padding: 30px;
# # #         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
# # #         border: 1px solid #334155;
# # #         margin-top: 10px;
# # #     }
    
# # #     .cover-letter-text {
# # #         font-family: 'Inter', sans-serif;
# # #         font-size: 1rem;
# # #         line-height: 1.7;
# # #         color: #CBD5E1;
# # #         white-space: pre-wrap; /* Preserves formatting */
# # #     }

# # #     /* --- TAGS & BADGES --- */
# # #     .skill-tag {
# # #         display: inline-flex;
# # #         background-color: #312E81;
# # #         color: #A5B4FC;
# # #         padding: 5px 12px;
# # #         border-radius: 20px;
# # #         font-size: 0.8rem;
# # #         font-weight: 600;
# # #         margin: 0 6px 6px 0;
# # #         border: 1px solid #4338CA;
# # #     }

# # #     /* --- STATUS & SIDEBAR --- */
# # #     div[data-testid="stStatusWidget"] {
# # #         background-color: #1E293B;
# # #         border: 1px solid #334155;
# # #         color: #E2E8F0;
# # #     }
    
# # #     section[data-testid="stSidebar"] {
# # #         background-color: #020617;
# # #         border-right: 1px solid #1E293B;
# # #     }
    
# # #     /* Expander styling */
# # #     .streamlit-expanderHeader {
# # #         background-color: #1E293B !important;
# # #         color: #E2E8F0 !important;
# # #         border-radius: 8px;
# # #     }
# # #     div[data-testid="stExpanderDetails"] {
# # #         background-color: #0F172A;
# # #         border: 1px solid #1E293B;
# # #         border-top: none;
# # #     }

# # #     /* --- DOWNLOAD BOX --- */
# # #     .download-box {
# # #         background: #064E3B;
# # #         border: 1px solid #059669;
# # #         color: #D1FAE5;
# # #         padding: 15px;
# # #         border-radius: 12px;
# # #         display: flex;
# # #         align-items: center;
# # #         gap: 15px;
# # #         margin-top: 20px;
# # #     }
    
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # --- SIDEBAR ---
# # # with st.sidebar:
# # #     st.markdown("### ⚙️ Configuration")
# # #     default_resume = """Sanchit
# # # Python Backend Engineer | 5 Years Experience

# # # Skills: Python, Django, FastAPI, Docker, Kubernetes, AWS, PostgreSQL, Redis.

# # # Experience:
# # # - Senior Engineer at TechCorp: Built microservices handling 10k RPS. Optimized SQL queries reducing load by 40%.
# # # - Developer at StartupX: Implemented CI/CD pipelines and automated scraping tools using Playwright.
# # # """
# # #     resume_text = st.text_area("Master Resume", value=default_resume, height=400)
# # #     st.markdown("---")
# # #     st.caption("JobHunter v2.2 • Dark Mode")

# # # # --- HERO SECTION ---
# # # st.markdown("""
# # # <div class="hero-container">
# # #     <div class="hero-title">JobHunter AI</div>
# # #     <div class="hero-subtitle">Autonomous Application Agent</div>
# # # </div>
# # # """, unsafe_allow_html=True)

# # # # --- INPUT SECTION ---
# # # c1, c2, c3 = st.columns([1, 6, 1])
# # # with c2:
# # #     col_input, col_btn = st.columns([5, 1])
# # #     with col_input:
# # #         job_url = st.text_input("Job URL", placeholder="Paste job link here...", label_visibility="collapsed")
# # #     with col_btn:
# # #         apply_btn = st.button("Analyze", type="primary")

# # # # --- APP LOGIC ---
# # # if apply_btn:
# # #     if not job_url:
# # #         st.toast("⚠️ Please enter a valid URL.")
# # #     else:
# # #         status_container = st.empty()
        
# # #         with status_container.status("🚀 Initializing...", expanded=True) as status:
# # #             try:
# # #                 # 1. Connect
# # #                 st.write("🔌 Connecting to backend...")
# # #                 payload = {"url": job_url, "original_resume_text": resume_text}
# # #                 response = requests.post(f"{API_URL}/apply", json=payload)
                
# # #                 if response.status_code == 200:
# # #                     job_data = response.json()
# # #                     job_id = job_data['id']
                    
# # #                     # 2. Polling Loop
# # #                     prog_bar = st.progress(0)
# # #                     step_descriptions = [
# # #                         "🕷️ Accessing job portal...", 
# # #                         "🧠 Analyzing requirements...", 
# # #                         "✨ Matching skills...", 
# # #                         "✍️ Writing cover letter...", 
# # #                         "🎨 Rendering PDF..."
# # #                     ]
                    
# # #                     for i in range(60):
# # #                         time.sleep(1)
# # #                         res = requests.get(f"{API_URL}/jobs/{job_id}")
# # #                         data = res.json()
# # #                         state = data['status']
                        
# # #                         # Progress Logic
# # #                         idx = min(len(step_descriptions) - 1, int(i / 8))
# # #                         status.update(label=f"**{state}**: {step_descriptions[idx]}")
                        
# # #                         if state == "SUCCESS":
# # #                             prog_bar.progress(100)
# # #                             # Collapse status to show results immediately
# # #                             status.update(label="✅ Analysis Complete! See results below.", state="complete", expanded=False)
# # #                             break
# # #                         elif "FAILED" in state:
# # #                             status.update(label="❌ Failed", state="error")
# # #                             st.error(f"Error: {state}")
# # #                             st.stop()
# # #                         else:
# # #                             prog_bar.progress(min(95, i * 3))

# # #                     # --- RESULTS VIEW ---
# # #                     st.divider()
# # #                     r_col1, r_col2 = st.columns([1.8, 1])
                    
# # #                     # LEFT COLUMN: COVER LETTER & DOWNLOAD
# # #                     with r_col1:
# # #                         st.markdown("#### 📄 Draft Application")
                        
# # #                         # --- FIX: Single f-string for HTML ---
# # #                         cover_letter = data.get('cover_letter', 'No content.')
# # #                         st.markdown(f"""
# # #                         <div class="paper-card">
# # #                             <div class="cover-letter-text">{cover_letter}</div>
# # #                         </div>
# # #                         """, unsafe_allow_html=True)

# # #                         # PDF Link
# # #                         pdf_path = f"generated_applications/{job_id}.pdf"
# # #                         st.markdown(f"""
# # #                         <div class="download-box">
# # #                             <div style="font-size: 2rem;">📥</div>
# # #                             <div>
# # #                                 <div style="font-weight: bold;">Application Ready</div>
# # #                                 <code style="background:rgba(0,0,0,0.2); color:#D1FAE5; padding:2px 6px; border-radius:4px;">{pdf_path}</code>
# # #                             </div>
# # #                         </div>
# # #                         """, unsafe_allow_html=True)

# # #                     # RIGHT COLUMN: STRATEGY
# # #                     with r_col2:
# # #                         st.markdown("#### 🎯 Strategy Board")
# # #                         content = data.get('tailored_resume_content', {})
                        
# # #                         with st.container():
# # #                             st.caption("PITCH SUMMARY")
# # #                             st.info(content.get('professional_summary', 'Pending...'))
                        
# # #                         st.markdown("###")
# # #                         st.caption("SKILLS DETECTED")
# # #                         skills = content.get('skills', [])
# # #                         if skills:
# # #                             tags_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
# # #                             st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)
                        
# # #                         st.markdown("###")
# # #                         st.caption("RESUME EDITS")
# # #                         # --- FIX: Expanded=True by default ---
# # #                         for company, bullets in content.get('experience_bullets', {}).items():
# # #                             with st.expander(company, expanded=True):
# # #                                 for b in bullets:
# # #                                     st.markdown(f"- {b}")

# # #                 else:
# # #                     st.error(f"Backend Error: {response.text}")
            
# # #             except Exception as e:
# # #                 st.error(f"System Error: {str(e)}")



# # import streamlit as st
# # import requests
# # import time
# # import json
# # from io import BytesIO
# # try:
# #     from pypdf import PdfReader
# # except ImportError:
# #     st.error("Please run: pip install pypdf")

# # # --- CONFIG ---
# # API_URL = "http://127.0.0.1:8000/api/v1"
# # st.set_page_config(
# #     page_title="JobHunter Pro",
# #     page_icon="⚡",
# #     layout="wide",
# #     initial_sidebar_state="collapsed" # Starts collapsed for mobile friendliness
# # )

# # # --- CUSTOM CSS (Responsive & Modern) ---
# # st.markdown("""
# # <style>
# #     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

# #     :root {
# #         --bg-color: #0f172a;
# #         --card-bg: #1e293b;
# #         --text-color: #f1f5f9;
# #         --accent: #6366f1;
# #         --success: #10b981;
# #     }

# #     /* Base Reset */
# #     .stApp {
# #         background-color: var(--bg-color);
# #         font-family: 'Inter', sans-serif;
# #         color: var(--text-color);
# #     }
    
# #     /* Header & Hero */
# #     .hero-section {
# #         text-align: center;
# #         padding: 2rem 1rem;
# #         margin-bottom: 2rem;
# #     }
# #     .hero-title {
# #         font-size: clamp(2rem, 5vw, 3.5rem); /* Responsive Font */
# #         font-weight: 800;
# #         background: linear-gradient(135deg, #818cf8, #38bdf8);
# #         -webkit-background-clip: text;
# #         -webkit-text-fill-color: transparent;
# #         margin-bottom: 0.5rem;
# #     }
# #     .hero-subtitle {
# #         color: #94a3b8;
# #         font-size: clamp(1rem, 2vw, 1.2rem);
# #     }

# #     /* Cards */
# #     .glass-card {
# #         background: rgba(30, 41, 59, 0.7);
# #         backdrop-filter: blur(10px);
# #         border: 1px solid rgba(255, 255, 255, 0.1);
# #         border-radius: 16px;
# #         padding: 1.5rem;
# #         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
# #         height: 100%;
# #     }

# #     /* Typography */
# #     .section-header {
# #         font-size: 0.85rem;
# #         text-transform: uppercase;
# #         letter-spacing: 0.05em;
# #         color: #94a3b8;
# #         font-weight: 600;
# #         margin-bottom: 1rem;
# #         border-bottom: 1px solid #334155;
# #         padding-bottom: 0.5rem;
# #     }

# #     /* Badges */
# #     .skill-pill {
# #         display: inline-block;
# #         background: rgba(99, 102, 241, 0.2);
# #         color: #c7d2fe;
# #         padding: 0.25rem 0.75rem;
# #         border-radius: 9999px;
# #         font-size: 0.8rem;
# #         font-weight: 500;
# #         margin: 0 0.5rem 0.5rem 0;
# #         border: 1px solid rgba(99, 102, 241, 0.3);
# #     }

# #     /* Inputs */
# #     .stTextInput input {
# #         background-color: #020617 !important;
# #         border-color: #334155 !important;
# #         color: white !important;
# #         padding: 1rem;
# #         border-radius: 10px;
# #     }
    
# #     /* Upload Box */
# #     .stFileUploader {
# #         padding: 1rem;
# #         border: 1px dashed #475569;
# #         border-radius: 12px;
# #         background: #020617;
# #     }

# #     /* Buttons */
# #     .stButton button {
# #         background: linear-gradient(to right, #4f46e5, #3b82f6);
# #         border: none;
# #         padding: 0.75rem 1.5rem;
# #         font-weight: 600;
# #         width: 100%;
# #         transition: transform 0.2s;
# #     }
# #     .stButton button:hover {
# #         transform: scale(1.02);
# #     }
    
# #     /* Cover Letter Paper Effect */
# #     .paper {
# #         background: #f8fafc;
# #         color: #1e293b;
# #         padding: 2rem;
# #         border-radius: 4px;
# #         box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
# #         font-family: 'Georgia', serif;
# #         line-height: 1.8;
# #         font-size: 0.95rem;
# #         white-space: pre-wrap;
# #     }

# #     /* Responsive adjustments */
# #     @media (max-width: 768px) {
# #         .paper { padding: 1rem; font-size: 0.9rem; }
# #         .hero-section { padding: 1rem 0; }
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # --- HELPER: PDF PARSER ---
# # def parse_resume(uploaded_file):
# #     try:
# #         reader = PdfReader(uploaded_file)
# #         text = ""
# #         for page in reader.pages:
# #             text += page.extract_text() + "\n"
# #         return text
# #     except Exception as e:
# #         st.error(f"Error reading PDF: {e}")
# #         return None

# # # --- STATE MANAGEMENT ---
# # if 'resume_text' not in st.session_state:
# #     st.session_state['resume_text'] = ""

# # # --- HERO ---
# # st.markdown("""
# #     <div class="hero-section">
# #         <div class="hero-title">JobHunter Pro</div>
# #         <div class="hero-subtitle">The Autonomous AI Agent for Professional Applications</div>
# #     </div>
# # """, unsafe_allow_html=True)

# # # --- MAIN LAYOUT ---
# # # We use a container to keep things centered on large screens
# # main_container = st.container()

# # with main_container:
# #     # --- ROW 1: INPUTS ---
# #     col1, col2 = st.columns([1, 1], gap="large")
    
# #     with col1:
# #         st.markdown('<div class="section-header">1. UPLOAD RESUME</div>', unsafe_allow_html=True)
# #         uploaded_file = st.file_uploader("Drop your PDF resume here", type=['pdf'], label_visibility="collapsed")
        
# #         if uploaded_file is not None:
# #             extracted_text = parse_resume(uploaded_file)
# #             if extracted_text:
# #                 st.session_state['resume_text'] = extracted_text
# #                 st.success("✅ Resume parsed successfully!")
# #                 with st.expander("View Extracted Text"):
# #                     st.text(st.session_state['resume_text'][:500] + "...")
# #         else:
# #             # Fallback manual text
# #             st.session_state['resume_text'] = st.text_area(
# #                 "Or paste resume text manually", 
# #                 value=st.session_state['resume_text'],
# #                 height=150,
# #                 placeholder="Paste text here if you don't have a PDF..."
# #             )

# #     with col2:
# #         st.markdown('<div class="section-header">2. JOB LINK</div>', unsafe_allow_html=True)
# #         job_url = st.text_input("Job URL", placeholder="https://linkedin.com/jobs/...", label_visibility="collapsed")
        
# #         st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
# #         analyze_btn = st.button("🚀 ANALYZE & APPLY", type="primary", use_container_width=True)

# #     # --- ROW 2: RESULTS ---
# #     if analyze_btn:
# #         if not job_url:
# #             st.toast("⚠️ Please enter a Job URL")
# #         elif not st.session_state['resume_text']:
# #             st.toast("⚠️ Please upload a Resume or enter text")
# #         else:
# #             st.divider()
            
# #             # --- PROCESSING UI ---
# #             status_text = st.empty()
# #             progress_bar = st.progress(0)
            
# #             try:
# #                 # 1. API CALL
# #                 status_text.markdown("🔄 **Initializing Agent...**")
# #                 payload = {
# #                     "url": job_url, 
# #                     "original_resume_text": st.session_state['resume_text']
# #                 }
# #                 response = requests.post(f"{API_URL}/apply", json=payload)
                
# #                 if response.status_code == 200:
# #                     job_id = response.json()['id']
                    
# #                     # 2. POLLING LOOP
# #                     steps = [
# #                         ("🕷️ Scraping Job Board...", 10),
# #                         ("🧠 Analyzing Fit...", 30),
# #                         ("💎 Optimizing Keywords...", 50),
# #                         ("✍️ Drafting Application...", 70),
# #                         ("📄 Generating PDF...", 90)
# #                     ]
                    
# #                     for i in range(60):
# #                         time.sleep(1)
# #                         # Fetch Status
# #                         res = requests.get(f"{API_URL}/jobs/{job_id}")
# #                         data = res.json()
# #                         status = data['status']
                        
# #                         # Fake Progress Visualization
# #                         current_prog = progress_bar.progress(min(95, i*2))
                        
# #                         # Update Text based on time
# #                         for txt, thresh in steps:
# #                             if i * 2 > thresh:
# #                                 status_text.markdown(f"**{txt}**")

# #                         if status == "SUCCESS":
# #                             progress_bar.progress(100)
# #                             status_text.success("✅ Application Generated Successfully!")
# #                             time.sleep(1)
# #                             status_text.empty() # Clear status
# #                             progress_bar.empty()
                            
# #                             # --- DISPLAY RESULTS ---
# #                             res_c1, res_c2 = st.columns([1.5, 1], gap="medium")
                            
# #                             # LEFT: COVER LETTER
# #                             with res_c1:
# #                                 st.markdown('<div class="section-header">GENERATED COVER LETTER</div>', unsafe_allow_html=True)
# #                                 cover_letter = data.get('cover_letter', '')
# #                                 st.markdown(f'<div class="paper">{cover_letter}</div>', unsafe_allow_html=True)
                                
# #                                 st.markdown("<br>", unsafe_allow_html=True)
# #                                 st.markdown(f"""
# #                                 <a href="file://generated_applications/{job_id}.pdf" target="_blank" style="text-decoration:none;">
# #                                     <div style="background:#10b981; color:white; padding:15px; border-radius:8px; text-align:center; font-weight:bold;">
# #                                         📥 Download Application Package (PDF)
# #                                         <br>
# #                                         <span style="font-size:0.8em; font-weight:normal; opacity:0.8">Saved at: generated_applications/{job_id}.pdf</span>
# #                                     </div>
# #                                 </a>
# #                                 """, unsafe_allow_html=True)

# #                             # RIGHT: RESUME ANALYSIS
# #                             with res_c2:
# #                                 st.markdown('<div class="section-header">RESUME OPTIMIZATION</div>', unsafe_allow_html=True)
# #                                 content = data.get('tailored_resume_content', {})
                                
# #                                 with st.container():
# #                                     st.markdown('<div class="glass-card">', unsafe_allow_html=True)
# #                                     st.caption("UPDATED PROFESSIONAL SUMMARY")
# #                                     st.info(content.get('professional_summary', ''))
                                    
# #                                     st.caption("MATCHED KEYWORDS")
# #                                     skills = content.get('skills', [])
# #                                     if skills:
# #                                         html = "".join([f'<span class="skill-pill">{s}</span>' for s in skills])
# #                                         st.markdown(html, unsafe_allow_html=True)
# #                                     st.markdown('</div>', unsafe_allow_html=True)
                                
# #                                 st.markdown("<br>", unsafe_allow_html=True)
                                
# #                                 with st.container():
# #                                     st.markdown('<div class="glass-card">', unsafe_allow_html=True)
# #                                     st.caption("EXPERIENCE BULLET POINTS")
# #                                     for company, bullets in content.get('experience_bullets', {}).items():
# #                                         with st.expander(company):
# #                                             for b in bullets:
# #                                                 st.markdown(f"• {b}")
# #                                     st.markdown('</div>', unsafe_allow_html=True)
                            
# #                             break # Exit Loop
                        
# #                         elif "FAILED" in status:
# #                             st.error(f"Process Failed: {status}")
# #                             break
# #                 else:
# #                     st.error(f"Server Error: {response.text}")
# #             except Exception as e:
# #                 st.error(f"Connection Error: {e}")



# import streamlit as st
# import requests
# import time
# import json
# from io import BytesIO

# # Try to import PDF Reader
# try:
#     from pypdf import PdfReader
# except ImportError:
#     st.error("Missing dependency. Please run: pip install pypdf")

# # --- CONFIG ---
# API_URL = "http://127.0.0.1:8000/api/v1"
# st.set_page_config(
#     page_title="JobHunter Pro",
#     page_icon="⚡",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- CUSTOM CSS (Responsive & Modern) ---
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

#     :root {
#         --bg-color: #0f172a;
#         --card-bg: #1e293b;
#         --text-color: #f1f5f9;
#         --accent: #6366f1;
#         --success: #10b981;
#     }

#     /* Base Reset */
#     .stApp {
#         background-color: var(--bg-color);
#         font-family: 'Inter', sans-serif;
#         color: var(--text-color);
#     }
    
#     /* Hero Section */
#     .hero-section {
#         text-align: center;
#         padding: 2rem 1rem;
#         margin-bottom: 2rem;
#     }
#     .hero-title {
#         font-size: clamp(2rem, 5vw, 3.5rem);
#         font-weight: 800;
#         background: linear-gradient(135deg, #818cf8, #38bdf8);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.5rem;
#     }
#     .hero-subtitle {
#         color: #94a3b8;
#         font-size: clamp(1rem, 2vw, 1.2rem);
#     }

#     /* Cards */
#     .glass-card {
#         background: rgba(30, 41, 59, 0.7);
#         backdrop-filter: blur(10px);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 16px;
#         padding: 1.5rem;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
#         margin-bottom: 1rem;
#     }

#     /* Headers */
#     .section-header {
#         font-size: 0.85rem;
#         text-transform: uppercase;
#         letter-spacing: 0.05em;
#         color: #94a3b8;
#         font-weight: 600;
#         margin-bottom: 1rem;
#         border-bottom: 1px solid #334155;
#         padding-bottom: 0.5rem;
#     }

#     /* Skills Pill */
#     .skill-pill {
#         display: inline-block;
#         background: rgba(99, 102, 241, 0.2);
#         color: #c7d2fe;
#         padding: 0.25rem 0.75rem;
#         border-radius: 9999px;
#         font-size: 0.8rem;
#         font-weight: 500;
#         margin: 0 0.5rem 0.5rem 0;
#         border: 1px solid rgba(99, 102, 241, 0.3);
#     }

#     /* Inputs Overrides */
#     .stTextInput input, .stTextArea textarea {
#         background-color: #020617 !important;
#         border-color: #334155 !important;
#         color: white !important;
#         border-radius: 10px;
#     }
    
#     .stFileUploader {
#         padding: 1rem;
#         border: 1px dashed #475569;
#         border-radius: 12px;
#         background: #020617;
#     }

#     /* Button Override */
#     div.stButton > button {
#         background: linear-gradient(to right, #4f46e5, #3b82f6);
#         border: none;
#         padding: 0.75rem 1.5rem;
#         font-weight: 600;
#         width: 100%;
#         color: white;
#         transition: transform 0.2s;
#     }
#     div.stButton > button:hover {
#         transform: scale(1.02);
#         color: white;
#     }
    
#     /* Paper Effect for Cover Letter */
#     .paper {
#         background: #f8fafc;
#         color: #1e293b;
#         padding: 2rem;
#         border-radius: 4px;
#         box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
#         font-family: 'Georgia', serif;
#         line-height: 1.8;
#         font-size: 0.95rem;
#         white-space: pre-wrap;
#     }
# </style>
# """, unsafe_allow_html=True)

# # --- HELPER: PDF PARSER ---
# def parse_resume(uploaded_file):
#     try:
#         reader = PdfReader(uploaded_file)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text() + "\n"
#         return text
#     except Exception as e:
#         st.error(f"Error reading PDF: {e}")
#         return None

# # --- STATE MANAGEMENT ---
# if 'resume_text' not in st.session_state:
#     st.session_state['resume_text'] = ""

# # --- UI: HEADER ---
# st.markdown("""
#     <div class="hero-section">
#         <div class="hero-title">JobHunter Pro</div>
#         <div class="hero-subtitle">The Autonomous AI Agent for Professional Applications</div>
#     </div>
# """, unsafe_allow_html=True)

# # --- UI: MAIN LAYOUT ---
# main_container = st.container()

# with main_container:
#     # --- ROW 1: INPUTS ---
#     col1, col2 = st.columns([1, 1], gap="large")
    
#     # ... inside frontend.py ...
#     with col1:
#         st.markdown('<div class="section-header">1. UPLOAD RESUME</div>', unsafe_allow_html=True)
#         uploaded_file = st.file_uploader("Drop your PDF resume here", type=['pdf'], label_visibility="collapsed")
        
#         if uploaded_file is not None:
#             extracted_text = parse_resume(uploaded_file)
#             if extracted_text:
#                 st.session_state['resume_text'] = extracted_text
#                 st.success("✅ Resume parsed successfully!")
                
#                 # --- CHANGED: Scrollable Text Box for FULL text ---
#                 with st.expander("View Full Extracted Text", expanded=False):
#                     st.text_area(
#                         "Raw Text", 
#                         value=st.session_state['resume_text'], 
#                         height=300, 
#                         label_visibility="collapsed",
#                         disabled=True
#                     )
#         else:
#             # Fallback manual text
#             st.session_state['resume_text'] = st.text_area(
#                 "Or paste resume text manually", 
#                 value=st.session_state['resume_text'],
#                 height=150,
#                 placeholder="Paste text here if you don't have a PDF..."
#             )
# # ... rest of file ...

#     with col2:
#         st.markdown('<div class="section-header">2. JOB LINK</div>', unsafe_allow_html=True)
#         job_url = st.text_input("Job URL", placeholder="https://linkedin.com/jobs/...", label_visibility="collapsed")
        
#         st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
#         analyze_btn = st.button("🚀 ANALYZE & APPLY", type="primary", use_container_width=True)

#     # --- ROW 2: RESULTS ---
#     if analyze_btn:
#         if not job_url:
#             st.toast("⚠️ Please enter a Job URL")
#         elif not st.session_state['resume_text']:
#             st.toast("⚠️ Please upload a Resume or enter text")
#         else:
#             st.divider()
            
#             # --- PROCESSING UI ---
#             status_text = st.empty()
#             progress_bar = st.progress(0)
            
#             try:
#                 # 1. API CALL
#                 status_text.markdown("🔄 **Initializing Agent...**")
#                 payload = {
#                     "url": job_url, 
#                     "original_resume_text": st.session_state['resume_text']
#                 }
#                 response = requests.post(f"{API_URL}/apply", json=payload)
                
#                 if response.status_code == 200:
#                     job_id = response.json()['id']
                    
#                     # 2. POLLING LOOP
#                     steps = [
#                         ("🕷️ Scraping Job Board...", 10),
#                         ("🧠 Analyzing Fit...", 30),
#                         ("💎 Optimizing Keywords...", 50),
#                         ("✍️ Drafting Application...", 70),
#                         ("📄 Generating PDF...", 90)
#                     ]
                    
#                     for i in range(90): # Increased timeout for full resume generation
#                         time.sleep(1)
#                         # Fetch Status
#                         res = requests.get(f"{API_URL}/jobs/{job_id}")
#                         data = res.json()
#                         status = data['status']
                        
#                         # Fake Progress Visualization
#                         current_prog = progress_bar.progress(min(95, i*2))
                        
#                         # Update Text based on time
#                         for txt, thresh in steps:
#                             if i * 2 > thresh:
#                                 status_text.markdown(f"**{txt}**")

#                         if status == "SUCCESS":
#                             progress_bar.progress(100)
#                             status_text.success("✅ Application Generated Successfully!")
#                             time.sleep(1)
#                             status_text.empty()
#                             progress_bar.empty()
                            
#                             # --- DISPLAY RESULTS ---
#                             res_c1, res_c2 = st.columns([1.5, 1], gap="medium")
                            
#                             content = data.get('tailored_resume_content', {})

#                             # LEFT: DOWNLOADS & COVER LETTER
#                             with res_c1:
#                                 # Download Button (Styled)
#                                 st.markdown(f"""
#                                 <a href="file://generated_applications/{job_id}.pdf" target="_blank" style="text-decoration:none;">
#                                     <div style="background: linear-gradient(135deg, #10b981, #059669); color:white; padding:20px; border-radius:12px; text-align:center; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3); margin-bottom:20px; transition: transform 0.2s;">
#                                         <div style="font-size:1.2rem; font-weight:800;">📥 DOWNLOAD RESUME PACKAGE</div>
#                                         <div style="font-size:0.9rem; opacity:0.9; margin-top:5px;">Professional PDF (Harvard Template)</div>
#                                     </div>
#                                 </a>
#                                 """, unsafe_allow_html=True)

#                                 st.markdown('<div class="section-header">GENERATED COVER LETTER</div>', unsafe_allow_html=True)
#                                 cover_letter = data.get('cover_letter', '')
#                                 if cover_letter:
#                                     st.markdown(f'<div class="paper">{cover_letter}</div>', unsafe_allow_html=True)

#                             # RIGHT: RESUME PREVIEW
#                             with res_c2:
#                                 st.markdown('<div class="section-header">RESUME PREVIEW</div>', unsafe_allow_html=True)
                                
#                                 # Summary
#                                 summary = content.get('professional_summary')
#                                 if summary:
#                                     with st.container():
#                                         st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#                                         st.caption("PROFESSIONAL SUMMARY")
#                                         st.info(summary)
#                                         st.markdown('</div>', unsafe_allow_html=True)
                                
#                                 st.markdown("<br>", unsafe_allow_html=True)

#                                 # Skills
#                                 skills = content.get('skills', [])
#                                 if skills:
#                                     with st.container():
#                                         st.caption("MATCHED SKILLS")
#                                         html = "".join([f'<span class="skill-pill">{s}</span>' for s in skills])
#                                         st.markdown(html, unsafe_allow_html=True)
#                                         st.markdown("<br>", unsafe_allow_html=True)

#                                 # Experience (Loop safely)
#                                 experiences = content.get('experience', [])
#                                 if experiences:
#                                     st.caption("EXPERIENCE UPDATES")
#                                     with st.container():
#                                         st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#                                         for exp in experiences:
#                                             # Robust check
#                                             if isinstance(exp, dict):
#                                                 role = exp.get('role', 'Role')
#                                                 comp = exp.get('company', 'Company')
#                                                 with st.expander(f"{role} @ {comp}"):
#                                                     for b in exp.get('description', []):
#                                                         st.markdown(f"• {b}")
#                                         st.markdown('</div>', unsafe_allow_html=True)
                                
#                                 st.markdown("<br>", unsafe_allow_html=True)

#                                 # Projects
#                                 projects = content.get('projects', [])
#                                 if projects:
#                                     st.caption("PROJECT HIGHLIGHTS")
#                                     with st.container():
#                                         st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#                                         for proj in projects:
#                                             if isinstance(proj, dict):
#                                                 st.markdown(f"**{proj.get('name')}**")
#                                                 st.caption(proj.get('tech_stack'))
#                                                 st.divider()
#                                         st.markdown('</div>', unsafe_allow_html=True)
                            
#                             break # Exit Loop
                        
#                         elif "FAILED" in status:
#                             st.error(f"Process Failed: {status}")
#                             break
#                 else:
#                     st.error(f"Server Error: {response.text}")
#             except Exception as e:
#                 st.error(f"Connection Error: {e}")



import streamlit as st
import requests
import time
from io import BytesIO

try:
    from pypdf import PdfReader
except ImportError:
    st.error("Missing dependency. Please run: pip install pypdf")

# --- CONFIG ---
API_URL = "http://127.0.0.1:8000/api/v1"
st.set_page_config(page_title="JobHunter Pro", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    :root { --bg-color: #0f172a; --card-bg: #1e293b; --text-color: #f1f5f9; --accent: #6366f1; }
    .stApp { background-color: var(--bg-color); font-family: 'Inter', sans-serif; color: var(--text-color); }
    
    /* Card Style */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8; font-weight: 700;
        margin-top: 1.5rem; margin-bottom: 0.5rem;
    }
    /* Input Overrides */
    .stTextInput input, .stTextArea textarea { background-color: #020617 !important; border: 1px solid #334155 !important; color: white !important; border-radius: 8px; }
    div.stButton > button { background: linear-gradient(to right, #4f46e5, #3b82f6); border: none; font-weight: 600; color: white; width: 100%; padding: 0.6rem; border-radius: 8px; }
    div.stButton > button:hover { transform: scale(1.01); }
</style>
""", unsafe_allow_html=True)

# --- HELPER ---
def parse_resume(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        return "".join([page.extract_text() + "\n" for page in reader.pages])
    except: return None

if 'resume_text' not in st.session_state: st.session_state['resume_text'] = ""

# --- UI HEADER ---
st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 0;'>JobHunter Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Autonomous Resume Tailoring Agent</p>", unsafe_allow_html=True)

# --- MAIN INPUTS ---
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    uploaded_file = st.file_uploader("1. Upload Resume (PDF)", type=['pdf'])
    if uploaded_file:
        text = parse_resume(uploaded_file)
        if text:
            st.session_state['resume_text'] = text
            st.success("PDF Parsed!")
            with st.expander("Show extracted text"):
                st.text_area("Raw", st.session_state['resume_text'], height=200)

with col2:
    job_url = st.text_input("2. Job URL", placeholder="https://linkedin.com/jobs/...")
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 GENERATE APPLICATION PACKAGE")

# --- RESULTS ---
if analyze_btn:
    if not job_url or not st.session_state['resume_text']:
        st.error("Please provide both a Resume and a Job URL.")
    else:
        st.divider()
        status_box = st.empty()
        pbar = st.progress(0)
        
        try:
            status_box.info("🔄 Connecting to Agent...")
            payload = {"url": job_url, "original_resume_text": st.session_state['resume_text']}
            resp = requests.post(f"{API_URL}/apply", json=payload)
            
            if resp.status_code == 200:
                job_id = resp.json()['id']
                
                # Polling
                for i in range(90):
                    time.sleep(1)
                    r = requests.get(f"{API_URL}/jobs/{job_id}").json()
                    status = r['status']
                    
                    pbar.progress(min(95, i+2))
                    status_box.markdown(f"**Status:** {status} ({i}s)")
                    
                    if status == "SUCCESS":
                        pbar.progress(100)
                        status_box.success("✅ Done!")
                        time.sleep(0.5)
                        status_box.empty()
                        pbar.empty()
                        
                        data = r.get('tailored_resume_content', {})
                        
                        # --- LAYOUT ---
                        c_left, c_right = st.columns([1, 1.2], gap="medium")
                        
                        with c_left:
                            # DOWNLOAD BUTTON
                            st.markdown(f"""
                            <a href="file://generated_applications/{job_id}.pdf" target="_blank" style="text-decoration:none;">
                                <div style="background: #10b981; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; margin-bottom: 20px;">
                                    📥 Download Resume + Cover Letter (PDF)
                                </div>
                            </a>
                            """, unsafe_allow_html=True)
                            
                            st.markdown('<div class="section-header">COVER LETTER PREVIEW</div>', unsafe_allow_html=True)
                            cl = r.get('cover_letter', '')
                            if cl:
                                st.markdown(f'<div style="background:white; color:black; padding:20px; border-radius:5px; font-size:0.9rem;">{cl}</div>', unsafe_allow_html=True)

                        with c_right:
                            st.markdown('<div class="section-header">RESUME OPTIMIZATION</div>', unsafe_allow_html=True)
                            
                            # Summary (Only show if exists)
                            summ = data.get('professional_summary')
                            if summ:
                                st.caption("Updated Summary")
                                st.info(summ)
                            
                            # Experience (Only show if exists)
                            exps = data.get('experience', [])
                            if exps:
                                st.caption("Experience Improvements")
                                for exp in exps:
                                    if isinstance(exp, dict):
                                        with st.expander(f"{exp.get('role', 'Role')} at {exp.get('company', 'Company')}"):
                                            for b in exp.get('description', []):
                                                st.markdown(f"- {b}")

                            # Projects (Only show if exists)
                            projs = data.get('projects', [])
                            if projs:
                                st.caption("Project Highlights")
                                for p in projs:
                                    if isinstance(p, dict):
                                        st.markdown(f"**{p.get('name')}**")
                                        st.markdown(f"<span style='font-size:0.8rem; color:#94a3b8'>{p.get('tech_stack')}</span>", unsafe_allow_html=True)
                                        st.markdown("---")

                        break
                    elif "FAILED" in status:
                        st.error(f"Failed: {status}")
                        break
            else:
                st.error(f"API Error: {resp.text}")
        except Exception as e:
            st.error(f"Connection Error: {e}")