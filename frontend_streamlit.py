# ================================================================
#  frontend_streamlit.py — TFTML ENHANCER AI
#  Şəkil + Video + Crop + Effektlər + Fon Dəyişdirmə
# ================================================================

import streamlit as st
import requests, base64, hashlib, io, time, threading
from PIL import Image, ImageEnhance

API_URL  = "https://stacie-apertural-ardelia.ngrok-free.dev"
LOGO_B64 = "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"

BACKGROUNDS = {
    "🦕 Dinozavrlar":    "https://images.unsplash.com/photo-1606206873764-fd15e242ff80?w=1280&q=80",
    "🏛️ Big Ben":        "https://images.unsplash.com/photo-1529655683826-aba9b3e77383?w=1280&q=80",
    "🌌 Kainat":         "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1280&q=80",
    "🌊 Okean":          "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=1280&q=80",
    "🗼 Paris":          "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1280&q=80",
    "🏔️ Dağlar":         "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1280&q=80",
    "🌸 Çiçəklər":       "https://images.unsplash.com/photo-1490750967868-88df5691cc9e?w=1280&q=80",
    "🌆 Gecə şəhər":     "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1280&q=80",
    "🏖️ Çimərlik":       "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280&q=80",
    "🌋 Vulkan":         "https://images.unsplash.com/photo-1570571717080-2481e0a7f014?w=1280&q=80",
    "❄️ Şimal işıqları": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=1280&q=80",
    "🎨 Öz fonum":       "custom",
}

