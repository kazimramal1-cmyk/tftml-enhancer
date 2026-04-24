# ================================================================
#  frontend_streamlit.py — TFTML ENHANCER AI v6
#  RAMAL KAZIMZADE | Şəkil + Inpainting + Video
# ================================================================

import streamlit as st
import requests, base64, hashlib, io, time, threading
from PIL import Image, ImageEnhance
import numpy as np

API_URL  = "https://stacie-apertural-ardelia.ngrok-free.dev"
# Nümunə olaraq:
LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCACWAJYDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSEl9fX5mfn6go6SoITWm9l83RkdPjw6fG5mJytK7197j5ufo6erx8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//Z"
    "🦕 Dinozavrlar":    "https://images.unsplash.com/photo-1606206873764-fd15e242ff80?w=1280&q=80",
    "🏛️ Big Ben":        "https://images.unsplash.com/photo-1529655683826-aba9b3e77383?w=1280&q=80",
    "🌌 Kainat":         "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1280&q=80",
    "🌊 Okean":          "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=1280&q=80",
    "🗼 Paris":          "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1280&q=80",
    "🏔️ Dağlar":         "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1280&q=80",
    "🌸 Çiçəklər":       "https://images.unsplash.com/photo-1490750967868-88df5691cc9e?w=1280&q=80",
    "🌆 Gecə şəhər":     "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1280&q=80",
    "🏖️ Çimərlik":       "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280&q=80",
    "🎨 Öz fonum":       "custom",
}

