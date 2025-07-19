import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import io
import base64
import random
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Lab Kimia Interaktif",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema warna yang lebih kontras dan menyenangkan
primary_color = "#FF6B6B"
secondary_color = "#4ECDC4"
accent_color = "#FFD166"
background_color = "#F7FFF7"
dark_color = "#1A535C"
text_color = "#333333"  
header_color = "#FFFFFF"  
card_background = "#FFFFFF"
contrast_color = "#073B4C"

# CSS untuk styling yang lebih baik
st.markdown(f"""
<style>
    /* Warna utama dengan kontras lebih baik */
    .stApp {{
        background: linear-gradient(135deg, {background_color}, #E0F7E0);
        background-attachment: fixed;
    }}
    .css-1d391kg, .st-b7, .st-b8, .st-b9 {{
        background-color: transparent !important;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {contrast_color} !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        position: relative;
        z-index: 2;
    }}
    .header-with-emoji {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}
    .header-with-emoji .emoji {{
        animation: bounce 2s infinite;
    }}
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        50% {{ transform: translateY(-10px) rotate(10deg); }}
    }}
    p, div, span, li, td {{
        color: {text_color} !important;
    }}
    .stButton>button {{
        background: linear-gradient(to right, {primary_color}, {accent_color}) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 12px 28px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
    }}
    .stSelectbox>div>div {{
        background-color: white !important;
        border-radius: 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }}
    .stSlider>div>div>div {{
        background: linear-gradient(to right, {accent_color}, {secondary_color}) !important;
    }}
    .stTabs>div>div>div>div {{
        background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.4)) !important;
        color: {contrast_color} !important;
        border-radius: 15px 15px 0 0 !important;
        padding: 12px 24px !important;
        font-weight: bold;
        margin: 0 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px solid {secondary_color};
        transition: all 0.3s ease;
    }}
    .stTabs>div>div>div>div:hover {{
        transform: scale(1.05);
        background: linear-gradient(135deg, {secondary_color}, {primary_color}) !important;
        color: white !important;
    }}
    .stTabs>div>div>div>div[aria-selected="true"] {{
        background: linear-gradient(135deg, {primary_color}, {accent_color}) !important;
        color: white !important;
        transform: scale(1.05);
        z-index: 1;
    }}
    .stDataFrame {{
        border-radius: 15px !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
        overflow: hidden;
    }}
    .stAlert {{
        border-radius: 15px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }}
    .element-card {{
        background: {card_background};
        border-radius: 20px;
        padding: 20px;
        margin: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: all 0.4s ease;
        height: 100%;
        border: 2px solid {secondary_color};
        position: relative;
        overflow: hidden;
    }}
    .element-card:hover {{
        transform: translateY(-10px) rotate(2deg);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        border: 2px solid {primary_color};
    }}
    .reaction-container {{
        background: white;
        border-radius: 25px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        border: 3px solid {accent_color};
        background-image: radial-gradient(circle at top right, rgba(255,255,255,0.8), rgba(255,255,255,0.4));
    }}
    .color-box {{
        width: 100%;
        height: 180px;
        border-radius: 20px;
        margin: 20px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 28px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2), 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border: 2px solid white;
    }}
    .color-box:hover {{
        transform: scale(1.03);
        box-shadow: inset 0 0 30px rgba(0,0,0,0.3), 0 6px 12px rgba(0,0,0,0.3);
    }}
    .warning-badge {{
        background: linear-gradient(135deg, #FFD166, #FF9E6D);
        color: {dark_color};
        border-radius: 50px;
        padding: 8px 20px;
        margin: 10px;
        display: inline-block;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    .apd-badge {{
        background: linear-gradient(135deg, {secondary_color}, #118AB2);
        color: white;
        border-radius: 50px;
        padding: 8px 20px;
        margin: 10px;
        display: inline-block;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    .periodic-header {{
        background: linear-gradient(135deg, {dark_color}, #073B4C);
        padding: 25px;
        border-radius: 20px;
        color: {header_color};
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }}
    .periodic-header::after {{
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }}
    @keyframes rotate {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    .chemical-equation {{
        font-family: 'Courier New', monospace;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px dashed {accent_color};
        color: {text_color};
    }}
    .bubble {{
        position: absolute;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        animation: float 15s infinite ease-in-out;
        z-index: 1;
    }}
    @keyframes float {{
        0% {{ transform: translateY(0) translateX(0) rotate(0); opacity: 0; }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 0.8; }}
        100% {{ transform: translateY(-1000px) translateX(200px) rotate(360deg); opacity: 0; }}
    }}
    .floating-emoji {{
        position: absolute;
        font-size: 24px;
        animation: float-emoji 10s infinite ease-in-out;
        z-index: 1;
    }}
    @keyframes float-emoji {{
        0%, 100% {{ transform: translateY(0) translateX(0) rotate(0deg); }}
        25% {{ transform: translateY(-20px) translateX(10px) rotate(10deg); }}
        50% {{ transform: translateY(-40px) translateX(20px) rotate(20deg); }}
        75% {{ transform: translateY(-20px) translateX(30px) rotate(10deg); }}
    }}
    .compatibility-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }}
    .compatibility-table th, .compatibility-table td {{
        padding: 12px 15px;
        text-align: center;
        border: 1px solid #ddd;
    }}
    .compatibility-table th {{
        background-color: {dark_color};
        color: {header_color};
        font-weight: bold;
    }}
    .compatibility-table tr:nth-child(even) {{
        background-color: #f8f9fa;
    }}
    .compatibility-table tr:hover {{
        background-color: #e9ecef;
    }}
    .compatibility-table .compatible {{
        background-color: #d4edda;
        color: #155724;
        font-weight: bold;
    }}
    .compatibility-table .incompatible {{
        background-color: #f8d7da;
        color: #721c24;
        font-weight: bold;
    }}
    .compatibility-table .conditional {{
        background-color: #fff3cd;
        color: #856404;
        font-weight: bold;
    }}
    .hazard-symbol {{
        font-size: 36px;
        margin-right: 15px;
        display: inline-block;
        width: 60px;
        text-align: center;
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.2); }}
        100% {{ transform: scale(1); }}
    }}
    /* Perbaikan kontras untuk header di dalam card */
    .element-card h3 {{
        color: {dark_color} !important;
        position: relative;
        z-index: 2;
    }}
    .element-card p {{
        position: relative;
        z-index: 2;
    }}
    .tab-content {{
        position: relative;
        z-index: 2;
    }}
    .floating-chem {{
        position: absolute;
        font-size: 40px;
        opacity: 0.2;
        animation: float-chem 15s infinite linear;
        z-index: 1;
    }}
    @keyframes float-chem {{
        0% {{ transform: translate(0, 0) rotate(0deg); opacity: 0; }}
        10% {{ opacity: 0.2; }}
        90% {{ opacity: 0.2; }}
        100% {{ transform: translate(100vw, -100vh) rotate(360deg); opacity: 0; }}
    }}
    .element-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at center, rgba(255,255,255,0.8), rgba(255,255,255,0.4));
        z-index: 1;
    }}
</style>
""", unsafe_allow_html=True)

# Animasi gelembung dan emoji
st.markdown("""
<script>
function createBubble() {
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    
    const size = Math.random() * 100 + 50;
    bubble.style.width = `${size}px`;
    bubble.style.height = `${size}px`;
    
    const posX = Math.random() * window.innerWidth;
    bubble.style.left = `${posX}px`;
    bubble.style.bottom = `-100px`;
    
    const animationDuration = Math.random() * 20 + 10;
    bubble.style.animationDuration = `${animationDuration}s`;
    
    document.body.appendChild(bubble);
    
    setTimeout(() => {
        bubble.remove();
    }, animationDuration * 1000);
}

function createFloatingEmoji() {
    const emojis = ["🧪", "🔬", "⚗️", "🧫", "🧴", "💧", "🔥", "⚡", "🧲", "🧪", "🔭"];
    const emoji = document.createElement('div');
    emoji.classList.add('floating-emoji');
    emoji.innerHTML = emojis[Math.floor(Math.random() * emojis.length)];
    
    const size = Math.random() * 30 + 20;
    emoji.style.fontSize = `${size}px`;
    
    const posX = Math.random() * window.innerWidth;
    const posY = Math.random() * window.innerHeight;
    emoji.style.left = `${posX}px`;
    emoji.style.top = `${posY}px`;
    
    const animationDuration = Math.random() * 15 + 10;
    emoji.style.animationDuration = `${animationDuration}s`;
    
    document.body.appendChild(emoji);
    
    setTimeout(() => {
        emoji.remove();
    }, animationDuration * 1000);
}

// Create bubbles every 1.5 seconds
setInterval(createBubble, 1500);
// Create floating emojis every 3 seconds
setInterval(createFloatingEmoji, 3000);
</script>
""", unsafe_allow_html=True)