st.set_page_config(page_title="TFTML ENHANCER AI", page_icon="🎓",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');
#MainMenu,footer,header,.stDeployButton,[data-testid="stToolbar"]{display:none!important}
.stApp{background:#0d0f0e!important;font-family:'DM Sans',sans-serif!important}
.block-container{max-width:920px!important;padding:2rem 1.5rem!important;margin:0 auto!important}
.stApp::before{content:'';position:fixed;inset:0;z-index:0;
  background:radial-gradient(ellipse at 15% 40%,rgba(26,107,47,.12) 0%,transparent 55%),
             radial-gradient(ellipse at 85% 20%,rgba(224,112,32,.10) 0%,transparent 55%);
  pointer-events:none}
.logo-wrap{display:flex;justify-content:center;margin:2rem 0 .8rem}
.logo-img{width:120px;height:120px;border-radius:50%;object-fit:cover;animation:glowPulse 3s ease-in-out infinite}
@keyframes glowPulse{
  0%,100%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #1a6b2f,0 0 0 7px #0d0f0e,0 0 25px rgba(26,107,47,.55),0 0 55px rgba(224,112,32,.2)}
  50%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #e07020,0 0 0 7px #0d0f0e,0 0 30px rgba(224,112,32,.6),0 0 65px rgba(26,107,47,.25)}}
.main-title{font-family:'Playfair Display',serif;font-size:clamp(1.3rem,3.5vw,2rem);
  font-weight:700;text-align:center;color:#f0f0f0;letter-spacing:.05em;margin:.2rem 0 .1rem}
.main-title span{color:#e07020}
.sname{text-align:center;font-size:.88rem;color:#888;line-height:1.65;margin:.1rem 0}
.sname b{color:#bbb}
.ssub{text-align:center;font-size:.63rem;color:#444;letter-spacing:.16em;text-transform:uppercase;margin-bottom:1.8rem}
.status-ok{background:linear-gradient(135deg,#0a1f10,#0d2b15);border:1px solid #1a6b2f;
  border-radius:12px;padding:.6rem 1.2rem;font-size:.8rem;color:#4dff88;font-weight:600;margin-bottom:1.2rem}
.status-err{background:linear-gradient(135deg,#1f0a0a,#2b0d0d);border:1px solid #6b1a1a;
  border-radius:12px;padding:.6rem 1.2rem;font-size:.8rem;color:#ff6b6b;font-weight:600;margin-bottom:1.2rem}
.card{background:linear-gradient(145deg,#131613,#111311);border-radius:20px;
  border:1.5px solid #1e251e;padding:1.8rem;margin-bottom:1.4rem;box-shadow:0 4px 40px rgba(0,0,0,.5)}
[data-testid="stFileUploader"]{border:2px dashed transparent!important;border-radius:18px!important;
  background:linear-gradient(#131613,#131613) padding-box,
             linear-gradient(135deg,#1a6b2f,#e07020,#1a6b2f) border-box!important;
  padding:1.4rem!important;transition:all .3s!important}
[data-testid="stFileUploader"]:hover{
  background:linear-gradient(#0f1a0f,#0f1a0f) padding-box,
             linear-gradient(135deg,#2d9e4a,#f59030,#2d9e4a) border-box!important;
  box-shadow:0 0 25px rgba(26,107,47,.2)!important}
[data-testid="stFileUploader"] *{color:#888!important}
[data-testid="stFileUploader"] svg{fill:#e07020!important}
[data-testid="stFileUploader"] button{background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:8px!important}
.stButton>button{font-family:'DM Sans',sans-serif!important;font-weight:700!important;
  font-size:1rem!important;background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:14px!important;
  padding:1rem 2rem!important;width:100%!important;
  box-shadow:0 4px 22px rgba(26,107,47,.4)!important;transition:transform .2s,box-shadow .2s!important}
.stButton>button:hover{transform:scale(1.04) translateY(-2px)!important;
  box-shadow:0 8px 36px rgba(45,158,74,.6)!important}
.stButton>button:disabled{opacity:.35!important}
[data-testid="stSlider"]>div>div>div{background:#1a6b2f!important}
[data-testid="stSlider"] label{color:#aaa!important;font-size:.8rem!important}
.fx-panel{background:#0d1510;border:1px solid #1a3320;border-radius:14px;padding:1.2rem 1.4rem;margin:.6rem 0}
.fx-title{font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#4dff88;margin-bottom:.8rem}
.video-warn{background:linear-gradient(135deg,#1a1200,#2b1e00);border:1px solid #6b4e00;
  border-radius:14px;padding:1rem 1.4rem;font-size:.85rem;color:#ffcc44;font-weight:600;
  margin:1rem 0;line-height:1.7;text-align:center}
.stProgress>div>div{background:linear-gradient(90deg,#1a6b2f,#e07020)!important;border-radius:3px!important}
[data-testid="stImage"] img{border-radius:14px!important;border:1.5px solid #1e251e!important;width:100%!important}
.spin-msg{text-align:center;font-size:1rem;font-weight:600;color:#e07020;padding:.8rem}
.badge{display:inline-block;font-size:.6rem;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;padding:.22rem .6rem;border-radius:5px;margin-bottom:.4rem}
.b-orig{background:rgba(80,80,80,.3);color:#aaa;border:1px solid #333}
.b-enh{background:rgba(26,107,47,.4);color:#4dff88;border:1px solid #1a6b2f}
.b-4x{background:linear-gradient(135deg,#e07020,#f59030);color:#fff;font-size:.62rem;
  font-weight:700;letter-spacing:.1em;padding:.24rem .7rem;border-radius:20px}
.stDownloadButton>button{font-family:'DM Sans',sans-serif!important;font-weight:600!important;
  font-size:.85rem!important;border-radius:11px!important;padding:.65rem 1.2rem!important;
  width:100%!important;background:#111!important;border:1.5px solid #1e251e!important;
  color:#aaa!important;transition:all .2s!important}
.stDownloadButton>button:hover{border-color:#2d9e4a!important;color:#4dff88!important}
[data-testid="stCaptionContainer"]{color:#555!important;font-size:.72rem!important}
[data-testid="stRadio"] label,[data-testid="stRadio"] p{color:#aaa!important}
video{border-radius:14px!important;border:1.5px solid #1e251e!important;width:100%!important}
</style>
""", unsafe_allow_html=True)

# ── Köməkçi funksiyalar ──────────────────────────────────────────
@st.cache_data(show_spinner=False, max_entries=100)
def enhance_cached(file_bytes: bytes, fname: str, api_url: str):
    try:
        resp = requests.post(
            f"{api_url}/enhance",
            files={"file": (fname, file_bytes, "application/octet-stream")},
            timeout=600,
            headers={"bypass-tunnel-reminder": "yes", "ngrok-skip-browser-warning": "true"}
        )
        data = resp.json()
        if data.get("success"):
            return base64.b64decode(data["image"]), data.get("type","image"), data, None
        return None, None, {}, data.get("error", "Naməlum xəta")
    except Exception as e:
        return None, None, {}, str(e)

def check_api(url):
    try:
        r = requests.get(f"{url}/health", timeout=6,
                         headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
        return r.status_code == 200
    except:
        return False

def pil_to_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()

def apply_effects(img, brightness, contrast):
    img = ImageEnhance.Brightness(img).enhance(brightness)
    return ImageEnhance.Contrast(img).enhance(contrast)

@st.cache_data(show_spinner=False)
def fetch_bg(url):
    r = requests.get(url, timeout=15)
    return Image.open(io.BytesIO(r.content)).convert("RGBA")

def composite_bg(fg: Image.Image, bg: Image.Image) -> Image.Image:
    try:
        from rembg import remove as rembg_remove
        no_bg = Image.open(io.BytesIO(rembg_remove(pil_to_bytes(fg)))).convert("RGBA")
    except ImportError:
        st.warning("⚠️  quraşdırılmayıb.  ilə qurun.")
        return fg
    bg_r = bg.resize(no_bg.size, Image.LANCZOS).convert("RGBA")
    return Image.alpha_composite(bg_r, no_bg).convert("RGB")

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
    st.markdown('<div class="status-err">⚠️ Colab Backend offline — Colab-ı işə salın və URL-i yeniləyin</div>', unsafe_allow_html=True)

mode = st.radio("", ["🖼️  Şəkil", "🎬  Video", "📦  Batch"],
                horizontal=True, label_visibility="collapsed")

# ══════════════════════════════════════════════════════════════════
#  ŞƏKİL REJİMİ
# ══════════════════════════════════════════════════════════════════
if "Şəkil" in mode:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded = st.file_uploader("📸  Şəkil seçin",
        type=["jpg","jpeg","png","webp","bmp"], label_visibility="visible")

    final_img = None

    if uploaded:
        orig_pil = Image.open(uploaded).convert("RGB")
        col_prev, col_fx = st.columns([3, 2])

        with col_fx:
            st.markdown('<div class="fx-panel">', unsafe_allow_html=True)
            st.markdown('<div class="fx-title">✂️ Kəsim (Crop)</div>', unsafe_allow_html=True)
            w, h = orig_pil.size
            c1, c2 = st.columns(2)
            with c1:
                cl = st.number_input("Sol",    0, w-10, 0, step=5, key="cl")
                ct = st.number_input("Yuxarı", 0, h-10, 0, step=5, key="ct")
            with c2:
                cr = st.number_input("Sağ",   10, w, w, step=5, key="cr")
                cb = st.number_input("Aşağı", 10, h, h, step=5, key="cb")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="fx-panel">', unsafe_allow_html=True)
            st.markdown('<div class="fx-title">🎨 Effektlər</div>', unsafe_allow_html=True)
            brightness = st.slider("☀️ Parlaqlıq", 0.5, 2.0, 1.0, 0.05, key="br")
            contrast   = st.slider("🌗 Kontrast",  0.5, 2.0, 1.0, 0.05, key="co")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="fx-panel">', unsafe_allow_html=True)
            st.markdown('<div class="fx-title">🖼️ Arxa Fon Dəyişdirmə</div>', unsafe_allow_html=True)
            bg_choice = st.selectbox("Fon seçin", list(BACKGROUNDS.keys()), key="bgc")
            apply_bg  = st.checkbox("✅ Arxa fonu dəyişdir", key="abg")
            custom_bg = None
            if BACKGROUNDS[bg_choice] == "custom":
                cbf = st.file_uploader("Öz fonunuzu yükləyin",
                    type=["jpg","jpeg","png","webp"], key="cbg",
                    label_visibility="visible")
                if cbf:
                    custom_bg = Image.open(cbf).convert("RGBA")
            else:
                try:
                    bg_prev = fetch_bg(BACKGROUNDS[bg_choice])
                    st.image(bg_prev.convert("RGB").resize((240,135),Image.LANCZOS),
                             use_container_width=True)
                except:
                    pass
            st.markdown('</div>', unsafe_allow_html=True)

        with col_prev:
            edited = apply_effects(orig_pil.crop((cl,ct,cr,cb)), brightness, contrast)
            if apply_bg:
                try:
                    bg_img = custom_bg if BACKGROUNDS[bg_choice]=="custom" else fetch_bg(BACKGROUNDS[bg_choice])
                    if bg_img:
                        with st.spinner("🎭 Arxa fon tətbiq edilir..."):
                            final_img = composite_bg(edited, bg_img)
                    else:
                        final_img = edited
                except Exception as e:
                    st.error(f"Fon xətası: {e}"); final_img = edited
            else:
                final_img = edited

            st.markdown('<p style="text-align:center;font-size:.7rem;color:#555;'
                        'letter-spacing:.1em;text-transform:uppercase;margin-bottom:.4rem">'
                        'Önizləmə</p>', unsafe_allow_html=True)
            st.image(final_img, use_container_width=True)
            st.caption(f"📐 {final_img.width}×{final_img.height} px")

        h_str = hashlib.md5(uploaded.read()).hexdigest()[:8]; uploaded.seek(0)
        st.markdown(f'<div style="font-size:.78rem;color:#666;padding:.3rem 0">'
                    f'📄 <span style="color:#bbb">{uploaded.name}</span> &nbsp;'
                    f'📦 <span style="color:#bbb">{uploaded.size/1024/1024:.2f} MB</span> &nbsp;'
                    f'🔑 <code style="background:#0d0f0e;color:#4dff88;padding:.1rem .35rem;'
                    f'border-radius:4px;border:1px solid #1a6b2f;font-size:.68rem">{h_str}</code>'
                    f'</div>', unsafe_allow_html=True)

    btn = st.button("✨  AI ilə 4× Keyfiyyəti Artır",
                    disabled=not (uploaded and api_ok and final_img is not None))
    st.markdown('</div>', unsafe_allow_html=True)

    if btn and final_img:
        send_bytes    = pil_to_bytes(final_img)
        img_hash_full = hashlib.md5(send_bytes).hexdigest()
        prog = st.progress(0); msg_box = st.empty(); stop = [False]

        def spin():
            i=0
            while not stop[0]:
                msg_box.markdown(f'<div class="spin-msg">{MSGS[i%len(MSGS)]}</div>',
                                 unsafe_allow_html=True)
                time.sleep(2); i+=1

        threading.Thread(target=spin, daemon=True).start()
        prog.progress(20, "Colab-a göndərilir...")
        result_bytes, rtype, meta, err = enhance_cached(send_bytes, "image.png", API_URL)
        stop[0]=True; msg_box.empty(); prog.progress(100, "Hazır! 🎉")

        if err:
            st.error(f"❌ Xəta: {err}")
        else:
            st.balloons()
            if st.session_state.get(f"c_{img_hash_full}"):
                st.markdown('<div style="background:#0a1520;border:1px solid #1a4a7a;border-radius:8px;'
                            'padding:.4rem .9rem;font-size:.72rem;color:#5bb3ff;font-weight:600;'
                            'display:inline-block;margin-bottom:.5rem">⚡ Cache — Colab-a sorğu getmədi</div>',
                            unsafe_allow_html=True)
            st.session_state[f"c_{img_hash_full}"] = True
            st.success("🎉 Emal tamamlandı!")
            result_pil = Image.open(io.BytesIO(result_bytes))

            st.markdown('<div class="card"><div style="display:flex;align-items:center;'
                        'justify-content:space-between;margin-bottom:1.2rem">'
                        '<span style="font-family:\'Playfair Display\',serif;font-size:1rem;color:#eee">Nəticə</span>'
                        '<span class="b-4x">4× Enhanced</span></div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<p style="text-align:center"><span class="badge b-orig">REDAKTƏLİ</span></p>',
                            unsafe_allow_html=True)
                st.image(final_img, use_container_width=True)
                st.caption(f"📐 {final_img.width}×{final_img.height} px")
            with c2:
                st.markdown('<p style="text-align:center"><span class="badge b-enh">4× AI</span></p>',
                            unsafe_allow_html=True)
                st.image(result_pil, use_container_width=True)
                st.caption(f"📐 {result_pil.width}×{result_pil.height} px")
            d1, d2 = st.columns(2)
            with d1:
                st.download_button("⬇  Artırılmışı Endir", result_bytes,
                    f"enhanced_{uploaded.name.rsplit('.',1)[0]}.png",
                    "image/png", use_container_width=True)
            with d2:
                st.download_button("⬇  Redaktəlini Endir", send_bytes,
                    f"edited_{uploaded.name.rsplit('.',1)[0]}.png",
                    "image/png", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  VİDEO REJİMİ
# ══════════════════════════════════════════════════════════════════
elif "Video" in mode:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="video-warn">⚠️ Video emalı uzun müddət çəkə bilər (GPU gücündən asılıdır).<br>'
                'Emal zamanı pəncərəni bağlamayın! Brauzer tabını açıq saxlayın.</div>',
                unsafe_allow_html=True)

    video_file = st.file_uploader("🎬  Video seçin",
        type=["mp4","mov","avi","mkv"], label_visibility="visible")

    if video_file:
        st.video(video_file)
        st.markdown(f'<div style="font-size:.78rem;color:#666;padding:.4rem 0">'
                    f'🎬 <span style="color:#bbb">{video_file.name}</span> &nbsp;'
                    f'📦 <span style="color:#bbb">{video_file.size/1024/1024:.1f} MB</span>'
                    f'</div>', unsafe_allow_html=True)

    btn_v = st.button("🎬  Video 4× Keyfiyyətini Artır",
                      disabled=not (video_file and api_ok))
    st.markdown('</div>', unsafe_allow_html=True)

    if btn_v and video_file:
        vid_bytes = video_file.read()
        vid_hash  = hashlib.md5(vid_bytes).hexdigest()

        st.markdown('<div class="video-warn">🔄 Video emal edilir — lütfən pəncərəni bağlamayın!<br>'
                    'Bu proses bir neçə dəqiqə çəkə bilər.</div>', unsafe_allow_html=True)

        prog    = st.progress(0); msg_box = st.empty(); stop = [False]

        def spin_v():
            i=0; msgs_v=["🎬 Kadrlar ayrılır...","⚡ GPU hər kadrı emal edir...",
                          "🔄 Video yenidən yığılır...","✨ Möcüzə baş verir..."]
            while not stop[0]:
                msg_box.markdown(f'<div class="spin-msg">{msgs_v[i%len(msgs_v)]}</div>',
                                 unsafe_allow_html=True)
                time.sleep(3); i+=1

        threading.Thread(target=spin_v, daemon=True).start()
        prog.progress(10, "Video backend-ə göndərilir...")

        result_bytes, rtype, meta, err = enhance_cached(vid_bytes, video_file.name, API_URL)
        stop[0]=True; msg_box.empty()

        if err:
            prog.progress(100, "Xəta!")
            st.error(f"❌ Xəta: {err}")
        else:
            prog.progress(100, "Video hazır! 🎉")
            st.balloons()
            st.success(f"🎉 Video uğurla emal edildi! "
                       f"{meta.get('original_size','?')} → {meta.get('enhanced_size','?')} | "
                       f"{meta.get('frames','?')} kadr")

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.download_button(
                "⬇  4× Videonu Endir (MP4)", result_bytes,
                f"enhanced_{video_file.name.rsplit('.',1)[0]}.mp4",
                "video/mp4", use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  BATCH REJİMİ
# ══════════════════════════════════════════════════════════════════
else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.82rem;color:#888;margin-bottom:.8rem">'
                '📦 Birdən çox şəkil seçin — hamısı ardıcıl emal ediləcək</div>',
                unsafe_allow_html=True)
    uploads = st.file_uploader("📸  Şəkilləri seçin (çoxlu)",
        type=["jpg","jpeg","png","webp","bmp"],
        accept_multiple_files=True, label_visibility="visible")
    if uploads:
        st.markdown(f'<div style="font-size:.8rem;color:#4dff88;margin:.5rem 0">'
                    f'✅ {len(uploads)} fayl seçildi</div>', unsafe_allow_html=True)
    btn_b = st.button(f"✨  {len(uploads) if uploads else 0} Şəkli Emal Et",
                      disabled=not (uploads and api_ok))
    st.markdown('</div>', unsafe_allow_html=True)

    if btn_b and uploads:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<span style="font-family:\'Playfair Display\',serif;font-size:1rem;color:#eee">'
                    'Batch Nəticələri</span>', unsafe_allow_html=True)
        tp = st.progress(0, f"0 / {len(uploads)}")
        for idx, up in enumerate(uploads):
            ib = up.read()
            with st.expander(f"🖼️  {up.name}  ({up.size/1024/1024:.2f} MB)", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.image(Image.open(io.BytesIO(ib)), use_container_width=True)
                    st.caption("Orijinal")
                with c2:
                    ph = st.empty()
                    ph.markdown('<div class="spin-msg">⚡ Emal edilir...</div>',
                                unsafe_allow_html=True)
                    rb, _, _, err = enhance_cached(ib, up.name, API_URL)
                    ph.empty()
                    if err:
                        st.error(f"❌ {err}")
                    else:
                        st.image(Image.open(io.BytesIO(rb)), use_container_width=True)
                        st.caption("4× AI")
                        st.download_button("⬇  Endir", rb,
                            f"enhanced_{up.name.rsplit('.',1)[0]}.png",
                            "image/png", key=f"dl_{idx}", use_container_width=True)
            tp.progress((idx+1)/len(uploads), f"{idx+1} / {len(uploads)} tamamlandı")
        st.balloons()
        st.success(f"🎉 {len(uploads)} şəkil uğurla emal edildi!")
        st.markdown('</div>', unsafe_allow_html=True)
