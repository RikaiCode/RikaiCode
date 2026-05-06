import streamlit as st
import os
import base64
import io
from PIL import Image

try:
    from zai import ZaiClient
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass 



SKIP_EXTENSIONS = {'.pdf', '.rtf', '.docx', '.pdf', '.xlsx', '.csv'}
LOGO_PATH = "assets/logo.png" if os.path.exists("assets/logo.png") else "logo.png"
MAX_LINES_INTERACTIVE_PREVIEW = 50000

def apply_styles():
    st.markdown("""
<style>

    html, body, [class*="css"] {

        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 { color: #ededed !important; font-weight: 700 !important; }
    .main .block-container { padding-top: 2rem; padding-bottom: 5rem; }
    .accent-text { color: #d3a0eb !important; }

   
    .stFileUploader {
        border: 1px dashed #d3a0eb !important;
        background-color: #1e1e1e !important;
        border-radius: 10px; padding: 20px;
    }
    

    .stButton > button {
        background-color: #d3a0eb !important;
        color: #171717 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
 
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #b589c8 !important;
        transform: translateY(-2px);
       
    }

    
    .streamlit-expanderHeader {
        background-color: #1e1e1e !important;
        color: #ededed !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderContent {
        background-color: #1e1e1e !important;
        border: 1px solid #333 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }


    [data-testid="stMetric"] {
        background-color: #1e1e1e !important; border: 1px solid #333 !important;
        border-radius: 10px; padding: 15px !important;
    }
    [data-testid="stMetricLabel"] { 
        color: #a0a0a0 !important; 
        font-size: 1.1rem !important; 
    }
    [data-testid="stMetricValue"] { color: #d3a0eb !important; font-size: 1.8rem !important; }


    .grade-box {
        background-color: #1e1e1e;
        border: 2px solid #7c5e8a;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;

    }
    .grade-letter {
        font-size: 4rem;
        font-weight: bold;
        color: #d3a0eb;
        line-height: 1;
    }
    .grade-reason {
        text-align: left;
        font-size: 0.9rem;
        color: #a0a0a0;
        margin-top: 10px;
        border-top: 1px solid #333;
        padding-top: 10px;
    }


    .arch-box {
       
        border: 0.5px solid #333;
       
        padding: 20px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        white-space: pre;
        overflow-x: auto;
        color: #ededed;
    }


    .footer-custom {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: #1e1e1e; border-top: 1px solid #333;
        padding: 15px 20px; display: flex; justify-content: space-between;
        align-items: center; z-index: 9999; font-size: 14px;
    }
    .footer-link {
        color: #d3a0eb !important;
        text-decoration: none !important;
    }

    .footer-link:hover {
        color: #9d76ad !important; 

    }


    @keyframes float {
        0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); }
    }
    .logo-container { display: flex; justify-content: center; margin-bottom: 1px; }
    .logo-img { width: 160px; }


    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: #1e1e1e !important; color: #ededed !important; border: 1px solid #333 !important;
    }
    

    .info-box {
        background-color: rgba(211, 160, 235, 0.05);

        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        color: #ededed;
    }


    .dep-tag {
        display: inline-block;
        background-color: #252525;

        padding: 4px 8px;
        border-radius: 4px;
        margin: 2px;
        font-size: 0.85rem;
        border: 1px solid #333;
    }
    
    .security-alert {
        background-color: rgba(255, 75, 75, 0.1);
        border-left: 4px solid #ff4b4b;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 4px;
    }


    .ai-response-box {
        background-color: #121212;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
        color: #ededed;
        margin-bottom: 10px;
  
    }
    
  
    .ai-response-box h3 {
        color: #d3a0eb !important;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .ai-response-box strong {
        color: #fff !important;
    }

    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def load_logo():
    if os.path.exists("assets/logo.png"):
        try:
            img = Image.open("assets/logo.png")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            data = base64.b64encode(buf.getvalue()).decode("utf-8")
            return f"data:image/png;base64,{data}"
        except: pass
    elif os.path.exists("logo.png"):
        try:
            img = Image.open("logo.png")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            data = base64.b64encode(buf.getvalue()).decode("utf-8")
            return f"data:image/png;base64,{data}"
        except: pass
    return None

def estimate_tokens(text):
    return len(text) // 4

class StringIO:
    def __init__(self): self.buffer = io.StringIO()
    def write(self, text): self.buffer.write(text)
    def get_value(self): return self.buffer.getvalue()