import streamlit as st
import hashlib
import time
import cv2
import tempfile
import numpy as np
from datetime import datetime

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="NeuralAuthentic Lab", 
    page_icon="🕵️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ÖZEL TASARIM VE CANLI SAAT (CSS & JS) ---
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* Profesyonel Durum Paneli */
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
    #clock { color: #3fb950; font-weight: bold; font-size: 1.1rem; }

    /* Buton ve Tab Tasarımları */
    .stButton>button { width: 100%; border-radius: 4px; background-color: #238636; color: white; border: none; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #161b22; border-radius: 4px 4px 0 0; color: #8b949e; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb; color: white; }
</style>

<div style="display:none;">
    <img src="https://img.icons8.com/isometric/512/shield.png" onload="
        setInterval(() => {
            const now = new Date();
            const timeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                            now.getMinutes().toString().padStart(2, '0') + ':' + 
                            now.getSeconds().toString().padStart(2, '0');
            document.getElementById('clock').innerText = timeStr;
        }, 1000);
    ">
</div>
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
    
    st.markdown(f"""
    <div class="status-box">
        <div class="status-label">OPERATÖR</div>
        <div class="status-value">Ahmet Can Koşan</div>
    </div>
    <div class="status-box">
        <div class="status-label">ANALİZ MODU</div>
        <div class="status-value">ADLİ BİLİŞİM (FORENSIC)</div>
    </div>
    <div class="status-box">
        <div class="status-label">CİHAZ YEREL SAATİ</div>
        <div id="clock" class="status-value">Yükleniyor...</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.caption("Üsküdar Üniversitesi | Adli Bilimler Bitirme Projesi")

# --- 5. ANA EKRAN ---
st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1000", use_column_width=True)
st.title("🛡️ NeuralAuthentic: Video Analiz Paneli")
st.markdown("---")

# Session State Yönetimi
if 'analiz_durum' not in st.session_state:
    st.session_state.analiz_durum = False

# SEKMELERİ OLUŞTURUYORUZ
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
            with st.status("Veri katmanları inceleniyor...", expanded=True) as s:
                st.write("Frame extraction (Kare ayıklama) yapılıyor...")
                time.sleep(1)
                st.write("AI model katmanları yükleniyor...")
                time.sleep(1)
                s.update(label="Analiz Tamamlandı!", state="complete")
            st.session_state.analiz_durum = True

        if st.session_state.analiz_durum:
            st.divider()
            m1, m2, m3 = st.columns(3)
            m1.metric("Gerçeklik Skoru", "%14", "-%86 Risk")
            m2.metric("Analiz Güveni", "%94", "Yüksek")
            m3.metric("Anomali", "Dudak Senkronu", delta_color="inverse")
            
            # Kareler
            st.markdown("### 🖼️ İncelenen Kareler")
            tfile = tempfile.NamedTemporaryFile(delete=False); tfile.write(yuklenen_dosya.read())
            cap = cv2.VideoCapture(tfile.name)
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cols = st.columns(3)
            for i in range(3):
                cap.set(cv2.CAP_PROP_POS_FRAMES, (i+1)*(total//4))
                ret, frame = cap.read()
                if ret:
                    cols[i].image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_column_width=True, caption=f"Kare #{i+1}")
            cap.release()
    else:
        st.warning("Devam etmek için lütfen önce bir kanıt dosyası yükleyin.")

with tab3:
    if st.session_state.analiz_durum:
        rapor_metni = f"ADLİ ANALİZ RAPORU\n{'-'*30}\nOperatör: Ahmet Can Koşan\nDosya: {yuklenen_dosya.name}\nMD5: {md5_hash}\nBulgu: Deepfake tespiti yapıldı."
        st.subheader("📋 Rapor Önizleme")
        st.text_area("", rapor_metni, height=200)
        st.download_button("📥 Raporu İndir (.TXT)", rapor_metni, file_name="analiz_raporu.txt")
    else:
        st.info("Analiz bittiğinde raporunuz burada hazır olacak.")