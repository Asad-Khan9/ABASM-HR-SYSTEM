import streamlit as st
from helperfunctions import *
from datetime import date, datetime
import pandas as pd
def employee_dashboard(username):

    st.title("Employee Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["Vacation Leave Request","Absence Leave Request", "View Leave Status"])
    
    with tab1:
        # today_date = str(date.today().strftime("%Y-%m-%d"))
        today_date = str(date.today().strftime("%Y-%m-%d %A"))
        main_type = "Vacation Leave"
        left, right = st.columns(2, vertical_alignment="bottom")
        left.header("Vacation Leave Request")
        right.info(f"**{main_type} requesting on:** {today_date}")

        name = st.text_input("Name")
        employee_id = st.text_input("Employee ID")
        job_title = st.text_input("Job title")
        leave_days = st.number_input("Leave request Days", min_value=1, value=1)
        from_date = st.date_input("Dates of absence: From")
        to_date = st.date_input("To")
        leave_type = st.selectbox("Type of leave", ["Paid Leave", "Unpaid Leave", "Other"])
        reason = st.text_area("Reason for the Leave")

        # if st.button("Submit request"):
        #     insert_employee_request(username, name, employee_id, job_title, str(leave_days), str(from_date), str(to_date), leave_type, reason, main_type)
        #     st.success("Request submitted successfully")
        if st.button("Submit request"):
            insert_employee_request(username, name, employee_id, job_title, str(leave_days), str(from_date), str(to_date), leave_type, reason, main_type)
            st.success("Request submitted successfully")
    with tab2:
        today_date = str(date.today().strftime("%Y-%m-%d %A"))
        main_type = "Absence Leave"
        left, right = st.columns(2, vertical_alignment="bottom")
        left.header("Absence Leave Request")
        right.info(f"**{main_type} requesting on:** {today_date}")

        name = st.text_input("Name ")
        employee_id = st.text_input("Employee ID ")
        job_title = st.text_input("Job title ")
        type_of_absence = st.selectbox("Type of Absence", ["Paid Leave", "Unpaid Leave", "Sick", "Appointment", "Other"])


        Appointment_from_date = None
        Appointment_to_date = None
        sick_from_date = None
        sick_to_date = None
        appointment_letter_PDF = None
        sick_letter_PDF = None
        other_reason = None

        if(type_of_absence == "Appointment"):
            st.write("Please provide the following Appointment information:")
            Appointment_from_date = st.date_input("Appointment from")
            Appointment_to_date = st.date_input("Appointment till")
            appointment_letter_PDF = st.file_uploader("Upload Appointment Letter")
        elif (type_of_absence == "Sick"):
            st.write("Please provide the following Sick information:")
            sick_from_date = st.date_input("Sick from")
            sick_to_date = st.date_input("Sick till")
            sick_letter_PDF = st.file_uploader("Upload Sick Letter")
        elif (type_of_absence == "Other"):
            st.write("Please provide the following Other information:")
            other_reason = st.text_area("Reason for the Absence")
        from_date = st.date_input("From ")
        to_date = st.date_input("To ")
        reason = st.text_area("Reason for the Absence ")

        if st.button("Submit request "):
            insert_employee_request(username, name, employee_id, job_title, "0", str(from_date), str(to_date), type_of_absence, reason, main_type, str(Appointment_from_date), str(Appointment_to_date), str(sick_from_date), str(sick_to_date), appointment_letter_PDF, sick_letter_PDF, other_reason)

            # insert_employee_request(username, name, employee_id, job_title, "0", str(from_date), str(to_date), type_of_absence, reason, main_type, str(Appointment_from_date), str(Appointment_to_date), str(sick_from_date), str(sick_to_date), appointment_letter_PDF, sick_letter_PDF, other_reason)    
            st.success("Request submitted successfully")
    with tab3:
        st.header("My Leave Requests")
        requests = fetch_all_employee_requests()
        my_requests = [req for req in requests if req[0] == username]
        my_requests.reverse()
        # st.write(requests)
        if my_requests:

            st.write("Sample request structure:")
            # st.write(my_requests)
            
            st.table(my_requests)


            # for req in my_requests[:2]:
            #     st.write(req)
                # status = get_leave_status(req[2], req[5], req[6], req[7])
                
                # st.write(f"**Request for {req[1]}**")
                # st.write(f"Main Type: {req[9]}")
                # st.write(f"From: {req[5]} To: {req[6]}")
                # st.write(f"Type: {req[7]}")
                # # st.write(f"**Status: {status if status else 'Pending'}**")

                # st.write(f"Reason: {req[8]}")

                # if(req[10] == "VacationLeave"):
                #     st.write(f"Leave Days: {req[4]}")

                # if(status == "Approve"):

                #     st.write("**:green-background[Status: :green[Approved]]**")
                # elif(status == "Reject"):
                #     st.write("**:red-background[Status: :red[Rejected]]**")
                # else:
                #     st.write("**:orange-background[Status: :orange[Pending]]**")

                # st.write("---")









        # else:
        #     st.info("You haven't submitted any leave requests yet.")
        # st.write("**My leave requests history**")
        # history_data = []
        # for req in my_requests:
        #     status = get_leave_status(req[2], req[5], req[6], req[7])
        #     history_data.append(tuple(req) + (status,))

        # # columns = ["Username", "Name", "Employee ID", "Position", "Days Requested","Start Date",
        # #            "End Date", "Leave Type", "Reason", "Request Type", "Leave Status"]
        # columns = ["Username", "Name", "Employee ID", "Position", "Days Requested", "Start Date",
        #            "End Date", "Leave Type", "Reason", "Request Type", "Original Leave Status", "Final Leave Status"]
        # st.write()
        # df = pd.DataFrame(history_data, columns=columns)
        # df.drop('Original Leave Status', axis=1, inplace=True)
        
        # with st.expander("Click to see requests history"):
        #     st.dataframe(df.iloc[:, :], use_container_width=True, height=500, width=1000 )
        
        else:
            if my_requests:
                for req in my_requests[:2]:
                    st.write(req)
            
                st.write("**My leave requests history**")
                history_data = []
                for req in my_requests:
                    status = get_leave_status(req[2], req[5], req[6], req[7])
                    history_data.append(req + (status,))
            
                # Get column names dynamically
                columns = [f"Column_{i}" for i in range(len(history_data[0]))]
                
                df = pd.DataFrame(history_data, columns=columns)
                
                # Rename columns as needed
                column_mapping = {
                    "Column_0": "Username",
                    "Column_1": "Name",
                    "Column_2": "Employee ID",
                    "Column_3": "Position",
                    "Column_4": "Days Requested",
                    "Column_5": "Start Date",
                    "Column_6": "End Date",
                    "Column_7": "Leave Type",
                    "Column_8": "Reason",
                    "Column_9": "Request Type",
                    # Add mappings for the additional columns as needed
                    f"Column_{len(history_data[0])-1}": "Final Leave Status"
                }
                df.rename(columns=column_mapping, inplace=True)
            
                with st.expander("Click to see requests history"):
                    st.dataframe(df, use_container_width=True, height=500, width=1000)
                    
            
            