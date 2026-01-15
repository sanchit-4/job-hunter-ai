import streamlit as st
import requests
import time
from io import BytesIO

try:
    from pypdf import PdfReader
except ImportError:
    st.error("Missing dependency. Please run: pip install pypdf")

# --- CONFIG ---
if "API_URL" in st.secrets:
    API_URL = st.secrets["API_URL"]
else:
    API_URL = "http://127.0.0.1:8000/api/v1"
st.set_page_config(page_title="JobHunter", page_icon="", layout="wide", initial_sidebar_state="collapsed")

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
                            # 1. Fetch the PDF bytes from the Backend
                            try:
                                pdf_response = requests.get(f"{API_URL}/download/{job_id}")
                                
                                if pdf_response.status_code == 200:
                                    # 2. Use Streamlit's Native Download Button
                                    st.download_button(
                                        label="📥 DOWNLOAD RESUME PACKAGE (PDF)",
                                        data=pdf_response.content,
                                        file_name=f"JobApplication_{job_id}.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                                else:
                                    st.error("PDF not found on server.")
                            except Exception as e:
                                st.error(f"Download Error: {e}")
                            
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