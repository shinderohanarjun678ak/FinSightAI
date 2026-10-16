
import streamlit as st

from src.frontend.services.auth_api import (
    login_user,
    register_user,
)


def show_login_form():
    st.subheader("Welcome back")

    with st.form("login_form"):
        email = st.text_input("Email address")
        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Sign In",
            use_container_width=True,
        )

    if submitted:
        if not email.strip() or not password:
            st.error("Please enter your email and password.")
            return

        try:
            result = login_user(email, password)
            status_code = result["status_code"]
            data = result["data"]

            if status_code == 200:
                st.session_state["user"] = data["user"]
                st.success("Login successful!")
                st.rerun()

            elif status_code == 401:
                st.error("Invalid email or password.")

            else:
                st.error(data.get("detail", "Login failed."))

        except Exception:
            st.error(
                "Unable to connect to the backend. "
                "Please try again."
            )


def show_register_form():
    st.subheader("Create your account")

    with st.form("register_form"):
        email = st.text_input(
            "Email address",
            key="register_email",
        )
        password = st.text_input(
            "Password",
            type="password",
            key="register_password",
        )
        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            key="confirm_password",
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True,
        )

    if submitted:
        if not email.strip() or not password:
            st.error("Please complete all required fields.")
            return

        if len(password) < 8:
            st.error("Password must contain at least 8 characters.")
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        try:
            result = register_user(email, password)
            status_code = result["status_code"]
            data = result["data"]

            if status_code == 201:
                st.success(
                    "Account created successfully! "
                    "You can now sign in."
                )

            elif status_code == 409:
                st.error("This email is already registered.")

            elif status_code == 422:
                st.error(
                    "Please enter a valid email address."
                )

            else:
                st.error(
                    data.get("detail", "Registration failed.")
                )

        except Exception:
            st.error(
                "Unable to connect to the backend. "
                "Please try again."
            )
