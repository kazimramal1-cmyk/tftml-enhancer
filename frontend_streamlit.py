# ================================================================
#  frontend_streamlit.py — TFTML ENHANCER AI v9
#  Şəkil + Video | SAM yoxdur
# ================================================================

import streamlit as st

if not hasattr(st, 'image_to_url'):
    st.image_to_url = lambda x: x

import requests, base64, io, time, threading, os
from PIL import Image, ImageEnhance
import numpy as np

# ══════════════════════════════════════════════════════
#  KONFİQURASİYA
# ══════════════════════════════════════════════════════
API_URL   = "https://stacie-apertural-ardelia.ngrok-free.dev"  # ← Colab URL-ini dəyiş
LOGO_FILE = "logo_png.jpeg"

def load_logo():
    """logo_png.jpeg-i base64-ə çevirir. Tapılmasa None."""
    try:
        if os.path.exists(LOGO_FILE):
            with open(LOGO_FILE, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception:
        pass
    return None

LOGO_B64 = load_logo()

# ══════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="TFTML ENHANCER AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

#MainMenu,footer,header,.stDeployButton,[data-testid="stToolbar"]{display:none!important}
.stApp{background:#0d0f0e!important;font-family:'DM Sans',sans-serif!important}
.block-container{max-width:980px!important;padding:1.5rem!important;margin:0 auto!important}
.stApp::before{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background:radial-gradient(ellipse at 15% 40%,rgba(26,107,47,.12) 0%,transparent 55%),
             radial-gradient(ellipse at 85% 20%,rgba(224,112,32,.10) 0%,transparent 55%)}

.rk-brand{position:fixed;top:16px;left:20px;z-index:999;
  font-size:.72rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
  color:#e07020;text-decoration:underline;text-underline-offset:4px}

.logo-wrap{display:flex;justify-content:center;margin:1.5rem 0 .6rem}
.logo-img{width:110px;height:110px;border-radius:50%;object-fit:cover;
  animation:glowPulse 3s ease-in-out infinite}
.logo-emoji{width:110px;height:110px;border-radius:50%;background:#1a6b2f;
  display:flex;align-items:center;justify-content:center;font-size:3rem;
  margin:auto;animation:glowPulse 3s ease-in-out infinite}
@keyframes glowPulse{
  0%,100%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #1a6b2f,0 0 25px rgba(26,107,47,.55)}
  50%    {box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #e07020,0 0 30px rgba(224,112,32,.6)}}

.main-title{font-family:'Playfair Display',serif;font-size:clamp(1.2rem,3vw,1.8rem);
  font-weight:700;text-align:center;color:#f0f0f0;margin:.2rem 0 .1rem}
.main-title span{color:#e07020}
.sname{text-align:center;font-size:.82rem;color:#888;line-height:1.6;margin:.1rem 0}
.sname b{color:#bbb}
.ssub{text-align:center;font-size:.62rem;color:#444;letter-spacing:.15em;
  text-transform:uppercase;margin-bottom:1.4rem}

.status-ok {background:linear-gradient(135deg,#0a1f10,#0d2b15);border:1px solid #1a6b2f;
  border-radius:12px;padding:.55rem 1.2rem;font-size:.78rem;color:#4dff88;font-weight:600;margin-bottom:1rem}
.status-err{background:linear-gradient(135deg,#1f0a0a,#2b0d0d);border:1px solid #6b1a1a;
  border-radius:12px;padding:.55rem 1.2rem;font-size:.78rem;color:#ff6b6b;font-weight:600;margin-bottom:1rem}

[data-testid="stTabs"] [data-testid="stTab"]{
  background:transparent!important;border:none!important;color:#666!important;
  font-weight:600!important;font-size:.85rem!important;padding:.6rem 1.2rem!important;
  border-radius:10px 10px 0 0!important}
[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"]{
  background:linear-gradient(135deg,#1a6b2f,#0d3d1a)!important;
  color:#4dff88!important;border-bottom:2px solid #2d9e4a!important}
[data-testid="stTabContent"]{border:1.5px solid #1e251e!important;
  border-radius:0 16px 16px 16px!important;
  background:linear-gradient(145deg,#111311,#0f110f)!important;padding:1.5rem!important}

.stButton>button{font-family:'DM Sans',sans-serif!important;font-weight:700!important;
  background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;color:#fff!important;
  border:none!important;border-radius:12px!important;padding:.85rem 2rem!important;
  width:100%!important;box-shadow:0 4px 20px rgba(26,107,47,.4)!important;transition:transform .2s!important}
.stButton>button:hover{transform:scale(1.03) translateY(-2px)!important}
.stButton>button:disabled{opacity:.35!important}

.stProgress>div>div{background:linear-gradient(90deg,#1a6b2f,#e07020)!important;border-radius:3px!important}
[data-testid="stImage"] img{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}
video{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}

.badge{display:inline-block;font-size:.58rem;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;padding:.2rem .55rem;border-radius:4px;margin-bottom:.4rem}
.b-orig{background:rgba(80,80,80,.3);color:#aaa;border:1px solid #333}
.b-enh {background:rgba(26,107,47,.4);color:#4dff88;border:1px solid #1a6b2f}

.info-box{background:#0d1510;border:1px solid #1a3320;border-radius:10px;
  padding:.7rem 1rem;font-size:.76rem;color:#4dff88;margin:.5rem 0}
.warn-box{background:linear-gradient(135deg,#1a1200,#2b1e00);border:1px solid #6b4e00;
  border-radius:12px;padding:.8rem 1.2rem;font-size:.78rem;color:#ffcc44;
  line-height:1.7;margin:.6rem 0;text-align:center}

.stDownloadButton>button{font-weight:600!important;font-size:.82rem!important;
  border-radius:10px!important;padding:.6rem 1.2rem!important;width:100%!important;
  background:#111!important;border:1.5px solid #1e251e!important;color:#aaa!important}
.stDownloadButton>button:hover{border-color:#2d9e4a!important;color:#4dff88!important}
[data-testid="stSlider"]>div>div>div{background:#1a6b2f!important}
</style>
<div class="rk-brand">RAMAL KAZIMZADE</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════
if LOGO_B64:
    st.markdown(
        f'<div class="logo-wrap"><img class="logo-img" src="data:image/jpeg;base64,{LOGO_B64}"></div>',
        unsafe_allow_html=True)
else:
    st.markdown('<div class="logo-wrap"><div class="logo-emoji">🎓</div></div>',
                unsafe_allow_html=True)

st.markdown("""
<div class="main-title">TFTML <span>ENHANCER</span> AI</div>
<div class="sname">K. Ağayev adına <b>Biləsuvar Şəhər</b><br>
Texniki Fənlər Təmayüllü İnternat Tipli Məktəb-Lisey</div>
<div class="ssub">Real-ESRGAN 4× · H.264 Video · AI Şəkil Keyfiyyəti</div>
""", unsafe_allow_html=True)

# ── API statusu ──────────────────────────────────────
def check_api(url):
    try:
        r = requests.get(f"{url}/health", timeout=6,
                         headers={"bypass-tunnel-reminder":"yes",
                                  "ngrok-skip-browser-warning":"true"})
        if r.status_code == 200:
            return True, r.json()
    except:
        pass
    return False, {}

api_ok, api_info = check_api(API_URL)

if api_ok:
    gpu_txt = api_info.get("device", "CPU")
    ffm_txt = "H.264 ✅" if api_info.get("ffmpeg") else "mp4v ⚠️"
    st.markdown(
        f'<div class="status-ok">✅ Backend Aktiv &nbsp;·&nbsp; '
        f'🖥️ {gpu_txt} &nbsp;·&nbsp; 🎞️ {ffm_txt}</div>',
        unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="status-err">⚠️ Backend offline — Colab-ı işə salın</div>',
        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  KÖMƏKÇI FUNKSIYALAR
# ══════════════════════════════════════════════════════
def pil_to_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()

def apply_effects(img, brightness, contrast):
    return ImageEnhance.Contrast(
        ImageEnhance.Brightness(img).enhance(brightness)).enhance(contrast)

MSGS_IMG = ["🚀 AI mühərriki işə düşür...","🧪 Piksellər bərpa olunur...",
            "✨ Möcüzə baş verir...","🎨 Rənglər canlanır...","⚡ GPU tam gücündə..."]
MSGS_VID = ["🎬 Kadrlar ayrılır...","⚡ Hər kadr böyüdülür...",
            "🔄 Video yığılır...","🎞️ H.264 çevrilir...","✨ Az qaldı..."]

HEADERS = {"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"}

# ══════════════════════════════════════════════════════
#  TABLƏR
# ══════════════════════════════════════════════════════
tab1, tab2 = st.tabs(["🖼️  Şəkil Artır", "🎬  Video Artır"])

# ══════════════════════════════════════════════════════
#  TAB 1 — ŞƏKİL
# ══════════════════════════════════════════════════════
with tab1:
    uploaded  = st.file_uploader("📸  Şəkil seçin (JPG, PNG, WEBP, BMP)",
                                  type=["jpg","jpeg","png","webp","bmp"], key="img_up")
    final_img = None

    if uploaded:
        orig_pil = Image.open(uploaded).convert("RGB")
        col_prev, col_fx = st.columns([3, 2])

        with col_fx:
            with st.expander("✂️ Kəsim", expanded=False):
                w, h = orig_pil.size
                c1, c2 = st.columns(2)
                with c1:
                    cl = st.number_input("Sol",    0, w-10, 0, step=5, key="cl")
                    ct = st.number_input("Yuxarı", 0, h-10, 0, step=5, key="ct")
                with c2:
                    cr = st.number_input("Sağ",   10, w, w, step=5, key="cr")
                    cb = st.number_input("Aşağı", 10, h, h, step=5, key="cb")

            with st.expander("🎨 Effektlər", expanded=True):
                brightness = st.slider("☀️ Parlaqlıq", 0.5, 2.0, 1.0, 0.05, key="br")
                contrast   = st.slider("🌗 Kontrast",  0.5, 2.0, 1.0, 0.05, key="co")

        with col_prev:
            final_img = apply_effects(orig_pil.crop((cl, ct, cr, cb)), brightness, contrast)
            st.markdown('<p style="text-align:center;font-size:.68rem;color:#555;'
                        'text-transform:uppercase;margin-bottom:.3rem">Önizləmə</p>',
                        unsafe_allow_html=True)
            st.image(final_img, use_container_width=True)
            st.caption(f"📐 {final_img.width}×{final_img.height} px")

    btn1 = st.button("✨  AI ilə 4× Keyfiyyəti Artır",
                     disabled=not (uploaded and api_ok and final_img is not None),
                     key="btn1")

    if btn1 and final_img:
        send_bytes = pil_to_bytes(final_img)
        prog = st.progress(0); msg_box = st.empty(); stop = [False]

        def spin_img():
            i = 0
            while not stop[0]:
                msg_box.markdown(
                    f'<div style="text-align:center;font-size:.95rem;font-weight:600;'
                    f'color:#e07020;padding:.7rem">{MSGS_IMG[i%len(MSGS_IMG)]}</div>',
                    unsafe_allow_html=True)
                time.sleep(2); i += 1
        threading.Thread(target=spin_img, daemon=True).start()
        prog.progress(15, "Göndərilir...")

        rb, err = None, None
        try:
            resp = requests.post(f"{API_URL}/enhance",
                                 files={"image":("img.png", send_bytes, "image/png")},
                                 timeout=300, headers=HEADERS)
            d = resp.json()
            rb  = base64.b64decode(d["image"]) if d.get("success") else None
            err = None if d.get("success") else d.get("error","Xəta")
        except Exception as e:
            err = str(e)

        stop[0] = True; msg_box.empty(); prog.progress(100)

        if err:
            st.error(f"❌ {err}")
        else:
            st.balloons(); st.success("🎉 Tamamlandı!")
            result_pil = Image.open(io.BytesIO(rb))
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<p style="text-align:center"><span class="badge b-orig">ƏVVƏLKİ</span></p>',
                            unsafe_allow_html=True)
                st.image(final_img, use_container_width=True)
                st.caption(f"📐 {final_img.width}×{final_img.height}")
            with c2:
                st.markdown('<p style="text-align:center"><span class="badge b-enh">4× AI</span></p>',
                            unsafe_allow_html=True)
                st.image(result_pil, use_container_width=True)
                st.caption(f"📐 {result_pil.width}×{result_pil.height}")
            st.download_button("⬇  Artırılmış Şəkli Endir", rb,
                f"enhanced_{uploaded.name.rsplit('.',1)[0]}.png",
                "image/png", use_container_width=True)

# ══════════════════════════════════════════════════════
#  TAB 2 — VİDEO
# ══════════════════════════════════════════════════════
with tab2:
    st.markdown(
        '<div class="warn-box">⚠️ Video emalı bir neçə dəqiqə çəkə bilər.<br>'
        'Emal zamanı pəncərəni bağlamayın! Böyük videolar üçün GPU tövsiyə edilir.</div>',
        unsafe_allow_html=True)

    video_file = st.file_uploader("🎬  Video seçin (MP4, MOV, AVI)",
                                   type=["mp4","mov","avi","mkv"], key="vid_up")
    if video_file:
        size_mb = video_file.size / 1024 / 1024
        st.video(video_file)
        st.markdown(
            f'<div class="info-box">📦 {video_file.name} &nbsp;·&nbsp; {size_mb:.1f} MB</div>',
            unsafe_allow_html=True)

        if size_mb > 200:
            st.warning("⚠️ Fayl 200 MB-dan böyükdür. Emal uzun çəkə bilər.")

    btn2 = st.button("🎬  Video 4× Keyfiyyətini Artır",
                     disabled=not (video_file and api_ok), key="btn2")

    if btn2 and video_file:
        vid_bytes = video_file.read()
        prog_v    = st.progress(0)
        msg_v     = st.empty()
        pct_box   = st.empty()
        stop_v    = [False]

        def spin_vid():
            i = 0
            while not stop_v[0]:
                msg_v.markdown(
                    f'<div style="text-align:center;font-size:.95rem;font-weight:600;'
                    f'color:#e07020;padding:.7rem">{MSGS_VID[i%len(MSGS_VID)]}</div>',
                    unsafe_allow_html=True)
                time.sleep(4); i += 1
        threading.Thread(target=spin_vid, daemon=True).start()

        # Progress simulasiya (real progress server-sidedədir)
        def fake_progress():
            p = 5
            while not stop_v[0] and p < 90:
                time.sleep(8)
                p = min(p + 5, 90)
                prog_v.progress(p, f"Emal edilir... ~{p}%")
        threading.Thread(target=fake_progress, daemon=True).start()

        prog_v.progress(5, "Video göndərilir...")
        ext = video_file.name.rsplit(".", 1)[-1].lower()

        rb_v, err_v, meta = None, None, {}
        try:
            resp_v = requests.post(
                f"{API_URL}/enhance-video",
                files={"video": (video_file.name, vid_bytes, f"video/{ext}")},
                timeout=1800,       # 30 dəqiqə — uzun videolar üçün
                headers=HEADERS)
            d = resp_v.json()
            if d.get("success"):
                rb_v = base64.b64decode(d["video"])
                meta = d
            else:
                err_v = d.get("error","Naməlum xəta")
        except Exception as e:
            err_v = str(e)

        stop_v[0] = True
        msg_v.empty(); pct_box.empty()

        if err_v:
            prog_v.progress(100, "Xəta!")
            st.error(f"❌ {err_v}")
        else:
            prog_v.progress(100, "Video hazır! 🎉")
            st.balloons()
            st.success(
                f"🎉 Video hazır! &nbsp; "
                f"{meta.get('original','?')} → {meta.get('enhanced','?')} &nbsp;·&nbsp; "
                f"{meta.get('frames','?')} kadr &nbsp;·&nbsp; "
                f"{meta.get('fps','?')} FPS &nbsp;·&nbsp; "
                f"Codec: {meta.get('codec','?')}")

            # Videonu göstər
            st.markdown("**📺 Nəticə:**")
            st.video(rb_v)

            st.download_button(
                "⬇  4× Videonu Endir (MP4 H.264)", rb_v,
                f"enhanced_{video_file.name.rsplit('.',1)[0]}.mp4",
                "video/mp4", use_container_width=True)
