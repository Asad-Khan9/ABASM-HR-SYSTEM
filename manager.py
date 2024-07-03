# import streamlit as st
# import pandas as pd
# import os
# import pdfkit
# from datetime import datetime
# from datetime import date 
# from io import BytesIO
# import base64
# # -----------importing local files -----------
# from helperfunctions import *
# from html_contents import *
# # --------------------------------------------




# def manager_dashboard(username):
   
#     st.title("Manager Dashboard")
    
#     # Fetch all requests
#     requests = fetch_all_employee_requests()
#     # requests.reverse()
#     tab1, tab2, tab3 = st.tabs(["Pending Leave Requests", "Employee Contract", "Employee Details"])

#     with tab1:
#         def generate_request_pdf(request_data, action):
#             # Constructing HTML content dynamically using Python variables
#             html_content = sick_leave_request_html(request_data, action)

#             options = {
#                 'page-size': 'A4',
#                 'margin-top': '0.5in',
#                 'margin-right': '0.5in',
#                 'margin-bottom': '0.5in',
#                 'margin-left': '0.5in',
#                 'encoding': "UTF-8",
#                 'no-outline': None
#             }
#             pdf_data = pdfkit.from_string(html_content, False, options=options)
#             return pdf_data

#         # Function to download PDF as a link
#         def get_binary_file_downloader_html(bin_data, file_name='file.pdf', btn_label='Download PDF'):
#             bin_str = base64.b64encode(bin_data).decode()
#             href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_name}">{btn_label}</a>'
#             return href

#         # Display pending leave requests
#         if requests:
#             st.write("### Pending Leave Requests")

#             #-------------
#             request_data = []
#             for req in requests:
#                 status = get_leave_status(req[2], req[5], req[6], req[7])
#                 if status is None:
#                     request_data.append({
#                         "Name": req[1],
#                         "Employee ID": req[2],
#                         "Job Title": req[3],
#                         "Leave Days": req[4],
#                         "From": req[5],
#                         "To": req[6],
#                         "Leave Type": req[7],
#                         "Reason": req[8],
#                         "Main Type": req[10],
#                         "Status": "Pending",
#                         "Request ID": f"{req[2]}_{req[5]}_{req[6]}_{req[7]}"  # Unique identifier
#                     })
#             if request_data:
#             #-------------
#                 df = pd.DataFrame(request_data, columns=["Name", "Employee ID", "Job Title", "Leave Days", "From", "To", "Leave Type", "Reason", "Main Type", "Status"])
#                 # Display requests in a custom format
#                 for index, row in df.iterrows():
#                     with st.container(height=400):
#                         st.write(f"### {row['Name']}")
#                         st.write(f"**Name:** {row['Name']}, **Employee ID:** {row['Employee ID']}, **Leave Type:** {row['Leave Type']}, **From:** {row['From']}, **To:** {row['To']}")
#                         st.write(f"**Reason for leave:**")
#                         st.write(row['Reason'])
#                         action_key = f"action_{index}"  # Create a unique key for each radio button
#                         action = st.radio(f"Choose an action for {row['Name']}:", ("Approve", "Reject"), key=action_key)
#                         if st.button(f"Process Request for {row['Name']}", key=f"process_{index}"):

#                             # Perform processing logic here (e.g., update status in database, generate PDF)
#                             insert_leave_status(username, row["Name"], row["Employee ID"], action, row["From"], row["To"], row["Leave Type"])

#                             pdf_content = generate_request_pdf(row, action)
#                             st.markdown(get_binary_file_downloader_html(pdf_content, f'Leave_Request_{row["Employee ID"]}.pdf', 'Download PDF'), unsafe_allow_html=True)
#                             # Update database or perform other actions as needed

#                     # st.write("---")
#             else:
#                 st.info("No pending leave requests found.")
#         else:
#             st.info("No pending leave requests found.")


#     with tab2:
#         def get_binary_file_downloader_html(bin_data, file_label='File', btn_label='Download', file_name='file.pdf'):
#             bin_str = base64.b64encode(bin_data).decode()
#             href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_name}">{btn_label}</a>'
#             return href
#         st.header("Employment Contract Form")
        
#         contract_date = st.date_input("Contract Date")
#         employee_name = st.text_input("Employee Name")
#         national_id = st.text_input("National ID Number")
        
#         # Text area for agreed terms
#         agreed_terms = st.text_area("Terms of Agreement", height=300, 
#                                     value="""1. The second party is committed to working for the first party in the profession of [JOB TITLE].
#                                     2. The duration of this contract is [DURATION] starting from [START DATE].
#                                     3. The second party's salary is a monthly total of [TOTAL SALARY] Saudi riyals.
#                                     4. [ADD MORE TERMS AS NEEDED]

#                                     The parties agree to abide by these terms and conditions.""")
    
#         if st.button("Generate Contract PDF"):
#             # Create the HTML content (use the html_content string from above)
#             html_content = contract_form_html(contract_date, employee_name, national_id, agreed_terms)

