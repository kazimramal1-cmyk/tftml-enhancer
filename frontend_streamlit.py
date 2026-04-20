# ================================================================
#  frontend_streamlit.py — TFTML ENHANCER AI v7
#  RAMAL KAZIMZADE | Şəkil + Inpainting + Video
# ================================================================

import streamlit as st
import requests, base64, hashlib, io, time, threading
from PIL import Image, ImageEnhance
import numpy as np

# ── Monkey Patch (AttributeError qarşısını alır) ─────
if not hasattr(st, 'image_to_url'):
    st.image_to_url = lambda x: x

API_URL  = "https://stacie-apertural-ardelia.ngrok-free.dev"
LOGO_B64 = ""   # logo_png.jpeg-dən base64 buraya

BACKGROUNDS = {
    "🦕 Dinozavrlar":  "https://images.unsplash.com/photo-1606206873764-fd15e242ff80?w=1280&q=80",
    "🏛️ Big Ben":      "https://images.unsplash.com/photo-1529655683826-aba9b3e77383?w=1280&q=80",
    "🌌 Kainat":       "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1280&q=80",
    "🌊 Okean":        "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=1280&q=80",
    "🗼 Paris":        "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1280&q=80",
    "🏔️ Dağlar":       "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1280&q=80",
    "🌸 Çiçəklər":     "https://images.unsplash.com/photo-1490750967868-88df5691cc9e?w=1280&q=80",
    "🌆 Gecə şəhər":   "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1280&q=80",
    "🏖️ Çimərlik":     "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280&q=80",
    "🎨 Öz fonum":     "custom",
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
.rk-brand{position:fixed;top:16px;left:20px;z-index:999;
  font-family:'DM Sans',sans-serif;font-size:.72rem;font-weight:700;
  letter-spacing:.2em;text-transform:uppercase;color:#e07020;
  text-decoration:underline;text-underline-offset:4px;
  text-decoration-color:rgba(224,112,32,.4);cursor:pointer;transition:all .2s}
.rk-brand:hover{color:#f59030;letter-spacing:.25em}
.logo-wrap{display:flex;justify-content:center;margin:1.5rem 0 .6rem}
.logo-img{width:110px;height:110px;border-radius:50%;object-fit:cover;
  animation:glowPulse 3s ease-in-out infinite}
@keyframes glowPulse{
  0%,100%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #1a6b2f,0 0 25px rgba(26,107,47,.55)}
  50%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #e07020,0 0 30px rgba(224,112,32,.6)}}
.main-title{font-family:'Playfair Display',serif;font-size:clamp(1.2rem,3vw,1.8rem);
  font-weight:700;text-align:center;color:#f0f0f0;letter-spacing:.05em;margin:.2rem 0 .1rem}
.main-title span{color:#e07020}
.sname{text-align:center;font-size:.82rem;color:#888;line-height:1.6;margin:.1rem 0}
.sname b{color:#bbb}
.ssub{text-align:center;font-size:.62rem;color:#444;letter-spacing:.15em;
  text-transform:uppercase;margin-bottom:1.4rem}
.status-ok{background:linear-gradient(135deg,#0a1f10,#0d2b15);border:1px solid #1a6b2f;
  border-radius:12px;padding:.55rem 1.2rem;font-size:.78rem;color:#4dff88;font-weight:600;margin-bottom:1rem}
.status-err{background:linear-gradient(135deg,#1f0a0a,#2b0d0d);border:1px solid #6b1a1a;
  border-radius:12px;padding:.55rem 1.2rem;font-size:.78rem;color:#ff6b6b;font-weight:600;margin-bottom:1rem}
[data-testid="stTabs"] [data-testid="stTab"]{
  background:transparent!important;border:none!important;
  color:#666!important;font-weight:600!important;font-size:.85rem!important;
  padding:.6rem 1.2rem!important;border-radius:10px 10px 0 0!important;transition:all .2s!important}
[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"]{
  background:linear-gradient(135deg,#1a6b2f,#0d3d1a)!important;
  color:#4dff88!important;border-bottom:2px solid #2d9e4a!important}
[data-testid="stTabContent"]{border:1.5px solid #1e251e!important;
  border-radius:0 16px 16px 16px!important;
  background:linear-gradient(145deg,#111311,#0f110f)!important;padding:1.5rem!important}
.stButton>button{font-family:'DM Sans',sans-serif!important;font-weight:700!important;
  font-size:.95rem!important;background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:12px!important;
  padding:.85rem 2rem!important;width:100%!important;
  box-shadow:0 4px 20px rgba(26,107,47,.4)!important;transition:transform .2s!important}
.stButton>button:hover{transform:scale(1.03) translateY(-2px)!important}
.stButton>button:disabled{opacity:.35!important}
.stProgress>div>div{background:linear-gradient(90deg,#1a6b2f,#e07020)!important}
[data-testid="stImage"] img{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}
.badge{display:inline-block;font-size:.58rem;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;padding:.2rem .55rem;border-radius:4px;margin-bottom:.4rem}
.b-orig{background:rgba(80,80,80,.3);color:#aaa;border:1px solid #333}
.b-enh{background:rgba(26,107,47,.4);color:#4dff88;border:1px solid #1a6b2f}
.b-4x{background:linear-gradient(135deg,#e07020,#f59030);color:#fff;font-size:.6rem;
  font-weight:700;padding:.22rem .65rem;border-radius:18px}
.stDownloadButton>button{font-family:'DM Sans',sans-serif!important;font-weight:600!important;
  font-size:.82rem!important;border-radius:10px!important;padding:.6rem 1.2rem!important;
  width:100%!important;background:#111!important;border:1.5px solid #1e251e!important;
  color:#aaa!important}
.stDownloadButton>button:hover{border-color:#2d9e4a!important;color:#4dff88!important}
.inpaint-tip{background:linear-gradient(135deg,#1a1200,#2b1e00);border:1px solid #6b4e00;
  border-radius:12px;padding:.8rem 1.2rem;font-size:.78rem;color:#ffcc44;
  line-height:1.7;margin:.6rem 0}
.video-warn{background:linear-gradient(135deg,#1a1200,#2b1e00);border:1px solid #6b4e00;
  border-radius:14px;padding:1rem 1.4rem;font-size:.82rem;color:#ffcc44;font-weight:600;
  margin:1rem 0;line-height:1.7;text-align:center}
[data-testid="stSlider"]>div>div>div{background:#1a6b2f!important}
video{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}
</style>
<div class="rk-brand">RAMAL KAZIMZADE</div>
""", unsafe_allow_html=True)

# ── Köməkçi funksiyalar ──────────────────────────────
def check_api(url):
    try:
        r = requests.get(f"{url}/health", timeout=6,
                         headers={"bypass-tunnel-reminder": "yes",
                                  "ngrok-skip-browser-warning": "true"})
        return r.status_code == 200
    except:
        return False

def pil_to_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()

def apply_effects(img, brightness, contrast):
    return ImageEnhance.Contrast(
        ImageEnhance.Brightness(img).enhance(brightness)).enhance(contrast)

@st.cache_data(show_spinner=False, max_entries=20)
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
        st.warning("⚠️ rembg quraşdırılmayıb — arxa fon dəyişdirilmədi")
        return fg

MSGS = ["🚀 AI mühərriki işə düşür...", "🧪 Piksellər bərpa olunur...",
        "✨ Möcüzə baş verir...", "🎨 Rənglər canlanır...", "⚡ GPU tam gücündə..."]

# ── Header ───────────────────────────────────────────
if LOGO_B64:
    st.markdown(f'<div class="logo-wrap"><img class="logo-img" src="data:image/jpeg;base64,{LOGO_B64}"></div>',
                unsafe_allow_html=True)
else:
    # Logo tapılmasa warning ver, dayanma
    st.markdown('<div class="logo-wrap"><div style="width:110px;height:110px;border-radius:50%;'
                'background:#1a6b2f;display:flex;align-items:center;justify-content:center;'
                'font-size:3rem;margin:auto">🎓</div></div>', unsafe_allow_html=True)

st.markdown("""
<div class="main-title">TFTML <span>ENHANCER</span> AI</div>
<div class="sname">K. Ağayev adına <b>Biləsuvar Şəhər</b><br>
Texniki Fənlər Təmayüllü İnternat Tipli Məktəb-Lisey</div>
<div class="ssub">AI Şəkil və Video Keyfiyyət Platforması · Real-ESRGAN 4×</div>
""", unsafe_allow_html=True)

api_ok = check_api(API_URL)
if api_ok:
    st.markdown('<div class="status-ok">✅ Colab Backend — Online · GPU/CPU Aktiv</div>',
                unsafe_allow_html=True)
else:
    st.markdown('<div class="status-err">⚠️ Colab Backend offline — Colab-ı işə salın</div>',
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  TABLƏR
# ══════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["🖼️  Şəkil Artır", "🧹  Obyekt Sil (Inpainting)", "🎬  Video Artır"])

# ──────────────────────────────────────────────────────
#  TAB 1 — ŞƏKİL
# ──────────────────────────────────────────────────────
with tab1:
    uploaded = st.file_uploader("📸  Şəkil seçin",
                                 type=["jpg","jpeg","png","webp","bmp"],
                                 key="img_up")
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

            with st.expander("🖼️ Arxa Fon", expanded=False):
                bg_choice = st.selectbox("Fon", list(BACKGROUNDS.keys()), key="bgc")
                apply_bg  = st.checkbox("✅ Arxa fonu dəyişdir", key="abg")
                custom_bg = None
                if BACKGROUNDS[bg_choice] == "custom":
                    cbf = st.file_uploader("Öz fonunuzu yükləyin",
                                           type=["jpg","jpeg","png","webp"],
                                           key="cbg")
                    if cbf:
                        custom_bg = Image.open(cbf).convert("RGBA")
                else:
                    try:
                        bg_prev = fetch_bg(BACKGROUNDS[bg_choice])
                        st.image(bg_prev.convert("RGB").resize((220,124), Image.LANCZOS),
                                 use_container_width=True)
                    except:
                        pass

        with col_prev:
            edited = apply_effects(orig_pil.crop((cl, ct, cr, cb)), brightness, contrast)
            if apply_bg:
                try:
                    bg_img = custom_bg if BACKGROUNDS[bg_choice]=="custom" else fetch_bg(BACKGROUNDS[bg_choice])
                    if bg_img:
                        with st.spinner("🎭 Arxa fon tətbiq edilir..."):
                            final_img = composite_bg(edited, bg_img)
                    else:
                        final_img = edited
                except Exception as e:
                    st.warning(f"Fon xətası: {e}")
                    final_img = edited
            else:
                final_img = edited

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
        img_hash   = hashlib.md5(send_bytes).hexdigest()
        prog = st.progress(0); msg_box = st.empty(); stop = [False]

        def spin():
            i = 0
            while not stop[0]:
                msg_box.markdown(f'<div style="text-align:center;font-size:.95rem;'
                                 f'font-weight:600;color:#e07020;padding:.7rem">'
                                 f'{MSGS[i % len(MSGS)]}</div>', unsafe_allow_html=True)
                time.sleep(2); i += 1

        threading.Thread(target=spin, daemon=True).start()
        prog.progress(20, "Colab-a göndərilir...")

        try:
            resp = requests.post(
                f"{API_URL}/enhance",
                files={"image": ("image.png", send_bytes, "image/png")},
                timeout=300,  # ağır şəkillər üçün
                headers={"bypass-tunnel-reminder": "yes",
                         "ngrok-skip-browser-warning": "true"})
            rb   = base64.b64decode(resp.json()["image"])
            err  = None if resp.json().get("success") else resp.json().get("error")
        except Exception as e:
            rb, err = None, str(e)

        stop[0] = True; msg_box.empty(); prog.progress(100, "Hazır! 🎉")

        if err or rb is None:
            st.error(f"❌ {err}")
        else:
            st.balloons()
            st.success("🎉 Tamamlandı!")
            result_pil = Image.open(io.BytesIO(rb))
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
                st.download_button("⬇  Artırılmışı Endir", rb,
                    f"enhanced_{uploaded.name.rsplit('.',1)[0]}.png", "image/png",
                    use_container_width=True)
            with d2:
                st.download_button("⬇  Redaktəlini Endir", send_bytes,
                    f"edited_{uploaded.name.rsplit('.',1)[0]}.png", "image/png",
                    use_container_width=True)

# ──────────────────────────────────────────────────────
#  TAB 2 — INPAINTING
# ──────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="inpaint-tip">🖌️ Şəkil yükləyin → Silmək istədiyiniz obyektin '
                'üzərini <b style="color:#e07020">narıncı fırça</b> ilə rəngləyin → '
                '<b>"Obyekti Yox Et"</b> düyməsini basın.</div>', unsafe_allow_html=True)

    inp_file = st.file_uploader("📸  Şəkil seçin (Inpainting üçün)",
                                 type=["jpg","jpeg","png","webp"], key="inp_up")

    if inp_file:
        inp_pil = Image.open(inp_file).convert("RGB")
        iw, ih  = inp_pil.size
        scale   = min(700/iw, 500/ih, 1.0)
        cw, ch  = int(iw*scale), int(ih*scale)

        try:
            from streamlit_drawable_canvas import st_canvas

            col_c, col_ctrl = st.columns([4, 1])
            with col_ctrl:
                stroke_w = st.slider("Fırça ölçüsü", 5, 60, 20, key="sw")

            with col_c:
                canvas_result = st_canvas(
                    fill_color   = "rgba(224, 112, 32, 0.85)",
                    stroke_width = stroke_w,
                    stroke_color = "#e07020",
                    background_image = inp_pil.resize((cw, ch), Image.LANCZOS),
                    update_streamlit = True,
                    width=cw, height=ch,
                    drawing_mode="freedraw",
                    key="canvas")

            btn_inp = st.button("🧹  Obyekti Yox Et",
                                disabled=not api_ok, key="btn_inp")

            if btn_inp and canvas_result is not None and canvas_result.image_data is not None:
                mask_arr  = canvas_result.image_data
                mask_rgba = Image.fromarray(mask_arr.astype(np.uint8), "RGBA")
                r, g, b, a = mask_rgba.split()
                mask_bin = a.point(lambda x: 255 if x > 10 else 0).resize(
                    (iw, ih), Image.NEAREST)
                mask_rgb = Image.merge("RGB", [mask_bin]*3)

                orig_bytes = pil_to_bytes(inp_pil)
                mask_bytes = pil_to_bytes(mask_rgb)

                prog2 = st.progress(0, "Backend-ə göndərilir...")
                try:
                    resp = requests.post(
                        f"{API_URL}/sam-inpaint",
                        files={"image": ("image.png", orig_bytes, "image/png"),
                               "mask":  ("mask.png",  mask_bytes, "image/png")},
                        timeout=300,
                        headers={"bypass-tunnel-reminder": "yes",
                                 "ngrok-skip-browser-warning": "true"})
                    prog2.progress(90, "Emal edilir...")
                    data = resp.json()
                    if data.get("success"):
                        prog2.progress(100, "Hazır! 🎉")
                        st.success("🎉 Obyekt silindi!")
                        result_inp = Image.open(io.BytesIO(base64.b64decode(data["image"])))
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown('<p style="text-align:center">'
                                        '<span class="badge b-orig">ORİGİNAL</span></p>',
                                        unsafe_allow_html=True)
                            st.image(inp_pil, use_container_width=True)
                        with c2:
                            st.markdown('<p style="text-align:center">'
                                        '<span class="badge b-enh">OBYEKTSİZ</span></p>',
                                        unsafe_allow_html=True)
                            st.image(result_inp, use_container_width=True)
                        st.download_button("⬇  Nəticəni Endir",
                            base64.b64decode(data["image"]),
                            f"inpainted_{inp_file.name.rsplit('.',1)[0]}.png",
                            "image/png", use_container_width=True)
                    else:
                        prog2.progress(100, "Xəta!")
                        st.error(f"❌ {data.get('error','Naməlum xəta')}")
                except Exception as e:
                    prog2.progress(100, "Xəta!")
                    st.error(f"❌ {str(e)}")

        except ImportError:
            st.info("📦 streamlit-drawable-canvas quraşdırılmayıb.\n\n"
                    "requirements.txt-ə əlavə edin: `streamlit-drawable-canvas`")

# ──────────────────────────────────────────────────────
#  TAB 3 — VİDEO
# ──────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="video-warn">⚠️ Video emalı bir neçə dəqiqə çəkə bilər.<br>'
                'Emal zamanı pəncərəni bağlamayın!</div>', unsafe_allow_html=True)

    video_file = st.file_uploader("🎬  Video seçin",
                                   type=["mp4","mov","avi","mkv"], key="vid_up")

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
        prog3 = st.progress(0); msg3 = st.empty(); stop3 = [False]
        mv = ["🎬 Kadrlar ayrılır...","⚡ GPU hər kadrı emal edir...",
              "🔄 Video yenidən yığılır...","✨ Möcüzə baş verir..."]

        def spin3():
            i = 0
            while not stop3[0]:
                msg3.markdown(f'<div style="text-align:center;font-size:.95rem;'
                              f'font-weight:600;color:#e07020;padding:.7rem">'
                              f'{mv[i%len(mv)]}</div>', unsafe_allow_html=True)
                time.sleep(3); i += 1

        threading.Thread(target=spin3, daemon=True).start()
        prog3.progress(10, "Video göndərilir...")

        try:
            resp3 = requests.post(
                f"{API_URL}/enhance-video",
                files={"video": (video_file.name, vid_bytes,
                                 f"video/{video_file.name.rsplit('.',1)[-1]}")},
                timeout=600,
                headers={"bypass-tunnel-reminder": "yes",
                         "ngrok-skip-browser-warning": "true"})
            data3 = resp3.json()
            rb3   = base64.b64decode(data3["image"]) if data3.get("success") else None
            err3  = None if data3.get("success") else data3.get("error")
        except Exception as e:
            rb3, err3 = None, str(e)

        stop3[0] = True; msg3.empty()

        if err3 or rb3 is None:
            prog3.progress(100, "Xəta!")
            st.error(f"❌ {err3}")
        else:
            prog3.progress(100, "Video hazır! 🎉")
            st.balloons()
            st.success(f"🎉 Video hazır! "
                       f"{data3.get('original','?')} → {data3.get('enhanced','?')} | "
                       f"{data3.get('frames','?')} kadr")
            st.download_button("⬇  4× Videonu Endir (MP4)", rb3,
                f"enhanced_{video_file.name.rsplit('.',1)[0]}.mp4",
                "video/mp4", use_container_width=True)