st.set_page_config(page_title="TFTML ENHANCER AI", page_icon="🎓",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

#MainMenu,footer,header,.stDeployButton,[data-testid="stToolbar"]{display:none!important}
.stApp{background:#0d0f0e!important;font-family:'DM Sans',sans-serif!important}
.block-container{max-width:960px!important;padding:1.5rem 1.5rem 2rem!important;margin:0 auto!important}
.stApp::before{content:'';position:fixed;inset:0;z-index:0;
  background:radial-gradient(ellipse at 15% 40%,rgba(26,107,47,.12) 0%,transparent 55%),
             radial-gradient(ellipse at 85% 20%,rgba(224,112,32,.10) 0%,transparent 55%);
  pointer-events:none}

/* ── RAMAL KAZIMZADE imzası ── */
.rk-brand{position:fixed;top:16px;left:20px;z-index:999;
  font-family:'DM Sans',sans-serif;font-size:.72rem;font-weight:700;
  letter-spacing:.2em;text-transform:uppercase;color:#e07020;
  text-decoration:underline;text-underline-offset:4px;
  text-decoration-color:rgba(224,112,32,.4);
  cursor:pointer;transition:all .2s}
.rk-brand:hover{color:#f59030;text-decoration-color:#f59030;
  text-shadow:0 0 12px rgba(224,112,32,.5);letter-spacing:.25em}

/* ── Logo ── */
.logo-wrap{display:flex;justify-content:center;margin:1.5rem 0 .6rem}
.logo-img{width:110px;height:110px;border-radius:50%;object-fit:cover;animation:glowPulse 3s ease-in-out infinite}
@keyframes glowPulse{
  0%,100%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #1a6b2f,0 0 0 7px #0d0f0e,0 0 25px rgba(26,107,47,.55),0 0 55px rgba(224,112,32,.2)}
  50%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #e07020,0 0 0 7px #0d0f0e,0 0 30px rgba(224,112,32,.6),0 0 65px rgba(26,107,47,.25)}}

.main-title{font-family:'Playfair Display',serif;font-size:clamp(1.2rem,3vw,1.8rem);
  font-weight:700;text-align:center;color:#f0f0f0;letter-spacing:.05em;margin:.2rem 0 .1rem}
.main-title span{color:#e07020}
.sname{text-align:center;font-size:.82rem;color:#888;line-height:1.6;margin:.1rem 0}
.sname b{color:#bbb}
.ssub{text-align:center;font-size:.62rem;color:#444;letter-spacing:.15em;
  text-transform:uppercase;margin-bottom:1.4rem}

/* ── Status ── */
.status-ok{background:linear-gradient(135deg,#0a1f10,#0d2b15);border:1px solid #1a6b2f;
  border-radius:12px;padding:.55rem 1.2rem;font-size:.78rem;color:#4dff88;font-weight:600;margin-bottom:1rem}
.status-err{background:linear-gradient(135deg,#1f0a0a,#2b0d0d);border:1px solid #6b1a1a;
  border-radius:12px;padding:.55rem 1.2rem;font-size:.78rem;color:#ff6b6b;font-weight:600;margin-bottom:1rem}

/* ── Tab ── */
[data-testid="stTabs"] [data-testid="stTab"]{
  background:transparent!important;border:none!important;
  color:#666!important;font-weight:600!important;font-size:.85rem!important;
  padding:.6rem 1.2rem!important;border-radius:10px 10px 0 0!important;transition:all .2s!important}
[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"]{
  background:linear-gradient(135deg,#1a6b2f,#0d3d1a)!important;
  color:#4dff88!important;border-bottom:2px solid #2d9e4a!important}
[data-testid="stTabs"] [data-testid="stTab"]:hover{color:#e07020!important}
[data-testid="stTabContent"]{border:1.5px solid #1e251e!important;border-radius:0 16px 16px 16px!important;
  background:linear-gradient(145deg,#111311,#0f110f)!important;padding:1.5rem!important}

/* ── Kart ── */
.card{background:linear-gradient(145deg,#131613,#111311);border-radius:16px;
  border:1.5px solid #1e251e;padding:1.5rem;margin-bottom:1.2rem;box-shadow:0 4px 30px rgba(0,0,0,.4)}

/* ── Upload ── */
[data-testid="stFileUploader"]{border:2px dashed transparent!important;border-radius:16px!important;
  background:linear-gradient(#131613,#131613) padding-box,
             linear-gradient(135deg,#1a6b2f,#e07020,#1a6b2f) border-box!important;
  padding:1.2rem!important;transition:all .3s!important}
[data-testid="stFileUploader"]:hover{
  background:linear-gradient(#0f1a0f,#0f1a0f) padding-box,
             linear-gradient(135deg,#2d9e4a,#f59030,#2d9e4a) border-box!important}
[data-testid="stFileUploader"] *{color:#888!important}
[data-testid="stFileUploader"] svg{fill:#e07020!important}
[data-testid="stFileUploader"] button{background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:8px!important}

/* ── Düymə ── */
.stButton>button{font-family:'DM Sans',sans-serif!important;font-weight:700!important;
  font-size:.95rem!important;background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:12px!important;
  padding:.85rem 2rem!important;width:100%!important;
  box-shadow:0 4px 20px rgba(26,107,47,.4)!important;transition:transform .2s,box-shadow .2s!important}
.stButton>button:hover{transform:scale(1.03) translateY(-2px)!important;
  box-shadow:0 8px 30px rgba(45,158,74,.55)!important}
.stButton>button:disabled{opacity:.35!important}

/* ── Inpainting canvas ── */
.canvas-wrap{border:2px solid #1e251e;border-radius:14px;overflow:hidden;
  background:#0a0c0a;margin:.8rem 0}
.brush-info{background:#0d1510;border:1px solid #1a3320;border-radius:10px;
  padding:.6rem 1rem;font-size:.75rem;color:#4dff88;margin:.5rem 0;
  display:flex;align-items:center;gap:.6rem}
.inpaint-tip{background:linear-gradient(135deg,#1a1200,#2b1e00);border:1px solid #6b4e00;
  border-radius:12px;padding:.8rem 1.2rem;font-size:.78rem;color:#ffcc44;
  line-height:1.7;margin:.6rem 0}

/* ── Slider + FX ── */
[data-testid="stSlider"]>div>div>div{background:#1a6b2f!important}
[data-testid="stSlider"] label{color:#aaa!important;font-size:.78rem!important}
.fx-panel{background:#0d1510;border:1px solid #1a3320;border-radius:12px;padding:1rem 1.2rem;margin:.5rem 0}
.fx-title{font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#4dff88;margin-bottom:.7rem}

/* ── Video xəbərdarlıq ── */
.video-warn{background:linear-gradient(135deg,#1a1200,#2b1e00);border:1px solid #6b4e00;
  border-radius:14px;padding:1rem 1.4rem;font-size:.82rem;color:#ffcc44;font-weight:600;
  margin:1rem 0;line-height:1.7;text-align:center}

/* ── Progress ── */
.stProgress>div>div{background:linear-gradient(90deg,#1a6b2f,#e07020)!important;border-radius:3px!important}
[data-testid="stImage"] img{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}
.spin-msg{text-align:center;font-size:.95rem;font-weight:600;color:#e07020;padding:.7rem}
.badge{display:inline-block;font-size:.58rem;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;padding:.2rem .55rem;border-radius:4px;margin-bottom:.4rem}
.b-orig{background:rgba(80,80,80,.3);color:#aaa;border:1px solid #333}
.b-enh{background:rgba(26,107,47,.4);color:#4dff88;border:1px solid #1a6b2f}
.b-4x{background:linear-gradient(135deg,#e07020,#f59030);color:#fff;font-size:.6rem;
  font-weight:700;letter-spacing:.1em;padding:.22rem .65rem;border-radius:18px}
.stDownloadButton>button{font-family:'DM Sans',sans-serif!important;font-weight:600!important;
  font-size:.82rem!important;border-radius:10px!important;padding:.6rem 1.2rem!important;
  width:100%!important;background:#111!important;border:1.5px solid #1e251e!important;
  color:#aaa!important;transition:all .2s!important}
.stDownloadButton>button:hover{border-color:#2d9e4a!important;color:#4dff88!important}
[data-testid="stCaptionContainer"]{color:#555!important;font-size:.7rem!important}
[data-testid="stRadio"] label,[data-testid="stRadio"] p{color:#aaa!important}
video{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}
</style>

<div class="rk-brand">RAMAL KAZIMZADE</div>
""", unsafe_allow_html=True)

# ── Köməkçi funksiyalar ──────────────────────────────────────────
@st.cache_data(show_spinner=False, max_entries=100)
def enhance_cached(img_bytes: bytes, fname: str, api_url: str):
    try:
        resp = requests.post(f"{api_url}/enhance",
            files={"image": (fname, img_bytes, "image/png")},
            timeout=300,
            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
        try: data = resp.json()
        except: return None,None,{},f"Parse xətası ({resp.status_code}): {resp.text[:200]}"
        if data.get("success"):
            return base64.b64decode(data["image"]),data.get("type","image"),data,None
        return None,None,{},data.get("error",f"Backend xətası: {data}")
    except requests.exceptions.Timeout: return None,None,{},"Timeout xətası"
    except requests.exceptions.ConnectionError: return None,None,{},"Bağlantı xətası"
    except Exception as e: return None,None,{},f"{type(e).__name__}: {str(e)}"

@st.cache_data(show_spinner=False, max_entries=20)
def enhance_video_cached(vid_bytes: bytes, fname: str, api_url: str):
    try:
        ext = fname.rsplit(".",1)[-1].lower() if "." in fname else "mp4"
        mime = {"mp4":"video/mp4","mov":"video/quicktime","avi":"video/x-msvideo"}.get(ext,"video/mp4")
        resp = requests.post(f"{api_url}/enhance-video",
            files={"video": (fname, vid_bytes, mime)},
            timeout=600,
            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
        try: data = resp.json()
        except: return None,{},f"Parse xətası ({resp.status_code}): {resp.text[:200]}"
        if data.get("success"): return base64.b64decode(data["image"]),data,None
        return None,{},data.get("error",f"Backend xətası: {data}")
    except requests.exceptions.Timeout: return None,{},"Timeout: Video çox böyükdür"
    except requests.exceptions.ConnectionError: return None,{},"Bağlantı xətası"
    except Exception as e: return None,{},f"{type(e).__name__}: {str(e)}"

def check_api(url):
    try:
        r = requests.get(f"{url}/health", timeout=6,
            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
        return r.status_code == 200
    except: return False

def pil_to_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()

def apply_effects(img, brightness, contrast):
    return ImageEnhance.Contrast(ImageEnhance.Brightness(img).enhance(brightness)).enhance(contrast)

@st.cache_data(show_spinner=False)
def fetch_bg(url):
    r = requests.get(url, timeout=15)
    return Image.open(io.BytesIO(r.content)).convert("RGBA")

def composite_bg(fg, bg):
    try:
        from rembg import remove as rembg_remove
        no_bg = Image.open(io.BytesIO(rembg_remove(pil_to_bytes(fg)))).convert("RGBA")
        bg_r  = bg.resize(no_bg.size, Image.LANCZOS).convert("RGBA")
        return Image.alpha_composite(bg_r, no_bg).convert("RGB")
    except ImportError:
        st.warning("⚠️  quraşdırılmayıb."); return fg

MSGS = ["🚀 AI mühərriki işə düşür...","🧪 Piksellər bərpa olunur...",
        "✨ Möcüzə baş verir...","🎨 Rənglər canlanır...","⚡ GPU tam gücündə..."]

# ── Header ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="logo-wrap"><img class="logo-img" src="data:image/jpeg;base64,{LOGO_B64}"></div>
<div class="main-title">TFTML <span>ENHANCER</span> AI</div>
<div class="sname">K. Ağayev adına <b>Biləsuvar Şəhər</b><br>
Texniki Fənlər Təmayüllü İnternat Tipli Məktəb-Lisey</div>
<div class="ssub">AI Şəkil və Video Keyfiyyət Platforması · Real-ESRGAN 4×</div>
""", unsafe_allow_html=True)

api_ok = check_api(API_URL)
if api_ok:
    st.markdown('<div class="status-ok">✅ Colab Backend — Online · GPU Aktiv</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-err">⚠️ Colab Backend offline — Colab-ı işə salın</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  TAB SİSTEMİ
# ══════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["🖼️  Şəkil Artır", "🧹  Obyekt Sil (Inpainting)", "🎬  Video Artır"])

# ══════════════════════════════════════════════════════════════════
#  TAB 1 — ŞƏKİL
# ══════════════════════════════════════════════════════════════════
with tab1:
    uploaded = st.file_uploader("📸  Şəkil seçin",
        type=["jpg","jpeg","png","webp","bmp"], label_visibility="visible", key="img_up")

    final_img = None
    if uploaded:
        orig_pil = Image.open(uploaded).convert("RGB")
        col_prev, col_fx = st.columns([3, 2])

        with col_fx:
            st.markdown('<div class="fx-panel">', unsafe_allow_html=True)
            st.markdown('<div class="fx-title">✂️ Kəsim</div>', unsafe_allow_html=True)
            w, h = orig_pil.size
            c1,c2 = st.columns(2)
            with c1:
                cl = st.number_input("Sol",   0,w-10,0,step=5,key="cl")
                ct = st.number_input("Yuxarı",0,h-10,0,step=5,key="ct")
            with c2:
                cr = st.number_input("Sağ",  10,w,w,step=5,key="cr")
                cb = st.number_input("Aşağı",10,h,h,step=5,key="cb")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="fx-panel">', unsafe_allow_html=True)
            st.markdown('<div class="fx-title">🎨 Effektlər</div>', unsafe_allow_html=True)
            brightness = st.slider("☀️ Parlaqlıq",0.5,2.0,1.0,0.05,key="br")
            contrast   = st.slider("🌗 Kontrast", 0.5,2.0,1.0,0.05,key="co")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="fx-panel">', unsafe_allow_html=True)
            st.markdown('<div class="fx-title">🖼️ Arxa Fon</div>', unsafe_allow_html=True)
            bg_choice = st.selectbox("Fon",list(BACKGROUNDS.keys()),key="bgc")
            apply_bg  = st.checkbox("✅ Arxa fonu dəyişdir",key="abg")
            custom_bg = None
            if BACKGROUNDS[bg_choice]=="custom":
                cbf = st.file_uploader("Öz fonunuzu yükləyin",
                    type=["jpg","jpeg","png","webp"],key="cbg",label_visibility="visible")
                if cbf: custom_bg = Image.open(cbf).convert("RGBA")
            else:
                try:
                    bg_prev = fetch_bg(BACKGROUNDS[bg_choice])
                    st.image(bg_prev.convert("RGB").resize((220,124),Image.LANCZOS),use_container_width=True)
                except: pass
            st.markdown('</div>', unsafe_allow_html=True)

        with col_prev:
            edited = apply_effects(orig_pil.crop((cl,ct,cr,cb)), brightness, contrast)
            if apply_bg:
                try:
                    bg_img = custom_bg if BACKGROUNDS[bg_choice]=="custom" else fetch_bg(BACKGROUNDS[bg_choice])
                    if bg_img:
                        with st.spinner("🎭 Arxa fon tətbiq edilir..."):
                            final_img = composite_bg(edited, bg_img)
                    else: final_img = edited
                except Exception as e:
                    st.error(f"Fon xətası: {e}"); final_img = edited
            else:
                final_img = edited
            st.markdown('<p style="text-align:center;font-size:.68rem;color:#555;'
                        'letter-spacing:.1em;text-transform:uppercase;margin-bottom:.3rem">'
                        'Önizləmə</p>', unsafe_allow_html=True)
            st.image(final_img, use_container_width=True)
            st.caption(f"📐 {final_img.width}×{final_img.height} px")

    btn1 = st.button("✨  AI ilə 4× Keyfiyyəti Artır",
                     disabled=not (uploaded and api_ok and final_img is not None), key="btn1")

    if btn1 and final_img:
        send_bytes    = pil_to_bytes(final_img)
        img_hash_full = hashlib.md5(send_bytes).hexdigest()
        prog = st.progress(0); msg_box = st.empty(); stop = [False]
        def spin():
            i=0
            while not stop[0]:
                msg_box.markdown(f'<div class="spin-msg">{MSGS[i%len(MSGS)]}</div>',unsafe_allow_html=True)
                time.sleep(2); i+=1
        threading.Thread(target=spin,daemon=True).start()
        prog.progress(20,"Colab-a göndərilir...")
        rb, rtype, meta, err = enhance_cached(send_bytes, "image.png", API_URL)
        stop[0]=True; msg_box.empty(); prog.progress(100,"Hazır! 🎉")
        if err:
            st.error(f"❌ {err}")
        else:
            st.balloons()
            if st.session_state.get(f"c_{img_hash_full}"):
                st.markdown('<div style="background:#0a1520;border:1px solid #1a4a7a;border-radius:8px;'
                            'padding:.35rem .9rem;font-size:.7rem;color:#5bb3ff;font-weight:600;'
                            'display:inline-block;margin-bottom:.4rem">⚡ Cache</div>',unsafe_allow_html=True)
            st.session_state[f"c_{img_hash_full}"] = True
            st.success("🎉 Tamamlandı!")
            result_pil = Image.open(io.BytesIO(rb))
            st.markdown('<div class="card"><div style="display:flex;align-items:center;'
                        'justify-content:space-between;margin-bottom:1rem">'
                        '<span style="font-family:\'Playfair Display\',serif;font-size:.95rem;color:#eee">Nəticə</span>'
                        '<span class="b-4x">4× Enhanced</span></div>', unsafe_allow_html=True)
            c1,c2 = st.columns(2)
            with c1:
                st.markdown('<p style="text-align:center"><span class="badge b-orig">REDAKTƏLİ</span></p>',unsafe_allow_html=True)
                st.image(final_img, use_container_width=True)
                st.caption(f"📐 {final_img.width}×{final_img.height} px")
            with c2:
                st.markdown('<p style="text-align:center"><span class="badge b-enh">4× AI</span></p>',unsafe_allow_html=True)
                st.image(result_pil, use_container_width=True)
                st.caption(f"📐 {result_pil.width}×{result_pil.height} px")
            d1,d2 = st.columns(2)
            with d1:
                st.download_button("⬇  Artırılmışı Endir",rb,
                    f"enhanced_{uploaded.name.rsplit('.',1)[0]}.png","image/png",use_container_width=True)
            with d2:
                st.download_button("⬇  Redaktəlini Endir",send_bytes,
                    f"edited_{uploaded.name.rsplit('.',1)[0]}.png","image/png",use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  TAB 2 — INPAINTING (Obyekt Silmə)
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="inpaint-tip">🖌️ Şəkil yükləyin → Silmək istədiyiniz obyektin üzərini <b style="color:#e07020">narıncı fırça</b> ilə rəngləyin → <b>"Obyekti Yox Et"</b> düyməsini basın.</div>', unsafe_allow_html=True)

    inp_file = st.file_uploader("📸  Şəkil seçin (Inpainting üçün)",
        type=["jpg","jpeg","png","webp"], label_visibility="visible", key="inp_up")

    if inp_file:
        inp_pil = Image.open(inp_file).convert("RGB")
        iw, ih  = inp_pil.size
        # Canvas ölçüsü — max 700px en
        scale   = min(700 / iw, 500 / ih, 1.0)
        cw, ch  = int(iw * scale), int(ih * scale)

        try:
            from streamlit_drawable_canvas import st_canvas

            st.markdown(f'<div class="brush-info">🖌️ Fırça aktiv — narıncı ilə rəngləyin | Canvas: {cw}×{ch} px</div>',
                        unsafe_allow_html=True)

            col_c, col_ctrl = st.columns([4, 1])
            with col_ctrl:
                stroke_w = st.slider("Fırça ölçüsü", 5, 60, 20, key="sw")
                st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)
                st.markdown('<div style="background:#e07020;width:100%;height:6px;border-radius:3px"></div>',
                            unsafe_allow_html=True)
                st.caption("Fırça rəngi: narıncı")

            with col_c:
                st.markdown('<div class="canvas-wrap">', unsafe_allow_html=True)
                canvas_result = st_canvas(
                    fill_color   = "rgba(224, 112, 32, 0.85)",
                    stroke_width = stroke_w,
                    stroke_color = "#e07020",
                    background_image = inp_pil.resize((cw, ch), Image.LANCZOS),
                    update_streamlit = True,
                    width  = cw,
                    height = ch,
                    drawing_mode = "freedraw",
                    key = "canvas",
                )
                st.markdown('</div>', unsafe_allow_html=True)

            btn_inp = st.button("🧹  Obyekti Yox Et", disabled=not api_ok, key="btn_inp")

            if btn_inp and canvas_result is not None and canvas_result.image_data is not None:
                mask_arr  = canvas_result.image_data
                mask_rgba = Image.fromarray(mask_arr.astype(np.uint8), "RGBA")

                # Maskadan yalnız rənglənmiş hissəni götür
                r,g,b,a = mask_rgba.split()
                mask_bin = a.point(lambda x: 255 if x > 10 else 0).resize((iw,ih), Image.NEAREST)
                mask_rgb = Image.merge("RGB", [mask_bin, mask_bin, mask_bin])

                orig_bytes = pil_to_bytes(inp_pil)
                mask_bytes = pil_to_bytes(mask_rgb)

                prog2 = st.progress(0,"Backend-ə göndərilir...")
                try:
                    resp = requests.post(
                        f"{API_URL}/inpaint",
                        files={
                            "image": ("image.png", orig_bytes, "image/png"),
                            "mask":  ("mask.png",  mask_bytes, "image/png"),
                        },
                        timeout=120,
                        headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"}
                    )
                    prog2.progress(90,"Emal edilir...")
                    data = resp.json()
                    if data.get("success"):
                        prog2.progress(100,"Hazır! 🎉")
                        st.success("🎉 Obyekt silindi!")
                        result_inp = Image.open(io.BytesIO(base64.b64decode(data["image"])))
                        c1,c2 = st.columns(2)
                        with c1:
                            st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',unsafe_allow_html=True)
                            st.image(inp_pil, use_container_width=True)
                        with c2:
                            st.markdown('<p style="text-align:center"><span class="badge b-enh">OBYEKTSİZ</span></p>',unsafe_allow_html=True)
                            st.image(result_inp, use_container_width=True)
                        st.download_button("⬇  Nəticəni Endir",
                            base64.b64decode(data["image"]),
                            f"inpainted_{inp_file.name.rsplit('.',1)[0]}.png",
                            "image/png", use_container_width=True)
                    else:
                        prog2.progress(100,"Xəta!")
                        st.error(f"❌ {data.get('error','Naməlum xəta')}")
                except Exception as e:
                    prog2.progress(100,"Xəta!")
                    st.error(f"❌ {str(e)}")

        except ImportError:
            st.markdown("""<div class="card" style="text-align:center;padding:2rem">
            <div style="font-size:2rem;margin-bottom:.8rem">📦</div>
            <div style="color:#e07020;font-weight:700;font-size:.9rem;margin-bottom:.5rem">
            streamlit-drawable-canvas quraşdırılmayıb</div>
            <div style="color:#666;font-size:.8rem">requirements.txt faylına əlavə edin:</div>
            <code style="background:#0d0f0e;color:#4dff88;padding:.3rem .8rem;
            border-radius:6px;font-size:.78rem;display:inline-block;margin-top:.5rem">
            streamlit-drawable-canvas</code></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  TAB 3 — VİDEO
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="video-warn">⚠️ Video emalı bir neçə dəqiqə çəkə bilər.<br>'
                'Emal zamanı pəncərəni bağlamayın!</div>', unsafe_allow_html=True)

    video_file = st.file_uploader("🎬  Video seçin",
        type=["mp4","mov","avi","mkv"], label_visibility="visible", key="vid_up")

    if video_file:
        st.video(video_file)
        st.markdown(f'<div style="font-size:.76rem;color:#666;padding:.3rem 0">'
                    f'🎬 <span style="color:#bbb">{video_file.name}</span> &nbsp;'
                    f'📦 <span style="color:#bbb">{video_file.size/1024/1024:.1f} MB</span></div>',
                    unsafe_allow_html=True)

    btn3 = st.button("🎬  Video 4× Keyfiyyətini Artır",
                     disabled=not (video_file and api_ok), key="btn3")

    if btn3 and video_file:
        vid_bytes = video_file.read()
        st.markdown('<div class="video-warn">🔄 Video emal edilir — lütfən pəncərəni bağlamayın!</div>',
                    unsafe_allow_html=True)
        prog3 = st.progress(0); msg3 = st.empty(); stop3 = [False]
        def spin3():
            i=0; mv=["🎬 Kadrlar ayrılır...","⚡ GPU hər kadrı emal edir...",
                      "🔄 Video yenidən yığılır...","✨ Möcüzə baş verir..."]
            while not stop3[0]:
                msg3.markdown(f'<div class="spin-msg">{mv[i%len(mv)]}</div>',unsafe_allow_html=True)
                time.sleep(3); i+=1
        threading.Thread(target=spin3,daemon=True).start()
        prog3.progress(10,"Video göndərilir...")
        rb3, meta3, err3 = enhance_video_cached(vid_bytes, video_file.name, API_URL)
        stop3[0]=True; msg3.empty()
        if err3:
            prog3.progress(100,"Xəta!")
            st.error(f"❌ {err3}")
        else:
            prog3.progress(100,"Video hazır! 🎉")
            st.balloons()
            st.success(f"🎉 Video hazır! {meta3.get('original','?')} → {meta3.get('enhanced','?')} | {meta3.get('frames','?')} kadr")
            st.download_button("⬇  4× Videonu Endir (MP4)", rb3,
                f"enhanced_{video_file.name.rsplit('.',1)[0]}.mp4",
                "video/mp4", use_container_width=True)
