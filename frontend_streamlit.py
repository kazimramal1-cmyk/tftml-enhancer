# ================================================================
#  frontend_streamlit.py — TFTML ENHANCER AI
#  RAMAL KAZIMZADE
# ================================================================

import streamlit as st

# ── Monkey Patch: st_image xətasını aradan qaldır ────
try:
    from streamlit.elements import image as _st_img
    if not hasattr(_st_img, "image_to_url"):
        _st_img.image_to_url = lambda x, *a, **kw: x
except Exception:
    pass

import requests, base64, io, time, threading, json
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np
import os

# ── API URL ───────────────────────────────────────────
API_URL = "https://stacie-apertural-ardelia.ngrok-free.dev"

# ── Logo yüklə ────────────────────────────────────────
_LOGO_PATH = "/mnt/user-data/uploads/logo_png.jpeg"
if os.path.exists(_LOGO_PATH):
    with open(_LOGO_PATH, "rb") as _f:
        LOGO_B64 = base64.b64encode(_f.read()).decode()
    LOGO_MIME = "image/jpeg"
else:
    # 1x1 şəffaf fallback
    LOGO_B64  = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    LOGO_MIME = "image/png"

BACKGROUNDS = {
    "🦕 Dinozavrlar": "https://images.unsplash.com/photo-1606206873764-fd15e242ff80?w=1280&q=80",
    "🏛️ Big Ben":     "https://images.unsplash.com/photo-1529655683826-aba9b3e77383?w=1280&q=80",
    "🌌 Kainat":      "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1280&q=80",
    "🌊 Okean":       "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=1280&q=80",
    "🗼 Paris":       "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1280&q=80",
    "🏔️ Dağlar":      "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1280&q=80",
    "🌸 Çiçəklər":    "https://images.unsplash.com/photo-1490750967868-88df5691cc9e?w=1280&q=80",
    "🌆 Gecə şəhər":  "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1280&q=80",
    "🏖️ Çimərlik":    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280&q=80",
    "🎨 Öz fonum":    "custom",
}

