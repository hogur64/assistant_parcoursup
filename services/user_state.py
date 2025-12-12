import streamlit as st
import time

def get_user_state():
    if "premium_until" not in st.session_state:
        st.session_state["premium_until"] = 0

    if "tries" not in st.session_state:
        st.session_state["tries"] = {
            "pfm": False,
            "lm": False,
            "cv": False
        }

    return st.session_state


def is_premium():
    return time.time() < st.session_state["premium_until"]


def activate_premium_24h():
    st.session_state["premium_until"] = time.time() + 24 * 3600
