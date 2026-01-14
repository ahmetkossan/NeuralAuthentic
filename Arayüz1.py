import streamlit as st
import hashlib
import time
import cv2
import tempfile
import numpy as np
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="NeuralAuthentic Lab", page_icon="⚖️", layout="wide")

# --- ÖZEL TASARIM VE CANLI SAAT SCRİPTİ ---
st.markdown("""
<style>
    /* Arka plan ve genel yazı tipi */
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    
    /* Yan menü (Sidebar) tasarımı */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* "Çocuksu" kutu yerine daha profesyonel bir durum alanı */
    .status-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #0d1117;
        border: 1px solid #30363d;
        margin-bottom: 10px;
        font-family: 'Courier New', monospace;
    }
    .status-label { color: #8b949e; font-size: 0.8rem; text-transform: uppercase; }
    .status-value { color: #58a6ff; font-weight: bold; font-size: 1rem; }

    /* Dijital Saat Tasarımı */
    #digital-clock {
        font-family: 'Courier New', monospace;
        color: #3fb950;
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>

<script>
    // Kullanıcının cihaz saatini anlık güncelleyen fonksiyon
    function updateClock() {
        const now = new Date();
        const timeStr = now.getHours().toString().padStart(2, '0') + ":" + 
                        now.getMinutes().toString().padStart(2, '0') + ":" + 
                        now.getSeconds().toString().padStart(2, '0');
        document.getElementById('digital-clock').innerText = timeStr;
    }
    setInterval(updateClock, 1000); // Her saniye güncelle
</script>
""", unsafe_allow_html=True)

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/shield.png", width=80)
    st.title("NeuralAuthentic")
    st.markdown("---")
    
    # Yeni, profesyonel durum paneli
    st.markdown("""
    <div class="status-box">
        <div class="status-label">Analiz Modu</div>
        <div class="status-value">ADLİ BİLİŞİM (FORENSIC)</div>
    </div>
    <div class="status-box">
        <div class="status-label">Operatör</div>
        <div class="status-value">Ahmet Can Koşan</div>
    </div>
    <div class="status-box">
        <div class="status-label">Cihaz Yerel Saati</div>
        <div id="digital-clock">Yükleniyor...</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.caption("Üsküdar Üniversitesi | Bitirme Tezi v2.0")

# --- ANA EKRAN ---
st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1000", use_column_width=True)
st.title("🛡️ NeuralAuthentic: Video Otantisite Konsolu")
st.write("Dijital delil inceleme ve doğrulama arayüzü.")
st.markdown("---")

# Not: Diğer fonksiyonlar (MD5, Sekmeler, Analiz) önceki kodla aynı kalacak şekilde buraya eklenebilir.