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
    page_title="Lab Kimia Interaktif 2025",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Warna tema yang lebih terang dan kontras
primary_color = "#4B8DF8"  # Biru cerah
secondary_color = "#00D1B2"  # Hijau tosca
accent_color = "#FFA500"  # Oranye
background_color = "#F9F9F9"  # Putih sangat muda
dark_color = "#2C3E50"  # Biru tua
text_color = "#333333"  # Abu tua
header_color = "#FFFFFF"  # Putih
card_background = "#FFFFFF"  # Putih
contrast_color = "#1A5276"  # Biru tua lebih terang

# CSS untuk styling yang lebih baik dengan gradasi tetap dan teks yang jelas
st.markdown(f"""
<style>
    /* Warna utama dengan kontras lebih baik */
    .stApp {{
        background: linear-gradient(135deg, {background_color}, #E6F0F9) !important;
        background-attachment: fixed;
    }}
    
    /* Gradasi tetap untuk semua elemen */
    .gradient-bg {{
        background: linear-gradient(135deg, {primary_color}, {secondary_color}) !important;
        color: white !important;
    }}
    
    .gradient-bg-light {{
        background: linear-gradient(135deg, rgba(75, 141, 248, 0.1), rgba(0, 209, 178, 0.1)) !important;
    }}
    
    /* Perbaikan kontras teks */
    h1, h2, h3, h4, h5, h6 {{
        color: {dark_color} !important;
        position: relative;
        z-index: 2;
    }}
    
    p, div, span, li, td {{
        color: {text_color} !important;
    }}
    
    /* Header dengan emoji */
    .header-with-emoji {{
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }}
    
    .header-with-emoji .emoji {{
        animation: bounce 2s infinite;
        font-size: 1.5em;
    }}
    
    /* Animasi */
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        50% {{ transform: translateY(-10px) rotate(10deg); }}
    }}
    
    /* Tombol dengan gradasi tetap */
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
    
    /* Kartu elemen dengan gradasi tetap */
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
    
    /* Container reaksi dengan gradasi tetap */
    .reaction-container {{
        background: white;
        border-radius: 25px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        border: 3px solid {accent_color};
        background-image: radial-gradient(circle at top right, rgba(255,255,255,0.8), rgba(255,255,255,0.4));
    }}
    
    /* Kotak warna dengan gradasi tetap */
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
    
    /* Badge dengan gradasi tetap */
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
    
    /* Header periodik dengan gradasi tetap */
    .periodic-header {{
        background: linear-gradient(135deg, {primary_color}, {secondary_color}) !important;
        padding: 25px;
        border-radius: 20px;
        color: {header_color};
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }}
    
    /* Animasi emoji melayang */
    .floating-emoji {{
        position: fixed;
        font-size: 24px;
        animation: float-emoji 15s infinite ease-in-out;
        z-index: 1;
        pointer-events: none;
    }}
    
    @keyframes float-emoji {{
        0% {{ transform: translate(0, 0) rotate(0deg); opacity: 0; }}
        10% {{ opacity: 0.8; }}
        90% {{ opacity: 0.8; }}
        100% {{ transform: translate(100vw, -100vh) rotate(360deg); opacity: 0; }}
    }}
    
    /* Animasi gelembung */
    .bubble {{
        position: fixed;
        border-radius: 50%;
        background: rgba(75, 141, 248, 0.1);
        animation: float-bubble 20s infinite ease-in-out;
        z-index: 1;
        pointer-events: none;
    }}
    
    @keyframes float-bubble {{
        0% {{ transform: translate(0, 0) scale(0.5); opacity: 0; }}
        10% {{ opacity: 0.5; }}
        90% {{ opacity: 0.5; }}
        100% {{ transform: translate(100vw, -100vh) scale(1.5); opacity: 0; }}
    }}
    
    /* Perbaikan kontras untuk semua teks */
    .stTabs > div > div > div > div {{
        color: {dark_color} !important;
    }}
    
    .stSelectbox > div > div {{
        background-color: white !important;
        color: {text_color} !important;
    }}
    
    /* Tab dengan gradasi tetap */
    .stTabs > div > div > div > div {{
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
    
    .stTabs > div > div > div > div:hover {{
        transform: scale(1.05);
        background: linear-gradient(135deg, {secondary_color}, {primary_color}) !important;
        color: white !important;
    }}
    
    .stTabs > div > div > div > div[aria-selected="true"] {{
        background: linear-gradient(135deg, {primary_color}, {accent_color}) !important;
        color: white !important;
        transform: scale(1.05);
        z-index: 1;
    }}
</style>
""", unsafe_allow_html=True)

# Animasi emoji dan gelembung melayang
st.markdown("""
<script>
// Fungsi untuk membuat emoji melayang
function createFloatingEmoji() {
    const emojis = ["🧪", "🔬", "⚗️", "🧫", "🧴", "💧", "🔥", "⚡", "🧲", "🧪", "🔭", "⚛️", "🧬", "🌡️", "🧼"];
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

// Fungsi untuk membuat gelembung
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

// Buat emoji dan gelembung secara berkala
setInterval(createFloatingEmoji, 2000);
setInterval(createBubble, 3000);

// Buat beberapa emoji dan gelembung saat pertama kali dimuat
for (let i = 0; i < 10; i++) {
    setTimeout(createFloatingEmoji, i * 500);
    setTimeout(createBubble, i * 700);
}
</script>
""", unsafe_allow_html=True)

