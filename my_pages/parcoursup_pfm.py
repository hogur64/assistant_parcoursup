import streamlit as st
from services.openai_client import call_openai
from services.exporters import build_docx_from_text, build_pdf_from_text
from services.extractors import extract_from_pdf, extract_from_docx
from utils.prompts import PFM_GENERATOR_PROMPT, PFM_OPTIMIZER_PROMPT
from services.user_state import get_user_state, is_premium
from services.payment import create_checkout_session


def render():
    st.header("🏫 Projet de Formation Motivé (PFM)")

    state = get_user_state()
    MODULE = "pfm"

    # --------------------------
    # PAYWALL PFM
    # --------------------------
    if not is_premium() and state["tries"][MODULE]:
        st.warning("🚫 Votre essai gratuit PFM est utilisé. Le Pass 24h (2,50€) débloque un accès illimité.")

        if st.button("💳 Activer le Pass 24h (2,50€)"):
            checkout_url = create_checkout_session(
                success_url="https://ton-app.streamlit.app/?premium=true",
                cancel_url="https://ton-app.streamlit.app/?cancel=true"
            )
            st.markdown(f"[👉 Procéder au paiement]({checkout_url})")
        return

    # --------------------------
    # CRÉATION PFM
    # --------------------------
    st.subheader("✏️ 1. Créer un PFM")

    formation = st.text_input("Formation visée")
    motivation = st.text_area("Pourquoi cette formation ?", height=100)
    specialites = st.text_input("Spécialités / matières")
    compet_sco = st.text_area("Compétences scolaires", height=80)
    compet_pers = st.text_area("Compétences personnelles", height=80)
    experiences = st.text_area("Expériences", height=120)
    objectif = st.text_area("Projet professionnel", height=80)

    if st.button("✨ Générer mon PFM"):
        if not formation or not motivation:
            st.warning("Merci d’indiquer la formation + motivation.")
            return

        prompt = PFM_GENERATOR_PROMPT.format(
            formation=formation,
            motivation=motivation,
            specialites=specialites or "Non précisé",
            competences_scolaires=compet_sco or "Non précisées",
            competences_perso=compet_pers or "Non précisées",
            experiences=experiences or "Non précisées",
            objectif_pro=objectif or "Non précisé",
        )

        result = call_openai(prompt)
        st.text_area("📝 PFM généré :", result, height=220)

        if not result.startswith("❌"):
            if not is_premium():
                state["tries"][MODULE] = True

            st.download_button("📥 Télécharger (.docx)", build_docx_from_text(result), "PFM.docx")
            st.download_button("📄 Télécharger (.pdf)", build_pdf_from_text(result), "PFM.pdf")

    # --------------------------
    # IMPORT + OPTIMISATION
    # --------------------------
    st.markdown("---")
    st.subheader("📂 2. Importer un PFM et l’optimiser")

    uploaded = st.file_uploader("Importer fichier (PDF / DOCX)", type=["pdf", "docx"])
    texte = ""

    if uploaded:
        try:
            if uploaded.name.endswith(".pdf"):
                texte = extract_from_pdf(uploaded)
            else:
                texte = extract_from_docx(uploaded)
        except:
            st.error("Impossible de lire le fichier.")
            return

        st.text_area("Texte extrait :", texte, height=200)

    texte_opt = st.text_area("Texte à optimiser :", texte, height=200)

    if st.button("🚀 Optimiser mon PFM"):
        if not texte_opt.strip():
            st.warning("Ajoutez ou importez un texte.")
            return

        if not is_premium():
            state["tries"][MODULE] = True

        result = call_openai(
            PFM_OPTIMIZER_PROMPT.format(
                texte_initial=texte_opt,
                formation="",
                experiences="",
                competences=""
            )
        )

        st.text_area("✨ PFM optimisé :", result, height=250)

        if not result.startswith("❌"):
            st.download_button("📥 Télécharger (.docx)", build_docx_from_text(result), "PFM_Optimise.docx")
            st.download_button("📄 Télécharger (.pdf)", build_pdf_from_text(result), "PFM_Optimise.pdf")
