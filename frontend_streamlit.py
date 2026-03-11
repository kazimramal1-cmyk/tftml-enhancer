# ================================================================
#  frontend_streamlit.py — Real-ESRGAN Streamlit Frontend
#  Backend: https://long-geese-wave.loca.lt
# ================================================================

import streamlit as st
import requests, base64, hashlib, io
from PIL import Image

API_URL = 'https://stacie-apertural-ardelia.ngrok-free.dev'
LOGO_B64 = "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"

st.set_page_config(page_title="Lisey AI", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');
#MainMenu,footer,header,.stDeployButton,[data-testid="stToolbar"]{display:none!important}
.stApp{background:#f5f3ef!important;font-family:'DM Sans',sans-serif!important}
.block-container{max-width:860px!important;padding:2rem 1.5rem!important;margin:0 auto!important}
.hdr{text-align:center;padding:2rem 1rem 1.2rem;display:flex;flex-direction:column;align-items:center;gap:.9rem}
.ring{width:116px;height:116px;border-radius:50%;padding:6px;background:conic-gradient(#e07020,#1a6b2f,#f59030,#0d4f1c,#e07020);animation:spin 6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.sname{font-family:'Playfair Display',serif;font-size:1.15rem;line-height:1.55;color:#1a1a1a}
.sname span{color:#e07020}
.ssub{font-size:.68rem;font-weight:300;color:#aaa;letter-spacing:.14em;text-transform:uppercase}
.card{background:#fff;border-radius:20px;border:1.5px solid #e8e4de;padding:1.8rem;margin-bottom:1.4rem;box-shadow:0 2px 28px rgba(0,0,0,.05)}
[data-testid="stFileUploader"]{border:2px dashed #e0dcd6!important;border-radius:16px!important;background:#faf8f5!important;transition:all .2s!important}
[data-testid="stFileUploader"]:hover{border-color:#e07020!important;background:#fff8f4!important}
.stButton>button{font-family:'DM Sans',sans-serif!important;font-weight:700!important;font-size:1rem!important;background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;color:#fff!important;border:none!important;border-radius:14px!important;padding:1rem 2rem!important;width:100%!important;box-shadow:0 4px 22px rgba(26,107,47,.32)!important;transition:all .2s!important;letter-spacing:.03em!important}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 30px rgba(26,107,47,.42)!important}
.stDownloadButton>button{font-family:'DM Sans',sans-serif!important;font-weight:600!important;font-size:.85rem!important;border-radius:11px!important;padding:.6rem 1.2rem!important;width:100%!important;transition:all .2s!important}
.badge{display:inline-block;font-size:.6rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:.22rem .6rem;border-radius:5px;margin-bottom:.4rem}
.b-orig{background:rgba(80,80,80,.8);color:#fff}
.b-enh{background:rgba(26,107,47,.9);color:#fff}
.b-4x{background:linear-gradient(135deg,#e07020,#f59030);color:#fff;font-size:.62rem;font-weight:700;letter-spacing:.1em;padding:.24rem .7rem;border-radius:20px}
.stProgress>div>div{background:linear-gradient(90deg,#1a6b2f,#e07020)!important;border-radius:3px!important}
[data-testid="stImage"] img{border-radius:12px!important;border:1px solid #f0ece6!important;width:100%!important}
.status-ok{background:#f0faf3;border:1px solid #b7dfc5;border-radius:10px;padding:.55rem 1rem;font-size:.78rem;color:#1a6b2f;font-weight:600;margin-bottom:1rem}
.status-err{background:#fff5f5;border:1px solid #fcc;border-radius:10px;padding:.55rem 1rem;font-size:.78rem;color:#c00;font-weight:600;margin-bottom:1rem}
.cache-tag{background:#e8f4ff;border:1px solid #b3d4f5;border-radius:8px;padding:.3rem .8rem;font-size:.72rem;color:#2266aa;font-weight:600;display:inline-block;margin-bottom:.5rem}
</style>
""", unsafe_allow_html=True)

# ── Cache funksiyası ─────────────────────────────────────────────
@st.cache_data(show_spinner=False, max_entries=50)
def enhance_cached(img_bytes: bytes, api_url: str):
    try:
        resp = requests.post(
            f"{api_url}/enhance",
            files={"image": ("img.png", img_bytes, "image/png")},
            timeout=180,
            headers={"bypass-tunnel-reminder": "yes"}
        )
        data = resp.json()
        if data.get("success"):
            return base64.b64decode(data["image"]), None, False
        return None, data.get("error", "Naməlum xəta"), False
    except Exception as e:
        return None, str(e), False

def check_api(url):
    try:
        r = requests.get(f"{url}/health", timeout=6, headers={"bypass-tunnel-reminder": "yes"})
        return r.status_code == 200
    except:
        return False

# ── Header ──────────────────────────────────────────────────────
st.markdown(f"""
<div class="hdr">
  <div class="ring">
    <img src="data:image/jpeg;base64,{LOGO_B64}"
         style="width:104px;height:104px;border-radius:50%;object-fit:contain;background:#fff;padding:5px;display:block">
  </div>
  <div class="sname">K. Ağayev adına <span>Biləsuvar Şəhər</span><br>
  Texniki Fənlər Təmayüllü İnternat Tipli Məktəb-Lisey</div>
  <div class="ssub">AI Şəkil Keyfiyyət Platforması · Real-ESRGAN 4×</div>
</div>
""", unsafe_allow_html=True)

# ── API yoxla ───────────────────────────────────────────────────
api_ok = check_api(API_URL)
if api_ok:
    st.markdown('<div class="status-ok">✅ Colab Backend — Online · GPU aktiv</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-err">⚠️ Colab Backend offline — Colab-ı işə salın və URL-i yeniləyin</div>', unsafe_allow_html=True)

# ── Upload ──────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded = st.file_uploader("📸  Şəkli seçin və ya sürükləyin",
                             type=["jpg","jpeg","png","webp","bmp"],
                             label_visibility="visible")
if uploaded:
    col_p, col_i = st.columns([2,1])
    with col_p:
        st.image(uploaded, use_container_width=True)
    with col_i:
        img_hash = hashlib.md5(uploaded.read()).hexdigest()[:8]
        uploaded.seek(0)
        st.markdown(f"""
        <div style="padding:.6rem 0;font-size:.82rem;color:#666;line-height:2">
        <b>📄 Ad:</b> {uploaded.name}<br>
        <b>📦 Həcm:</b> {uploaded.size/1024/1024:.2f} MB<br>
        <b>🔑 Hash:</b> <code style="font-size:.7rem">{img_hash}</code>
        </div>""", unsafe_allow_html=True)

btn = st.button("✨  AI ilə 4× Keyfiyyəti Artır", disabled=not (uploaded and api_ok))
st.markdown('</div>', unsafe_allow_html=True)

# ── Emal ────────────────────────────────────────────────────────
if btn and uploaded:
    img_bytes = uploaded.read()

    # Cache yoxla
    cache_info = st.cache_data.clear  # sadəcə referans
    img_hash_full = hashlib.md5(img_bytes).hexdigest()

    prog = st.progress(0, "Colab-a göndərilir...")
    prog.progress(15, "Neyron şəbəkəsi aktivdir...")

    result_bytes, err, _ = enhance_cached(img_bytes, API_URL)

    prog.progress(100, "Hazır! ✅")

    if err:
        st.error(f"❌ Xəta: {err}")
    else:
        # Cache olub-olmadığını yoxla (eyni hash ikinci dəfə isə)
        if st.session_state.get(f"done_{img_hash_full}"):
            st.markdown('<div class="cache-tag">⚡ Cache-dən göstərilir — Colab-a sorğu getmədi</div>', unsafe_allow_html=True)
        st.session_state[f"done_{img_hash_full}"] = True

        st.success("✅ Emal tamamlandı!")

        orig_pil   = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        result_pil = Image.open(io.BytesIO(result_bytes))

        st.markdown("""<div class="card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem">
        <span style="font-family:'Playfair Display',serif;font-size:1rem">Nəticə</span>
        <span class="b-4x">4× Enhanced</span></div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>', unsafe_allow_html=True)
            st.image(orig_pil, use_container_width=True)
            st.caption(f"📐 {orig_pil.width}×{orig_pil.height} px")
        with c2:
            st.markdown('<p style="text-align:center"><span class="badge b-enh">4× AI</span></p>', unsafe_allow_html=True)
            st.image(result_pil, use_container_width=True)
            st.caption(f"📐 {result_pil.width}×{result_pil.height} px")

        d1, d2 = st.columns(2)
        with d1:
            st.download_button("⬇  Artırılmışı Endir (PNG)", result_bytes,
                               f"enhanced_{uploaded.name.rsplit('.',1)[0]}.png",
                               "image/png", use_container_width=True)
        with d2:
            st.download_button("⬇  Orijinalı Endir", img_bytes,
                               uploaded.name, "image/png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)