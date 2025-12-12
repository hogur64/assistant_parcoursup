import streamlit as st
from services.openai_client import call_openai
from services.extractors import extract_from_pdf, extract_from_docx
from services.exporters import build_docx_from_text
from utils.prompts import LM_FORMATION_PROMPT, LM_OPTIMIZER_PROMPT
from services.user_state import get_user_state, is_premium
from services.payment import create_checkout_session


def render():
    st.header("✉️ Lettre de Motivation – Parcoursup")

    state = get_user_state()
    MODULE = "lm"

    # --------------------------
    # PAYWALL LM
    # --------------------------
    if not is_premium() and state["tries"][MODULE]:
        st.warning("🚫 Votre essai gratuit est utilisé. Le Pass 24h (2,50€) débloque un accès illimité.")

        if st.button("💳 Activer le Pass 24h (2,50€)"):
            checkout_url = create_checkout_session(
                success_url="https://ton-app.streamlit.app/?premium=true",
                cancel_url="https://ton-app.streamlit.app/?cancel=true"
            )
            st.markdown(f"[👉 Procéder au paiement]({checkout_url})")
        return

    # --------------------------
    # CRÉATION LM
    # --------------------------
    st.subheader("✏️ 1. Créer une Lettre de Motivation")

    formation = st.text_input("Formation visée")
    motivation = st.text_area("Pourquoi cette formation ?", height=100)
    compet_sco = st.text_area("Compétences scolaires", height=80)
    compet_pers = st.text_area("Compétences personnelles", height=80)
    experiences = st.text_area("Expériences / projets", height=120)
    apport = st.text_area("Ce que vous pouvez apporter", height=80)
    projet = st.text_area("Projet professionnel", height=80)

    if st.button("✨ Générer la LM"):
        if not formation or not motivation:
            st.warning("Indique formation + motivation.")
            return

        prompt = LM_FORMATION_PROMPT.format(
            formation=formation,
            motivation=motivation,
            competences_scolaires=compet_sco,
            competences_perso=compet_pers,
            experiences=experiences,
            apport=apport,
            projet_pro=projet,
        )

        contenu = call_openai(prompt)
        st.text_area("✉️ LM générée :", contenu, height=260)

        if not contenu.startswith("❌"):
            if not is_premium():
                state["tries"][MODULE] = True

            st.download_button("📥 Télécharger (.docx)", build_docx_from_text(contenu), "LM.docx")

    # --------------------------
    # OPTIMISATION LM IMPORTÉE
    # --------------------------
    st.markdown("---")
    st.subheader("📂 2. Optimiser une LM existante")

    uploaded = st.file_uploader("Importer LM (PDF ou DOCX)", type=["pdf", "docx"])
    texte = ""

    if uploaded:
        texte = extract_from_pdf(uploaded) if uploaded.name.endswith(".pdf") \
               else extract_from_docx(uploaded)

        st.text_area("Texte extrait :", texte, height=200)

    texte_opt = st.text_area("Texte à optimiser :", texte, height=200)

    if st.button("🚀 Optimiser ma LM"):

        if not texte_opt.strip():
            st.warning("Ajoute ou importe une LM.")
            return

        if not is_premium():
            state["tries"][MODULE] = True

        result = call_openai(
            LM_OPTIMIZER_PROMPT.format(
                texte_initial=texte_opt,
                formation_ou_poste=formation,
                competences=compet_sco,
                experiences=experiences
            )
        )

        st.text_area("✨ LM optimisée :", result, height=250)

        if not result.startswith("❌"):
            st.download_button("📥 Télécharger (.docx)", build_docx_from_text(result), "LM_Optimisee.docx")
