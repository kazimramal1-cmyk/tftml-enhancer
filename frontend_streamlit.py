# ================================================================
#  frontend_streamlit.py — TFTML ENHANCER AI
#  RAMAL KAZIMZADE
# ================================================================

import streamlit as st

# FIX 5: st_image monkey patch — image_to_url xətası aradan qaldırılır
try:
    from streamlit.elements import image as _st_img
    if not hasattr(_st_img, "image_to_url"):
        _st_img.image_to_url = lambda x, *a, **kw: x
except Exception:
    pass

import requests, base64, hashlib, io, time, threading, json
from PIL import Image, ImageEnhance, ImageDraw   # FIX 2: Pillow==9.5.0 lazımdır (requirements.txt-də)
import numpy as np

API_URL = "https://stacie-apertural-ardelia.ngrok-free.dev"

# FIX 4: Logo — düzgün ad və mərkəzdə göstərmə
# Faylın adı: logo_png.jpeg (uploads-da olan fayl)
import os as _os
_LOGO_PATH = "/mnt/user-data/uploads/logo_png.jpeg"
if _os.path.exists(_LOGO_PATH):
    with open(_LOGO_PATH, "rb") as _f:
        LOGO_B64 = base64.b64encode(_f.read()).decode()
else:
    # Fallback: boş şəffaf piksel
    LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

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
             radial-gradient(ellipse at 85% 20%,rgba(224,112,32,.10) 0%,transparent 55%);pointer-events:none}
.rk-brand{position:fixed;top:14px;left:18px;z-index:999;font-family:'DM Sans',sans-serif;
  font-size:.7rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#e07020;
  text-decoration:underline;text-underline-offset:4px;text-decoration-color:rgba(224,112,32,.4)}
.logo-wrap{display:flex;justify-content:center;align-items:center;margin:1.5rem 0 .6rem}
.logo-img{width:110px;height:110px;border-radius:50%;object-fit:cover;
  display:block;margin:0 auto;
  animation:glowPulse 3s ease-in-out infinite}
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
  padding:1.2rem!important}
