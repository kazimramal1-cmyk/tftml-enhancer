# ================================================================
#  frontend_streamlit.py — TFTML ENHANCER AI
#  RAMAL KAZIMZADE | SAM Inpainting + Şəkil + Video + Fırça
#  Python 3.14 uyğun — xarici canvas yoxdur
# ================================================================

import streamlit as st
import requests, base64, hashlib, io, time, threading, json
from PIL import Image, ImageEnhance, ImageDraw
import numpy as np

API_URL = "https://stacie-apertural-ardelia.ngrok-free.dev"
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
             radial-gradient(ellipse at 85% 20%,rgba(224,112,32,.10) 0%,transparent 55%);pointer-events:none}
.rk-brand{position:fixed;top:14px;left:18px;z-index:999;font-family:'DM Sans',sans-serif;
  font-size:.7rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#e07020;
  text-decoration:underline;text-underline-offset:4px;text-decoration-color:rgba(224,112,32,.4);transition:all .2s}
.rk-brand:hover{color:#f59030;text-shadow:0 0 12px rgba(224,112,32,.5)}
.logo-wrap{display:flex;justify-content:center;margin:1.5rem 0 .6rem}
.logo-img{width:110px;height:110px;border-radius:50%;object-fit:cover;animation:glowPulse 3s ease-in-out infinite}
@keyframes glowPulse{
  0%,100%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #1a6b2f,0 0 0 7px #0d0f0e,0 0 25px rgba(26,107,47,.55),0 0 55px rgba(224,112,32,.2)}
  50%{box-shadow:0 0 0 3px #0d0f0e,0 0 0 5px #e07020,0 0 0 7px #0d0f0e,0 0 30px rgba(224,112,32,.6),0 0 65px rgba(26,107,47,.25)}}
.main-title{font-family:'Playfair Display',serif;font-size:clamp(1.2rem,3vw,1.8rem);font-weight:700;
  text-align:center;color:#f0f0f0;letter-spacing:.05em;margin:.2rem 0 .1rem}
.main-title span{color:#e07020}
.sname{text-align:center;font-size:.82rem;color:#888;line-height:1.6;margin:.1rem 0}
.sname b{color:#bbb}
.ssub{text-align:center;font-size:.62rem;color:#444;letter-spacing:.15em;text-transform:uppercase;margin-bottom:1.4rem}
.status-ok{background:linear-gradient(135deg,#0a1f10,#0d2b15);border:1px solid #1a6b2f;
  border-radius:12px;padding:.55rem 1.2rem;font-size:.78rem;color:#4dff88;font-weight:600;margin-bottom:1rem}
.status-err{background:linear-gradient(135deg,#1f0a0a,#2b0d0d);border:1px solid #6b1a1a;
  border-radius:12px;padding:.55rem 1.2rem;font-size:.78rem;color:#ff6b6b;font-weight:600;margin-bottom:1rem}
[data-testid="stTabs"] [data-testid="stTab"]{background:transparent!important;border:none!important;
  color:#666!important;font-weight:600!important;font-size:.85rem!important;
  padding:.6rem 1.2rem!important;border-radius:10px 10px 0 0!important;transition:all .2s!important}
[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"]{
  background:linear-gradient(135deg,#1a6b2f,#0d3d1a)!important;color:#4dff88!important;
  border-bottom:2px solid #2d9e4a!important}
[data-testid="stTabContent"]{border:1.5px solid #1e251e!important;border-radius:0 16px 16px 16px!important;
  background:linear-gradient(145deg,#111311,#0f110f)!important;padding:1.5rem!important}
.card{background:linear-gradient(145deg,#131613,#111311);border-radius:16px;
  border:1.5px solid #1e251e;padding:1.5rem;margin-bottom:1.2rem;box-shadow:0 4px 30px rgba(0,0,0,.4)}
[data-testid="stFileUploader"]{border:2px dashed transparent!important;border-radius:16px!important;
  background:linear-gradient(#131613,#131613) padding-box,
             linear-gradient(135deg,#1a6b2f,#e07020,#1a6b2f) border-box!important;
  padding:1.2rem!important;transition:all .3s!important}
[data-testid="stFileUploader"] *{color:#888!important}
[data-testid="stFileUploader"] svg{fill:#e07020!important}
[data-testid="stFileUploader"] button{background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:8px!important}
.stButton>button{font-family:'DM Sans',sans-serif!important;font-weight:700!important;
  font-size:.95rem!important;background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:12px!important;
  padding:.85rem 2rem!important;width:100%!important;
  box-shadow:0 4px 20px rgba(26,107,47,.4)!important;transition:transform .2s,box-shadow .2s!important}
.stButton>button:hover{transform:scale(1.03) translateY(-2px)!important;box-shadow:0 8px 30px rgba(45,158,74,.55)!important}
.stButton>button:disabled{opacity:.35!important}
[data-testid="stSlider"]>div>div>div{background:#1a6b2f!important}
[data-testid="stSlider"] label{color:#aaa!important;font-size:.78rem!important}
.fx-panel{background:#0d1510;border:1px solid #1a3320;border-radius:12px;padding:1rem 1.2rem;margin:.5rem 0}
.fx-title{font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#4dff88;margin-bottom:.7rem}
.video-warn{background:linear-gradient(135deg,#1a1200,#2b1e00);border:1px solid #6b4e00;
  border-radius:14px;padding:1rem 1.4rem;font-size:.82rem;color:#ffcc44;font-weight:600;
  margin:1rem 0;line-height:1.7;text-align:center}
.sam-tip{background:linear-gradient(135deg,#0d1a2b,#0a1020);border:1px solid #1a3a6b;
  border-radius:12px;padding:.8rem 1.2rem;font-size:.78rem;color:#88ccff;line-height:1.8;margin:.6rem 0}
.brush-tip{background:linear-gradient(135deg,#1a0d2b,#100a20);border:1px solid #4a1a8b;
  border-radius:12px;padding:.8rem 1.2rem;font-size:.78rem;color:#cc88ff;line-height:1.8;margin:.6rem 0}
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
video{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}
[data-testid="stCaptionContainer"]{color:#555!important;font-size:.7rem!important}
</style>
<div class="rk-brand">RAMAL KAZIMZADE</div>
""", unsafe_allow_html=True)

# ── Köməkçi funksiyalar ──────────────────────────────────────────
@st.cache_data(show_spinner=False, max_entries=100)
def enhance_cached(img_bytes, fname, api_url):
    try:
        resp = requests.post(f"{api_url}/enhance",
            files={"image":(fname, img_bytes, "image/png")}, timeout=300,
            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
        try: data = resp.json()
        except: return None,None,{},f"Parse xətası ({resp.status_code}): {resp.text[:200]}"
        if data.get("success"): return base64.b64decode(data["image"]),data.get("type","image"),data,None
        return None,None,{},data.get("error",f"Xəta: {data}")
    except requests.exceptions.Timeout: return None,None,{},"Timeout xətası"
    except requests.exceptions.ConnectionError: return None,None,{},"Bağlantı xətası"
    except Exception as e: return None,None,{},f"{type(e).__name__}: {str(e)}"

@st.cache_data(show_spinner=False, max_entries=20)
def enhance_video_cached(vid_bytes, fname, api_url):
    try:
        ext  = fname.rsplit(".",1)[-1].lower() if "." in fname else "mp4"
        mime = {"mp4":"video/mp4","mov":"video/quicktime","avi":"video/x-msvideo"}.get(ext,"video/mp4")
        resp = requests.post(f"{api_url}/enhance-video",
            files={"video":(fname, vid_bytes, mime)}, timeout=600,
            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
        try: data = resp.json()
        except: return None,{},f"Parse xətası: {resp.text[:200]}"
        if data.get("success"): return base64.b64decode(data["image"]),data,None
        return None,{},data.get("error","Xəta")
    except Exception as e: return None,{},f"{type(e).__name__}: {str(e)}"

def check_api(url):
    try:
        r = requests.get(f"{url}/health", timeout=6,
            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
        return r.status_code == 200
    except: return False

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

MSGS = ["🚀 AI mühərriki işə düşür...","🧪 Piksellər bərpa olunur...",
        "✨ Möcüzə baş verir...","🎨 Rənglər canlanır...","⚡ GPU tam gücündə..."]

# ── SAM Klik Komponenti ──────────────────────────────────────────
def sam_canvas(img_pil, key="sam"):
    iw, ih = img_pil.size
    scale  = min(680/iw, 460/ih, 1.0)
    cw, ch = int(iw*scale), int(ih*scale)
    buf    = io.BytesIO()
    img_pil.resize((cw,ch),Image.LANCZOS).save(buf,format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    html = f"""
<div id="wrap_{key}" style="text-align:center">
<canvas id="c_{key}" width="{cw}" height="{ch}"
  style="border-radius:12px;border:2px solid #1e251e;cursor:crosshair;
         background:#0a0c0a;display:block;margin:0 auto;max-width:100%"></canvas>
</div>
<div style="display:flex;gap:.5rem;justify-content:center;margin:.7rem 0;flex-wrap:wrap">
  <button id="bAdd_{key}" onclick="mode_{key}='add';upd_{key}()"
    style="background:linear-gradient(135deg,#1a6b2f,#2d9e4a);border:none;color:#fff;
    padding:.4rem 1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">
    ➕ Sil (yaşıl)
  </button>
  <button id="bExc_{key}" onclick="mode_{key}='exc';upd_{key}()"
    style="background:linear-gradient(135deg,#6b1a1a,#9e2d2d);border:none;color:#fff;
    padding:.4rem 1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">
    ➖ Saxla (qırmızı)
  </button>
  <button onclick="clicks_{key}=[];redraw_{key}();upd_{key}()"
    style="background:#1a1a1a;border:1px solid #444;color:#aaa;
    padding:.4rem .8rem;border-radius:8px;cursor:pointer;font-size:.75rem">
    🗑️ Sıfırla
  </button>
</div>
<div id="inf_{key}" style="text-align:center;font-size:.72rem;color:#888;margin:.3rem 0;min-height:1.2em"></div>
<script>
(function(){{
  const canvas = document.getElementById('c_{key}');
  const ctx    = canvas.getContext('2d');
  const scX    = {iw}/{cw}, scY = {ih}/{ch};
  let clicks   = [];
  let mode     = 'add';
  const img = new Image();
  img.onload = () => redraw_{key}();
  img.src = 'data:image/png;base64,{img_b64}';
  window['clicks_{key}']  = clicks;
  window['mode_{key}']    = mode;
  window['redraw_{key}'] = function() {{
    ctx.clearRect(0,0,{cw},{ch});
    ctx.drawImage(img,0,0,{cw},{ch});
    clicks.forEach(([cx,cy,lbl]) => {{
      ctx.beginPath(); ctx.arc(cx,cy,9,0,Math.PI*2);
      ctx.fillStyle   = lbl===1?'rgba(45,200,80,.9)':'rgba(220,50,50,.9)';
      ctx.fill();
      ctx.strokeStyle = '#fff'; ctx.lineWidth=2; ctx.stroke();
      ctx.fillStyle='#fff'; ctx.font='bold 11px sans-serif';
      ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText(lbl===1?'✓':'✗',cx,cy);
    }});
  }};
  window['upd_{key}'] = function() {{
    const out = clicks.map(([x,y,l])=>({{x:Math.round(x*scX),y:Math.round(y*scY),label:l}}));
    const txt = JSON.stringify(out);
    const inp = document.querySelector('input[data-testid="stTextInput"][aria-label="clicks_{key}"]');
    if(inp){{ inp.value=txt; inp.dispatchEvent(new Event('input',{{bubbles:true}})); }}
    const inf = document.getElementById('inf_{key}');
    inf.textContent = clicks.length===0
      ? '🖱️ Şəkilə klikləyin — yaşıl nöqtə silinəcək obyekti göstərir'
      : clicks.length+' nöqtə seçildi';
    inf.style.color = clicks.length>0?'#4dff88':'#888';
    window['mode_{key}'] = mode;
  }};
  canvas.addEventListener('click',e=>{{
    const r=canvas.getBoundingClientRect();
    const x=(e.clientX-r.left)*(canvas.width/r.width);
    const y=(e.clientY-r.top )*(canvas.height/r.height);
    clicks.push([Math.round(x),Math.round(y),mode==='add'?1:0]);
    redraw_{key}(); upd_{key}();
  }});
  upd_{key}();
}})();
</script>"""
    st.components.v1.html(html, height=ch+110, scrolling=False)

# ── YENİ: Fırça Canvas Komponenti ───────────────────────────────
def brush_canvas(img_pil, key="brush"):
    iw, ih = img_pil.size
    scale  = min(680/iw, 500/ih, 1.0)
    cw, ch = int(iw*scale), int(ih*scale)
    buf    = io.BytesIO()
    img_pil.resize((cw,ch),Image.LANCZOS).save(buf,format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    html = f"""
<div style="text-align:center">
  <canvas id="bc_{key}" width="{cw}" height="{ch}"
    style="border-radius:12px;border:2px solid #4a1a8b;cursor:crosshair;
           display:block;margin:0 auto;max-width:100%;touch-action:none"></canvas>
</div>

<div style="display:flex;gap:.6rem;justify-content:center;margin:.8rem 0;flex-wrap:wrap;align-items:center">
  <button onclick="setTool_{key}('brush')"
    style="background:linear-gradient(135deg,#8b0000,#cc2200);border:none;color:#fff;
    padding:.45rem 1.1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">
    🖌️ Fırça (qırmızı)
  </button>
  <button onclick="setTool_{key}('erase')"
    style="background:linear-gradient(135deg,#1a3a6b,#2a5aab);border:none;color:#fff;
    padding:.45rem 1.1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">
    ⬜ Pozucu
  </button>
  <button onclick="clearAll_{key}()"
    style="background:#1a1a1a;border:1px solid #444;color:#aaa;
    padding:.45rem .9rem;border-radius:8px;cursor:pointer;font-size:.75rem">
    🗑️ Hamısını Sil
  </button>
  <label style="color:#aaa;font-size:.72rem;font-weight:600">
    Ölçü:
    <input type="range" id="sz_{key}" min="5" max="80" value="25"
      style="width:90px;vertical-align:middle;accent-color:#cc2200">
    <span id="szv_{key}">25</span>px
  </label>
</div>

<div id="binf_{key}" style="text-align:center;font-size:.72rem;color:#cc88ff;margin:.3rem 0">
  🖌️ Qırmızı fırça ilə silinəcək sahəni boyayın, sonra "Sil" düyməsini basın
</div>

<input type="hidden" id="bmask_{key}" value="">

<script>
(function(){{
  const canvas  = document.getElementById('bc_{key}');
  const ctx     = canvas.getContext('2d');
  const szEl    = document.getElementById('sz_{key}');
  const szvEl   = document.getElementById('szv_{key}');
  const inf     = document.getElementById('binf_{key}');
  const scX     = {iw}/{cw}, scY = {ih}/{ch};

  let tool      = 'brush';
  let painting  = false;
  let painted   = false;

  // Arxa şəkil
  const bg = new Image();
  bg.src   = 'data:image/png;base64,{img_b64}';
  bg.onload= () => ctx.drawImage(bg,0,0,{cw},{ch});

  // Fırça qatı
  const overlay = document.createElement('canvas');
  overlay.width={cw}; overlay.height={ch};
  const oc = overlay.getContext('2d');

  function redraw() {{
    ctx.clearRect(0,0,{cw},{ch});
    ctx.drawImage(bg,0,0,{cw},{ch});
    ctx.globalAlpha=0.55;
    ctx.drawImage(overlay,0,0);
    ctx.globalAlpha=1.0;
  }}

  function paint(e) {{
    if(!painting) return;
    const r   = canvas.getBoundingClientRect();
    const cex = e.touches?e.touches[0].clientX:e.clientX;
    const cey = e.touches?e.touches[0].clientY:e.clientY;
    const x   = (cex-r.left)*(canvas.width/r.width);
    const y   = (cey-r.top )*(canvas.height/r.height);
    const sz  = parseInt(szEl.value);
    oc.globalCompositeOperation = tool==='erase'?'destination-out':'source-over';
    oc.fillStyle='rgba(220,30,30,1)';
    oc.beginPath(); oc.arc(x,y,sz/2,0,Math.PI*2); oc.fill();
    redraw();
    painted=true;
    inf.textContent='✅ Rənglənmiş sahə hazırdır — aşağıdakı düyməni basın';
    inf.style.color='#ff8888';
    // maskanı yenilə
    document.getElementById('bmask_{key}').value = overlay.toDataURL('image/png');
  }}

  canvas.addEventListener('mousedown', e=>{{painting=true;paint(e)}});
  canvas.addEventListener('mousemove', paint);
  canvas.addEventListener('mouseup',   ()=>painting=false);
  canvas.addEventListener('mouseleave',()=>painting=false);
  canvas.addEventListener('touchstart',e=>{{painting=true;paint(e);e.preventDefault()}},{{passive:false}});
  canvas.addEventListener('touchmove', e=>{{paint(e);e.preventDefault()}},{{passive:false}});
  canvas.addEventListener('touchend',  ()=>painting=false);

  szEl.addEventListener('input',()=>szvEl.textContent=szEl.value);

  window['setTool_{key}'] = function(t) {{
    tool=t;
    inf.textContent = t==='brush'
      ? '🖌️ Fırça: silinəcək sahəni qırmızı boyayın'
      : '⬜ Pozucu: səhvən boyanan sahəni təmizləyin';
    inf.style.color = t==='brush'?'#ff8888':'#88aaff';
  }};

  window['clearAll_{key}'] = function() {{
    oc.clearRect(0,0,{cw},{ch});
    redraw(); painted=false;
    document.getElementById('bmask_{key}').value='';
    inf.textContent='🖌️ Qırmızı fırça ilə silinəcək sahəni boyayın';
    inf.style.color='#cc88ff';
  }};

  // Streamlit-ə mask göndər (hər saniyə yoxla)
  setInterval(()=>{{
    const v=document.getElementById('bmask_{key}').value;
    const inp=document.querySelector('textarea[aria-label="bmask_{key}"]') ||
              document.querySelector('input[aria-label="bmask_{key}"]');
    if(inp && v){{ inp.value=v; inp.dispatchEvent(new Event('input',{{bubbles:true}})); }}
  }},1000);
}})();
</script>"""
    st.components.v1.html(html, height=ch+140, scrolling=False)

# ── Header ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="logo-wrap">
  <img class="logo-img" src="data:image/jpeg;base64,{LOGO_B64}">
</div>
<div class="main-title">TFTML <span>ENHANCER</span> AI</div>
<div class="sname">K. Ağayev adına <b>Biləsuvar Şəhər</b><br>
Texniki Fənlər Təmayüllü İnternat Tipli Məktəb-Lisey</div>
<div class="ssub">AI Şəkil · SAM Inpainting · Fırça Silmə · Video | Real-ESRGAN 4×</div>
""", unsafe_allow_html=True)

api_ok = check_api(API_URL)
if api_ok:
    st.markdown('<div class="status-ok">✅ Colab Backend — Online · GPU Aktiv</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-err">⚠️ Colab Backend offline — Colab-ı işə salın</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🖼️  Şəkil Artır",
    "🧹  Ağıllı Sil (SAM)",
    "🖌️  Fırça ilə Sil",
    "🎬  Video Artır"
])

# ══════════════════════════════════════════════════════════════════
#  TAB 1 — ŞƏKİL
# ══════════════════════════════════════════════════════════════════
with tab1:
    uploaded = st.file_uploader("📸  Şəkil seçin",
        type=["jpg","jpeg","png","webp","bmp"], key="img_up")
    final_img = None

    if uploaded:
        orig_pil = Image.open(uploaded).convert("RGB")
        col_prev, col_fx = st.columns([3,2])
        with col_fx:
            st.markdown('<div class="fx-panel"><div class="fx-title">✂️ Kəsim</div>', unsafe_allow_html=True)
            w,h = orig_pil.size
            c1,c2 = st.columns(2)
            with c1:
                cl=st.number_input("Sol",   0,w-10,0,step=5,key="cl")
                ct=st.number_input("Yuxarı",0,h-10,0,step=5,key="ct")
            with c2:
                cr=st.number_input("Sağ",  10,w,w,step=5,key="cr")
                cb=st.number_input("Aşağı",10,h,h,step=5,key="cb")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="fx-panel"><div class="fx-title">🎨 Effektlər</div>', unsafe_allow_html=True)
            br=st.slider("☀️ Parlaqlıq",0.5,2.0,1.0,0.05,key="br")
            co=st.slider("🌗 Kontrast", 0.5,2.0,1.0,0.05,key="co")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="fx-panel"><div class="fx-title">🖼️ Arxa Fon</div>', unsafe_allow_html=True)
            bgc=st.selectbox("Fon",list(BACKGROUNDS.keys()),key="bgc")
            abg=st.checkbox("✅ Arxa fonu dəyişdir",key="abg")
            cbg=None
            if BACKGROUNDS[bgc]=="custom":
                cf=st.file_uploader("Öz fonunuzu yükləyin",type=["jpg","jpeg","png","webp"],key="cbg2",label_visibility="visible")
                if cf: cbg=Image.open(cf).convert("RGBA")
            else:
                try: st.image(fetch_bg(BACKGROUNDS[bgc]).convert("RGB").resize((220,124),Image.LANCZOS),use_container_width=True)
                except: pass
            st.markdown('</div>', unsafe_allow_html=True)

        with col_prev:
            edited = apply_effects(orig_pil.crop((cl,ct,cr,cb)),br,co)
            if abg:
                try:
                    bg_img = cbg if BACKGROUNDS[bgc]=="custom" else fetch_bg(BACKGROUNDS[bgc])
                    final_img = composite_bg(edited,bg_img) if bg_img else edited
                except Exception as e:
                    st.error(f"Fon xətası: {e}"); final_img=edited
            else:
                final_img=edited
            st.markdown('<p style="text-align:center;font-size:.68rem;color:#555;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.3rem">Önizləmə</p>',unsafe_allow_html=True)
            st.image(final_img,use_container_width=True)
            st.caption(f"📐 {final_img.width}×{final_img.height} px")

    btn1=st.button("✨  AI ilə 4× Keyfiyyəti Artır",
                   disabled=not(uploaded and api_ok and final_img is not None),key="btn1")
    if btn1 and final_img:
        sb=pil_to_bytes(final_img); hsh=hashlib.md5(sb).hexdigest()
        prog=st.progress(0); mb=st.empty(); stop=[False]
        def sp():
            i=0
            while not stop[0]: mb.markdown(f'<div class="spin-msg">{MSGS[i%len(MSGS)]}</div>',unsafe_allow_html=True); time.sleep(2); i+=1
        threading.Thread(target=sp,daemon=True).start()
        prog.progress(20,"Colab-a göndərilir...")
        rb,rt,meta,err=enhance_cached(sb,"image.png",API_URL)
        stop[0]=True; mb.empty(); prog.progress(100,"Hazır! 🎉")
        if err: st.error(f"❌ {err}")
        else:
            st.balloons()
            rp=Image.open(io.BytesIO(rb))
            st.markdown('<div class="card"><div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem"><span style="font-family:\'Playfair Display\',serif;font-size:.95rem;color:#eee">Nəticə</span><span class="b-4x">4× Enhanced</span></div>',unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1: st.markdown('<p style="text-align:center"><span class="badge b-orig">REDAKTƏLİ</span></p>',unsafe_allow_html=True); st.image(final_img,use_container_width=True)
            with c2: st.markdown('<p style="text-align:center"><span class="badge b-enh">4× AI</span></p>',unsafe_allow_html=True); st.image(rp,use_container_width=True)
            d1,d2=st.columns(2)
            with d1: st.download_button("⬇  Artırılmışı Endir",rb,f"enhanced_{uploaded.name.rsplit('.',1)[0]}.png","image/png",use_container_width=True)
            with d2: st.download_button("⬇  Redaktəlini Endir",sb,f"edited_{uploaded.name.rsplit('.',1)[0]}.png","image/png",use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  TAB 2 — SAM AĞILLI SİLMƏ
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""<div class="sam-tip">
    🧠 <b>SAM — Segment Anything Model</b><br>
    1️⃣ Şəkil yükləyin<br>
    2️⃣ <b style="color:#4dff88">➕ Sil</b> rejimini seçib silinəcək obyektə klikləyin (yaşıl nöqtə)<br>
    3️⃣ <b style="color:#ff8888">➖ Saxla</b> rejimini seçib saxlanılacaq hissəyə klikləyin (qırmızı nöqtə)<br>
    4️⃣ Koordinatları aşağıya kopyalayıb <b>"Ağıllı Sil"</b> düyməsini basın
    </div>""", unsafe_allow_html=True)

    inp_file = st.file_uploader("📸  Şəkil seçin (SAM üçün)",
        type=["jpg","jpeg","png","webp"], key="sam_up")

    if inp_file:
        inp_pil = Image.open(inp_file).convert("RGB")
        iw, ih  = inp_pil.size
        sam_canvas(inp_pil, key="sam1")
        clicks_json = st.text_input(
            "📍 Klik koordinatları (canvas-dan avtomatik):",
            placeholder='[{"x":200,"y":150,"label":1}]',
            key="sam_clicks", label_visibility="visible")
        st.caption("💡 Yuxarıdakı şəkilə kliklədikdən sonra bu sahəyə koordinatlar yazılır.")

        btn_sam = st.button("🧠  Ağıllı Sil (SAM + Inpainting)",
                            disabled=not api_ok, key="btn_sam")
        if btn_sam:
            clicks = []
            raw = clicks_json.strip()
            if raw:
                try: clicks = json.loads(raw)
                except: clicks = [{"x": iw//2, "y": ih//2, "label": 1}]
            else:
                st.warning("⚠️ Nöqtə seçilmədi. Şəkil mərkəzi istifadə edilir.")
                clicks = [{"x": iw//2, "y": ih//2, "label": 1}]

            orig_bytes = pil_to_bytes(inp_pil)
            prog_s = st.progress(0, "SAM-a göndərilir...")
            try:
                resp = requests.post(f"{API_URL}/sam-inpaint",
                    files={"image": ("image.png", orig_bytes, "image/png")},
                    data={"clicks": json.dumps(clicks)},
                    timeout=180,
                    headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
                prog_s.progress(70, "SAM segmentasiya edir...")
                data = resp.json()
                if data.get("success"):
                    prog_s.progress(100, "Hazır! 🎉")
                    st.success(f"🎉 Tamamlandı! {'SAM ✅' if data.get('sam_used') else 'Fallback mask'}")
                    c1,c2,c3 = st.columns(3)
                    with c1:
                        st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',unsafe_allow_html=True)
                        st.image(inp_pil, use_container_width=True)
                    with c2:
                        if data.get("mask"):
                            mask_img = Image.open(io.BytesIO(base64.b64decode(data["mask"])))
                            st.markdown('<p style="text-align:center"><span class="badge" style="background:#1a3a6b;color:#88ccff;border:1px solid #2a5aab">SAM MASK</span></p>',unsafe_allow_html=True)
                            st.image(mask_img, use_container_width=True)
                    with c3:
                        result_img = Image.open(io.BytesIO(base64.b64decode(data["image"])))
                        st.markdown('<p style="text-align:center"><span class="badge b-enh">NƏTİCƏ</span></p>',unsafe_allow_html=True)
                        st.image(result_img, use_container_width=True)
                    st.download_button("⬇  Nəticəni Endir",
                        base64.b64decode(data["image"]),
                        f"sam_{inp_file.name.rsplit('.',1)[0]}.png",
                        "image/png", use_container_width=True)
                else:
                    prog_s.progress(100,"Xəta!"); st.error(f"❌ {data.get('error','Naməlum xəta')}")
            except Exception as e:
                prog_s.progress(100,"Xəta!"); st.error(f"❌ {str(e)}")

# ══════════════════════════════════════════════════════════════════
#  TAB 3 — FIRÇA İLƏ SİLMƏ (YENİ)
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""<div class="brush-tip">
    🖌️ <b>Fırça ilə Silmə</b><br>
    1️⃣ Şəkil yükləyin<br>
    2️⃣ <b style="color:#ff8888">🖌️ Fırça</b> ilə silinəcək hissəni <b>qırmızı</b> rənglə boyayın<br>
    3️⃣ <b style="color:#88aaff">⬜ Pozucu</b> ilə səhvən boyanan yeri təmizləyin<br>
    4️⃣ <b>"Fırça ilə Sil"</b> düyməsini basın — AI arxasını doldurur
    </div>""", unsafe_allow_html=True)

    brush_file = st.file_uploader("📸  Şəkil seçin (Fırça üçün)",
        type=["jpg","jpeg","png","webp"], key="brush_up")

    if brush_file:
        brush_pil = Image.open(brush_file).convert("RGB")
        st.markdown('<p style="text-align:center;font-size:.72rem;color:#666;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.4rem">Fırça Canvas</p>',unsafe_allow_html=True)
        brush_canvas(brush_pil, key="br1")

        # Maska base64-ü saxlamaq üçün text_area (gizli)
        mask_data = st.text_area("bmask_br1", key="bmask_br1",
                                  label_visibility="hidden", height=1)

        btn_brush = st.button("🖌️  Fırça ilə Sil (AI Inpainting)",
                              disabled=not api_ok, key="btn_brush")

        if btn_brush:
            raw_mask = st.session_state.get("bmask_br1","").strip()
            if not raw_mask or not raw_mask.startswith("data:image"):
                st.warning("⚠️ Əvvəlcə şəkil üzərini qırmızı fırça ilə boyayın!")
            else:
                # base64 data URL-dən maska şəkilini çevir
                try:
                    header, b64part = raw_mask.split(",", 1)
                    mask_bytes = base64.b64decode(b64part)
                    orig_bytes = pil_to_bytes(brush_pil)

                    prog_b = st.progress(0, "Göndərilir...")
                    resp = requests.post(
                        f"{API_URL}/brush-inpaint",
                        files={
                            "image": ("image.png", orig_bytes, "image/png"),
                            "mask":  ("mask.png",  mask_bytes, "image/png"),
                        },
                        timeout=180,
                        headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"}
                    )
                    prog_b.progress(70, "AI doldurur...")
                    data = resp.json()

                    if data.get("success"):
                        prog_b.progress(100, "Hazır! 🎉")
                        st.success("🎉 Tamamlandı!")
                        result_bytes = base64.b64decode(data["image"])
                        result_pil   = Image.open(io.BytesIO(result_bytes))

                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',unsafe_allow_html=True)
                            st.image(brush_pil, use_container_width=True)
                        with c2:
                            st.markdown('<p style="text-align:center"><span class="badge b-enh">NƏTİCƏ</span></p>',unsafe_allow_html=True)
                            st.image(result_pil, use_container_width=True)

                        st.download_button("⬇  Nəticəni Endir",
                            result_bytes,
                            f"brush_{brush_file.name.rsplit('.',1)[0]}.png",
                            "image/png", use_container_width=True)
                    else:
                        prog_b.progress(100,"Xəta!")
                        st.error(f"❌ {data.get('error','Naməlum xəta')}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")

# ══════════════════════════════════════════════════════════════════
#  TAB 4 — VİDEO
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="video-warn">⚠️ Video emalı bir neçə dəqiqə çəkə bilər.<br>Emal zamanı pəncərəni bağlamayın!</div>', unsafe_allow_html=True)
    video_file = st.file_uploader("🎬  Video seçin",type=["mp4","mov","avi","mkv"],key="vid_up")
    if video_file:
        st.video(video_file)
        st.markdown(f'<div style="font-size:.76rem;color:#666;padding:.3rem 0">🎬 <span style="color:#bbb">{video_file.name}</span> &nbsp; 📦 <span style="color:#bbb">{video_file.size/1024/1024:.1f} MB</span></div>',unsafe_allow_html=True)
    btn3=st.button("🎬  Video 4× Keyfiyyətini Artır",disabled=not(video_file and api_ok),key="btn3")
    if btn3 and video_file:
        vb=video_file.read()
        st.markdown('<div class="video-warn">🔄 Video emal edilir — pəncərəni bağlamayın!</div>',unsafe_allow_html=True)
        p3=st.progress(0); m3=st.empty(); s3=[False]
        def sp3():
            i=0; mv=["🎬 Kadrlar ayrılır...","⚡ GPU emal edir...","🔄 Video yığılır...","✨ Möcüzə..."]
            while not s3[0]: m3.markdown(f'<div class="spin-msg">{mv[i%len(mv)]}</div>',unsafe_allow_html=True); time.sleep(3); i+=1
        threading.Thread(target=sp3,daemon=True).start()
        p3.progress(10,"Video göndərilir...")
        rb3,meta3,err3=enhance_video_cached(vb,video_file.name,API_URL)
        s3[0]=True; m3.empty()
        if err3: p3.progress(100,"Xəta!"); st.error(f"❌ {err3}")
        else:
            p3.progress(100,"Video hazır! 🎉"); st.balloons()
            st.success(f"🎉 {meta3.get('original','?')} → {meta3.get('enhanced','?')} | {meta3.get('frames','?')} kadr")
            st.download_button("⬇  4× Videonu Endir",rb3,f"enhanced_{video_file.name.rsplit('.',1)[0]}.mp4","video/mp4",use_container_width=True)
