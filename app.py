import streamlit as st
from helperfunctions import *
from employee import employee_dashboard
from manager import manager_dashboard
from database import init_db
import time
import random
import secrets
import string

def main():
    st.set_page_config(page_title="HR Management System", layout="wide")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_type = None

    init_db()
    companies = get_companies()
    
    with st.container(border=False):
        col1, col2, col3 = st.columns([.5, 3, .5])
        with col1:
            st.write("")
        with col2:
            if not st.session_state.logged_in:
                st.markdown('<h1 class="auth-title">HR Management System</h1>', unsafe_allow_html=True)

                tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Admins"])

                with tab1:
                    user_type = st.selectbox("I am a", ["Employee", "HR Manager"], key="login_user_type")
                    company_names = [company[1] for company in companies]
                    selected_company = st.selectbox("Select Company", company_names, key="login_company")
                    username = st.text_input("Username", key="login_username")
                    password = st.text_input("Password", type="password", key="login_password")
                    otp = st.text_input("Enter OTP", key="login_otp")

                    if st.button("Log In"):
                        if user_type == "HR Manager":
                            otp_secret = login_hr(username, password)
                        else:
                            otp_secret = login_user(username, password)

                        if otp_secret and verify_otp(otp_secret, otp):
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.user_type = user_type
                            st.success(f"Logged in as {user_type}: {username}")
                            st.experimental_rerun()
                        else:
                            st.error("Incorrect username, password, or OTP")

                with tab2:
                    user_type = st.selectbox("I want to register as", ["Employee", "HR Manager"], key="signup_user_type")
                    if user_type == "HR Manager":
                        company_option = st.radio("Company", ["Existing Company", "New Company"])
                        if company_option == "Existing Company":
                            if companies:
                                company_names = [company[1] for company in companies]
                                selected_company = st.selectbox("Select Company", company_names, key="signup_company")
                                company_id = next(company[0] for company in companies if company[1] == selected_company)
                            else:
                                st.error("No existing companies. Please register a new company.")
                                company_option = "New Company"
                        if company_option == "New Company":
                            new_company_name = st.text_input("New Company Name")
                    else:
                        if companies:
                            company_names = [company[1] for company in companies]
                            selected_company = st.selectbox("Select Company", company_names, key="signup_company")
                            company_id = next(company[0] for company in companies if company[1] == selected_company)
                        else:
                            st.error("No companies available. Please contact an HR Manager to create a company first.")
                            return
                    
                    username = st.text_input("New Username", key="signup_username")
                    if user_type == "HR Manager":
                        email = st.text_input("HR Email", key="signup_hr_email")
                    else:
                        email = st.text_input("Email", key="signup_email")
                    password = st.text_input("New Password", type="password", key="signup_password")

                    if st.button("Sign Up"):
                        if user_type == "HR Manager":
                            if company_option == "New Company":
                                company_id = register_company(new_company_name)
                                if company_id is None:
                                    st.error("Company registration failed. Company name may already exist.")
                                    return  
                            otp_secret = register_hr(username, password, company_id, email)
                        else:
                            otp_secret = register_user(username, password, company_id, email)

                        st.success("Registration successful! Scan the QR code with your authenticator app.")
                        if otp_secret:
                            uri = generate_otp_uri(otp_secret, username)
                            col1, col2 = st.columns(2)
                            with col1:
                                qr_code = generate_qr_code(uri)
                                st.markdown(f"""
                                    <style>
                                        .qr-code {{
                                            width: auto;
                                            height: auto;
                                            display: block;
                                            margin: auto;
                                        }}
                                    </style>
                                    <img src='data:image/png;base64,{qr_code}' alt='QR Code' class='qr-code'>
                                    """, unsafe_allow_html=True)

                            with col2:
                                st.info("Instructions:")
                                st.write("1. Open your authenticator app (e.g., Google Authenticator, Authy)")
                                st.write("2. Add a new account by scanning the QR code above")
                                st.write("3. Enter the 6-digit code displayed in your app below")
                                st.info("After scanning, enter the OTP to complete setup:")
                            setup_otp = st.text_input("Enter OTP to complete setup", key="setup_otp")


                            if st.button("Verify OTP"):
                                if verify_otp(otp_secret, setup_otp):
                                    st.success(f"{user_type} registered successfully!")
                                    st.experimental_rerun()
                                else:
                                    st.error("Invalid OTP. Please try again.")
                        else:
                            st.error("Registration failed. Username may already exist.")

                with tab3:
                    st.header("Subscription Plans")
                    st.selectbox("Select Plans", ["3 Months", "6 Month", "1 Year"])


                    def generate_subscription_key(length=40):
                        characters = string.ascii_letters + string.digits + "$@#-"
                        return ''.join(secrets.choice(characters) for _ in range(length))

                    # Example usage
                    if st.button("Generate Subscription Key"):
                        subscription_key = generate_subscription_key()
                        st.header(subscription_key)



                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.title("HR Management System")
                st.write(f"Welcome, {st.session_state.username}")

                if st.sidebar.button("Logout"):
                    st.session_state.logged_in = False
                    st.session_state.username = None
                    st.session_state.user_type = None
                    st.experimental_rerun()

                if st.session_state.user_type == "HR Manager":
                    manager_dashboard(st.session_state.username)
                else:
                    employee_dashboard(st.session_state.username)
        with col3:
            st.write("")

if __name__ == "__main__":
    main()