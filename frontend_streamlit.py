# ================================================================
#  frontend_streamlit.py — TFTML ENHANCER AI v4
#  RAMAL KAZIMZADE | Düzəldilmiş + rembg tab əlavə edildi
# ================================================================

import streamlit as st
import requests
import base64
import hashlib
import io
import json
import time
import threading
from PIL import Image, ImageEnhance
import numpy as np

# ▼▼▼  Colab-dan kopyaladığınız ngrok URL-i buraya yazın  ▼▼▼
API_URL = "https://YOUR_NGROK_URL_HERE"
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAB4AHgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL"

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

st.set_page_config(
    page_title="TFTML ENHANCER AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
.rk-brand{position:fixed;top:14px;left:18px;z-index:999;font-size:.7rem;font-weight:700;
  letter-spacing:.2em;text-transform:uppercase;color:#e07020;text-decoration:underline;
  text-underline-offset:4px;text-decoration-color:rgba(224,112,32,.4);transition:all .2s}
.rk-brand:hover{color:#f59030;text-shadow:0 0 12px rgba(224,112,32,.5)}
.logo-wrap{display:flex;flex-direction:column;align-items:center;gap:.8rem;margin:2rem 0 1.2rem}
.logo-circle{width:114px;height:114px;border-radius:50%;object-fit:cover;
  animation:glowPulse 3s ease-in-out infinite}
@keyframes glowPulse{
  0%,100%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #1a6b2f,0 0 0 7px #0d0f0e,
          0 0 28px rgba(26,107,47,.55),0 0 55px rgba(224,112,32,.2)}
  50%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #e07020,0 0 0 7px #0d0f0e,
      0 0 35px rgba(224,112,32,.65),0 0 70px rgba(26,107,47,.28)}}