# Database tabel periodik (118 unsur lengkap)
PERIODIC_TABLE = [
    # Periode 1
    {"Symbol": "H", "Name": "Hidrogen", "AtomicNumber": 1, "AtomicMass": 1.008, 
     "Group": 1, "Period": 1, "Category": "Nonlogam", "Color": "#FF6B6B", "Electronegativity": 2.20, "Hazards": ["Mudah Terbakar"]},
    {"Symbol": "He", "Name": "Helium", "AtomicNumber": 2, "AtomicMass": 4.0026, 
     "Group": 18, "Period": 1, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": None, "Hazards": []},
    
    # Periode 2
    {"Symbol": "Li", "Name": "Litium", "AtomicNumber": 3, "AtomicMass": 6.94, 
     "Group": 1, "Period": 2, "Category": "Logam Alkali", "Color": "#FFD166", "Electronegativity": 0.98, "Hazards": ["Mudah Terbakar", "Reaktif"]},
    {"Symbol": "Be", "Name": "Berilium", "AtomicNumber": 4, "AtomicMass": 9.0122, 
     "Group": 2, "Period": 2, "Category": "Logam Alkali Tanah", "Color": "#06D6A0", "Electronegativity": 1.57, "Hazards": ["Beracun"]},
    {"Symbol": "B", "Name": "Boron", "AtomicNumber": 5, "AtomicMass": 10.81, 
     "Group": 13, "Period": 2, "Category": "Metaloid", "Color": "#118AB2", "Electronegativity": 2.04, "Hazards": []},
    {"Symbol": "C", "Name": "Karbon", "AtomicNumber": 6, "AtomicMass": 12.011, 
     "Group": 14, "Period": 2, "Category": "Nonlogam", "Color": "#073B4C", "Electronegativity": 2.55, "Hazards": []},
    {"Symbol": "N", "Name": "Nitrogen", "AtomicNumber": 7, "AtomicMass": 14.007, 
     "Group": 15, "Period": 2, "Category": "Nonlogam", "Color": "#118AB2", "Electronegativity": 3.04, "Hazards": ["Gas Bertekanan"]},
    {"Symbol": "O", "Name": "Oksigen", "AtomicNumber": 8, "AtomicMass": 15.999, 
     "Group": 16, "Period": 2, "Category": "Nonlogam", "Color": "#EF476F", "Electronegativity": 3.44, "Hazards": ["Pengoksidasi"]},
    {"Symbol": "F", "Name": "Fluor", "AtomicNumber": 9, "AtomicMass": 18.998, 
     "Group": 17, "Period": 2, "Category": "Halogen", "Color": "#06D6A0", "Electronegativity": 3.98, "Hazards": ["Korosif", "Beracun"]},
    {"Symbol": "Ne", "Name": "Neon", "AtomicNumber": 10, "AtomicMass": 20.180, 
     "Group": 18, "Period": 2, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": None, "Hazards": ["Gas Bertekanan"]},
    
    # Periode 3
    {"Symbol": "Na", "Name": "Natrium", "AtomicNumber": 11, "AtomicMass": 22.990, 
     "Group": 1, "Period": 3, "Category": "Logam Alkali", "Color": "#FFD166", "Electronegativity": 0.93, "Hazards": ["Mudah Terbakar", "Reaktif"]},
    {"Symbol": "Mg", "Name": "Magnesium", "AtomicNumber": 12, "AtomicMass": 24.305, 
     "Group": 2, "Period": 3, "Category": "Logam Alkali Tanah", "Color": "#06D6A0", "Electronegativity": 1.31, "Hazards": ["Mudah Terbakar"]},
    {"Symbol": "Al", "Name": "Aluminium", "AtomicNumber": 13, "AtomicMass": 26.982, 
     "Group": 13, "Period": 3, "Category": "Logam Pascatransisi", "Color": "#118AB2", "Electronegativity": 1.61, "Hazards": []},
    {"Symbol": "Si", "Name": "Silikon", "AtomicNumber": 14, "AtomicMass": 28.085, 
     "Group": 14, "Period": 3, "Category": "Metaloid", "Color": "#073B4C", "Electronegativity": 1.90, "Hazards": []},
    {"Symbol": "P", "Name": "Fosfor", "AtomicNumber": 15, "AtomicMass": 30.974, 
     "Group": 15, "Period": 3, "Category": "Nonlogam", "Color": "#FF6B6B", "Electronegativity": 2.19, "Hazards": ["Mudah Terbakar", "Beracun"]},
    {"Symbol": "S", "Name": "Belerang", "AtomicNumber": 16, "AtomicMass": 32.06, 
     "Group": 16, "Period": 3, "Category": "Nonlogam", "Color": "#FFD166", "Electronegativity": 2.58, "Hazards": []},
    {"Symbol": "Cl", "Name": "Klor", "AtomicNumber": 17, "AtomicMass": 35.45, 
     "Group": 17, "Period": 3, "Category": "Halogen", "Color": "#06D6A0", "Electronegativity": 3.16, "Hazards": ["Korosif", "Beracun"]},
    {"Symbol": "Ar", "Name": "Argon", "AtomicNumber": 18, "AtomicMass": 39.948, 
     "Group": 18, "Period": 3, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": None, "Hazards": ["Gas Bertekanan"]},
    
    # Periode 4
    {"Symbol": "K", "Name": "Kalium", "AtomicNumber": 19, "AtomicMass": 39.098, 
     "Group": 1, "Period": 4, "Category": "Logam Alkali", "Color": "#FFD166", "Electronegativity": 0.82, "Hazards": ["Mudah Terbakar", "Reaktif"]},
    {"Symbol": "Ca", "Name": "Kalsium", "AtomicNumber": 20, "AtomicMass": 40.078, 
     "Group": 2, "Period": 4, "Category": "Logam Alkali Tanah", "Color": "#06D6A0", "Electronegativity": 1.00, "Hazards": []},
    {"Symbol": "Sc", "Name": "Skandium", "AtomicNumber": 21, "AtomicMass": 44.956, 
     "Group": 3, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.36, "Hazards": []},
    {"Symbol": "Ti", "Name": "Titanium", "AtomicNumber": 22, "AtomicMass": 47.867, 
     "Group": 4, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.54, "Hazards": []},
    {"Symbol": "V", "Name": "Vanadium", "AtomicNumber": 23, "AtomicMass": 50.942, 
     "Group": 5, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.63, "Hazards": ["Beracun"]},
    {"Symbol": "Cr", "Name": "Kromium", "AtomicNumber": 24, "AtomicMass": 51.996, 
     "Group": 6, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.66, "Hazards": ["Beracun"]},
    {"Symbol": "Mn", "Name": "Mangan", "AtomicNumber": 25, "AtomicMass": 54.938, 
     "Group": 7, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.55, "Hazards": ["Beracun"]},
    {"Symbol": "Fe", "Name": "Besi", "AtomicNumber": 26, "AtomicMass": 55.845, 
     "Group": 8, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.83, "Hazards": []},
    {"Symbol": "Co", "Name": "Kobalt", "AtomicNumber": 27, "AtomicMass": 58.933, 
     "Group": 9, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.88, "Hazards": ["Beracun"]},
    {"Symbol": "Ni", "Name": "Nikel", "AtomicNumber": 28, "AtomicMass": 58.693, 
     "Group": 10, "Period": 4, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.91, "Hazards": ["Karsinogen"]},
    {"Symbol": "Cu", "Name": "Tembaga", "AtomicNumber": 29, "AtomicMass": 63.546, 
     "Group": 11, "Period": 4, "Category": "Logam Transisi", "Color": "#D2691E", "Electronegativity": 1.90, "Hazards": []},
    {"Symbol": "Zn", "Name": "Seng", "AtomicNumber": 30, "AtomicMass": 65.38, 
     "Group": 12, "Period": 4, "Category": "Logam Transisi", "Color": "#7FFFD4", "Electronegativity": 1.65, "Hazards": []},
    {"Symbol": "Ga", "Name": "Galium", "AtomicNumber": 31, "AtomicMass": 69.723, 
     "Group": 13, "Period": 4, "Category": "Logam Pascatransisi", "Color": "#118AB2", "Electronegativity": 1.81, "Hazards": []},
    {"Symbol": "Ge", "Name": "Germanium", "AtomicNumber": 32, "AtomicMass": 72.630, 
     "Group": 14, "Period": 4, "Category": "Metaloid", "Color": "#073B4C", "Electronegativity": 2.01, "Hazards": []},
    {"Symbol": "As", "Name": "Arsen", "AtomicNumber": 33, "AtomicMass": 74.922, 
     "Group": 15, "Period": 4, "Category": "Metaloid", "Color": "#FF6B6B", "Electronegativity": 2.18, "Hazards": ["Beracun", "Karsinogen"]},
    {"Symbol": "Se", "Name": "Selenium", "AtomicNumber": 34, "AtomicMass": 78.971, 
     "Group": 16, "Period": 4, "Category": "Nonlogam", "Color": "#FFD166", "Electronegativity": 2.55, "Hazards": ["Beracun"]},
    {"Symbol": "Br", "Name": "Brom", "AtomicNumber": 35, "AtomicMass": 79.904, 
     "Group": 17, "Period": 4, "Category": "Halogen", "Color": "#06D6A0", "Electronegativity": 2.96, "Hazards": ["Korosif", "Beracun"]},
    {"Symbol": "Kr", "Name": "Kripton", "AtomicNumber": 36, "AtomicMass": 83.798, 
     "Group": 18, "Period": 4, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": 3.00, "Hazards": ["Gas Bertekanan"]},
    
    # Periode 5
    {"Symbol": "Rb", "Name": "Rubidium", "AtomicNumber": 37, "AtomicMass": 85.468, 
     "Group": 1, "Period": 5, "Category": "Logam Alkali", "Color": "#FFD166", "Electronegativity": 0.82, "Hazards": ["Mudah Terbakar", "Reaktif"]},
    {"Symbol": "Sr", "Name": "Stronsium", "AtomicNumber": 38, "AtomicMass": 87.62, 
     "Group": 2, "Period": 5, "Category": "Logam Alkali Tanah", "Color": "#06D6A0", "Electronegativity": 0.95, "Hazards": []},
    {"Symbol": "Y", "Name": "Yttrium", "AtomicNumber": 39, "AtomicMass": 88.906, 
     "Group": 3, "Period": 5, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.22, "Hazards": []},
    {"Symbol": "Zr", "Name": "Zirkonium", "AtomicNumber": 40, "AtomicMass": 91.224, 
     "Group": 4, "Period": 5, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.33, "Hazards": []},
    {"Symbol": "Nb", "Name": "Niobium", "AtomicNumber": 41, "AtomicMass": 92.906, 
     "Group": 5, "Period": 5, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.6, "Hazards": []},
    {"Symbol": "Mo", "Name": "Molibdenum", "AtomicNumber": 42, "AtomicMass": 95.95, 
     "Group": 6, "Period": 5, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 2.16, "Hazards": []},
    {"Symbol": "Tc", "Name": "Teknesium", "AtomicNumber": 43, "AtomicMass": 98, 
     "Group": 7, "Period": 5, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.9, "Hazards": ["Radioaktif"]},
    {"Symbol": "Ru", "Name": "Rutenium", "AtomicNumber": 44, "AtomicMass": 101.07, 
     "Group": 8, "Period": 5, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 2.2, "Hazards": []},
    {"Symbol": "Rh", "Name": "Rodium", "AtomicNumber": 45, "AtomicMass": 102.91, 
     "Group": 9, "Period": 5, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 2.28, "Hazards": []},
    {"Symbol": "Pd", "Name": "Paladium", "AtomicNumber": 46, "AtomicMass": 106.42, 
     "Group": 10, "Period": 5, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 2.20, "Hazards": []},
    {"Symbol": "Ag", "Name": "Perak", "AtomicNumber": 47, "AtomicMass": 107.87, 
     "Group": 11, "Period": 5, "Category": "Logam Transisi", "Color": "#D3D3D3", "Electronegativity": 1.93, "Hazards": []},
    {"Symbol": "Cd", "Name": "Kadmium", "AtomicNumber": 48, "AtomicMass": 112.41, 
     "Group": 12, "Period": 5, "Category": "Logam Transisi", "Color": "#7FFFD4", "Electronegativity": 1.69, "Hazards": ["Beracun"]},
    {"Symbol": "In", "Name": "Indium", "AtomicNumber": 49, "AtomicMass": 114.82, 
     "Group": 13, "Period": 5, "Category": "Logam Pascatransisi", "Color": "#118AB2", "Electronegativity": 1.78, "Hazards": []},
    {"Symbol": "Sn", "Name": "Timah", "AtomicNumber": 50, "AtomicMass": 118.71, 
     "Group": 14, "Period": 5, "Category": "Logam Pascatransisi", "Color": "#073B4C", "Electronegativity": 1.96, "Hazards": []},
    {"Symbol": "Sb", "Name": "Antimon", "AtomicNumber": 51, "AtomicMass": 121.76, 
     "Group": 15, "Period": 5, "Category": "Metaloid", "Color": "#FF6B6B", "Electronegativity": 2.05, "Hazards": ["Beracun"]},
    {"Symbol": "Te", "Name": "Telurium", "AtomicNumber": 52, "AtomicMass": 127.60, 
     "Group": 16, "Period": 5, "Category": "Metaloid", "Color": "#FFD166", "Electronegativity": 2.1, "Hazards": ["Beracun"]},
    {"Symbol": "I", "Name": "Iodin", "AtomicNumber": 53, "AtomicMass": 126.90, 
     "Group": 17, "Period": 5, "Category": "Halogen", "Color": "#9400D3", "Electronegativity": 2.66, "Hazards": ["Beracun"]},
    {"Symbol": "Xe", "Name": "Xenon", "AtomicNumber": 54, "AtomicMass": 131.29, 
     "Group": 18, "Period": 5, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": 2.6, "Hazards": ["Gas Bertekanan"]},
    
    # Periode 6
    {"Symbol": "Cs", "Name": "Sesium", "AtomicNumber": 55, "AtomicMass": 132.91, 
     "Group": 1, "Period": 6, "Category": "Logam Alkali", "Color": "#FFD166", "Electronegativity": 0.79, "Hazards": ["Mudah Terbakar", "Reaktif"]},
    {"Symbol": "Ba", "Name": "Barium", "AtomicNumber": 56, "AtomicMass": 137.33, 
     "Group": 2, "Period": 6, "Category": "Logam Alkali Tanah", "Color": "#06D6A0", "Electronegativity": 0.89, "Hazards": ["Beracun"]},
    {"Symbol": "La", "Name": "Lantanum", "AtomicNumber": 57, "AtomicMass": 138.91, 
     "Group": 3, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.10, "Hazards": []},
    {"Symbol": "Ce", "Name": "Serium", "AtomicNumber": 58, "AtomicMass": 140.12, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.12, "Hazards": []},
    {"Symbol": "Pr", "Name": "Praseodimium", "AtomicNumber": 59, "AtomicMass": 140.91, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.13, "Hazards": []},
    {"Symbol": "Nd", "Name": "Neodimium", "AtomicNumber": 60, "AtomicMass": 144.24, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.14, "Hazards": []},
    {"Symbol": "Pm", "Name": "Prometium", "AtomicNumber": 61, "AtomicMass": 145, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.13, "Hazards": ["Radioaktif"]},
    {"Symbol": "Sm", "Name": "Samarium", "AtomicNumber": 62, "AtomicMass": 150.36, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.17, "Hazards": []},
    {"Symbol": "Eu", "Name": "Europium", "AtomicNumber": 63, "AtomicMass": 151.96, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.2, "Hazards": []},
    {"Symbol": "Gd", "Name": "Gadolinium", "AtomicNumber": 64, "AtomicMass": 157.25, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.2, "Hazards": []},
    {"Symbol": "Tb", "Name": "Terbium", "AtomicNumber": 65, "AtomicMass": 158.93, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.2, "Hazards": []},
    {"Symbol": "Dy", "Name": "Disprosium", "AtomicNumber": 66, "AtomicMass": 162.50, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.22, "Hazards": []},
    {"Symbol": "Ho", "Name": "Holmium", "AtomicNumber": 67, "AtomicMass": 164.93, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.23, "Hazards": []},
    {"Symbol": "Er", "Name": "Erbium", "AtomicNumber": 68, "AtomicMass": 167.26, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.24, "Hazards": []},
    {"Symbol": "Tm", "Name": "Tulium", "AtomicNumber": 69, "AtomicMass": 168.93, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.25, "Hazards": []},
    {"Symbol": "Yb", "Name": "Iterbium", "AtomicNumber": 70, "AtomicMass": 173.05, 
     "Group": None, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.1, "Hazards": []},
    {"Symbol": "Lu", "Name": "Lutesium", "AtomicNumber": 71, "AtomicMass": 174.97, 
     "Group": 3, "Period": 6, "Category": "Lantanida", "Color": "#FF9E6D", "Electronegativity": 1.27, "Hazards": []},
    {"Symbol": "Hf", "Name": "Hafnium", "AtomicNumber": 72, "AtomicMass": 178.49, 
     "Group": 4, "Period": 6, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.3, "Hazards": []},
    {"Symbol": "Ta", "Name": "Tantalum", "AtomicNumber": 73, "AtomicMass": 180.95, 
     "Group": 5, "Period": 6, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.5, "Hazards": []},
    {"Symbol": "W", "Name": "Wolfram", "AtomicNumber": 74, "AtomicMass": 183.84, 
     "Group": 6, "Period": 6, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 2.36, "Hazards": []},
    {"Symbol": "Re", "Name": "Renium", "AtomicNumber": 75, "AtomicMass": 186.21, 
     "Group": 7, "Period": 6, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 1.9, "Hazards": []},
    {"Symbol": "Os", "Name": "Osmium", "AtomicNumber": 76, "AtomicMass": 190.23, 
     "Group": 8, "Period": 6, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 2.2, "Hazards": ["Beracun"]},
    {"Symbol": "Ir", "Name": "Iridium", "AtomicNumber": 77, "AtomicMass": 192.22, 
     "Group": 9, "Period": 6, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 2.20, "Hazards": []},
    {"Symbol": "Pt", "Name": "Platina", "AtomicNumber": 78, "AtomicMass": 195.08, 
     "Group": 10, "Period": 6, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": 2.28, "Hazards": []},
    {"Symbol": "Au", "Name": "Emas", "AtomicNumber": 79, "AtomicMass": 196.97, 
     "Group": 11, "Period": 6, "Category": "Logam Transisi", "Color": "#FFD700", "Electronegativity": 2.54, "Hazards": []},
    {"Symbol": "Hg", "Name": "Raksa", "AtomicNumber": 80, "AtomicMass": 200.59, 
     "Group": 12, "Period": 6, "Category": "Logam Transisi", "Color": "#7FFFD4", "Electronegativity": 2.00, "Hazards": ["Beracun"]},
    {"Symbol": "Tl", "Name": "Talium", "AtomicNumber": 81, "AtomicMass": 204.38, 
     "Group": 13, "Period": 6, "Category": "Logam Pascatransisi", "Color": "#118AB2", "Electronegativity": 1.62, "Hazards": ["Beracun"]},
    {"Symbol": "Pb", "Name": "Timbal", "AtomicNumber": 82, "AtomicMass": 207.2, 
     "Group": 14, "Period": 6, "Category": "Logam Pascatransisi", "Color": "#073B4C", "Electronegativity": 2.33, "Hazards": ["Beracun"]},
    {"Symbol": "Bi", "Name": "Bismut", "AtomicNumber": 83, "AtomicMass": 208.98, 
     "Group": 15, "Period": 6, "Category": "Logam Pascatransisi", "Color": "#FF6B6B", "Electronegativity": 2.02, "Hazards": []},
    {"Symbol": "Po", "Name": "Polonium", "AtomicNumber": 84, "AtomicMass": 209, 
     "Group": 16, "Period": 6, "Category": "Metaloid", "Color": "#FFD166", "Electronegativity": 2.0, "Hazards": ["Radioaktif", "Beracun"]},
    {"Symbol": "At", "Name": "Astatin", "AtomicNumber": 85, "AtomicMass": 210, 
     "Group": 17, "Period": 6, "Category": "Halogen", "Color": "#06D6A0", "Electronegativity": 2.2, "Hazards": ["Radioaktif"]},
    {"Symbol": "Rn", "Name": "Radon", "AtomicNumber": 86, "AtomicMass": 222, 
     "Group": 18, "Period": 6, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    
    # Periode 7
    {"Symbol": "Fr", "Name": "Fransium", "AtomicNumber": 87, "AtomicMass": 223, 
     "Group": 1, "Period": 7, "Category": "Logam Alkali", "Color": "#FFD166", "Electronegativity": 0.7, "Hazards": ["Radioaktif"]},
    {"Symbol": "Ra", "Name": "Radium", "AtomicNumber": 88, "AtomicMass": 226, 
     "Group": 2, "Period": 7, "Category": "Logam Alkali Tanah", "Color": "#06D6A0", "Electronegativity": 0.9, "Hazards": ["Radioaktif"]},
    {"Symbol": "Ac", "Name": "Aktinium", "AtomicNumber": 89, "AtomicMass": 227, 
     "Group": 3, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.1, "Hazards": ["Radioaktif"]},
    {"Symbol": "Th", "Name": "Thorium", "AtomicNumber": 90, "AtomicMass": 232.04, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.3, "Hazards": ["Radioaktif"]},
    {"Symbol": "Pa", "Name": "Protaktinium", "AtomicNumber": 91, "AtomicMass": 231.04, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.5, "Hazards": ["Radioaktif"]},
    {"Symbol": "U", "Name": "Uranium", "AtomicNumber": 92, "AtomicMass": 238.03, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.38, "Hazards": ["Radioaktif"]},
    {"Symbol": "Np", "Name": "Neptunium", "AtomicNumber": 93, "AtomicMass": 237, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.36, "Hazards": ["Radioaktif"]},
    {"Symbol": "Pu", "Name": "Plutonium", "AtomicNumber": 94, "AtomicMass": 244, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.28, "Hazards": ["Radioaktif"]},
    {"Symbol": "Am", "Name": "Amerisium", "AtomicNumber": 95, "AtomicMass": 243, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.13, "Hazards": ["Radioaktif"]},
    {"Symbol": "Cm", "Name": "Curium", "AtomicNumber": 96, "AtomicMass": 247, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.28, "Hazards": ["Radioaktif"]},
    {"Symbol": "Bk", "Name": "Berkelium", "AtomicNumber": 97, "AtomicMass": 247, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.3, "Hazards": ["Radioaktif"]},
    {"Symbol": "Cf", "Name": "Kalifornium", "AtomicNumber": 98, "AtomicMass": 251, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.3, "Hazards": ["Radioaktif"]},
    {"Symbol": "Es", "Name": "Einsteinium", "AtomicNumber": 99, "AtomicMass": 252, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.3, "Hazards": ["Radioaktif"]},
    {"Symbol": "Fm", "Name": "Fermium", "AtomicNumber": 100, "AtomicMass": 257, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.3, "Hazards": ["Radioaktif"]},
    {"Symbol": "Md", "Name": "Mendelevium", "AtomicNumber": 101, "AtomicMass": 258, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.3, "Hazards": ["Radioaktif"]},
    {"Symbol": "No", "Name": "Nobelium", "AtomicNumber": 102, "AtomicMass": 259, 
     "Group": None, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.3, "Hazards": ["Radioaktif"]},
    {"Symbol": "Lr", "Name": "Lawrensium", "AtomicNumber": 103, "AtomicMass": 262, 
     "Group": 3, "Period": 7, "Category": "Aktinida", "Color": "#FF9E6D", "Electronegativity": 1.3, "Hazards": ["Radioaktif"]},
    {"Symbol": "Rf", "Name": "Rutherfordium", "AtomicNumber": 104, "AtomicMass": 267, 
     "Group": 4, "Period": 7, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Db", "Name": "Dubnium", "AtomicNumber": 105, "AtomicMass": 268, 
     "Group": 5, "Period": 7, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Sg", "Name": "Seaborgium", "AtomicNumber": 106, "AtomicMass": 271, 
     "Group": 6, "Period": 7, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Bh", "Name": "Bohrium", "AtomicNumber": 107, "AtomicMass": 272, 
     "Group": 7, "Period": 7, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Hs", "Name": "Hassium", "AtomicNumber": 108, "AtomicMass": 270, 
     "Group": 8, "Period": 7, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Mt", "Name": "Meitnerium", "AtomicNumber": 109, "AtomicMass": 276, 
     "Group": 9, "Period": 7, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Ds", "Name": "Darmstadtium", "AtomicNumber": 110, "AtomicMass": 281, 
     "Group": 10, "Period": 7, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Rg", "Name": "Roentgenium", "AtomicNumber": 111, "AtomicMass": 280, 
     "Group": 11, "Period": 7, "Category": "Logam Transisi", "Color": "#B5651D", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Cn", "Name": "Kopernisium", "AtomicNumber": 112, "AtomicMass": 285, 
     "Group": 12, "Period": 7, "Category": "Logam Transisi", "Color": "#7FFFD4", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Nh", "Name": "Nihonium", "AtomicNumber": 113, "AtomicMass": 286, 
     "Group": 13, "Period": 7, "Category": "Logam Pascatransisi", "Color": "#118AB2", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Fl", "Name": "Flerovium", "AtomicNumber": 114, "AtomicMass": 289, 
     "Group": 14, "Period": 7, "Category": "Logam Pascatransisi", "Color": "#073B4C", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Mc", "Name": "Moscovium", "AtomicNumber": 115, "AtomicMass": 290, 
     "Group": 15, "Period": 7, "Category": "Logam Pascatransisi", "Color": "#FF6B6B", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Lv", "Name": "Livermorium", "AtomicNumber": 116, "AtomicMass": 293, 
     "Group": 16, "Period": 7, "Category": "Logam Pascatransisi", "Color": "#FFD166", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Ts", "Name": "Tennessine", "AtomicNumber": 117, "AtomicMass": 294, 
     "Group": 17, "Period": 7, "Category": "Halogen", "Color": "#06D6A0", "Electronegativity": None, "Hazards": ["Radioaktif"]},
    {"Symbol": "Og", "Name": "Oganesson", "AtomicNumber": 118, "AtomicMass": 294, 
     "Group": 18, "Period": 7, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": None, "Hazards": ["Radioaktif"]}
]

# Database senyawa kimia (diperbanyak)
COMPOUNDS = {
    "Asam Klorida (HCl)": {"color": "#F0F0F0", "formula": "HCl", "type": "Asam Kuat", "hazards": ["Korosif"]},
    "Natrium Hidroksida (NaOH)": {"color": "#FFFFFF", "formula": "NaOH", "type": "Basa Kuat", "hazards": ["Korosif"]},
    "Tembaga Sulfat (CuSO₄)": {"color": "#00B4D8", "formula": "CuSO₄", "type": "Garam", "hazards": ["Beracun"]},
    "Besi (Fe)": {"color": "#B5651D", "formula": "Fe", "type": "Logam", "hazards": []},
    "Kalium Permanganat (KMnO₄)": {"color": "#9D00FF", "formula": "KMnO₄", "type": "Oksidator", "hazards": ["Pengoksidasi"]},
    "Asam Sulfat (H₂SO₄)": {"color": "#F5F5F5", "formula": "H₂SO₄", "type": "Asam Kuat", "hazards": ["Korosif"]},
    "Air (H₂O)": {"color": "#ADD8E6", "formula": "H₂O", "type": "Pelarut", "hazards": []},
    "Hidrogen Peroksida (H₂O₂)": {"color": "#F0F8FF", "formula": "H₂O₂", "type": "Oksidator", "hazards": ["Pengoksidasi"]},
    "Natrium Karbonat (Na₂CO₃)": {"color": "#FFFFFF", "formula": "Na₂CO₃", "type": "Garam", "hazards": []},
    "Kalsium Klorida (CaCl₂)": {"color": "#FFFFFF", "formula": "CaCl₂", "type": "Garam", "hazards": ["Iritan"]},
    "Asam Asetat (CH₃COOH)": {"color": "#F5F5DC", "formula": "CH₃COOH", "type": "Asam Lemah", "hazards": ["Korosif"]},
    "Amonia (NH₃)": {"color": "#F0F8FF", "formula": "NH₃", "type": "Basa Lemah", "hazards": ["Beracun", "Korosif"]},
    "Etanol (C₂H₅OH)": {"color": "#F0FFF0", "formula": "C₂H₅OH", "type": "Alkohol", "hazards": ["Mudah Terbakar"]},
    "Metana (CH₄)": {"color": "#87CEEB", "formula": "CH₄", "type": "Hidrokarbon", "hazards": ["Mudah Terbakar", "Gas"]},
    "Glukosa (C₆H₁₂O₆)": {"color": "#FFFFFF", "formula": "C₆H₁₂O₆", "type": "Karbohidrat", "hazards": []},
    "Natrium Klorida (NaCl)": {"color": "#FFFFFF", "formula": "NaCl", "type": "Garam", "hazards": []},
    "Besi Sulfat (FeSO₄)": {"color": "#76D7EA", "formula": "FeSO₄", "type": "Garam", "hazards": []},
    "Karbon Dioksida (CO₂)": {"color": "#A9A9A9", "formula": "CO₂", "type": "Gas", "hazards": ["Gas Bertekanan"]},
    "Oksigen (O₂)": {"color": "#87CEEB", "formula": "O₂", "type": "Gas", "hazards": ["Pengoksidasi"]},
    "Tembaga (Cu)": {"color": "#D2691E", "formula": "Cu", "type": "Logam", "hazards": []},
    "Asam Nitrat (HNO₃)": {"color": "#FFFFE0", "formula": "HNO₃", "type": "Asam Kuat", "hazards": ["Korosif", "Pengoksidasi"]},
    "Kalium Hidroksida (KOH)": {"color": "#FFFFFF", "formula": "KOH", "type": "Basa Kuat", "hazards": ["Korosif"]},
    "Perak Nitrat (AgNO₃)": {"color": "#FFFFFF", "formula": "AgNO₃", "type": "Garam", "hazards": ["Korosif"]},
    "Klorin (Cl₂)": {"color": "#90EE90", "formula": "Cl₂", "type": "Gas", "hazards": ["Beracun", "Korosif"]},
    "Belerang Dioksida (SO₂)": {"color": "#F5F5F5", "formula": "SO₂", "type": "Gas", "hazards": ["Beracun"]},
    "Amonium Nitrat (NH₄NO₃)": {"color": "#FFFFFF", "formula": "NH₄NO₃", "type": "Garam", "hazards": ["Pengoksidasi"]},
    "Kalsium Karbida (CaC₂)": {"color": "#FFFFFF", "formula": "CaC₂", "type": "Senyawa Karbon", "hazards": ["Reaktif"]},
    "Asam Sitrat (C₆H₈O₇)": {"color": "#FFFFE0", "formula": "C₆H₈O₇", "type": "Asam Organik", "hazards": []},
    "Benzena (C₆H₆)": {"color": "#87CEEB", "formula": "C₆H₆", "type": "Hidrokarbon", "hazards": ["Mudah Terbakar", "Karsinogen"]},
    "Natrium Bikarbonat (NaHCO₃)": {"color": "#FFFFFF", "formula": "NaHCO₃", "type": "Garam", "hazards": []},
    "Magnesium (Mg)": {"color": "#FFD700", "formula": "Mg", "type": "Logam", "hazards": ["Mudah Terbakar"]},
    "Fenolftalein": {"color": "#FF69B4", "formula": "C₂₀H₁₄O₄", "type": "Indikator", "hazards": ["Iritan"]},
    "Kalium Iodida (KI)": {"color": "#FFFFFF", "formula": "KI", "type": "Garam", "hazards": []},
    "Hidrogen (H₂)": {"color": "#F0F8FF", "formula": "H₂", "type": "Gas", "hazards": ["Mudah Terbakar", "Gas"]},
    "Kalsium Oksida (CaO)": {"color": "#FFFFFF", "formula": "CaO", "type": "Oksida", "hazards": ["Korosif"]},
    "Seng Klorida (ZnCl₂)": {"color": "#FFFFFF", "formula": "ZnCl₂", "type": "Garam", "hazards": ["Korosif"]},
    "Natrium Tiosulfat (Na₂S₂O₃)": {"color": "#FFFFFF", "formula": "Na₂S₂O₃", "type": "Garam", "hazards": []},
    "Asam Fosfat (H₃PO₄)": {"color": "#F5F5F5", "formula": "H₃PO₄", "type": "Asam", "hazards": ["Korosif"]},
    "Kalium Sianida (KCN)": {"color": "#FFFFFF", "formula": "KCN", "type": "Garam", "hazards": ["Beracun", "Sangat Berbahaya"]},
    "Natrium Asetat (CH₃COONa)": {"color": "#FFFFFF", "formula": "CH₃COONa", "type": "Garam", "hazards": []},
    "Karbon Monoksida (CO)": {"color": "#A9A9A9", "formula": "CO", "type": "Gas", "hazards": ["Beracun"]},
    "Iodin (I₂)": {"color": "#9400D3", "formula": "I₂", "type": "Halogen", "hazards": ["Beracun"]},
    "Aluminium Klorida (AlCl₃)": {"color": "#FFFFFF", "formula": "AlCl₃", "type": "Garam", "hazards": ["Korosif"]},
    "Natrium Sulfat (Na₂SO₄)": {"color": "#FFFFFF", "formula": "Na₂SO₄", "type": "Garam", "hazards": []},
    "Kalium Klorat (KClO₃)": {"color": "#FFFFFF", "formula": "KClO₃", "type": "Oksidator", "hazards": ["Pengoksidasi"]},
    "Seng (Zn)": {"color": "#7FFFD4", "formula": "Zn", "type": "Logam", "hazards": []},
    "Asam Oksalat (H₂C₂O₄)": {"color": "#FFFFFF", "formula": "H₂C₂O₄", "type": "Asam Organik", "hazards": ["Korosif", "Beracun"]},
    "Kalium Dikromat (K₂Cr₂O₇)": {"color": "#FF4500", "formula": "K₂Cr₂O₇", "type": "Oksidator", "hazards": ["Karsinogen"]},
    "Natrium Hipoklorit (NaClO)": {"color": "#F0F8FF", "formula": "NaClO", "type": "Oksidator", "hazards": ["Korosif"]},
    "Amonium Hidroksida (NH₄OH)": {"color": "#F0F8FF", "formula": "NH₄OH", "type": "Basa Lemah", "hazards": ["Korosif"]},
    "Kalsium Hidroksida (Ca(OH)₂)": {"color": "#FFFFFF", "formula": "Ca(OH)₂", "type": "Basa", "hazards": ["Iritan"]},
    "Belerang (S)": {"color": "#FFD166", "formula": "S", "type": "Nonlogam", "hazards": []},
    "Natrium Nitrat (NaNO₃)": {"color": "#FFFFFF", "formula": "NaNO₃", "type": "Garam", "hazards": ["Pengoksidasi"]},
    "Asam Tartarat (C₄H₆O₆)": {"color": "#FFFFFF", "formula": "C₄H₆O₆", "type": "Asam Organik", "hazards": []},
    "Toluena (C₇H₈)": {"color": "#87CEEB", "formula": "C₇H₈", "type": "Hidrokarbon", "hazards": ["Mudah Terbakar"]},
    "Kalsium Oksalat (CaC₂O₄)": {"color": "#FFFFFF", "formula": "CaC₂O₄", "type": "Garam", "hazards": ["Beracun"]},
    "Natrium Asam Sulfat (NaHSO₄)": {"color": "#FFFFFF", "formula": "NaHSO₄", "type": "Garam Asam", "hazards": ["Korosif"]},
    "Barium Klorida (BaCl₂)": {"color": "#FFFFFF", "formula": "BaCl₂", "type": "Garam", "hazards": ["Beracun"]},
    "Natrium Sulfida (Na₂S)": {"color": "#FFFFE0", "formula": "Na₂S", "type": "Garam", "hazards": ["Korosif", "Beracun"]},
    "Asam Benzoat (C₇H₆O₂)": {"color": "#FFFFFF", "formula": "C₇H₆O₂", "type": "Asam Organik", "hazards": ["Iritan"]},
    "Fosfor Pentaklorida (PCl₅)": {"color": "#FFFFFF", "formula": "PCl₅", "type": "Reagen", "hazards": ["Korosif"]},
    "Kalium Hidrogen Ftalat (KHC₈H₄O₄)": {"color": "#FFFFFF", "formula": "KHC₈H₄O₄", "type": "Standar", "hazards": []},
    "Kloroform (CHCl₃)": {"color": "#87CEEB", "formula": "CHCl₃", "type": "Pelarut", "hazards": ["Karsinogen"]},
    "Asam Borat (H₃BO₃)": {"color": "#FFFFFF", "formula": "H₃BO₃", "type": "Asam Lemah", "hazards": ["Iritan"]},
    "Tembaga Oksida (CuO)": {"color": "#000000", "formula": "CuO", "type": "Oksida", "hazards": []},
    "Besi Oksida (Fe₂O₃)": {"color": "#B22222", "formula": "Fe₂O₃", "type": "Oksida", "hazards": []},
    "Natrium Oksida (Na₂O)": {"color": "#FFFFFF", "formula": "Na₂O", "type": "Oksida", "hazards": ["Korosif"]},
    "Magnesium Oksida (MgO)": {"color": "#FFFFFF", "formula": "MgO", "type": "Oksida", "hazards": []},
    "Aluminium Oksida (Al₂O₃)": {"color": "#FFFFFF", "formula": "Al₂O₃", "type": "Oksida", "hazards": []},
    "Seng Oksida (ZnO)": {"color": "#FFFFFF", "formula": "ZnO", "type": "Oksida", "hazards": []},
    "Timbal Oksida (PbO)": {"color": "#FFD700", "formula": "PbO", "type": "Oksida", "hazards": ["Beracun"]},
    "Perak Oksida (Ag₂O)": {"color": "#C0C0C0", "formula": "Ag₂O", "type": "Oksida", "hazards": []},
    "Merkuri Oksida (HgO)": {"color": "#FF0000", "formula": "HgO", "type": "Oksida", "hazards": ["Beracun"]},
    "Kalsium Karbonat (CaCO₃)": {"color": "#FFFFFF", "formula": "CaCO₃", "type": "Garam", "hazards": []},
    "Natrium Fosfat (Na₃PO₄)": {"color": "#FFFFFF", "formula": "Na₃PO₄", "type": "Garam", "hazards": []},
    "Kalium Karbonat (K₂CO₃)": {"color": "#FFFFFF", "formula": "K₂CO₃", "type": "Garam", "hazards": []},
    "Magnesium Sulfat (MgSO₄)": {"color": "#FFFFFF", "formula": "MgSO₄", "type": "Garam", "hazards": []},
    "Barium Sulfat (BaSO₄)": {"color": "#FFFFFF", "formula": "BaSO₄", "type": "Garam", "hazards": []},
    "Kalium Sulfat (K₂SO₄)": {"color": "#FFFFFF", "formula": "K₂SO₄", "type": "Garam", "hazards": []},
    "Amonium Klorida (NH₄Cl)": {"color": "#FFFFFF", "formula": "NH₄Cl", "type": "Garam", "hazards": []},
    "Natrium Hidroksida (NaOH)": {"color": "#FFFFFF", "formula": "NaOH", "type": "Basa Kuat", "hazards": ["Korosif"]},
    "Kalium Hidroksida (KOH)": {"color": "#FFFFFF", "formula": "KOH", "type": "Basa Kuat", "hazards": ["Korosif"]},
    "Kalsium Hidroksida (Ca(OH)₂)": {"color": "#FFFFFF", "formula": "Ca(OH)₂", "type": "Basa", "hazards": ["Iritan"]},
    "Magnesium Hidroksida (Mg(OH)₂)": {"color": "#FFFFFF", "formula": "Mg(OH)₂", "type": "Basa", "hazards": []},
    "Aluminium Hidroksida (Al(OH)₃)": {"color": "#FFFFFF", "formula": "Al(OH)₃", "type": "Basa", "hazards": []},
    "Besi Hidroksida (Fe(OH)₃)": {"color": "#B5651D", "formula": "Fe(OH)₃", "type": "Basa", "hazards": []},
    "Tembaga Hidroksida (Cu(OH)₂)": {"color": "#00B4D8", "formula": "Cu(OH)₂", "type": "Basa", "hazards": []},
    "Seng Hidroksida (Zn(OH)₂)": {"color": "#FFFFFF", "formula": "Zn(OH)₂", "type": "Basa", "hazards": []},
    "Timbal Hidroksida (Pb(OH)₂)": {"color": "#FFD700", "formula": "Pb(OH)₂", "type": "Basa", "hazards": ["Beracun"]},
    "Perak Hidroksida (AgOH)": {"color": "#C0C0C0", "formula": "AgOH", "type": "Basa", "hazards": []},
    "Merkuri Hidroksida (Hg(OH)₂)": {"color": "#FF0000", "formula": "Hg(OH)₂", "type": "Basa", "hazards": ["Beracun"]}
}

# Database reaksi kimia (diperbanyak)
REACTIONS = [
    # Reaksi asam-basa
    {
        "reagents": ["Asam Klorida (HCl)", "Natrium Hidroksida (NaOH)"],
        "products": ["Natrium Klorida (NaCl)", "Air (H₂O)"],
        "equation": "HCl + NaOH → NaCl + H₂O",
        "type": "Netralisasi",
        "color_change": ["#F0F0F0 + #FFFFFF → #FFFFFF + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Korosif"],
        "apd": ["Kacamata", "Sarung Tangan"],
        "description": "Reaksi netralisasi antara asam kuat dan basa kuat menghasilkan garam dan air."
    },
    {
        "reagents": ["Asam Sulfat (H₂SO₄)", "Kalium Hidroksida (KOH)"],
        "products": ["Kalium Sulfat (K₂SO₄)", "Air (H₂O)"],
        "equation": "H₂SO₄ + 2KOH → K₂SO₄ + 2H₂O",
        "type": "Netralisasi",
        "color_change": ["#F5F5F5 + #FFFFFF → #FFFFFF + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Korosif"],
        "apd": ["Kacamata", "Sarung Tangan", "Jas Lab"],
        "description": "Reaksi netralisasi antara asam sulfat dan kalium hidroksida."
    },
    {
        "reagents": ["Asam Asetat (CH₃COOH)", "Natrium Hidroksida (NaOH)"],
        "products": ["Natrium Asetat (CH₃COONa)", "Air (H₂O)"],
        "equation": "CH₃COOH + NaOH → CH₃COONa + H₂O",
        "type": "Netralisasi",
        "color_change": ["#F5F5DC + #FFFFFF → #FFFFFF + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Korosif"],
        "apd": ["Kacamata", "Sarung Tangan"],
        "description": "Reaksi netralisasi antara asam lemah dan basa kuat."
    },
    
    # Reaksi logam-asam
    {
        "reagents": ["Magnesium (Mg)", "Asam Klorida (HCl)"],
        "products": ["Magnesium Klorida (MgCl₂)", "Hidrogen (H₂)"],
        "equation": "Mg + 2HCl → MgCl₂ + H₂",
        "type": "Reaksi Logam-Asam",
        "color_change": ["#FFD700 + #F0F0F0 → #FFFFFF + #F0F8FF"],
        "energy": "Eksoterm",
        "hazards": ["Gas Mudah Terbakar"],
        "apd": ["Kacamata", "Sarung Tangan"],
        "description": "Logam magnesium bereaksi dengan asam klorida menghasilkan gas hidrogen."
    },
    {
        "reagents": ["Seng (Zn)", "Asam Sulfat (H₂SO₄)"],
        "products": ["Seng Sulfat (ZnSO₄)", "Hidrogen (H₂)"],
        "equation": "Zn + H₂SO₄ → ZnSO₄ + H₂",
        "type": "Reaksi Logam-Asam",
        "color_change": ["#7FFFD4 + #F5F5F5 → #FFFFFF + #F0F8FF"],
        "energy": "Eksoterm",
        "hazards": ["Gas Mudah Terbakar"],
        "apd": ["Kacamata", "Sarung Tangan"],
        "description": "Logam seng bereaksi dengan asam sulfat menghasilkan gas hidrogen."
    },
    {
        "reagents": ["Besi (Fe)", "Asam Klorida (HCl)"],
        "products": ["Besi Klorida (FeCl₂)", "Hidrogen (H₂)"],
        "equation": "Fe + 2HCl → FeCl₂ + H₂",
        "type": "Reaksi Logam-Asam",
        "color_change": ["#B5651D + #F0F0F0 → #76D7EA + #F0F8FF"],
        "energy": "Eksoterm",
        "hazards": ["Gas Mudah Terbakar"],
        "apd": ["Kacamata", "Sarung Tangan"],
        "description": "Logam besi bereaksi dengan asam klorida menghasilkan gas hidrogen."
    },
    
    # Reaksi pengendapan
    {
        "reagents": ["Perak Nitrat (AgNO₃)", "Natrium Klorida (NaCl)"],
        "products": ["Perak Klorida (AgCl)", "Natrium Nitrat (NaNO₃)"],
        "equation": "AgNO₃ + NaCl → AgCl + NaNO₃",
        "type": "Pengendapan",
        "color_change": ["#FFFFFF + #FFFFFF → #FFFFFF + #FFFFFF"],
        "energy": "Endoterm",
        "hazards": [],
        "apd": ["Kacamata"],
        "description": "Reaksi pengendapan menghasilkan endapan putih perak klorida."
    },
    {
        "reagents": ["Barium Klorida (BaCl₂)", "Natrium Sulfat (Na₂SO₄)"],
        "products": ["Barium Sulfat (BaSO₄)", "Natrium Klorida (NaCl)"],
        "equation": "BaCl₂ + Na₂SO₄ → BaSO₄ + 2NaCl",
        "type": "Pengendapan",
        "color_change": ["#FFFFFF + #FFFFFF → #FFFFFF + #FFFFFF"],
        "energy": "Endoterm",
        "hazards": ["Beracun"],
        "apd": ["Kacamata", "Sarung Tangan"],
        "description": "Reaksi pengendapan menghasilkan endapan putih barium sulfat."
    },
    {
        "reagents": ["Tembaga Sulfat (CuSO₄)", "Natrium Hidroksida (NaOH)"],
        "products": ["Tembaga Hidroksida (Cu(OH)₂)", "Natrium Sulfat (Na₂SO₄)"],
        "equation": "CuSO₄ + 2NaOH → Cu(OH)₂ + Na₂SO₄",
        "type": "Pengendapan",
        "color_change": ["#00B4D8 + #FFFFFF → #00B4D8 + #FFFFFF"],
        "energy": "Endoterm",
        "hazards": [],
        "apd": ["Kacamata"],
        "description": "Reaksi pengendapan menghasilkan endapan biru tembaga hidroksida."
    },
    
    # Reaksi redoks
    {
        "reagents": ["Kalium Permanganat (KMnO₄)", "Asam Oksalat (H₂C₂O₄)"],
        "products": ["Mangan Sulfat (MnSO₄)", "Karbon Dioksida (CO₂)", "Kalium Sulfat (K₂SO₄)", "Air (H₂O)"],
        "equation": "2KMnO₄ + 5H₂C₂O₄ + 3H₂SO₄ → 2MnSO₄ + 10CO₂ + K₂SO₄ + 8H₂O",
        "type": "Redoks",
        "color_change": ["#9D00FF + #FFFFFF → #B5651D + #A9A9A9 + #FFFFFF + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Beracun"],
        "apd": ["Kacamata", "Sarung Tangan", "Jas Lab"],
        "description": "Reaksi titrasi antara kalium permanganat dan asam oksalat."
    },
    {
        "reagents": ["Kalium Dikromat (K₂Cr₂O₇)", "Asam Sulfat (H₂SO₄)"],
        "products": ["Kromium Sulfat (Cr₂(SO₄)₃)", "Kalium Sulfat (K₂SO₄)", "Air (H₂O)", "Oksigen (O₂)"],
        "equation": "4K₂Cr₂O₇ + 6H₂SO₄ → 2Cr₂(SO₄)₃ + 2K₂SO₄ + 6H₂O + 3O₂",
        "type": "Redoks",
        "color_change": ["#FF4500 + #F5F5F5 → #B5651D + #FFFFFF + #ADD8E6 + #87CEEB"],
        "energy": "Eksoterm",
        "hazards": ["Pengoksidasi", "Korosif", "Karsinogen"],
        "apd": ["Sarung Tangan", "Kacamata", "Jas Lab", "Pelindung Wajah"],
        "description": "Reaksi dekomposisi kalium dikromat dengan asam sulfat menghasilkan gas oksigen."
    },
    {
        "reagents": ["Hidrogen Peroksida (H₂O₂)", "Kalium Iodida (KI)"],
        "products": ["Iodin (I₂)", "Kalium Hidroksida (KOH)"],
        "equation": "H₂O₂ + 2KI → I₂ + 2KOH",
        "type": "Redoks",
        "color_change": ["#F0F8FF + #FFFFFF → #9400D3 + #FFFFFF"],
        "energy": "Eksoterm",
        "hazards": ["Beracun"],
        "apd": ["Kacamata", "Sarung Tangan"],
        "description": "Reaksi menghasilkan iodin yang berwarna ungu."
    },
    
    # Reaksi pembakaran
    {
        "reagents": ["Metana (CH₄)", "Oksigen (O₂)"],
        "products": ["Karbon Dioksida (CO₂)", "Air (H₂O)"],
        "equation": "CH₄ + 2O₂ → CO₂ + 2H₂O",
        "type": "Pembakaran",
        "color_change": ["#87CEEB + #87CEEB → #A9A9A9 + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Mudah Terbakar"],
        "apd": ["Kacamata"],
        "description": "Pembakaran metana menghasilkan karbon dioksida dan air."
    },
    {
        "reagents": ["Etanol (C₂H₅OH)", "Oksigen (O₂)"],
        "products": ["Karbon Dioksida (CO₂)", "Air (H₂O)"],
        "equation": "C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O",
        "type": "Pembakaran",
        "color_change": ["#F0FFF0 + #87CEEB → #A9A9A9 + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Mudah Terbakar"],
        "apd": ["Kacamata"],
        "description": "Pembakaran etanol menghasilkan karbon dioksida dan air."
    },
    {
        "reagents": ["Magnesium (Mg)", "Oksigen (O₂)"],
        "products": ["Magnesium Oksida (MgO)"],
        "equation": "2Mg + O₂ → 2MgO",
        "type": "Pembakaran",
        "color_change": ["#FFD700 + #87CEEB → #FFFFFF"],
        "energy": "Eksoterm",
        "hazards": ["Cahaya Terang"],
        "apd": ["Kacamata Pelindung", "Sarung Tangan"],
        "description": "Pembakaran magnesium menghasilkan cahaya putih terang."
    },
    
    # Reaksi sintesis
    {
        "reagents": ["Belerang (S)", "Besi (Fe)"],
        "products": ["Besi Sulfida (FeS)"],
        "equation": "Fe + S → FeS",
        "type": "Sintesis",
        "color_change": ["#FFD166 + #B5651D → #B5651D"],
        "energy": "Eksoterm",
        "hazards": ["Panas"],
        "apd": ["Sarung Tangan", "Kacamata"],
        "description": "Pembentukan besi sulfida dari logam besi dan belerang."
    },
    {
        "reagents": ["Hidrogen (H₂)", "Oksigen (O₂)"],
        "products": ["Air (H₂O)"],
        "equation": "2H₂ + O₂ → 2H₂O",
        "type": "Sintesis",
        "color_change": ["#F0F8FF + #87CEEB → #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Ledakan"],
        "apd": ["Kacamata", "Pelindung Wajah"],
        "description": "Reaksi pembentukan air dari hidrogen dan oksigen."
    },
    {
        "reagents": ["Natrium (Na)", "Klorin (Cl₂)"],
        "products": ["Natrium Klorida (NaCl)"],
        "equation": "2Na + Cl₂ → 2NaCl",
        "type": "Sintesis",
        "color_change": ["#FFD166 + #90EE90 → #FFFFFF"],
        "energy": "Eksoterm",
        "hazards": ["Ledakan"],
        "apd": ["Kacamata", "Pelindung Wajah", "Sarung Tangan"],
        "description": "Reaksi pembentukan garam dapur dari natrium dan klorin."
    },
    
    # Reaksi dekomposisi
    {
        "reagents": ["Kalium Klorat (KClO₃)"],
        "products": ["Kalium Klorida (KCl)", "Oksigen (O₂)"],
        "equation": "2KClO₃ → 2KCl + 3O₂",
        "type": "Dekomposisi",
        "color_change": ["#FFFFFF → #FFFFFF + #87CEEB"],
        "energy": "Endoterm",
        "hazards": ["Pengoksidasi"],
        "apd": ["Kacamata"],
        "description": "Dekomposisi kalium klorat menghasilkan oksigen."
    },
    {
        "reagents": ["Kalsium Karbonat (CaCO₃)"],
        "products": ["Kalsium Oksida (CaO)", "Karbon Dioksida (CO₂)"],
        "equation": "CaCO₃ → CaO + CO₂",
        "type": "Dekomposisi",
        "color_change": ["#FFFFFF → #FFFFFF + #A9A9A9"],
        "energy": "Endoterm",
        "hazards": [],
        "apd": ["Kacamata"],
        "description": "Dekomposisi kalsium karbonat menghasilkan kalsium oksida dan karbon dioksida."
    },
    {
        "reagents": ["Hidrogen Peroksida (H₂O₂)"],
        "products": ["Air (H₂O)", "Oksigen (O₂)"],
        "equation": "2H₂O₂ → 2H₂O + O₂",
        "type": "Dekomposisi",
        "color_change": ["#F0F8FF → #ADD8E6 + #87CEEB"],
        "energy": "Eksoterm",
        "hazards": ["Pengoksidasi"],
        "apd": ["Kacamata"],
        "description": "Dekomposisi hidrogen peroksida menghasilkan oksigen."
    },
    
    # Reaksi pertukaran ganda
    {
        "reagents": ["Natrium Nitrat (NaNO₃)", "Kalium Klorida (KCl)"],
        "products": ["Kalium Nitrat (KNO₃)", "Natrium Klorida (NaCl)"],
        "equation": "NaNO₃ + KCl → KNO₃ + NaCl",
        "type": "Pertukaran Ganda",
        "color_change": ["#FFFFFF + #FFFFFF → #FFFFFF + #FFFFFF"],
        "energy": "Endoterm",
        "hazards": [],
        "apd": ["Sarung Tangan"],
        "description": "Reaksi pertukaran ion antara natrium nitrat dan kalium klorida."
    },
    {
        "reagents": ["Tembaga Sulfat (CuSO₄)", "Besi (Fe)"],
        "products": ["Besi Sulfat (FeSO₄)", "Tembaga (Cu)"],
        "equation": "CuSO₄ + Fe → FeSO₄ + Cu",
        "type": "Pertukaran Ganda",
        "color_change": ["#00B4D8 + #B5651D → #76D7EA + #D2691E"],
        "energy": "Eksoterm",
        "hazards": [],
        "apd": ["Kacamata"],
        "description": "Reaksi pertukaran logam tembaga dengan besi."
    },
    {
        "reagents": ["Perak Nitrat (AgNO₃)", "Tembaga (Cu)"],
        "products": ["Tembaga Nitrat (Cu(NO₃)₂)", "Perak (Ag)"],
        "equation": "2AgNO₃ + Cu → Cu(NO₃)₂ + 2Ag",
        "type": "Pertukaran Ganda",
        "color_change": ["#FFFFFF + #D2691E → #00B4D8 + #C0C0C0"],
        "energy": "Eksoterm",
        "hazards": [],
        "apd": ["Kacamata"],
        "description": "Reaksi pertukaran logam perak dengan tembaga."
    },
    
    # Reaksi khusus
    {
        "reagents": ["Kalium Klorat (KClO₃)", "Gula (C₁₂H₂₂O₁₁)"],
        "products": ["Kalium Klorida (KCl)", "Karbon Dioksida (CO₂)", "Air (H₂O)"],
        "equation": "8KClO₃ + C₁₂H₂₂O₁₁ → 8KCl + 12CO₂ + 11H₂O",
        "type": "Reaksi Pembakaran",
        "color_change": ["#FFFFFF + #FFFFFF → #FFFFFF + #A9A9A9 + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Ledakan", "Panas"],
        "apd": ["Kacamata", "Sarung Tangan", "Pelindung Wajah"],
        "description": "Reaksi pembakaran gula dengan kalium klorat menghasilkan nyala api yang kuat."
    },
    {
        "reagents": ["Natrium Hipoklorit (NaClO)", "Hidrogen Peroksida (H₂O₂)"],
        "products": ["Natrium Klorida (NaCl)", "Oksigen (O₂)", "Air (H₂O)"],
        "equation": "NaClO + H₂O₂ → NaCl + O₂ + H₂O",
        "type": "Redoks",
        "color_change": ["#F0F8FF + #F0F8FF → #FFFFFF + #87CEEB + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Gas Bertekanan"],
        "apd": ["Sarung Tangan", "Kacamata"],
        "description": "Reaksi antara pemutih dan hidrogen peroksida menghasilkan gas oksigen."
    },
    {
        "reagents": ["Amonium Hidroksida (NH₄OH)", "Tembaga Sulfat (CuSO₄)"],
        "products": ["Tembaga Hidroksida (Cu(OH)₂)", "Amonium Sulfat ((NH₄)₂SO₄)"],
        "equation": "2NH₄OH + CuSO₄ → Cu(OH)₂ + (NH₄)₂SO₄",
        "type": "Pengendapan",
        "color_change": ["#F0F8FF + #00B4D8 → #00B4D8 + #FFFFFF"],
        "energy": "Endoterm",
        "hazards": ["Iritan"],
        "apd": ["Sarung Tangan", "Kacamata"],
        "description": "Reaksi menghasilkan endapan tembaga hidroksida berwarna biru."
    },
    {
        "reagents": ["Kloroform (CHCl₃)", "Oksigen (O₂)"],
        "products": ["Karbon Dioksida (CO₂)", "Hidrogen Klorida (HCl)"],
        "equation": "2CHCl₃ + 5O₂ → 2CO₂ + 2HCl + 2Cl₂",
        "type": "Pembakaran",
        "color_change": ["#87CEEB + #87CEEB → #A9A9A9 + #F0F0F0"],
        "energy": "Eksoterm",
        "hazards": ["Gas Beracun"],
        "apd": ["Masker Respirator", "Kacamata"],
        "description": "Pembakaran kloroform menghasilkan gas beracun."
    }
]

# Fungsi untuk membuat kartu unsur
def create_element_card(element):
    hazards_html = ""
    if element["Hazards"]:
        hazards_html = "<div style='margin-top:10px;'><b>Bahaya:</b><br>"
        for hazard in element["Hazards"]:
            hazards_html += f"<span class='warning-badge'>{hazard}</span> "
        hazards_html += "</div>"
    
    card = f"""
    <div class="element-card">
        <div style="background:{element['Color']}; 
                    background:linear-gradient(135deg, {element['Color']}, #FFFFFF);
                    border-radius:50%; width:80px; height:80px; 
                    display:flex; align-items:center; justify-content:center; margin:0 auto 15px;
                    box-shadow: 0 6px 12px rgba(0,0,0,0.2);">
            <h2 style="color:white; margin:0; text-shadow:2px 2px 4px rgba(0,0,0,0.5);">{element['Symbol']}</h2>
        </div>
        <h3 style="text-align:center; margin-bottom:10px; color:{dark_color};">{element['Name']}</h3>
        <div style="background:rgba(255,255,255,0.7); border-radius:15px; padding:10px;">
            <p style="text-align:center; margin:5px 0; font-size:1rem; color:{text_color};">
                <b>No Atom:</b> {element['AtomicNumber']}<br>
                <b>Massa:</b> {element['AtomicMass']}<br>
                <b>Golongan:</b> {element['Group']}<br>
                <b>Periode:</b> {element['Period']}<br>
                <b>Kategori:</b> {element['Category']}
            </p>
        </div>
        {hazards_html}
    </div>
    """
    return card

# Fungsi untuk menampilkan tabel periodik
def show_periodic_table():
    st.markdown("""
    <div class="header-with-emoji">
        <span class="emoji">📋</span>
        <h1>Tabel Periodik Interaktif</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px;">Tabel Periodik Unsur Kimia (118 Unsur Lengkap)</h2>
        <p style="text-align:center; font-size:18px;">Klik pada kartu unsur untuk melihat detail lengkap</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Kategori warna
    categories = {
        "Logam Alkali": "#FFD166",
        "Logam Alkali Tanah": "#06D6A0",
        "Logam Transisi": "#118AB2",
        "Logam Pascatransisi": "#073B4C",
        "Metaloid": "#6A4C93",
        "Nonlogam": "#FF6B6B",
        "Halogen": "#4ECDC4",
        "Gas Mulia": "#EF476F",
        "Lantanida": "#FF9E6D",
        "Aktinida": "#FF9E6D",
        "Belum Diketahui": "#9D4EDD"
    }
    
    # Filter kategori
    selected_category = st.selectbox("Filter Kategori", ["Semua"] + list(categories.keys()), key="category_filter")
    
    # Tampilkan legenda
    st.subheader("Legenda Kategori")
    cols = st.columns(5)
    for i, (cat, color) in enumerate(categories.items()):
        cols[i % 5].markdown(f"""
        <div style="background:{color}; 
                    background:linear-gradient(135deg, {color}, #FFFFFF);
                    border-radius:10px; padding:1
