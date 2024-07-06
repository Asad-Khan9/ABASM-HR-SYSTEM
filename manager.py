import streamlit as st
import pandas as pd
import os
import pdfkit
from datetime import datetime
from datetime import date 
from io import BytesIO
import base64
# -----------importing local files -----------
from helperfunctions import *
from html_contents import *
# --------------------------------------------


def manager_dashboard(username):
   
    st.title("Manager Dashboard")
    
    # Fetch all requests
    requests = fetch_all_employee_requests()
    # requests.reverse()
    tab1, tab2, tab3 = st.tabs(["Pending Leave Requests", "Employee Contract", "Employee Details"])

    with tab1:

        def display_pdf(pdf_data):
            if pdf_data:
                base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.write("No PDF available")
        def generate_request_pdf(request_data, action):
            # Constructing HTML content dynamically using Python variables
            html_content = sick_leave_request_html(request_data, action)

            options = {
                'page-size': 'A4',
                'margin-top': '0.5in',
                'margin-right': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
                'encoding': "UTF-8",
                'no-outline': None
            }
            pdf_data = pdfkit.from_string(html_content, False, options=options)
            return pdf_data

        # Function to download PDF as a link
        def get_binary_file_downloader_html(bin_data, file_name='file.pdf', btn_label='Download PDF'):
            bin_str = base64.b64encode(bin_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_name}">{btn_label}</a>'
            return href

        # Display pending leave requests
        if requests:
            st.write("### Pending Leave Requests")

            #-------------
            request_data = []
            for req in requests:
                status = get_leave_status(req[2], req[5], req[6], req[7])
                if status is None:
                    request_data.append({
                        "Name": req[1],
                        "Employee ID": req[2],
                        "Job Title": req[3],
                        "Leave Days": req[4],
                        "From": req[5],
                        "To": req[6],
                        "Leave Type": req[7],
                        "Reason": req[8],
                        "Main Type": req[10],
                        "Status": "Pending",
                        "Request ID": f"{req[2]}_{req[5]}_{req[6]}_{req[7]}",  # Unique identifier
                        "Appointment_from_date": req[11],
                        "Appointment_to_date": req[12],
                        "sick_from_date": req[13],  
                        "sick_to_date": req[14], 
                        "appointment_letter_PDF": req[15],  
                        "sick_letter_PDF":req[16],  
                        "other_reason": req[17]
                    })
            if request_data:
                st.write("Sample request structure:")
                st.table(request_data)
                st.write("---")
            #-------------
                df = pd.DataFrame(request_data, columns=["Name", "Employee ID", "Job Title", "Leave Days", "From", "To", "Leave Type", "Reason", "Main Type", "Status", "Appointment_from_date", "Appointment_to_date", 
              "sick_from_date", "sick_to_date", "appointment_letter_PDF", "sick_letter_PDF", "other_reason" ])
                # Display requests in a custom format
                for index, row in df.iterrows():
                    with st.container():
                        st.write(f"### {row['Name']}")
                        st.write(f"**Name:** {row['Name']}, **Employee ID:** {row['Employee ID']}, **Leave Type:** {row['Leave Type']}, **From:** {row['From']}, **To:** {row['To']}")
                        st.write(f"**Leave Days:** {row['Leave Days']}")
                        st.write(f"**Main Type:** {row['Main Type']}")
                        st.write(f"**Status:** {row['Status']}")
                        st.write(f"**Appointment_from_date:** {row['Appointment_from_date']}")
                        st.write(f"**Appointment_to_date:** {row['Appointment_to_date']}")
                        st.write(f"**sick_from_date:** {row['sick_from_date']}")
                        st.write(f"**sick_to_date:** {row['sick_to_date']}")

                        if row['appointment_letter_PDF']:
                            if st.button(f"View Appointment Letter for {row['Name']}", key=f"view_appointment_{index}"):
                                display_pdf(row['appointment_letter_PDF'])

                        if row['sick_letter_PDF']:
                            if st.button(f"View Sick Leave Letter for {row['Name']}", key=f"view_sick_{index}"):
                                display_pdf(row['sick_letter_PDF'])

                        st.write(f"**other_reason:**")
                        col1, col2 , col3= st.columns([5, 4, 5])
                        with col1:
                            with st.container(height = 200, border= True):
                                st.write(row['other_reason'])
                        with col2:
                            st.write(" ")
                        with col3:
                            st.write(" ")

                        st.write(f"**Reason for leave:**")
                        st.write(row['Reason'])
                        action_key = f"action_{index}"  # Create a unique key for each radio button
                        action = st.radio(f"Choose an action for {row['Name']}:", ("Approve", "Reject"), key=action_key)
                        if st.button(f"Process Request for {row['Name']}", key=f"process_{index}"):

                            # Perform processing logic here (e.g., update status in database, generate PDF)
                            insert_leave_status(username, row["Name"], row["Employee ID"], action, row["From"], row["To"], row["Leave Type"])
                            st.success(f"Leave request for {row['Name']} processed successfully.")
                        #-->
                            # pdf_content = generate_request_pdf(row, action)
                            # st.markdown(get_binary_file_downloader_html(pdf_content, f'Leave_Request_{row["Employee ID"]}.pdf', 'Download PDF'), unsafe_allow_html=True)
                    
                            
                            # Update database or perform other actions as needed
                        #-->

                    st.write("---")
            else:
                st.info("No pending leave requests found.")
        else:
            st.info("No pending leave requests found.")
        with st.expander("View All Requests under me", expanded=False):
            requests_under_me = fetch_all_employee_requests_under_me(username)
            if requests_under_me:
                st.table(requests_under_me)

    with tab2:
        def get_binary_file_downloader_html(bin_data, file_label='File', btn_label='Download', file_name='file.pdf'):
            bin_str = base64.b64encode(bin_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_name}">{btn_label}</a>'
            return href
        st.header("Employment Contract Form")
        
        contract_date = st.date_input("Contract Date")
        employee_name = st.text_input("Employee Name")
        national_id = st.text_input("National ID Number")
        
        # Text area for agreed terms
        agreed_terms = st.text_area("Terms of Agreement", height=300, 
                                    value="""1. The second party is committed to working for the first party in the profession of [JOB TITLE].
                                    2. The duration of this contract is [DURATION] starting from [START DATE].
                                    3. The second party's salary is a monthly total of [TOTAL SALARY] Saudi riyals.
                                    4. [ADD MORE TERMS AS NEEDED]

                                    The parties agree to abide by these terms and conditions.""")
    
        if st.button("Generate Contract PDF"):
            # Create the HTML content (use the html_content string from above)
            html_content = contract_form_html(contract_date, employee_name, national_id, agreed_terms)

            options = {
                'page-size': 'A4',
                'margin-top': '0.5in',
                'margin-right': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
                'encoding': "UTF-8",
                'no-outline': None
            }
            
            # Generate PDF in memory
            pdf_data = pdfkit.from_string(html_content, False, options=options)
            
            # Offer the PDF as a download
            st.markdown(get_binary_file_downloader_html(pdf_data, 'Contract.pdf', 'Download PDF'), unsafe_allow_html=True)

    with tab3:
        employee_usernames = get_employee_username_by_hr_username(username)
        if employee_usernames:
            st.write("Employees under your management:")
            for emp_username in employee_usernames:
                st.write(f"- {emp_username}")
        else:
            st.write("No employees found under your management.")