.main-title{font-family:'Playfair Display',serif;font-size:clamp(1.3rem,3.5vw,2rem);
  font-weight:700;text-align:center;color:#f0f0f0;letter-spacing:.05em;margin:0}
.main-title span{color:#e07020}
.school-name{text-align:center;font-size:.82rem;color:#888;line-height:1.65}
.school-name b{color:#bbb}
.school-sub{text-align:center;font-size:.62rem;color:#444;letter-spacing:.15em;
  text-transform:uppercase;margin-bottom:.5rem}
.status-ok{background:linear-gradient(135deg,#0a1f10,#0d2b15);border:1px solid #1a6b2f;
  border-radius:12px;padding:.55rem 1.2rem;font-size:.78rem;color:#4dff88;
  font-weight:600;margin-bottom:1rem}
.status-err{background:linear-gradient(135deg,#1f0a0a,#2b0d0d);border:1px solid #6b1a1a;
  border-radius:12px;padding:.55rem 1.2rem;font-size:.78rem;color:#ff6b6b;
  font-weight:600;margin-bottom:1rem}
[data-testid="stTabs"] [data-testid="stTab"]{background:transparent!important;
  border:none!important;color:#666!important;font-weight:600!important;
  font-size:.85rem!important;padding:.6rem 1.2rem!important;
  border-radius:10px 10px 0 0!important;transition:all .2s!important}
[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"]{
  background:linear-gradient(135deg,#1a6b2f,#0d3d1a)!important;
  color:#4dff88!important;border-bottom:2px solid #2d9e4a!important}
[data-testid="stTabContent"]{border:1.5px solid #1e251e!important;
  border-radius:0 16px 16px 16px!important;
  background:linear-gradient(145deg,#111311,#0f110f)!important;padding:1.5rem!important}
.card{background:linear-gradient(145deg,#131613,#111311);border-radius:16px;
  border:1.5px solid #1e251e;padding:1.5rem;margin-bottom:1.2rem;
  box-shadow:0 4px 30px rgba(0,0,0,.4)}
[data-testid="stFileUploader"]{border:2px dashed transparent!important;
  border-radius:16px!important;
  background:linear-gradient(#131613,#131613) padding-box,
             linear-gradient(135deg,#1a6b2f,#e07020,#1a6b2f) border-box!important;
  padding:1.2rem!important;transition:all .3s!important}
[data-testid="stFileUploader"] *{color:#888!important}
[data-testid="stFileUploader"] svg{fill:#e07020!important}
[data-testid="stFileUploader"] button{
  background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:8px!important}
.stButton>button{font-family:'DM Sans',sans-serif!important;font-weight:700!important;
  font-size:.95rem!important;background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:12px!important;
  padding:.85rem 2rem!important;width:100%!important;
  box-shadow:0 4px 20px rgba(26,107,47,.4)!important;transition:transform .2s,box-shadow .2s!important}
.stButton>button:hover{transform:scale(1.03) translateY(-2px)!important;
  box-shadow:0 8px 30px rgba(45,158,74,.55)!important}
.stButton>button:disabled{opacity:.35!important}
[data-testid="stSlider"]>div>div>div{background:#1a6b2f!important}
[data-testid="stSlider"] label{color:#aaa!important;font-size:.78rem!important}
.fx-panel{background:#0d1510;border:1px solid #1a3320;border-radius:12px;
  padding:1rem 1.2rem;margin:.5rem 0}
.fx-title{font-size:.68rem;font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;color:#4dff88;margin-bottom:.7rem}
.sam-tip{background:linear-gradient(135deg,#0d1a2b,#0a1020);border:1px solid #1a3a6b;
  border-radius:12px;padding:.8rem 1.2rem;font-size:.78rem;color:#88ccff;
  line-height:1.8;margin:.6rem 0}
.video-warn{background:linear-gradient(135deg,#1a1200,#2b1e00);border:1px solid #6b4e00;
  border-radius:14px;padding:1rem 1.4rem;font-size:.82rem;color:#ffcc44;
  font-weight:600;margin:1rem 0;line-height:1.7;text-align:center}
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
video{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}
</style>
<div class="rk-brand">RAMAL KAZIMZADE</div>
""", unsafe_allow_html=True)

# ── Yardımçı funksiyalar ─────────────────────────────────────────
HDR = {"bypass-tunnel-reminder": "yes", "ngrok-skip-browser-warning": "true"}


def safe_post(url, timeout=300, **kwargs):
    try:
        resp = requests.post(url, timeout=timeout, headers=HDR, **kwargs)
        try:
            return resp.json(), None
        except Exception:
            return None, f"JSON parse xətası (HTTP {resp.status_code}): {resp.text[:300]}"
    except requests.exceptions.Timeout:
        return None, f"Timeout ({timeout}s) — backend cavab vermədi"
    except requests.exceptions.ConnectionError:
        return None, "Bağlantı xətası — Colab-ın işlədiyinə əmin olun"
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)}"


@st.cache_data(show_spinner=False, max_entries=80)
def enhance_cached(img_bytes, api_url):
    try:
        resp = requests.post(
            f"{api_url}/enhance",
            files={"image": ("img.png", img_bytes, "image/png")},
            timeout=300, headers=HDR
        )
        data = resp.json()
        if data.get("success"):
            return base64.b64decode(data["image"]), None
        return None, data.get("error", f"Xəta: {data}")
    except requests.exceptions.Timeout:
        return None, "Timeout — backend cavab vermədi"
    except requests.exceptions.ConnectionError:
        return None, "Bağlantı xətası"
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)}"


@st.cache_data(show_spinner=False, max_entries=10)
def enhance_video_cached(vid_bytes, fname, api_url):
    try:
        ext  = fname.rsplit(".", 1)[-1].lower() if "." in fname else "mp4"
        mime = {"mp4": "video/mp4", "mov": "video/quicktime", "avi": "video/x-msvideo"}.get(ext, "video/mp4")
        resp = requests.post(
            f"{api_url}/enhance-video",
            files={"video": (fname, vid_bytes, mime)},
            timeout=600, headers=HDR
        )
        data = resp.json()
        if data.get("success"):
            return base64.b64decode(data["image"]), data, None
        return None, {}, data.get("error", "Xəta")
    except Exception as e:
        return None, {}, f"{type(e).__name__}: {str(e)}"


def remove_bg_request(img_bytes: bytes, api_url: str):
    """
    /process_rembg endpointinə şəkil göndərir.
    Uğurlu: (bytes, None)
    Xəta:   (None, "rembg xətası: [detal]")
    """
    # Əvvəlcə health yoxla — rembg aktiv deyilsə vaxt itirmə
    try:
        h = requests.get(f"{api_url}/health", timeout=6, headers=HDR).json()
        if not h.get("rembg", True):
            detail = h.get("rembg_error") or ""
            return None, (
                "rembg xətası: Serverdə rembg quraşdırılmayıb.\n"
                "Həll: Colab-da `!pip install rembg onnxruntime` icra edin.\n"
                + (f"Texniki səbəb: {detail}" if detail else "")
            )
    except Exception:
        pass  # health əlçatmırsa sorğunu yenə də cəhd et

    try:
        resp = requests.post(
            f"{api_url}/process_rembg",
            files={"image": ("photo.png", img_bytes, "image/png")},
            timeout=120, headers=HDR
        )
    except requests.exceptions.Timeout:
        return None, "rembg xətası: Timeout (120s) — şəkil çox böyük ola bilər"
    except requests.exceptions.ConnectionError:
        return None, "rembg xətası: Bağlantı kəsildi — Colab-ı yoxlayın"
    except Exception as e:
        return None, f"rembg xətası: {type(e).__name__}: {e}"

    try:
        data = resp.json()
    except Exception:
        return None, f"rembg xətası: JSON parse alınmadı (HTTP {resp.status_code}): {resp.text[:200]}"

    if resp.status_code == 503:
        return None, f"rembg xətası: {data.get('error', 'Xidmət əlçatan deyil')}"
    if resp.status_code == 415:
        return None, f"rembg xətası: {data.get('error', 'Dəstəklənməyən fayl növü')}"
    if resp.status_code == 400:
        return None, f"rembg xətası: {data.get('error', 'Yanlış sorğu')}"
    if not data.get("success"):
        err    = data.get("error",  "Naməlum xəta")
        detail = data.get("detail", "")
        msg    = f"rembg xətası: {err}"
        if detail:
            msg += f"\n\nTexniki məlumat:\n{detail[:400]}"
        return None, msg

    try:
        return base64.b64decode(data["image"]), None
    except Exception as e:
        return None, f"rembg xətası: Base64 dekodlama — {e}"


def check_api(url):
    try:
        r = requests.get(f"{url}/health", timeout=6, headers=HDR)
        return r.status_code == 200
    except Exception:
        return False


def pil_to_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def apply_fx(img, br, co):
    return ImageEnhance.Contrast(ImageEnhance.Brightness(img).enhance(br)).enhance(co)


@st.cache_data(show_spinner=False)
def fetch_bg(url):
    return Image.open(io.BytesIO(requests.get(url, timeout=15).content)).convert("RGBA")


def composite_bg(fg, bg):
    try:
        from rembg import remove as rembg_remove
        no_bg = Image.open(io.BytesIO(rembg_remove(pil_to_bytes(fg)))).convert("RGBA")
        return Image.alpha_composite(
            bg.resize(no_bg.size, Image.LANCZOS).convert("RGBA"), no_bg
        ).convert("RGB")
    except ImportError:
        st.warning("⚠️ rembg yoxdur")
        return fg


MSGS = [
    "🚀 AI mühərriki işə düşür...", "🧪 Piksellər bərpa olunur...",
    "✨ Möcüzə baş verir...", "🎨 Rənglər canlanır...", "⚡ GPU tam gücündə..."
]


def spinner_thread(mb, stop):
    i = 0
    while not stop[0]:
        mb.markdown(f'<div class="spin-msg">{MSGS[i % len(MSGS)]}</div>', unsafe_allow_html=True)
        time.sleep(2)
        i += 1


# ── SAM HTML5 Canvas ─────────────────────────────────────────────
def sam_canvas(img_pil, key="sam"):
    iw, ih = img_pil.size
    s = min(680 / iw, 460 / ih, 1.0)
    cw, ch = int(iw * s), int(ih * s)
    buf = io.BytesIO()
    img_pil.resize((cw, ch), Image.LANCZOS).save(buf, format="PNG")
    ib64 = base64.b64encode(buf.getvalue()).decode()
    html = f"""
<div style="text-align:center">
<canvas id="cv{key}" width="{cw}" height="{ch}"
  style="border-radius:12px;border:2px solid #1e251e;cursor:crosshair;
         display:block;margin:0 auto;max-width:100%;background:#0a0c0a"></canvas>
</div>
<div style="display:flex;gap:.5rem;justify-content:center;margin:.7rem 0;flex-wrap:wrap">
  <button id="bA{key}" onclick="md{key}='add';hi{key}()"
    style="background:linear-gradient(135deg,#1a6b2f,#2d9e4a);border:none;color:#fff;
           padding:.4rem 1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">
    ➕ Sil (yaşıl)</button>
  <button id="bE{key}" onclick="md{key}='exc';hi{key}()"
    style="background:linear-gradient(135deg,#6b1a1a,#9e2d2d);border:none;color:#fff;
           padding:.4rem 1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">
    ➖ Saxla (qırmızı)</button>
  <button onclick="cl{key}=[];rd{key}();inf{key}()"
    style="background:#1a1a1a;border:1px solid #444;color:#aaa;
           padding:.4rem .8rem;border-radius:8px;cursor:pointer;font-size:.75rem">
    🗑️ Sıfırla</button>
</div>
<div id="inf{key}" style="text-align:center;font-size:.72rem;color:#888;min-height:1.2em;margin:.3rem 0"></div>
<script>
(function(){{
  const cv=document.getElementById('cv{key}');
  const ctx=cv.getContext('2d');
  const SX={iw}/{cw},SY={ih}/{ch};
  let cl{key}=[],md{key}='add';
  const bg=new Image();
  bg.onload=()=>rd{key}();
  bg.src='data:image/png;base64,{ib64}';
  function rd{key}(){{
    ctx.clearRect(0,0,{cw},{ch});ctx.drawImage(bg,0,0,{cw},{ch});
    cl{key}.forEach(([x,y,l])=>{{
      ctx.beginPath();ctx.arc(x,y,9,0,Math.PI*2);
      ctx.fillStyle=l===1?'rgba(45,200,80,.9)':'rgba(220,50,50,.9)';ctx.fill();
      ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      ctx.fillStyle='#fff';ctx.font='bold 11px sans-serif';
      ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(l===1?'✓':'✗',x,y);
    }});
  }}
  function inf{key}(){{
    const n=cl{key}.length;
    const el=document.getElementById('inf{key}');
    el.textContent=n===0?'🖱️ Şəkilə klikləyin — yaşıl nöqtə silinəcək obyekti göstərir':n+' nöqtə seçildi';
    el.style.color=n>0?'#4dff88':'#888';
    const out=JSON.stringify(cl{key}.map(([x,y,l])=>({{x:Math.round(x*SX),y:Math.round(y*SY),label:l}})));
    const inp=parent.document.querySelector('input[aria-label="coords_{key}"]');
    if(inp){{inp.value=out;inp.dispatchEvent(new Event('input',{{bubbles:true}}));}}
  }}
  window['hi{key}']=function(){{
    document.getElementById('bA{key}').style.opacity=md{key}==='add'?'1':'.55';
    document.getElementById('bE{key}').style.opacity=md{key}==='exc'?'1':'.55';
  }};
  cv.addEventListener('click',e=>{{
    const r=cv.getBoundingClientRect();
    cl{key}.push([Math.round((e.clientX-r.left)*(cv.width/r.width)),
                  Math.round((e.clientY-r.top)*(cv.height/r.height)),md{key}==='add'?1:0]);
    rd{key}();inf{key}();
  }});
  inf{key}();
}})();
</script>"""
    st.components.v1.html(html, height=ch + 120, scrolling=False)


# ── Header ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="logo-wrap">
  <img class="logo-circle" src="data:image/jpeg;base64,{LOGO_B64}" alt="logo">
  <div class="main-title">TFTML <span>ENHANCER</span> AI</div>
  <div class="school-name">K. Ağayev adına <b>Biləsuvar Şəhər</b><br>
  Texniki Fənlər Təmayüllü İnternat Tipli Məktəb-Lisey</div>
  <div class="school-sub">AI Şəkil · SAM · Fon Silmə · Video | Real-ESRGAN 4×</div>
</div>
""", unsafe_allow_html=True)

api_ok = check_api(API_URL)
if api_ok:
    st.markdown('<div class="status-ok">✅ Colab Backend — Online · GPU Aktiv</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-err">⚠️ Colab Backend offline — Colab-ı işə salın</div>', unsafe_allow_html=True)

# ── 4 Tab ────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🖼️  Şəkil Artır",
    "🧹  Ağıllı Sil (SAM)",
    "✂️  Arxa Fon Sil",   # ← YENİ TAB
    "🎬  Video Artır",
])

# ══════════════════════════════════════════════════════════════════
#  TAB 1 — ŞƏKİL ARTIR
# ══════════════════════════════════════════════════════════════════
with tab1:
    up1 = st.file_uploader("📸  Şəkil seçin", type=["jpg", "jpeg", "png", "webp", "bmp"], key="u1")
    fim = None
    if up1:
        op = Image.open(up1).convert("RGB")
        cp, fx = st.columns([3, 2])
        with fx:
            st.markdown('<div class="fx-panel"><div class="fx-title">✂️ Kəsim</div>', unsafe_allow_html=True)
            w, h = op.size
            a, b = st.columns(2)
            with a:
                cl = st.number_input("Sol",    0, w - 10, 0, step=5, key="cl")
                ct = st.number_input("Yuxarı", 0, h - 10, 0, step=5, key="ct")
            with b:
                cr = st.number_input("Sağ",   10, w, w, step=5, key="cr")
                cb = st.number_input("Aşağı", 10, h, h, step=5, key="cb")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="fx-panel"><div class="fx-title">🎨 Effektlər</div>', unsafe_allow_html=True)
            br = st.slider("☀️ Parlaqlıq", 0.5, 2.0, 1.0, 0.05, key="br")
            co = st.slider("🌗 Kontrast",  0.5, 2.0, 1.0, 0.05, key="co")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="fx-panel"><div class="fx-title">🖼️ Arxa Fon</div>', unsafe_allow_html=True)
            bgc = st.selectbox("Fon", list(BACKGROUNDS.keys()), key="bgc")
            abg = st.checkbox("✅ Arxa fonu dəyişdir", key="abg")
            cbg = None
            if BACKGROUNDS[bgc] == "custom":
                cf = st.file_uploader("Öz fonunuzu yükləyin", type=["jpg", "jpeg", "png", "webp"],
                                      key="cf", label_visibility="visible")
                if cf:
                    cbg = Image.open(cf).convert("RGBA")
            else:
                try:
                    st.image(fetch_bg(BACKGROUNDS[bgc]).convert("RGB").resize((220, 124), Image.LANCZOS),
                             use_container_width=True)
                except Exception:
                    pass
            st.markdown('</div>', unsafe_allow_html=True)
        with cp:
            ed = apply_fx(op.crop((cl, ct, cr, cb)), br, co)
            if abg:
                try:
                    bi  = cbg if BACKGROUNDS[bgc] == "custom" else fetch_bg(BACKGROUNDS[bgc])
                    fim = composite_bg(ed, bi) if bi else ed
                except Exception as e:
                    st.error(f"Fon: {e}")
                    fim = ed
            else:
                fim = ed
            st.markdown('<p style="text-align:center;font-size:.68rem;color:#555;'
                        'letter-spacing:.1em;text-transform:uppercase;margin-bottom:.3rem">Önizləmə</p>',
                        unsafe_allow_html=True)
            st.image(fim, use_container_width=True)
            st.caption(f"📐 {fim.width}×{fim.height} px")

    b1 = st.button("✨  AI ilə 4× Keyfiyyəti Artır",
                   disabled=not (up1 and api_ok and fim is not None), key="b1")
    if b1 and fim:
        sb = pil_to_bytes(fim)
        hh = hashlib.md5(sb).hexdigest()
        pg = st.progress(0)
        mb = st.empty()
        st_ = [False]
        threading.Thread(target=spinner_thread, args=(mb, st_), daemon=True).start()
        pg.progress(20, "Colab-a göndərilir...")
        rb, err = enhance_cached(sb, API_URL)
        st_[0] = True
        mb.empty()
        pg.progress(100, "Hazır! 🎉")
        if err:
            st.error(f"❌ {err}")
        else:
            st.balloons()
            if st.session_state.get(f"c_{hh}"):
                st.markdown('<div style="background:#0a1520;border:1px solid #1a4a7a;border-radius:8px;'
                            'padding:.35rem .9rem;font-size:.7rem;color:#5bb3ff;font-weight:600;'
                            'display:inline-block;margin-bottom:.4rem">⚡ Cache</div>', unsafe_allow_html=True)
            st.session_state[f"c_{hh}"] = True
            st.success("🎉 Tamamlandı!")
            rp = Image.open(io.BytesIO(rb))
            st.markdown('<div class="card"><div style="display:flex;align-items:center;'
                        'justify-content:space-between;margin-bottom:1rem">'
                        '<span style="font-family:\'Playfair Display\',serif;font-size:.95rem;'
                        'color:#eee">Nəticə</span><span class="b-4x">4× Enhanced</span></div>',
                        unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<p style="text-align:center"><span class="badge b-orig">REDAKTƏLİ</span></p>',
                            unsafe_allow_html=True)
                st.image(fim, use_container_width=True)
            with c2:
                st.markdown('<p style="text-align:center"><span class="badge b-enh">4× AI</span></p>',
                            unsafe_allow_html=True)
                st.image(rp, use_container_width=True)
            base_name = (up1.name or "image").rsplit(".", 1)[0]
            d1, d2 = st.columns(2)
            with d1:
                st.download_button("⬇  Artırılmışı Endir", rb,
                                   f"enhanced_{base_name}.png", "image/png", use_container_width=True)
            with d2:
                st.download_button("⬇  Redaktəlini Endir", sb,
                                   f"edited_{base_name}.png", "image/png", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  TAB 2 — SAM
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""<div class="sam-tip">
    🧠 <b>SAM — Segment Anything Model</b><br>
    1️⃣ Şəkil yükləyin<br>
    2️⃣ <b style="color:#4dff88">➕ Sil</b> — silinəcək obyektə klikləyin (yaşıl)<br>
    3️⃣ <b style="color:#ff8888">➖ Saxla</b> — saxlanacaq hissəyə klikləyin (opsional)<br>
    4️⃣ <b>"Ağıllı Sil"</b> düyməsini basın
    </div>""", unsafe_allow_html=True)

    up2 = st.file_uploader("📸  Şəkil seçin (SAM üçün)",
                           type=["jpg", "jpeg", "png", "webp"], key="u2")
    if up2:
        ip = Image.open(up2).convert("RGB")
        iw, ih = ip.size
        sam_canvas(ip, key="s1")
        cj = st.text_input("📍 Koordinatlar:",
                           placeholder='[{"x":200,"y":150,"label":1}]',
                           key="coords_s1", label_visibility="visible")
        st.caption("💡 Şəkilə kliklədikdən sonra koordinatlar burada görünür")

        bs = st.button("🧠  Ağıllı Sil", disabled=not api_ok, key="bs")
        if bs:
            cks = []
            try:
                cks = json.loads(cj) if cj.strip() else []
            except Exception:
                st.warning("⚠️ JSON oxunmadı")
            if not cks:
                cks = [{"x": iw // 2, "y": ih // 2, "label": 1}]
                st.info(f"ℹ️  Mərkəz nöqtəsi istifadə edilir ({iw // 2},{ih // 2})")
            ob  = pil_to_bytes(ip)
            pg2 = st.progress(0, "SAM-a göndərilir...")
            try:
                resp = requests.post(
                    f"{API_URL}/sam-inpaint",
                    files={"image": ("img.png", ob, "image/png")},
                    data={"clicks": json.dumps(cks)},
                    timeout=180, headers=HDR
                )
                pg2.progress(70, "SAM segmentasiya edir...")
                try:
                    data = resp.json()
                except Exception:
                    pg2.progress(100, "Xəta!")
                    st.error(f"❌ JSON parse xətası: {resp.text[:200]}")
                    data = None
                if data:
                    if data.get("success"):
                        pg2.progress(100, "Hazır! 🎉")
                        st.success(f"🎉 Tamamlandı! {'SAM ✅' if data.get('sam_used') else 'Fallback'}")
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',
                                        unsafe_allow_html=True)
                            st.image(ip, use_container_width=True)
                        with c2:
                            if data.get("mask"):
                                st.markdown('<p style="text-align:center"><span class="badge" '
                                            'style="background:#1a3a6b;color:#88ccff;border:1px solid #2a5aab">'
                                            'MASK</span></p>', unsafe_allow_html=True)
                                st.image(Image.open(io.BytesIO(base64.b64decode(data["mask"]))),
                                         use_container_width=True)
                        with c3:
                            st.markdown('<p style="text-align:center"><span class="badge b-enh">NƏTİCƏ</span></p>',
                                        unsafe_allow_html=True)
                            st.image(Image.open(io.BytesIO(base64.b64decode(data["image"]))),
                                     use_container_width=True)
                        sam_base = (up2.name or "image").rsplit(".", 1)[0]
                        st.download_button("⬇  Nəticəni Endir",
                                           base64.b64decode(data["image"]),
                                           f"sam_{sam_base}.png", "image/png",
                                           use_container_width=True)
                    else:
                        pg2.progress(100, "Xəta!")
                        st.error(f"❌ {data.get('error', 'Naməlum xəta')}")
            except requests.exceptions.Timeout:
                pg2.progress(100, "Xəta!")
                st.error("❌ Timeout (180s)")
            except requests.exceptions.ConnectionError:
                pg2.progress(100, "Xəta!")
                st.error("❌ Backend əlçatan deyil")
            except Exception as e:
                pg2.progress(100, "Xəta!")
                st.error(f"❌ {type(e).__name__}: {e}")

# ══════════════════════════════════════════════════════════════════
#  TAB 3 — ARXA FON SİL (YENİ)
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""<div class="sam-tip">
    ✂️ <b>Arxa Fon Silmə — rembg</b><br>
    1️⃣ Şəkil yükləyin<br>
    2️⃣ <b style="color:#4dff88">"Arxa Fonu Sil"</b> düyməsini basın<br>
    3️⃣ Nəticəni şəffaf PNG kimi endirin
    </div>""", unsafe_allow_html=True)

    up_rb = st.file_uploader("📸  Şəkil seçin",
                             type=["jpg", "jpeg", "png", "webp"], key="u_rb")
    if up_rb:
        orig_pil = Image.open(up_rb).convert("RGB")

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',
                        unsafe_allow_html=True)
            st.image(orig_pil, use_container_width=True)
            st.caption(f"📐 {orig_pil.width}×{orig_pil.height} px")

        btn_rb = st.button("✂️  Arxa Fonu Sil",
                           disabled=not api_ok, key="btn_rb")

        if btn_rb:
            buf = io.BytesIO()
            orig_pil.save(buf, format="PNG")
            img_bytes = buf.getvalue()

            pg_rb = st.progress(0, "rembg-yə göndərilir...")
            mb_rb = st.empty()
            st_rb = [False]

            def rb_spin():
                msgs = ["🔄 Fon analiz edilir...", "✂️ Kəsilir...", "🎨 Şəffaflaşdırılır..."]
                i = 0
                while not st_rb[0]:
                    mb_rb.markdown(f'<div class="spin-msg">{msgs[i % 3]}</div>',
                                   unsafe_allow_html=True)
                    time.sleep(1.5)
                    i += 1

            threading.Thread(target=rb_spin, daemon=True).start()
            pg_rb.progress(30, "Emal edilir...")

            result_bytes, err_msg = remove_bg_request(img_bytes, API_URL)

            st_rb[0] = True
            mb_rb.empty()

            if err_msg:
                # Xəta: "rembg xətası: [detal]" formatında göstər
                pg_rb.progress(100, "Xəta!")
                st.error(f"❌ {err_msg}")
                st.info("💡 Colab-da `!pip install rembg onnxruntime` icra edib serveri yenidən başladın.")
            else:
                pg_rb.progress(100, "Hazır! 🎉")
                st.balloons()
                st.success("🎉 Arxa fon uğurla silindi!")

                result_pil = Image.open(io.BytesIO(result_bytes)).convert("RGBA")
                with col_r:
                    st.markdown('<p style="text-align:center"><span class="badge b-enh">FON SİLİNMİŞ</span></p>',
                                unsafe_allow_html=True)
                    st.image(result_pil, use_container_width=True)
                    st.caption(f"📐 {result_pil.width}×{result_pil.height} px · RGBA PNG")

                rb_base = (up_rb.name or "image").rsplit(".", 1)[0]
                st.download_button(
                    "⬇  Şəffaf PNG kimi Endir",
                    result_bytes,
                    f"{rb_base}_no_bg.png",
                    "image/png",
                    use_container_width=True,
                )

# ══════════════════════════════════════════════════════════════════
#  TAB 4 — VİDEO ARTIR
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="video-warn">⚠️ Video emalı bir neçə dəqiqə çəkə bilər.<br>'
                'Emal zamanı pəncərəni bağlamayın!</div>', unsafe_allow_html=True)
    up3 = st.file_uploader("🎬  Video seçin", type=["mp4", "mov", "avi", "mkv"], key="u3")
    if up3:
        st.video(up3)
        st.markdown(f'<div style="font-size:.76rem;color:#666;padding:.3rem 0">🎬 '
                    f'<span style="color:#bbb">{up3.name}</span> &nbsp; 📦 '
                    f'<span style="color:#bbb">{up3.size / 1024 / 1024:.1f} MB</span></div>',
                    unsafe_allow_html=True)
    b3 = st.button("🎬  Video 4× Keyfiyyətini Artır",
                   disabled=not (up3 and api_ok), key="b3")
    if b3 and up3:
        vb = up3.read()
        st.markdown('<div class="video-warn">🔄 Video emal edilir — pəncərəni bağlamayın!</div>',
                    unsafe_allow_html=True)
        p3 = st.progress(0)
        m3 = st.empty()
        s3 = [False]
        vm = ["🎬 Kadrlar ayrılır...", "⚡ GPU emal edir...", "🔄 Video yığılır...", "✨ Möcüzə..."]

        def vsp():
            i = 0
            while not s3[0]:
                m3.markdown(f'<div class="spin-msg">{vm[i % 4]}</div>', unsafe_allow_html=True)
                time.sleep(3)
                i += 1

        threading.Thread(target=vsp, daemon=True).start()
        p3.progress(10, "Video göndərilir...")
        video_fname = up3.name or "video.mp4"
        rb3, mt3, er3 = enhance_video_cached(vb, video_fname, API_URL)
        s3[0] = True
        m3.empty()
        if er3:
            p3.progress(100, "Xəta!")
            st.error(f"❌ {er3}")
        else:
            p3.progress(100, "Video hazır! 🎉")
            st.balloons()
            st.success(f"🎉 {mt3.get('original','?')} → {mt3.get('enhanced','?')} | {mt3.get('frames','?')} kadr")
            video_base = video_fname.rsplit(".", 1)[0]
            st.download_button("⬇  4× Videonu Endir", rb3,
                               f"enhanced_{video_base}.mp4", "video/mp4",
                               use_container_width=True)
