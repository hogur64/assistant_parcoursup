import streamlit as st
from services.user_state import activate_premium_24h


# =======================================================
#   CONFIGURATION DE L'APPLICATION
# =======================================================
st.set_page_config(page_title="Assistant Parcoursup", layout="wide")


# =======================================================
#   ACTIVATION AUTOMATIQUE DU PASS 24H (Stripe Callback)
# =======================================================
if "premium" in st.query_params:
    activate_premium_24h()
    st.success("🎉 Pass 24h activé ! Vous avez maintenant accès illimité à toutes les fonctionnalités.")


# =======================================================
#   HEADER PRINCIPAL
# =======================================================
st.markdown("""
<div class='hero'>
    <h1>🎓 Assistant Intelligent Parcoursup & Dossiers Étudiants</h1>
    <p>Génère un PFM, une Lettre de Motivation ou un CV parfaitement optimisés — instantanément.</p>
</div>
""", unsafe_allow_html=True)


# =======================================================
#   NAVIGATION — MENU LATÉRAL
# =======================================================
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choisissez une section :",
    [
        "🏫 PFM",
        "✉️ Lettre de motivation",
        "📄 CV",
        "📘 Exemples",
        "ℹ️ À propos"
    ],
    label_visibility="visible"
)


# =======================================================
#   ROUTAGE – AFFICHAGE DES PAGES
# =======================================================
if page == "🏫 PFM":
    import my_pages.parcoursup_pfm as pfm
    pfm.render()

elif page == "✉️ Lettre de motivation":
    import my_pages.parcoursup_lm as lm
    lm.render()

elif page == "📄 CV":
    import my_pages.parcoursup_cv as cv
    cv.render()

elif page == "📘 Exemples":
    st.header("📘 Exemples de résultats")
    st.markdown("""
    Voici des exemples de documents générés par l'assistant :  

    ### 🏫 Exemple PFM  
    > *Un texte structuré de 150 mots présentant motivation, cohérence du parcours et projet professionnel.*

    ### ✉️ Exemple Lettre de Motivation  
    > *Une LM avec introduction, argumentation ciblée et conclusion impactante.*

    ### 📄 Exemple CV optimisé  
    > *CV réorganisé avec sections claires, compétences valorisées et structure professionnelle.*

    *(Tu pourras plus tard ajouter des images, PDF ou liens vers des exemples réels.)*
    """)

elif page == "ℹ️ À propos":
    st.header("ℹ️ À propos de l'Assistant IA")
    st.markdown("""
    ### 🤖 Qu’est-ce que cet outil ?
    Une plateforme intelligente pour aider les étudiants à créer :
    - des **PFM optimisés Parcoursup**
    - des **lettres de motivation professionnelles**
    - des **CV lisibles, cohérents et adaptés aux recruteurs**

    ### 💡 Fonctionnalités clés
    - IA spécialisée en admissions et recrutement  
    - Score de pertinence Parcoursup  
    - Diagnostics professionnels détaillés  
    - Téléchargement Word  
    - Système **1 essai gratuit** puis **Pass 24h illimité**

    ### 🧑‍💻 Développé par :
    **Hugo Roberts**, ingénieur et passionné par l'innovation.
    """)


# =======================================================
#   CHARGEMENT DU FICHIER CSS GLOBAL
# =======================================================
def load_css():
    try:
        with open("styles.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        st.warning("⚠ Impossible de charger styles.css")

load_css()
