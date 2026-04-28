# ================================================================
#  FRONTEND — Streamlit  |  "Arxa Fonu Sil" bölməsi
#  Mövcud frontend_streamlit.py faylınıza əlavə edin
#  və ya ayrıca test kimi işə salın.
# ================================================================

import streamlit as st
import requests
import base64
import io
from PIL import Image

# ── Öz API_URL-nizi buraya yazın ────────────────────────────────
API_URL = "https://COLAB_NGROK_URL_BURAYA"   # ← Colab-dan kopyalayın

HDR = {
    "bypass-tunnel-reminder": "yes",
    "ngrok-skip-browser-warning": "true",
}

# ================================================================
#  Yardımçı funksiya: backend-ə şəkil göndər, fonu sil
# ================================================================

def call_remove_bg(img_bytes: bytes, api_url: str) -> tuple[bytes | None, str | None]:
    """
    Backend-ə şəkil göndərir, uğurlu olarsa (bytes, None),
    xəta olarsa (None, "açıqlayıcı mesaj") qaytarır.
    """

    # ── 1) Backend-in işlədiyini yoxla ──────────────────────────
    try:
        health = requests.get(f"{api_url}/health", timeout=6, headers=HDR)
        health_data = health.json()

        if not health_data.get("rembg", False):
            # Backend açıqdır amma rembg quraşdırılmayıb
            detail = health_data.get("rembg_error") or ""
            return None, (
                "⚠️ Backend-də `rembg` kitabxanası tapılmadı.\n\n"
                "**Həll:** Google Colab-da aşağıdakı əmri icra edin:\n"
                "```\n!pip install rembg onnxruntime\n```\n"
                "Sonra Colab hücrəsini yenidən işə salın.\n\n"
                + (f"**Texniki səbəb:** `{detail}`" if detail else "")
            )

    except requests.exceptions.ConnectionError:
        return None, (
            "🔴 Colab backend-ə qoşulmaq mümkün olmadı.\n\n"
            "**Həll addımları:**\n"
            "1. Google Colab-ı açın\n"
            "2. Backend hücrəsini işə salın\n"
            "3. Ngrok URL-ni `API_URL` dəyişəninə yazın"
        )
    except requests.exceptions.Timeout:
        return None, (
            "⏱️ Backend 6 saniyə ərzində cavab vermədi.\n\n"
            "Colab-ın hələ işlədiyini yoxlayın."
        )
    except Exception as e:
        return None, f"🔴 Sağlamlıq yoxlaması xətası: `{type(e).__name__}: {e}`"

    # ── 2) Şəkli göndər ─────────────────────────────────────────
    try:
        resp = requests.post(
            f"{api_url}/remove-bg",
            files={"image": ("photo.png", img_bytes, "image/png")},
            timeout=120,   # böyük şəkillər üçün 2 dəq
            headers=HDR,
        )

    except requests.exceptions.Timeout:
        return None, (
            "⏱️ Sorğu 120 saniyə ərzində tamamlanmadı.\n\n"
            "Şəkil çox böyük ola bilər. Daha kiçik şəkil cəhd edin."
        )
    except requests.exceptions.ConnectionError:
        return None, "🔴 Sorğu zamanı bağlantı kəsildi. Colab-ı yoxlayın."
    except Exception as e:
        return None, f"🔴 Gözlənilməz şəbəkə xətası: `{type(e).__name__}: {e}`"

    # ── 3) Cavabı analiz et ──────────────────────────────────────
    try:
        data = resp.json()
    except Exception:
        return None, (
            f"🔴 Backend-dən JSON olmayan cavab gəldi (HTTP {resp.status_code}).\n\n"
            f"**Cavabın əvvəli:** `{resp.text[:300]}`"
        )

    if resp.status_code == 503:
        # rembg quraşdırılmayıb — backend-dən gələn açıqlayıcı mesaj
        return None, (
            f"⚠️ {data.get('error', 'Xidmət əlçatan deyil.')}\n\n"
            + (f"**Texniki səbəb:** `{data.get('detail', '')}`" if data.get('detail') else "")
        )

    if resp.status_code == 415:
        return None, f"📁 {data.get('error', 'Dəstəklənməyən fayl növü.')}"

    if resp.status_code == 400:
        return None, f"📋 {data.get('error', 'Yanlış sorğu.')}"

    if not data.get("success"):
        error_msg  = data.get("error",  "Naməlum xəta baş verdi.")
        error_detail = data.get("detail", "")
        full_msg = f"❌ {error_msg}"
        if error_detail:
            full_msg += f"\n\n**Texniki məlumat:**\n```\n{error_detail[:500]}\n```"
        return None, full_msg

    # ── 4) Base64 → bytes ────────────────────────────────────────
    try:
        result_bytes = base64.b64decode(data["image"])
        return result_bytes, None
    except Exception as e:
        return None, f"🔴 Şəkil dekodlanarkən xəta: `{e}`"


# ================================================================
#  Streamlit UI  —  "Arxa Fonu Sil" tab-ı
# ================================================================

st.set_page_config(page_title="Arxa Fon Sil", layout="wide")

st.title("🧹 Arxa Fonu Sil")
st.caption("Real-time `rembg` modeli ilə fon silmə")

# ── Fayl yükləmə ─────────────────────────────────────────────────
uploaded = st.file_uploader(
    "📸 Şəkil seçin (JPG, PNG, WEBP)",
    type=["jpg", "jpeg", "png", "webp"],
    key="rembg_upload",
)

if uploaded:
    original_pil = Image.open(uploaded).convert("RGB")

    # Önizləmə
    col_orig, col_result = st.columns(2)
    with col_orig:
        st.markdown("**🖼️ Orijinal**")
        st.image(original_pil, use_container_width=True)
        st.caption(f"📐 {original_pil.width}×{original_pil.height} px")

    # ── Düymə ────────────────────────────────────────────────────
    start = st.button("✂️  Arxa Fonu Sil", use_container_width=True, key="rembg_btn")

    if start:
        # Şəkli bytes-a çevir
        buf = io.BytesIO()
        original_pil.save(buf, format="PNG")
        img_bytes = buf.getvalue()

        with st.spinner("🔄 Arxa fon siliniyor..."):
            result_bytes, error_msg = call_remove_bg(img_bytes, API_URL)

        if error_msg:
            # ── Xəta: açıqlayıcı mesaj göstər ───────────────────
            st.error("**Xəta baş verdi**")
            st.markdown(error_msg)   # markdown formatında göstərir
            st.info(
                "💡 **İpucu:** Hər dəfə Colab yenidən başladıqda ngrok URL dəyişir. "
                "`API_URL` dəyişənini yeniləməyi unutmayın."
            )

        else:
            # ── Uğurlu nəticə ────────────────────────────────────
            result_pil = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

            with col_result:
                st.markdown("**✅ Fon Silinmiş (PNG)**")
                st.image(result_pil, use_container_width=True)
                st.caption(f"📐 {result_pil.width}×{result_pil.size[1]} px · RGBA")

            st.success("🎉 Arxa fon uğurla silindi!")

            # ── Endir düyməsi ────────────────────────────────────
            base_name = (uploaded.name or "image").rsplit(".", 1)[0]
            st.download_button(
                label="⬇️  Şəkli Endir (PNG, şəffaf fon)",
                data=result_bytes,
                file_name=f"{base_name}_no_bg.png",
                mime="image/png",
                use_container_width=True,
            )

else:
    st.info("👆 Yuxarıdan bir şəkil yükləyin.")