# Database tabel periodik (118 unsur lengkap)
PERIODIC_TABLE = [
    # Periode 1
    {"Symbol": "H", "Name": "Hidrogen", "AtomicNumber": 1, "AtomicMass": 1.008, 
     "Group": 1, "Period": 1, "Category": "Nonlogam", "Color": "#FF6B6B", "Electronegativity": 2.20, "Hazards": ["Mudah Terbakar"]},
    {"Symbol": "He", "Name": "Helium", "AtomicNumber": 2, "AtomicMass": 4.0026, 
     "Group": 18, "Period": 1, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": None, "Hazards": []},
    
    # ... (rest of your periodic table data remains the same)
]

# Database senyawa kimia
COMPOUNDS = {
    "Asam Klorida (HCl)": {"color": "#F0F0F0", "formula": "HCl", "type": "Asam Kuat", "hazards": ["Korosif"]},
    # ... (rest of your compounds data remains the same)
}

# Database reaksi kimia
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
    # ... (rest of your reactions data remains the same)
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
    <div class="element-card gradient-bg-light">
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
        <h1>Tabel Periodik Interaktif 2025</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">Tabel Periodik Unsur Kimia (118 Unsur Lengkap)</h2>
        <p style="text-align:center; font-size:18px; color:white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Klik pada kartu unsur untuk melihat detail lengkap</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ... (rest of your periodic table function remains the same)

# Fungsi untuk menampilkan simulasi reaksi
def show_reaction_simulator():
    st.markdown("""
    <div class="header-with-emoji">
        <span class="emoji">🧪</span>
        <h1>Simulator Reaksi Kimia 2025</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">Simulasi Reaksi Kimia Interaktif</h2>
        <p style="text-align:center; font-size:18px; color:white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Pilih dua senyawa untuk melihat reaksi yang terjadi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ... (rest of your reaction simulator function remains the same)

# Fungsi untuk menampilkan informasi tambahan
def show_additional_info():
    st.markdown("""
    <div class="header-with-emoji">
        <span class="emoji">📚</span>
        <h1>Ensiklopedia Kimia 2025</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">Panduan Lengkap Kimia Dasar</h2>
        <p style="text-align:center; font-size:18px; color:white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Pelajari konsep-konsep dasar kimia dan eksperimen menarik</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ... (rest of your additional info function remains the same)

# Fungsi untuk menampilkan informasi PBK
def show_chemical_safety():
    st.markdown("""
    <div class="header-with-emoji">
        <span class="emoji">🧪</span>
        <h1>Penanganan Bahan Kimia 2025</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">Pedoman Penyimpanan dan Kompatibilitas Bahan Kimia</h2>
        <p style="text-align:center; font-size:18px; color:white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Pelajari cara menyimpan bahan kimia dengan aman dan kelompok kompatibilitas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ... (rest of your chemical safety function remains the same)

# UI Utama dengan gradasi tetap
st.markdown("""
<div style="background:linear-gradient(135deg, #1A5276, #4B8DF8); 
            padding:30px; border-radius:25px; color:white; margin-bottom:30px;
            text-align:center; box-shadow:0 12px 24px rgba(0,0,0,0.3); position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(circle at center, rgba(255,255,255,0.1), transparent);"></div>
    <h1 style="color:white; font-size:42px; margin:0; position: relative; z-index: 2; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">🔬 Selamat Datang di Laboratorium Kimia Virtual 2025!</h1>
    <p style="font-size:20px; margin:10px 0 0; position: relative; z-index: 2; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Jelajahi tabel periodik, simulasikan reaksi kimia, dan pelajari konsep kimia dengan cara menyenangkan</p>
</div>
""", unsafe_allow_html=True)

# Tab navigasi dengan gradasi tetap
tab1, tab2, tab3, tab4 = st.tabs(["📋 Tabel Periodik", "🧪 Simulator Reaksi", "📚 Ensiklopedia Kimia", "🛡️ Penanganan Bahan Kimia"])

with tab1:
    show_periodic_table()

with tab2:
    show_reaction_simulator()

with tab3:
    show_additional_info()

with tab4:
    show_chemical_safety()

# Footer dengan tahun 2025
st.divider()
st.markdown("""
<div style="text-align:center; padding:30px; color:#1A5276;">
    <p style="font-size:18px; margin:0;">🔬 Laboratorium Kimia Interaktif © 2025</p>
    <p style="font-size:16px; margin:10px 0;">Dikembangkan dengan Streamlit | Untuk tujuan edukasi</p>
    <p style="font-size:14px; margin:0;">Versi 6.0 | Terakhir diperbarui: 19 Juli 2025</p>
</div>
""", unsafe_allow_html=True)
