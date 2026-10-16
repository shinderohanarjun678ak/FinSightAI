
import streamlit as st

from src.frontend.components.auth_form import (
    show_login_form,
    show_register_form,
)


def render_sign_in_page():
    st.set_page_config(
        page_title="Sign In | Finsight AI",
        page_icon="💰",
        layout="centered",
    )

    st.title("💰 Finsight AI")
    st.caption("Your intelligent personal finance companion")

    # Show the application if a user has logged in
    user = st.session_state.get("user")

    if user:
        st.success("You are logged in!")
        st.subheader("Welcome to Finsight AI")
        st.write(f"Email: {user['email']}")

        if st.button("Logout", use_container_width=True):
            st.session_state.pop("user", None)
            st.rerun()

        return

    # Login and registration tabs
    login_tab, register_tab = st.tabs(
        ["Sign In", "Create Account"]
    )

    with login_tab:
        show_login_form()

    with register_tab:
        show_register_form()


if __name__ == "__main__":
    render_sign_in_page()