[data-testid="stFileUploader"] *{color:#888!important}
[data-testid="stFileUploader"] svg{fill:#e07020!important}
[data-testid="stFileUploader"] button{background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:8px!important}
.stButton>button{font-family:'DM Sans',sans-serif!important;font-weight:700!important;
  font-size:.95rem!important;background:linear-gradient(135deg,#1a6b2f,#2d9e4a)!important;
  color:#fff!important;border:none!important;border-radius:12px!important;
  padding:.85rem 2rem!important;width:100%!important;
  box-shadow:0 4px 20px rgba(26,107,47,.4)!important;transition:transform .2s,box-shadow .2s!important}
.stButton>button:hover{transform:scale(1.03) translateY(-2px)!important}
.stButton>button:disabled{opacity:.35!important}
[data-testid="stSlider"]>div>div>div{background:#1a6b2f!important}
[data-testid="stSlider"] label{color:#aaa!important;font-size:.78rem!important}
.fx-panel{background:#0d1510;border:1px solid #1a3320;border-radius:12px;padding:1rem 1.2rem;margin:.5rem 0}
.fx-title{font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#4dff88;margin-bottom:.7rem}
.video-warn{background:linear-gradient(135deg,#1a1200,#2b1e00);border:1px solid #6b4e00;
  border-radius:14px;padding:1rem 1.4rem;font-size:.82rem;color:#ffcc44;font-weight:600;
  margin:1rem 0;line-height:1.7;text-align:center}
.brush-tip{background:linear-gradient(135deg,#1a0d2b,#100a20);border:1px solid #4a1a8b;
  border-radius:12px;padding:.8rem 1.2rem;font-size:.78rem;color:#cc88ff;line-height:1.8;margin:.6rem 0}
.sam-tip{background:linear-gradient(135deg,#0d1a2b,#0a1020);border:1px solid #1a3a6b;
  border-radius:12px;padding:.8rem 1.2rem;font-size:.78rem;color:#88ccff;line-height:1.8;margin:.6rem 0}
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
  color:#aaa!important}
.stDownloadButton>button:hover{border-color:#2d9e4a!important;color:#4dff88!important}
video{border-radius:12px!important;border:1.5px solid #1e251e!important;width:100%!important}
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

# ── SAM Canvas ───────────────────────────────────────
def sam_canvas(img_pil, key="sam"):
    iw, ih = img_pil.size
    scale  = min(680/iw, 460/ih, 1.0)
    cw, ch = int(iw*scale), int(ih*scale)
    buf    = io.BytesIO()
    img_pil.resize((cw,ch),Image.LANCZOS).save(buf,format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()
    html = f"""
<div style="text-align:center">
<canvas id="c_{key}" width="{cw}" height="{ch}"
  style="border-radius:12px;border:2px solid #1e251e;cursor:crosshair;
         background:#0a0c0a;display:block;margin:0 auto;max-width:100%"></canvas>
</div>
<div style="display:flex;gap:.5rem;justify-content:center;margin:.7rem 0;flex-wrap:wrap">
  <button onclick="mode_{key}='add'"
    style="background:linear-gradient(135deg,#1a6b2f,#2d9e4a);border:none;color:#fff;
    padding:.4rem 1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">➕ Sil (yaşıl)</button>
  <button onclick="mode_{key}='exc'"
    style="background:linear-gradient(135deg,#6b1a1a,#9e2d2d);border:none;color:#fff;
    padding:.4rem 1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">➖ Saxla (qırmızı)</button>
  <button onclick="clicks_{key}=[];redraw_{key}()"
    style="background:#1a1a1a;border:1px solid #444;color:#aaa;
    padding:.4rem .8rem;border-radius:8px;cursor:pointer;font-size:.75rem">🗑️ Sıfırla</button>
</div>
<div id="inf_{key}" style="text-align:center;font-size:.72rem;color:#888;margin:.3rem 0">
  🖱️ Şəkilə klikləyin
</div>
<script>
(function(){{
  const canvas=document.getElementById('c_{key}');
  const ctx=canvas.getContext('2d');
  const scX={iw}/{cw},scY={ih}/{ch};
  let clicks=[],mode='add';
  window['clicks_{key}']=clicks;
  window['mode_{key}']=mode;
  const img=new Image();
  img.onload=()=>redraw_{key}();
  img.src='data:image/png;base64,{img_b64}';
  window['redraw_{key}']=function(){{
    ctx.clearRect(0,0,{cw},{ch});ctx.drawImage(img,0,0,{cw},{ch});
    clicks.forEach(([cx,cy,l])=>{{
      ctx.beginPath();ctx.arc(cx,cy,9,0,Math.PI*2);
      ctx.fillStyle=l===1?'rgba(45,200,80,.9)':'rgba(220,50,50,.9)';ctx.fill();
      ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      ctx.fillStyle='#fff';ctx.font='bold 11px sans-serif';
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(l===1?'✓':'✗',cx,cy);
    }});
    const inf=document.getElementById('inf_{key}');
    inf.textContent=clicks.length===0?'🖱️ Şəkilə klikləyin':clicks.length+' nöqtə seçildi';
    inf.style.color=clicks.length>0?'#4dff88':'#888';
    const out=clicks.map(([x,y,l])=>({{x:Math.round(x*scX),y:Math.round(y*scY),label:l}}));
    const inp=document.querySelector('input[aria-label="clicks_{key}"]');
    if(inp){{inp.value=JSON.stringify(out);inp.dispatchEvent(new Event('input',{{bubbles:true}}));}}
  }};
  canvas.addEventListener('click',e=>{{
    const r=canvas.getBoundingClientRect();
    const x=(e.clientX-r.left)*(canvas.width/r.width);
    const y=(e.clientY-r.top)*(canvas.height/r.height);
    clicks.push([Math.round(x),Math.round(y),window['mode_{key}']==='add'?1:0]);
    redraw_{key}();
  }});
}})();
</script>"""
    st.components.v1.html(html, height=ch+110, scrolling=False)

# ── Fırça Canvas ─────────────────────────────────────
def brush_tool(img_pil, key="brush"):
    iw, ih = img_pil.size
    scale  = min(680/iw, 500/ih, 1.0)
    cw, ch = int(iw*scale), int(ih*scale)
    buf = io.BytesIO()
    img_pil.resize((cw,ch),Image.LANCZOS).save(buf,format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    html = f"""
<div style="text-align:center">
  <canvas id="cv_{key}" width="{cw}" height="{ch}"
    style="border-radius:12px;border:2px solid #4a1a8b;cursor:crosshair;
           display:block;margin:0 auto;max-width:100%;touch-action:none"></canvas>
</div>
<div style="display:flex;gap:.6rem;justify-content:center;margin:.8rem 0;flex-wrap:wrap;align-items:center">
  <button onclick="setTool_{key}('brush')"
    style="background:linear-gradient(135deg,#8b0000,#cc2200);border:none;color:#fff;
    padding:.45rem 1.1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">🖌️ Fırça</button>
  <button onclick="setTool_{key}('erase')"
    style="background:linear-gradient(135deg,#1a3a6b,#2a5aab);border:none;color:#fff;
    padding:.45rem 1.1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:700">⬜ Pozucu</button>
  <button onclick="clearAll_{key}()"
    style="background:#222;border:1px solid #444;color:#aaa;
    padding:.45rem .9rem;border-radius:8px;cursor:pointer;font-size:.75rem">🗑️ Hamısını Sil</button>
  <label style="color:#aaa;font-size:.72rem;font-weight:600">
    Ölçü:
    <input type="range" id="sz_{key}" min="5" max="100" value="30"
      style="width:80px;vertical-align:middle;accent-color:#cc2200"
      oninput="document.getElementById('szv_{key}').textContent=this.value">
    <span id="szv_{key}">30</span>px
  </label>
</div>
<div id="binf_{key}" style="text-align:center;font-size:.72rem;color:#cc88ff;margin:.4rem 0">
  🖌️ Qırmızı fırça ilə silinəcək hissəni boyayın
</div>
<script>
(function(){{
  const cv=document.getElementById('cv_{key}');
  const ctx=cv.getContext('2d');
  const ov=document.createElement('canvas');
  ov.width={cw};ov.height={ch};
  const oc=ov.getContext('2d');
  const scX={iw}/{cw},scY={ih}/{ch};
  let tool='brush',painting=false;
  const bg=new Image();
  bg.src='data:image/png;base64,{img_b64}';
  bg.onload=()=>draw();

  function draw(){{
    ctx.clearRect(0,0,{cw},{ch});
    ctx.drawImage(bg,0,0,{cw},{ch});
    ctx.globalAlpha=0.6;ctx.drawImage(ov,0,0);ctx.globalAlpha=1;
  }}

  function getPos(e){{
    const r=cv.getBoundingClientRect();
    const cx=e.touches?e.touches[0].clientX:e.clientX;
    const cy=e.touches?e.touches[0].clientY:e.clientY;
    return [(cx-r.left)*(cv.width/r.width),(cy-r.top)*(cv.height/r.height)];
  }}

  function paint(e){{
    if(!painting)return;
    const [x,y]=getPos(e);
    const sz=parseInt(document.getElementById('sz_{key}').value);
    oc.globalCompositeOperation=tool==='erase'?'destination-out':'source-over';
    oc.fillStyle='rgba(220,30,30,1)';
    oc.beginPath();oc.arc(x,y,sz/2,0,Math.PI*2);oc.fill();
    draw();
    // stroku saxla
    const sx=Math.round(x*scX),sy=Math.round(y*scY),sr=Math.round(sz/2*scX);
    const inp=document.querySelector('input[aria-label="strokes_{key}"]');
    if(inp){{
      let arr=[];try{{arr=JSON.parse(inp.value||'[]')}}catch{{}}
      arr.push({{x:sx,y:sy,r:Math.max(sr,3),t:tool}});
      inp.value=JSON.stringify(arr);
      inp.dispatchEvent(new Event('input',{{bubbles:true}}));
    }}
    document.getElementById('binf_{key}').textContent='✅ Rəngləndi — "Fırça ilə Sil" düyməsini basın';
    document.getElementById('binf_{key}').style.color='#ff8888';
  }}

  cv.addEventListener('mousedown',e=>{{painting=true;paint(e)}});
  cv.addEventListener('mousemove',paint);
  cv.addEventListener('mouseup',()=>painting=false);
  cv.addEventListener('mouseleave',()=>painting=false);
  cv.addEventListener('touchstart',e=>{{painting=true;paint(e);e.preventDefault()}},{{passive:false}});
  cv.addEventListener('touchmove',e=>{{paint(e);e.preventDefault()}},{{passive:false}});
  cv.addEventListener('touchend',()=>painting=false);

  window['setTool_{key}']=function(t){{
    tool=t;
    const inf=document.getElementById('binf_{key}');
    inf.textContent=t==='brush'?'🖌️ Fırça aktiv':'⬜ Pozucu aktiv';
    inf.style.color=t==='brush'?'#ff8888':'#88aaff';
  }};
  window['clearAll_{key}']=function(){{
    oc.clearRect(0,0,{cw},{ch});draw();
    const inp=document.querySelector('input[aria-label="strokes_{key}"]');
    if(inp){{inp.value='[]';inp.dispatchEvent(new Event('input',{{bubbles:true}}));}}
    document.getElementById('binf_{key}').textContent='🖌️ Qırmızı fırça ilə silinəcək hissəni boyayın';
    document.getElementById('binf_{key}').style.color='#cc88ff';
  }};
}})();
</script>"""
    st.components.v1.html(html, height=ch+160, scrolling=False)

    strokes_raw = st.text_input(
        "🖊️ Fırça məlumatı:",
        key=f"strokes_{key}",
        label_visibility="visible"
    )
    st.caption("💡 Şəkili boyayandan sonra bu sahə dolur — sonra 'Sil' düyməsini basın.")
    return strokes_raw

def strokes_to_mask(strokes_raw, iw, ih):
    mask = Image.new("L", (iw, ih), 0)
    draw = ImageDraw.Draw(mask)
    try:
        for s in json.loads(strokes_raw or "[]"):
            x,y,r = s["x"],s["y"],s.get("r",10)
            if s.get("t","brush")=="erase":
                draw.ellipse([x-r,y-r,x+r,y+r], fill=0)
            else:
                draw.ellipse([x-r,y-r,x+r,y+r], fill=255)
    except: pass
    return mask

# ── Header ───────────────────────────────────────────
# FIX 4: Logo mərkəzdə, düzgün ad ilə
st.markdown(f"""
<div class="logo-wrap">
  <img class="logo-img" src="data:image/jpeg;base64,{LOGO_B64}" alt="Logo">
</div>
<div class="main-title">TFTML <span>ENHANCER</span> AI</div>
<div class="sname">K. Ağayev adına <b>Biləsuvar Şəhər</b><br>
Texniki Fənlər Təmayüllü İnternat Tipli Məktəb-Lisey</div>
<div class="ssub">AI Şəkil · SAM · Fırça Silmə · Video | Real-ESRGAN 4×</div>
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

# ══════════════════════════════════════════════════════
#  TAB 1 — ŞƏKİL
# ══════════════════════════════════════════════════════
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
            st.image(final_img,use_container_width=True)
            st.caption(f"📐 {final_img.width}×{final_img.height} px")

    btn1=st.button("✨  AI ilə 4× Keyfiyyəti Artır",
                   disabled=not(uploaded and api_ok and final_img is not None),key="btn1")
    if btn1 and final_img:
        sb=pil_to_bytes(final_img)
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
            c1,c2=st.columns(2)
            with c1: st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',unsafe_allow_html=True); st.image(final_img,use_container_width=True)
            with c2: st.markdown('<p style="text-align:center"><span class="badge b-enh">4× AI</span></p>',unsafe_allow_html=True); st.image(rp,use_container_width=True)
            d1,d2=st.columns(2)
            with d1: st.download_button("⬇  Artırılmışı Endir",rb,f"enhanced_{uploaded.name.rsplit('.',1)[0]}.png","image/png",use_container_width=True)
            with d2: st.download_button("⬇  Redaktəlini Endir",sb,f"edited_{uploaded.name.rsplit('.',1)[0]}.png","image/png",use_container_width=True)

# ══════════════════════════════════════════════════════
#  TAB 2 — SAM
# ══════════════════════════════════════════════════════
with tab2:
    st.markdown("""<div class="sam-tip">
    🧠 <b>SAM — Segment Anything Model</b><br>
    1️⃣ Şəkil yükləyin &nbsp; 2️⃣ Silinəcək yerə <b style="color:#4dff88">yaşıl</b> klikləyin<br>
    3️⃣ Saxlanılacaq yerə <b style="color:#ff8888">qırmızı</b> klikləyin &nbsp; 4️⃣ "Ağıllı Sil" basın
    </div>""", unsafe_allow_html=True)

    inp_file = st.file_uploader("📸  Şəkil seçin (SAM üçün)",
        type=["jpg","jpeg","png","webp"], key="sam_up")
    if inp_file:
        inp_pil = Image.open(inp_file).convert("RGB")
        iw, ih  = inp_pil.size
        sam_canvas(inp_pil, key="sam1")
        clicks_json = st.text_input(
            "📍 Klik koordinatları:",
            placeholder='[{"x":200,"y":150,"label":1}]',
            key="sam_clicks", label_visibility="visible")
        st.caption("💡 Şəkilə kliklədikdən sonra bu sahə avtomatik dolur.")

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
                prog_s.progress(70, "SAM işləyir...")
                data = resp.json()
                if data.get("success"):
                    prog_s.progress(100, "Hazır! 🎉")
                    st.success(f"🎉 Tamamlandı! {'SAM ✅' if data.get('sam_used') else 'Fallback'}")
                    c1,c2,c3 = st.columns(3)
                    with c1:
                        st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',unsafe_allow_html=True)
                        st.image(inp_pil, use_container_width=True)
                    with c2:
                        if data.get("mask"):
                            st.markdown('<p style="text-align:center"><span class="badge" style="background:#1a3a6b;color:#88ccff;border:1px solid #2a5aab">SAM MASK</span></p>',unsafe_allow_html=True)
                            st.image(Image.open(io.BytesIO(base64.b64decode(data["mask"]))), use_container_width=True)
                    with c3:
                        st.markdown('<p style="text-align:center"><span class="badge b-enh">NƏTİCƏ</span></p>',unsafe_allow_html=True)
                        st.image(Image.open(io.BytesIO(base64.b64decode(data["image"]))), use_container_width=True)
                    st.download_button("⬇  Nəticəni Endir",
                        base64.b64decode(data["image"]),
                        f"sam_{inp_file.name.rsplit('.',1)[0]}.png",
                        "image/png", use_container_width=True)
                else:
                    prog_s.progress(100,"Xəta!"); st.error(f"❌ {data.get('error','Naməlum xəta')}")
            except Exception as e:
                st.error(f"❌ {str(e)}")

# ══════════════════════════════════════════════════════
#  TAB 3 — FIRÇA İLƏ SİLMƏ
# ══════════════════════════════════════════════════════
with tab3:
    st.markdown("""<div class="brush-tip">
    🖌️ <b>Fırça ilə Silmə:</b><br>
    1️⃣ Şəkil yükləyin &nbsp; 2️⃣ Qırmızı fırça ilə silinəcək hissəni boyayın<br>
    3️⃣ Pozucu ilə səhvi düzəldin &nbsp; 4️⃣ "Fırça ilə Sil" basın — AI arxasını doldurur
    </div>""", unsafe_allow_html=True)

    brush_file = st.file_uploader("📸  Şəkil seçin",
        type=["jpg","jpeg","png","webp"], key="brush_up")
    if brush_file:
        brush_pil = Image.open(brush_file).convert("RGB")
        iw, ih    = brush_pil.size
        strokes_raw = brush_tool(brush_pil, key="br1")

        btn_brush = st.button("🖌️  Fırça ilə Sil (AI Inpainting)",
                              disabled=not api_ok, key="btn_brush")
        if btn_brush:
            if not strokes_raw or strokes_raw.strip() in ("","[]"):
                st.warning("⚠️ Əvvəlcə şəkil üzərini boyayın!")
            else:
                mask = strokes_to_mask(strokes_raw, iw, ih)
                if np.array(mask).sum() == 0:
                    st.warning("⚠️ Maska boşdur — şəkili boyayın!")
                else:
                    orig_bytes = pil_to_bytes(brush_pil)
                    mask_bytes = pil_to_bytes(mask.convert("RGB"))
                    prog_b = st.progress(0, "Göndərilir...")
                    try:
                        resp = requests.post(f"{API_URL}/brush-inpaint",
                            files={"image":("image.png",orig_bytes,"image/png"),
                                   "mask": ("mask.png", mask_bytes,"image/png")},
                            timeout=180,
                            headers={"bypass-tunnel-reminder":"yes","ngrok-skip-browser-warning":"true"})
                        prog_b.progress(70, "AI doldurur...")
                        data = resp.json()
                        if data.get("success"):
                            prog_b.progress(100,"Hazır! 🎉"); st.success("🎉 Tamamlandı!")
                            result_bytes = base64.b64decode(data["image"])
                            c1,c2 = st.columns(2)
                            with c1:
                                st.markdown('<p style="text-align:center"><span class="badge b-orig">ORİGİNAL</span></p>',unsafe_allow_html=True)
                                st.image(brush_pil, use_container_width=True)
                            with c2:
                                st.markdown('<p style="text-align:center"><span class="badge b-enh">NƏTİCƏ</span></p>',unsafe_allow_html=True)
                                st.image(Image.open(io.BytesIO(result_bytes)), use_container_width=True)
                            st.download_button("⬇  Nəticəni Endir", result_bytes,
                                f"brush_{brush_file.name.rsplit('.',1)[0]}.png",
                                "image/png", use_container_width=True)
                        else:
                            prog_b.progress(100,"Xəta!"); st.error(f"❌ {data.get('error','Naməlum xəta')}")
                    except Exception as e:
                        st.error(f"❌ {str(e)}")

# ══════════════════════════════════════════════════════
#  TAB 4 — VİDEO
# ══════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="video-warn">⚠️ Video emalı bir neçə dəqiqə çəkə bilər.<br>Emal zamanı pəncərəni bağlamayın!</div>', unsafe_allow_html=True)
    video_file = st.file_uploader("🎬  Video seçin",type=["mp4","mov","avi","mkv"],key="vid_up")
    if video_file:
        st.video(video_file)
        st.markdown(f'<div style="font-size:.76rem;color:#666;padding:.3rem 0">🎬 <span style="color:#bbb">{video_file.name}</span> &nbsp; 📦 <span style="color:#bbb">{video_file.size/1024/1024:.1f} MB</span></div>',unsafe_allow_html=True)
    btn3=st.button("🎬  Video 4× Keyfiyyətini Artır",disabled=not(video_file and api_ok),key="btn3")
    if btn3 and video_file:
        vb=video_file.read()
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