#             options = {
#                 'page-size': 'A4',
#                 'margin-top': '0.5in',
#                 'margin-right': '0.5in',
#                 'margin-bottom': '0.5in',
#                 'margin-left': '0.5in',
#                 'encoding': "UTF-8",
#                 'no-outline': None
#             }
            
#             # Generate PDF in memory
#             pdf_data = pdfkit.from_string(html_content, False, options=options)
            
#             # Offer the PDF as a download
#             st.markdown(get_binary_file_downloader_html(pdf_data, 'Contract.pdf', 'Download PDF'), unsafe_allow_html=True)

#     with tab3:
#         employee_usernames = get_employee_username_by_hr_username(username)
#         if employee_usernames:
#             st.write("Employees under your management:")
#             for emp_username in employee_usernames:
#                 st.write(f"- {emp_username}")
#         else:
#             st.write("No employees found under your management.")

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

# Configure wkhtmltopdf path
wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

# Function to generate PDF with error handling
def generate_pdf_from_html(html_content, options):
    try:
        return pdfkit.from_string(html_content, False, options=options, configuration=config)
    except OSError as e:
        st.error(f"Error generating PDF: {e}")
        st.error("Please ensure wkhtmltopdf is installed and the path is correct.")
        return None

def manager_dashboard(username):
    st.title("Manager Dashboard")
    
    # Fetch all requests
    requests = fetch_all_employee_requests()
    tab1, tab2, tab3 = st.tabs(["Pending Leave Requests", "Employee Contract", "Employee Details"])

    with tab1:
        def generate_request_pdf(request_data, action):
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
            return generate_pdf_from_html(html_content, options)

        # Function to download PDF as a link
        def get_binary_file_downloader_html(bin_data, file_name='file.pdf', btn_label='Download PDF'):
            bin_str = base64.b64encode(bin_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_name}">{btn_label}</a>'
            return href

        # Display pending leave requests
        if requests:
            st.write("### Pending Leave Requests")

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
                        "Request ID": f"{req[2]}_{req[5]}_{req[6]}_{req[7]}"  # Unique identifier
                    })
            if request_data:
                df = pd.DataFrame(request_data, columns=["Name", "Employee ID", "Job Title", "Leave Days", "From", "To", "Leave Type", "Reason", "Main Type", "Status"])
                # Display requests in a custom format
                for index, row in df.iterrows():
                    with st.container(height=400):
                        st.write(f"### {row['Name']}")
                        st.write(f"**Name:** {row['Name']}, **Employee ID:** {row['Employee ID']}, **Leave Type:** {row['Leave Type']}, **From:** {row['From']}, **To:** {row['To']}")
                        st.write(f"**Reason for leave:**")
                        st.write(row['Reason'])
                        action_key = f"action_{index}"  # Create a unique key for each radio button
                        action = st.radio(f"Choose an action for {row['Name']}:", ("Approve", "Reject"), key=action_key)
                        if st.button(f"Process Request for {row['Name']}", key=f"process_{index}"):
                            insert_leave_status(username, row["Name"], row["Employee ID"], action, row["From"], row["To"], row["Leave Type"])

                            pdf_content = generate_request_pdf(row, action)
                            if pdf_content:
                                st.markdown(get_binary_file_downloader_html(pdf_content, f'Leave_Request_{row["Employee ID"]}.pdf', 'Download PDF'), unsafe_allow_html=True)
                            else:
                                st.error("Failed to generate PDF. Please check the system configuration.")
            else:
                st.info("No pending leave requests found.")
        else:
            st.info("No pending leave requests found.")

    with tab2:
        st.header("Employment Contract Form")
        
        contract_date = st.date_input("Contract Date")
        employee_name = st.text_input("Employee Name")
        national_id = st.text_input("National ID Number")
        
        agreed_terms = st.text_area("Terms of Agreement", height=300, 
                                    value="""1. The second party is committed to working for the first party in the profession of [JOB TITLE].
                                    2. The duration of this contract is [DURATION] starting from [START DATE].
                                    3. The second party's salary is a monthly total of [TOTAL SALARY] Saudi riyals.
                                    4. [ADD MORE TERMS AS NEEDED]

                                    The parties agree to abide by these terms and conditions.""")
    
        if st.button("Generate Contract PDF"):
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
            
            pdf_data = generate_pdf_from_html(html_content, options)
            if pdf_data:
                st.markdown(get_binary_file_downloader_html(pdf_data, 'Contract.pdf', 'Download PDF'), unsafe_allow_html=True)
            else:
                st.error("Failed to generate PDF. Please check the system configuration.")

    with tab3:
        employee_usernames = get_employee_username_by_hr_username(username)
        if employee_usernames:
            st.write("Employees under your management:")
            for emp_username in employee_usernames:
                st.write(f"- {emp_username}")
        else:
            st.write("No employees found under your management.")