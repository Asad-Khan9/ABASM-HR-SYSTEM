import streamlit as st
from helperfunctions import *
from employee import employee_dashboard
from manager import manager_dashboard
from database import init_db

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

                    tab1, tab2 = st.tabs(["Login", "Sign Up"])

                    with tab1:
                        user_type = st.selectbox("I am a", ["Employee", "HR Manager"], key="login_user_type")
                        company_names = [company[1] for company in companies]
                        selected_company = st.selectbox("Select Company", company_names, key="login_company")
                        username = st.text_input("Username", key="login_username")
                        password = st.text_input("Password", type="password", key="login_password")

                        if st.button("Log In"):
                            if user_type == "HR Manager":
                                result = login_hr(username, password)
                            else:
                                result = login_user(username, password)

                            if result:
                                st.session_state.logged_in = True
                                st.session_state.username = username
                                st.session_state.user_type = user_type
                                st.success(f"Logged in as {user_type}: {username}")
                                st.experimental_rerun()
                            else:
                                st.error("Incorrect username or password")

                    with tab2:
                        user_type = st.selectbox("I want to register as", ["Employee", "HR Manager"], key="signup_user_type")
                        if user_type == "HR Manager":
                            company_option = st.radio("Company", ["Existing Company", "New Company"])
                            if company_option == "Existing Company":
                                company_names = [company[1] for company in companies]
                                selected_company = st.selectbox("Select Company", company_names, key="signup_company")
                                company_id = next(company[0] for company in companies if company[1] == selected_company)
                            else:
                                new_company_name = st.text_input("New Company Name")
                        else:
                            company_names = [company[1] for company in companies]
                            selected_company = st.selectbox("Select Company", company_names, key="signup_company")
                            company_id = next(company[0] for company in companies if company[1] == selected_company)

                        username = st.text_input("New Username", key="signup_username")
                        password = st.text_input("New Password", type="password", key="signup_password")

                        if st.button("Sign Up"):
                            if user_type == "HR Manager":
                                if company_option == "New Company":
                                    company_id = register_company(new_company_name)
                                    if company_id is None:
                                        st.error("Company registration failed. Company name may already exist.")
                                        return
                                if register_hr(username, password, company_id):
                                    st.success("HR registered successfully!")
                                    st.session_state.logged_in = True
                                    st.session_state.username = username
                                    st.session_state.user_type = "HR Manager"
                                    st.experimental_rerun()
                                else:
                                    st.error("Registration failed. Username may already exist.")
                            else:
                                if register_user(username, password, company_id):
                                    st.success("Employee registered successfully!")
                                    st.session_state.logged_in = True
                                    st.session_state.username = username
                                    st.session_state.user_type = "Employee"
                                    st.experimental_rerun()
                                else:
                                    st.error("Registration failed. Username may already exist.")

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