st.set_page_config(page_title="TFTML ENHANCER AI", page_icon="🎓",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');
#MainMenu,footer,header,.stDeployButton,[data-testid="stToolbar"]{{display:none!important}}
.stApp{{background:#0d0f0e!important;font-family:'DM Sans',sans-serif!important}}
.block-container{{max-width:960px!important;padding:1.5rem 1.5rem 2rem!important;margin:0 auto!important}}
.stApp::before{{content:'';position:fixed;inset:0;z-index:0;
  background:radial-gradient(ellipse at 15% 40%,rgba(26,107,47,.12) 0%,transparent 55%),
             radial-gradient(ellipse at 85% 20%,rgba(224,112,32,.10) 0%,transparent 55%);
  pointer-events:none}}
/* ── Brand ── */
.rk-brand{{position:fixed;top:14px;left:18px;z-index:999;font-family:'DM Sans',sans-serif;
  font-size:.7rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#e07020;
  text-decoration:underline;text-underline-offset:4px;
  text-decoration-color:rgba(224,112,32,.4)}}
/* ── Logo: mərkəz + dairəvi ── */
.logo-outer{{display:flex;justify-content:center;margin:1.8rem 0 .5rem}}
.logo-img{{
  width:110px;height:110px;border-radius:50%;
  object-fit:cover;display:block;
  animation:glowPulse 3s ease-in-out infinite;
  border:3px solid transparent;
}}
@keyframes glowPulse{{
  0%,100%{{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #1a6b2f,
            0 0 25px rgba(26,107,47,.55),0 0 55px rgba(224,112,32,.2)}}
  50%{{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #e07020,
           0 0 30px rgba(224,112,32,.6),0 0 65px rgba(26,107,47,.25)}}}}
/* ── Header mətnlər ── */
.hdr-title{{font-family:'Playfair Display',serif;font-size:clamp(1.3rem,3vw,1.9rem);
  font-weight:700;text-align:center;color:#f0f0f0;letter-spacing:.04em;margin:.3rem 0 .1rem}}
.hdr-title span{{color:#e07020}}
.hdr-school{{text-align:center;font-size:.82rem;color:#888;line-height:1.65;margin:.1rem 0}}
.hdr-school b{{color:#bbb}}
.hdr-sub{{text-align:center;font-size:.6rem;color:#3a3a3a;letter-spacing:.18em;
  text-transform:uppercase;margin-bottom:1.5rem}}
/* ── Status ── */
.status-ok{{background:linear-gradient(135deg,#0a1f10,#0d2b15);border:1px solid #1a6b2f;
  border-radius:12px;padding:.5rem 1.2rem;font-size:.78rem;color:#4dff88;font-weight:600;margin-bottom:1rem}}
.status-err{{background:linear-gradient(135deg,#1f0a0a,#2b0d0d);border:1px solid #6b1a1a;
  border-radius:12px;padding:.5rem 1.2rem;font-size:.78rem;color:#ff6b6b;font-weight:600;margin-bottom:1rem}}
/* ── Tabs ── */
[data-testid="stTabs"] [data-testid="stTab"]{{background:transparent!important;border:none!important;
  color:#555!important;font-weight:600!important;font-size:.84rem!important;
  padding:.55rem 1.1rem!important;border-radius:10px 10px 0 0!important;transition:all .2s!important}}
[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"]{{
  background:linear-gradient(135deg,#1a6b2f,#0d3d1a)!important;
  color:#4dff88!important;border-bottom:2px solid #2d9e4a!important}}
[data-testid="stTabContent"]{{border:1.5px solid #1e251e!important;
  border-radius:0 16px 16px 16px!important;
  background:linear-gradient(145deg,#111311,#0f110f)!important;padding:1.5rem!important}}
/* ── Upload ── */
[data-testid="stFileUploader"]{{border:2px dashed transparent!important;border-radius:16px!important;
  background:linear-gradient(#131613,#131613) padding-box,
             linear-gradient(135deg,#1a6b2f,#e07020,#1a6b2f) border-box!important;padding:1.2rem!important}}
[data-testid="stFileUploader"] *{{color:#888!important}}
[data-testid="stFileUploader"] svg{{fill:#e07020!important}}
[data-testid="stFileUploader"] button{{background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:8px!important}}
/* ── Buttons ── */
.stButton>button{{font-family:'DM Sans',sans-serif!important;font-weight:700!important;
  font-size:.95rem!important;background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:12px!important;
  padding:.85rem 2rem!important;width:100%!important;
  box-shadow:0 4px 20px rgba(26,107,47,.4)!important;transition:transform .2s!important}}
.stButton>button:hover{{transform:scale(1.03) translateY(-2px)!important}}
.stButton>button:disabled{{opacity:.35!important}}
/* ── Sliders ── */
[data-testid="stSlider"]>div>div>div{{background:#1a6b2f!important}}
[data-testid="stSlider"] label{{color:#aaa!important;font-size:.78rem!important}}
/* ── Panels ── */
.fx-panel{{background:#0d1510;border:1px solid #1a3320;border-radius:12px;padding:1rem 1.2rem;margin:.5rem 0}}
.fx-title{{font-size:.65rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:#4dff88;margin-bottom:.7rem}}
/* ── Info boxes ── */
.video-warn{{background:linear-gradient(135deg,#1a1200,#2b1e00);border:1px solid #6b4e00;
  border-radius:14px;padding:1rem 1.4rem;font-size:.82rem;color:#ffcc44;font-weight:600;
  margin:1rem 0;line-height:1.7;text-align:center}}
.brush-tip{{background:linear-gradient(135deg,#1a0d2b,#100a20);border:1px solid #4a1a8b;
  border-radius:12px;padding:.8rem 1.2rem;font-size:.78rem;color:#cc88ff;line-height:1.8;margin:.6rem 0}}
.sam-tip{{background:linear-gradient(135deg,#0d1a2b,#0a1020);border:1px solid #1a3a6b;
  border-radius:12px;padding:.8rem 1.2rem;font-size:.78rem;color:#88ccff;line-height:1.8;margin:.6rem 0}}
/* ── Progress / images / download ── */
.stProgress>div>div{{background:linear-gradient(90deg,#1a6b2f,#e07020)!important;border-radius:3px!important}}
[data-testid="stImage"] img{{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}}
.spin-msg{{text-align:center;font-size:.95rem;font-weight:600;color:#e07020;padding:.7rem}}
.badge{{display:inline-block;font-size:.58rem;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;padding:.2rem .55rem;border-radius:4px;margin-bottom:.4rem}}
.b-orig{{background:rgba(80,80,80,.3);color:#aaa;border:1px solid #333}}
.b-enh{{background:rgba(26,107,47,.4);color:#4dff88;border:1px solid #1a6b2f}}
.b-4x{{background:linear-gradient(135deg,#e07020,#f59030);color:#fff;font-size:.6rem;
  font-weight:700;padding:.22rem .65rem;border-radius:18px;letter-spacing:.1em}}
.stDownloadButton>button{{font-family:'DM Sans',sans-serif!important;font-weight:600!important;
  font-size:.82rem!important;border-radius:10px!important;padding:.6rem 1.2rem!important;
  width:100%!important;background:#111!important;border:1.5px solid #1e251e!important;color:#aaa!important}}
.stDownloadButton>button:hover{{border-color:#2d9e4a!important;color:#4dff88!important}}
video{{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}}
</style>
<div class="rk-brand">RAMAL KAZIMZADE</div>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────
st.markdown(f"""
<div class="logo-outer">
  <img class="logo-img"
       src="data:{LOGO_MIME};base64,{LOGO_B64}"
       alt="Məktəb Loqosu">
</div>
<div class="hdr-title">TFTML <span>ENHANCER</span> AI</div>
<div class="hdr-school">
  K. Ağayev adına <b>Biləsuvar Şəhər</b><br>
  Texniki Fənlər Təmayüllü İnternat Tipli Məktəb-Lisey
</div>
<div class="hdr-sub">AI Şəkil &nbsp;·&nbsp; SAM &nbsp;·&nbsp; Fırça Silmə &nbsp;·&nbsp; Video &nbsp;|&nbsp; Real-ESRGAN 4×</div>
""", unsafe_allow_html=True)

# ── API Status ────────────────────────────────────────
def check_api(url):
    try:
        r = requests.get(f"{url}/health", timeout=6,
            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
        return r.status_code == 200
    except: return False

api_ok = check_api(API_URL)
if api_ok:
    st.markdown('<div class="status-ok">✅ Colab Backend — Online · GPU Aktiv</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-err">⚠️ Colab Backend offline — Colab-ı işə salın</div>', unsafe_allow_html=True)

# ── Köməkçi funksiyalar ───────────────────────────────
def pil_to_bytes(img):
    buf = io.BytesIO(); img.save(buf,format="PNG",optimize=True); return buf.getvalue()

def apply_effects(img, br, co):
    return ImageEnhance.Contrast(ImageEnhance.Brightness(img).enhance(br)).enhance(co)

@st.cache_data(show_spinner=False)
def fetch_bg(url):
    return Image.open(io.BytesIO(requests.get(url,timeout=15).content)).convert("RGBA")

def composite_bg(fg, bg):
    try:
        from rembg import remove as rembg_remove
        no_bg = Image.open(io.BytesIO(rembg_remove(pil_to_bytes(fg)))).convert("RGBA")
        return Image.alpha_composite(bg.resize(no_bg.size,Image.LANCZOS).convert("RGBA"),no_bg).convert("RGB")
    except ImportError:
        st.warning("⚠️ rembg yoxdur"); return fg

@st.cache_data(show_spinner=False, max_entries=50)
def enhance_cached(img_bytes, api_url):
    try:
        resp = requests.post(f"{api_url}/enhance",
            files={"image":("img.png", img_bytes, "image/png")}, timeout=300,
            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
        d = resp.json()
        if d.get("success"): return base64.b64decode(d["image"]), None
        return None, d.get("error","Xəta")
    except Exception as e: return None, str(e)

@st.cache_data(show_spinner=False, max_entries=10)
def enhance_video_cached(vid_bytes, fname, api_url):
    try:
        ext  = fname.rsplit(".",1)[-1].lower()
        mime = {"mp4":"video/mp4","mov":"video/quicktime","avi":"video/x-msvideo"}.get(ext,"video/mp4")
        resp = requests.post(f"{api_url}/enhance-video",
            files={"video":(fname, vid_bytes, mime)}, timeout=600,
            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
        d = resp.json()
        if d.get("success"): return base64.b64decode(d["image"]), d, None
        return None, {}, d.get("error","Xəta")
    except Exception as e: return None, {}, str(e)

MSGS = ["🚀 AI mühərriki işə düşür...","🧪 Piksellər bərpa olunur...",
        "✨ Möcüzə baş verir...","🎨 Rənglər canlanır...","⚡ GPU tam gücündə..."]

# ── SAM Canvas ────────────────────────────────────────
def sam_canvas(img_pil, key="sam"):
    iw,ih  = img_pil.size
    scale  = min(680/iw, 460/ih, 1.0)
    cw,ch  = int(iw*scale), int(ih*scale)
    buf    = io.BytesIO()
    img_pil.resize((cw,ch),Image.LANCZOS).save(buf,format="PNG")
    b64    = base64.b64encode(buf.getvalue()).decode()
    html = f"""
<div style="text-align:center">
<canvas id="c_{key}" width="{cw}" height="{ch}"
  style="border-radius:12px;border:2px solid #1e251e;cursor:crosshair;
         display:block;margin:0 auto;max-width:100%"></canvas>
</div>
<div style="display:flex;gap:.5rem;justify-content:center;margin:.7rem 0;flex-wrap:wrap">
  <button onclick="md_{key}='a'"
    style="background:linear-gradient(135deg,#1a6b2f,#2d9e4a);border:none;color:#fff;
    padding:.4rem 1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">➕ Sil (yaşıl)</button>
  <button onclick="md_{key}='e'"
    style="background:linear-gradient(135deg,#6b1a1a,#9e2d2d);border:none;color:#fff;
    padding:.4rem 1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">➖ Saxla (qırmızı)</button>
  <button onclick="cl_{key}=[];rdr_{key}()"
    style="background:#1a1a1a;border:1px solid #444;color:#aaa;
    padding:.4rem .8rem;border-radius:8px;cursor:pointer;font-size:.75rem">🗑️ Sıfırla</button>
</div>
<div id="inf_{key}" style="text-align:center;font-size:.72rem;color:#888;margin:.3rem 0">
  🖱️ Şəkilə klikləyin
</div>
<script>
(function(){{
  const cv=document.getElementById('c_{key}');
  const ctx=cv.getContext('2d');
  const scX={iw}/{cw},scY={ih}/{ch};
  let cl=[],md='a';
  window['cl_{key}']=cl; window['md_{key}']=md;
  const bg=new Image(); bg.src='data:image/png;base64,{b64}';
  bg.onload=()=>rdr_{key}();
  window['rdr_{key}']=function(){{
    ctx.clearRect(0,0,{cw},{ch}); ctx.drawImage(bg,0,0,{cw},{ch});
    cl.forEach(([x,y,l])=>{{
      ctx.beginPath(); ctx.arc(x,y,9,0,Math.PI*2);
      ctx.fillStyle=l?'rgba(45,200,80,.9)':'rgba(220,50,50,.9)'; ctx.fill();
      ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke();
      ctx.fillStyle='#fff'; ctx.font='bold 11px sans-serif';
      ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText(l?'✓':'✗',x,y);
    }});
    const inf=document.getElementById('inf_{key}');
    inf.textContent=cl.length?cl.length+' nöqtə seçildi':'🖱️ Şəkilə klikləyin';
    inf.style.color=cl.length?'#4dff88':'#888';
    const out=cl.map(([x,y,l])=>({{x:Math.round(x*scX),y:Math.round(y*scY),label:l}}));
    const inp=document.querySelector('input[aria-label="clicks_{key}"]');
    if(inp){{inp.value=JSON.stringify(out);inp.dispatchEvent(new Event('input',{{bubbles:true}}));}}
  }};
  cv.addEventListener('click',e=>{{
    const r=cv.getBoundingClientRect();
    cl.push([Math.round((e.clientX-r.left)*(cv.width/r.width)),
             Math.round((e.clientY-r.top)*(cv.height/r.height)),
             window['md_{key}']==='a'?1:0]);
    rdr_{key}();
  }});
}})();
</script>"""
    st.components.v1.html(html, height=ch+110, scrolling=False)

# ── Fırça Canvas ──────────────────────────────────────
def brush_tool(img_pil, key="br"):
    iw,ih  = img_pil.size
    scale  = min(680/iw, 500/ih, 1.0)
    cw,ch  = int(iw*scale), int(ih*scale)
    buf    = io.BytesIO()
    img_pil.resize((cw,ch),Image.LANCZOS).save(buf,format="PNG")
    b64    = base64.b64encode(buf.getvalue()).decode()
    html = f"""
<div style="text-align:center">
<canvas id="cv_{key}" width="{cw}" height="{ch}"
  style="border-radius:12px;border:2px solid #4a1a8b;cursor:crosshair;
         display:block;margin:0 auto;max-width:100%;touch-action:none"></canvas>
</div>
<div style="display:flex;gap:.6rem;justify-content:center;margin:.8rem 0;flex-wrap:wrap;align-items:center">
  <button onclick="st_{key}('b')"
    style="background:linear-gradient(135deg,#8b0000,#cc2200);border:none;color:#fff;
    padding:.45rem 1.1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">🖌️ Fırça</button>
  <button onclick="st_{key}('e')"
    style="background:linear-gradient(135deg,#1a3a6b,#2a5aab);border:none;color:#fff;
    padding:.45rem 1.1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">⬜ Pozucu</button>
  <button onclick="cl_{key}()"
    style="background:#222;border:1px solid #444;color:#aaa;
    padding:.45rem .9rem;border-radius:8px;cursor:pointer;font-size:.75rem">🗑️ Hamısını Sil</button>
  <label style="color:#aaa;font-size:.72rem;font-weight:600">Ölçü:
    <input type="range" id="sz_{key}" min="5" max="100" value="30"
      style="width:80px;vertical-align:middle;accent-color:#cc2200"
      oninput="document.getElementById('szv_{key}').textContent=this.value">
    <span id="szv_{key}">30</span>px
  </label>
</div>
<div id="bi_{key}" style="text-align:center;font-size:.72rem;color:#cc88ff;margin:.4rem 0">
  🖌️ Qırmızı fırça ilə silinəcək hissəni boyayın
</div>
<script>
(function(){{
  const cv=document.getElementById('cv_{key}');
  const ctx=cv.getContext('2d');
  const ov=document.createElement('canvas');
  ov.width={cw}; ov.height={ch};
  const oc=ov.getContext('2d');
  const scX={iw}/{cw},scY={ih}/{ch};
  let tool='b',paint=false;
  const bg=new Image(); bg.src='data:image/png;base64,{b64}';
  bg.onload=()=>drw();
  function drw(){{
    ctx.clearRect(0,0,{cw},{ch});
    ctx.drawImage(bg,0,0,{cw},{ch});
    ctx.globalAlpha=0.6; ctx.drawImage(ov,0,0); ctx.globalAlpha=1;
  }}
  function pos(e){{
    const r=cv.getBoundingClientRect();
    const cx=e.touches?e.touches[0].clientX:e.clientX;
    const cy=e.touches?e.touches[0].clientY:e.clientY;
    return [(cx-r.left)*(cv.width/r.width),(cy-r.top)*(cv.height/r.height)];
  }}
  function dot(e){{
    if(!paint)return;
    const [x,y]=pos(e);
    const sz=parseInt(document.getElementById('sz_{key}').value);
    oc.globalCompositeOperation=tool==='e'?'destination-out':'source-over';
    oc.fillStyle='rgba(220,30,30,1)';
    oc.beginPath(); oc.arc(x,y,sz/2,0,Math.PI*2); oc.fill();
    drw();
    const inp=document.querySelector('input[aria-label="strokes_{key}"]');
    if(inp){{
      let arr=[]; try{{arr=JSON.parse(inp.value||'[]')}}catch{{}}
      arr.push({{x:Math.round(x*scX),y:Math.round(y*scY),
                 r:Math.max(Math.round(sz/2*scX),3),t:tool}});
      inp.value=JSON.stringify(arr);
      inp.dispatchEvent(new Event('input',{{bubbles:true}}));
    }}
    document.getElementById('bi_{key}').textContent='✅ Rəngləndi — "Fırça ilə Sil" düyməsini basın';
    document.getElementById('bi_{key}').style.color='#ff8888';
  }}
  cv.addEventListener('mousedown',e=>{{paint=true;dot(e)}});
  cv.addEventListener('mousemove',dot);
  cv.addEventListener('mouseup',()=>paint=false);
  cv.addEventListener('mouseleave',()=>paint=false);
  cv.addEventListener('touchstart',e=>{{paint=true;dot(e);e.preventDefault()}},{{passive:false}});
  cv.addEventListener('touchmove',e=>{{dot(e);e.preventDefault()}},{{passive:false}});
  cv.addEventListener('touchend',()=>paint=false);
  window['st_{key}']=t=>{{
    tool=t;
    const bi=document.getElementById('bi_{key}');
    bi.textContent=t==='b'?'🖌️ Fırça aktiv':'⬜ Pozucu aktiv';
    bi.style.color=t==='b'?'#ff8888':'#88aaff';
  }};
  window['cl_{key}']=()=>{{
    oc.clearRect(0,0,{cw},{ch}); drw();
    const inp=document.querySelector('input[aria-label="strokes_{key}"]');
    if(inp){{inp.value='[]'; inp.dispatchEvent(new Event('input',{{bubbles:true}}));}}
    document.getElementById('bi_{key}').textContent='🖌️ Qırmızı fırça ilə silinəcək hissəni boyayın';
    document.getElementById('bi_{key}').style.color='#cc88ff';
  }};
}})();
</script>"""
    st.components.v1.html(html, height=ch+160, scrolling=False)
    strokes = st.text_input("🖊️ Fırça məlumatı:", key=f"strokes_{key}",
                             label_visibility="visible")
    st.caption("💡 Şəkili boyayandan sonra bu sahə dolur — sonra 'Sil' düyməsini basın.")
    return strokes

def strokes_to_mask(raw, iw, ih):
    mask = Image.new("L", (iw,ih), 0)
    draw = ImageDraw.Draw(mask)
    try:
        for s in json.loads(raw or "[]"):
            x,y,r = s["x"],s["y"],s.get("r",10)
            fill  = 0 if s.get("t")=="e" else 255
            draw.ellipse([x-r,y-r,x+r,y+r], fill=fill)
    except: pass
    return mask

# ══════════════════════════════════════════════════════
tab1,tab2,tab3,tab4 = st.tabs([
    "🖼️  Şəkil Artır",
    "🧹  Ağıllı Sil (SAM)",
    "🖌️  Fırça ilə Sil",
    "🎬  Video Artır"
])

# ── TAB 1: ŞƏKİL ─────────────────────────────────────
with tab1:
    uploaded = st.file_uploader("📸  Şəkil seçin",
        type=["jpg","jpeg","png","webp","bmp"], key="img_up")
    final_img = None
    if uploaded:
        orig = Image.open(uploaded).convert("RGB")
        cp, cf = st.columns([3,2])
        with cf:
            st.markdown('<div class="fx-panel"><div class="fx-title">✂️ Kəsim</div>',unsafe_allow_html=True)
            w,h=orig.size
            c1,c2=st.columns(2)
            with c1:
                cl2=st.number_input("Sol",   0,w-10,0,step=5,key="cl2")
                ct2=st.number_input("Yuxarı",0,h-10,0,step=5,key="ct2")
            with c2:
                cr2=st.number_input("Sağ",  10,w,w,step=5,key="cr2")
                cb2=st.number_input("Aşağı",10,h,h,step=5,key="cb2")
            st.markdown('</div>',unsafe_allow_html=True)
            st.markdown('<div class="fx-panel"><div class="fx-title">🎨 Effektlər</div>',unsafe_allow_html=True)
            br=st.slider("☀️ Parlaqlıq",0.5,2.0,1.0,0.05,key="br")
            co=st.slider("🌗 Kontrast", 0.5,2.0,1.0,0.05,key="co")
            st.markdown('</div>',unsafe_allow_html=True)
            st.markdown('<div class="fx-panel"><div class="fx-title">🖼️ Arxa Fon</div>',unsafe_allow_html=True)
            bgc=st.selectbox("Fon",list(BACKGROUNDS.keys()),key="bgc")
            abg=st.checkbox("✅ Arxa fonu dəyişdir",key="abg")
            cbg=None
            if BACKGROUNDS[bgc]=="custom":
                cf2=st.file_uploader("Öz fonunuzu yükləyin",
                    type=["jpg","jpeg","png","webp"],key="cbg2",label_visibility="visible")
                if cf2: cbg=Image.open(cf2).convert("RGBA")
            else:
                try: st.image(fetch_bg(BACKGROUNDS[bgc]).convert("RGB").resize((220,124),Image.LANCZOS),use_container_width=True)
                except: pass
            st.markdown('</div>',unsafe_allow_html=True)
        with cp:
            edited = apply_effects(orig.crop((cl2,ct2,cr2,cb2)),br,co)
            if abg:
                try:
                    bgi = cbg if BACKGROUNDS[bgc]=="custom" else fetch_bg(BACKGROUNDS[bgc])
                    final_img = composite_bg(edited,bgi) if bgi else edited
                except Exception as e:
                    st.error(f"Fon xətası: {e}"); final_img=edited
            else: final_img=edited
            st.image(final_img,use_container_width=True)
            st.caption(f"📐 {final_img.width}×{final_img.height} px")

    if st.button("✨  AI ilə 4× Keyfiyyəti Artır",
                 disabled=not(uploaded and api_ok and final_img is not None), key="btn1"):
        sb   = pil_to_bytes(final_img)
        prog = st.progress(0); mb=st.empty(); stop=[False]
        def _sp():
            i=0
            while not stop[0]:
                mb.markdown(f'<div class="spin-msg">{MSGS[i%len(MSGS)]}</div>',unsafe_allow_html=True)
                time.sleep(2); i+=1
        threading.Thread(target=_sp,daemon=True).start()
        prog.progress(20,"Colab-a göndərilir...")
        rb, err = enhance_cached(sb, API_URL)
        stop[0]=True; mb.empty(); prog.progress(100,"Hazır! 🎉")
        if err: st.error(f"❌ {err}")
        else:
            st.balloons()
            rp = Image.open(io.BytesIO(rb))
            c1,c2=st.columns(2)
            with c1:
                st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',unsafe_allow_html=True)
                st.image(final_img,use_container_width=True)
            with c2:
                st.markdown('<p style="text-align:center"><span class="badge b-enh">4× AI</span></p>',unsafe_allow_html=True)
                st.image(rp,use_container_width=True)
            d1,d2=st.columns(2)
            with d1: st.download_button("⬇  Artırılmışı Endir",rb,
                f"enhanced_{uploaded.name.rsplit('.',1)[0]}.png","image/png",use_container_width=True)
            with d2: st.download_button("⬇  Redaktəlini Endir",sb,
                f"edited_{uploaded.name.rsplit('.',1)[0]}.png","image/png",use_container_width=True)

# ── TAB 2: SAM ────────────────────────────────────────
with tab2:
    st.markdown("""<div class="sam-tip">
    🧠 <b>SAM — Segment Anything Model</b><br>
    1️⃣ Şəkil yükləyin &nbsp; 2️⃣ <b style="color:#4dff88">➕ Sil</b> rejimində silinəcək yerə klikləyin<br>
    3️⃣ <b style="color:#ff8888">➖ Saxla</b> rejimində saxlanılacaq yerə klikləyin &nbsp; 4️⃣ "Ağıllı Sil" basın
    </div>""", unsafe_allow_html=True)

    sf = st.file_uploader("📸  Şəkil seçin (SAM üçün)",
                          type=["jpg","jpeg","png","webp"], key="sam_up")
    if sf:
        sp = Image.open(sf).convert("RGB")
        iw,ih = sp.size
        sam_canvas(sp, key="sam1")
        cj = st.text_input("📍 Klik koordinatları:",
                           placeholder='[{"x":200,"y":150,"label":1}]',
                           key="sam_clicks", label_visibility="visible")
        st.caption("💡 Şəkilə kliklədikdən sonra bu sahə avtomatik dolur.")

        if st.button("🧠  Ağıllı Sil (SAM + Inpainting)",
                     disabled=not api_ok, key="btn_sam"):
            try: clicks = json.loads(cj.strip()) if cj.strip() else []
            except: clicks = []
            if not clicks:
                st.warning("⚠️ Nöqtə seçilmədi — şəkil mərkəzi istifadə edilir.")
                clicks = [{"x":iw//2,"y":ih//2,"label":1}]
            pg = st.progress(0,"SAM-a göndərilir...")
            try:
                resp = requests.post(f"{API_URL}/sam-inpaint",
                    files={"image":("img.png",pil_to_bytes(sp),"image/png")},
                    data={"clicks":json.dumps(clicks)}, timeout=180,
                    headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
                pg.progress(70,"SAM işləyir...")
                d = resp.json()
                if d.get("success"):
                    pg.progress(100,"Hazır! 🎉")
                    st.success(f"🎉 Tamamlandı! {'SAM ✅' if d.get('sam_used') else 'Fallback'}")
                    c1,c2,c3=st.columns(3)
                    with c1:
                        st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',unsafe_allow_html=True)
                        st.image(sp,use_container_width=True)
                    with c2:
                        if d.get("mask"):
                            st.markdown('<p style="text-align:center"><span class="badge" style="background:#1a3a6b;color:#88ccff;border:1px solid #2a5aab">SAM MASK</span></p>',unsafe_allow_html=True)
                            st.image(Image.open(io.BytesIO(base64.b64decode(d["mask"]))),use_container_width=True)
                    with c3:
                        st.markdown('<p style="text-align:center"><span class="badge b-enh">NƏTİCƏ</span></p>',unsafe_allow_html=True)
                        st.image(Image.open(io.BytesIO(base64.b64decode(d["image"]))),use_container_width=True)
                    st.download_button("⬇  Nəticəni Endir",
                        base64.b64decode(d["image"]),
                        f"sam_{sf.name.rsplit('.',1)[0]}.png","image/png",use_container_width=True)
                else:
                    pg.progress(100,"Xəta!"); st.error(f"❌ {d.get('error','Naməlum xəta')}")
            except Exception as e:
                st.error(f"❌ {e}")

# ── TAB 3: FIRÇA ──────────────────────────────────────
with tab3:
    st.markdown("""<div class="brush-tip">
    🖌️ <b>Fırça ilə Silmə:</b><br>
    1️⃣ Şəkil yükləyin &nbsp; 2️⃣ Qırmızı fırça ilə silinəcək hissəni boyayın<br>
    3️⃣ Pozucu ilə səhvi düzəldin &nbsp; 4️⃣ "Fırça ilə Sil" basın — AI arxasını doldurur
    </div>""", unsafe_allow_html=True)

    bf = st.file_uploader("📸  Şəkil seçin",
                          type=["jpg","jpeg","png","webp"], key="brush_up")
    if bf:
        bp = Image.open(bf).convert("RGB")
        iw,ih = bp.size
        strokes = brush_tool(bp, key="br1")

        if st.button("🖌️  Fırça ilə Sil (AI Inpainting)",
                     disabled=not api_ok, key="btn_brush"):
            if not strokes or strokes.strip() in ("","[]"):
                st.warning("⚠️ Əvvəlcə şəkil üzərini boyayın!")
            else:
                mask = strokes_to_mask(strokes, iw, ih)
                if np.array(mask).sum()==0:
                    st.warning("⚠️ Maska boşdur — şəkili boyayın!")
                else:
                    pg = st.progress(0,"Göndərilir...")
                    try:
                        resp = requests.post(f"{API_URL}/brush-inpaint",
                            files={"image":("img.png",pil_to_bytes(bp),"image/png"),
                                   "mask": ("msk.png",pil_to_bytes(mask.convert("RGB")),"image/png")},
                            timeout=180,
                            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
                        pg.progress(70,"AI doldurur...")
                        d = resp.json()
                        if d.get("success"):
                            pg.progress(100,"Hazır! 🎉"); st.success("🎉 Tamamlandı!")
                            rb2 = base64.b64decode(d["image"])
                            c1,c2=st.columns(2)
                            with c1:
                                st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',unsafe_allow_html=True)
                                st.image(bp,use_container_width=True)
                            with c2:
                                st.markdown('<p style="text-align:center"><span class="badge b-enh">NƏTİCƏ</span></p>',unsafe_allow_html=True)
                                st.image(Image.open(io.BytesIO(rb2)),use_container_width=True)
                            st.download_button("⬇  Nəticəni Endir",rb2,
                                f"brush_{bf.name.rsplit('.',1)[0]}.png","image/png",use_container_width=True)
                        else:
                            pg.progress(100,"Xəta!"); st.error(f"❌ {d.get('error','Naməlum xəta')}")
                    except Exception as e:
                        st.error(f"❌ {e}")

# ── TAB 4: VİDEO ──────────────────────────────────────
with tab4:
    st.markdown('<div class="video-warn">⚠️ Video emalı bir neçə dəqiqə çəkə bilər.<br>Emal zamanı pəncərəni bağlamayın!</div>',unsafe_allow_html=True)
    vf = st.file_uploader("🎬  Video seçin",type=["mp4","mov","avi","mkv"],key="vid_up")
    if vf:
        st.video(vf)
        st.markdown(f'<div style="font-size:.76rem;color:#555;padding:.3rem 0">🎬 <span style="color:#bbb">{vf.name}</span> &nbsp; 📦 <span style="color:#bbb">{vf.size/1024/1024:.1f} MB</span></div>',unsafe_allow_html=True)
    if st.button("🎬  Video 4× Keyfiyyətini Artır",disabled=not(vf and api_ok),key="btn3"):
        vb=vf.read()
        p3=st.progress(0); m3=st.empty(); s3=[False]
        def _sp3():
            i=0; mv=["🎬 Kadrlar ayrılır...","⚡ GPU emal edir...","🔄 Video yığılır...","✨ Möcüzə..."]
            while not s3[0]:
                m3.markdown(f'<div class="spin-msg">{mv[i%len(mv)]}</div>',unsafe_allow_html=True)
                time.sleep(3); i+=1
        threading.Thread(target=_sp3,daemon=True).start()
        p3.progress(10,"Video göndərilir...")
        rb3,meta3,err3 = enhance_video_cached(vb,vf.name,API_URL)
        s3[0]=True; m3.empty()
        if err3: p3.progress(100,"Xəta!"); st.error(f"❌ {err3}")
        else:
            p3.progress(100,"Video hazır! 🎉"); st.balloons()
            st.success(f"🎉 {meta3.get('original','?')} → {meta3.get('enhanced','?')} | {meta3.get('frames','?')} kadr")
            st.download_button("⬇  4× Videonu Endir",rb3,
                f"enhanced_{vf.name.rsplit('.',1)[0]}.mp4","video/mp4",use_container_width=True)
