import streamlit as st
from services.extractors import extract_from_pdf, extract_from_docx
from services.openai_client import call_openai
from services.exporters import build_docx_from_text
from utils.prompts import CV_OPTIMIZER_PROMPT
from services.user_state import get_user_state, is_premium
from services.payment import create_checkout_session


def render():
    st.header("📄 Optimiser mon CV (PDF / DOCX)")

    state = get_user_state()
    MODULE = "cv"

    # --------------------------
    # PAYWALL CV
    # --------------------------
    if not is_premium() and state["tries"][MODULE]:
        st.warning("🚫 Votre essai gratuit a été utilisé. Le Pass 24h (2,50€) débloque un accès illimité.")

        if st.button("💳 Activer le Pass 24h (2,50€)"):
            checkout_url = create_checkout_session(
                success_url="https://ton-app.streamlit.app/?premium=true",
                cancel_url="https://ton-app.streamlit.app/?cancel=true"
            )
            st.markdown(f"[👉 Procéder au paiement]({checkout_url})")
        return

    # --------------------------
    # IMPORT DU CV
    # --------------------------
    st.subheader("📥 Importer un CV (PDF ou DOCX)")
    fichier = st.file_uploader("Dépose ton CV :", type=["pdf", "docx"])
    texte = ""

    if fichier:
        try:
            if fichier.name.lower().endswith(".pdf"):
                texte = extract_from_pdf(fichier)
            else:
                texte = extract_from_docx(fichier)
        except Exception as e:
            st.error(f"❌ Impossible de lire le fichier : {e}")
            return

        st.text_area("📄 Texte extrait :", texte, height=250)

    texte_opt = st.text_area("Texte à optimiser :", texte, height=250)

    # --------------------------
    # OPTIMISATION IA
    # --------------------------
    if st.button("✨ Optimiser mon CV"):
        if not texte_opt.strip():
            st.warning("Veuillez d'abord importer un CV.")
            return

        if not is_premium():
            state["tries"][MODULE] = True  # essai consommé

        result = call_openai(CV_OPTIMIZER_PROMPT.format(cv_brut=texte_opt))

        st.text_area("📝 CV optimisé :", result, height=300)

        if not result.startswith("❌"):
            st.download_button(
                "📥 Télécharger le CV optimisé (.docx)",
                build_docx_from_text(result),
                file_name="CV_Optimise.docx"
            )
