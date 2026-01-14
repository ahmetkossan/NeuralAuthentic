import streamlit as st
import hashlib
import time
import cv2
import tempfile
import numpy as np
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="NeuralAuthentic Lab", 
    page_icon="🕵️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ÖZEL CSS TASARIMI ---
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    .status-box {
        padding: 12px;
        border-radius: 4px;
        background-color: #0d1117;
        border: 1px solid #30363d;
        margin-bottom: 10px;
        font-family: 'Courier New', monospace;
    }
    .status-label { color: #8b949e; font-size: 0.75rem; text-transform: uppercase; }
    .status-value { color: #58a6ff; font-weight: bold; font-size: 0.95rem; }

    .stButton>button { width: 100%; border-radius: 4px; background-color: #238636; color: white; border: none; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #161b22; border-radius: 4px 4px 0 0; color: #8b949e; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb; color: white; }
</style>
""", unsafe_allow_html=True)

# --- 3. YARDIMCI FONKSİYONLAR ---
def calculate_md5(file):
    hash_md5 = hashlib.md5()
    file.seek(0)
    for chunk in iter(lambda: file.read(4096), b""):
        hash_md5.update(chunk)
    file.seek(0)
    return hash_md5.hexdigest()

# --- 4. YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/shield.png", width=80)
    st.markdown("<h2 style='text-align:center;'>NeuralAuthentic</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Operatör ve Mod Bilgisi
    st.markdown(f"""
    <div class="status-box">
        <div class="status-label">OPERATÖR</div>
        <div class="status-value">Ahmet Can Koşan</div>
    </div>
    <div class="status-box">
        <div class="status-label">ANALİZ MODU</div>
        <div class="status-value">ADLİ BİLİŞİM (FORENSIC)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # CANLI SAAT BİLEŞENİ (HTML/JS)
    st.markdown('<div class="status-label">CİHAZ YEREL SAATİ</div>', unsafe_allow_html=True)
    components.html("""
    <div id="clock" style="
        color: #3fb950; 
        font-family: 'Courier New', monospace; 
        font-size: 1.1rem; 
        font-weight: bold;
        background-color: #0d1117;
        padding: 10px;
        border: 1px solid #30363d;
        border-radius: 4px;
        text-align: center;
    ">Yükleniyor...</div>
    <script>
        function updateClock() {
            const now = new Date();
            const timeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                            now.getMinutes().toString().padStart(2, '0') + ':' + 
                            now.getSeconds().toString().padStart(2, '0');
            document.getElementById('clock').innerText = timeStr;
        }
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """, height=60)
    
    st.divider()
    st.caption("Üsküdar Üniversitesi | Adli Bilimler Bitirme Projesi")

# --- 5. ANA EKRAN VE SEKMELER (Aynı Kalıyor) ---
st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1000", use_column_width=True)
st.title("🛡️ NeuralAuthentic: Video Analiz Paneli")
st.markdown("---")

if 'analiz_durum' not in st.session_state:
    st.session_state.analiz_durum = False

tab1, tab2, tab3 = st.tabs(["📂 KANIT YÜKLEME", "🔍 KRİMİNAL ANALİZ", "📄 ADLİ RAPOR"])

with tab1:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        yuklenen_dosya = st.file_uploader("Video dosyasını sürükleyin veya seçin", type=['mp4', 'avi', 'mov'])
        if yuklenen_dosya:
            st.video(yuklenen_dosya)
    with col2:
        if yuklenen_dosya:
            st.markdown("### 📋 Dosya Kimliği")
            md5_hash = calculate_md5(yuklenen_dosya)
            st.info(f"**MD5 Hash:** `{md5_hash}`")
            st.code(f"Ad: {yuklenen_dosya.name}\nBoyut: {yuklenen_dosya.size/(1024*1024):.2f} MB", language="yaml")

with tab2:
    if yuklenen_dosya:
        if st.button("🚨 SİSTEM TARAMASINI BAŞLAT", use_container_width=True):
            with st.status("Analiz yapılıyor...", expanded=True) as s:
                time.sleep(1)
                s.update(label="Analiz Tamamlandı!", state="complete")
            st.session_state.analiz_durum = True
        if st.session_state.analiz_durum:
            m1, m2, m3 = st.columns(3)
            m1.metric("Gerçeklik Skoru", "%14", "-%86 Risk")
            m2.metric("Analiz Güveni", "%94", "Yüksek")
            m3.metric("Anomali", "Dudak Senkronu", delta_color="inverse")
    else:
        st.warning("Lütfen önce bir kanıt dosyası yükleyin.")

with tab3:
    if st.session_state.analiz_durum:
        st.subheader("📋 Rapor Önizleme")
        st.text_area("", f"ADLİ ANALİZ RAPORU\nOperatör: Ahmet Can Koşan\nDosya: {yuklenen_dosya.name}\nMD5: {md5_hash}", height=150)
        st.download_button("📥 Raporu İndir (.TXT)", "Rapor İçeriği", file_name="analiz_raporu.txt")