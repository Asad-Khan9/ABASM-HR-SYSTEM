import streamlit as st
from helperfunctions import *

def company_registration_dashboard():
    st.header("Company Registration")
    
    company_name = st.text_input("Company Name")
    hr_username = st.text_input("HR Username")
    hr_password = st.text_input("HR Password", type="password")
    
    if st.button("Register Company"):
        company_id = register_company(company_name)
        if company_id:
            if register_hr(hr_username, hr_password, company_id):
                st.success("Company and HR registered successfully!")
                if st.button("Complete Registration"):
                    if login_hr(hr_username, hr_password):
                        st.session_state.logged_in = True
                        st.session_state.username = hr_username
                        st.session_state.user_type = "HR"
                        st.experimental_rerun()
            else:
                st.error("HR registration failed. Username may already exist.")
        else:
            st.error("Company registration failed. Company name may already exist.")