from datetime import date, datetime

def sick_leave_request_html(request_data, action):
    html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 20px; font-size: 12pt; color: #333; }}
                    .form-container {{ max-width: 800px; margin: auto; border: 1px solid #ccc; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                    .header {{ background-color: #f0f0f0; padding: 20px; margin: -30px -30px 20px -30px; border-bottom: 2px solid #ddd; }}
                    h2 {{ font-size: 24pt; margin: 0; color: #2c3e50; }}
                    .section {{ margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px solid #eee; }}
                    .field {{ margin-bottom: 12px; display: flex; align-items: center; }}
                    .label {{ font-weight: bold; width: 200px; color: #34495e; }}
                    .value {{ flex: 1; }}
                    .signature-line {{ border-top: 1px solid #999; width: 300px; display: inline-block; margin-left: 10px; }}
                    .approval-box {{ border: 1px solid #999; padding: 5px 10px; display: inline-block; margin-right: 10px; }}
                    h3 {{ font-size: 16pt; color: #2980b9; margin-bottom: 15px; }}
                    .note {{ font-style: italic; font-size: 10pt; color: #7f8c8d; }}
                    .reason-box {{ border: 1px solid #ddd; padding: 10px; background-color: #f9f9f9; }}
                    .approved {{ color: green; font-weight: bold; }}
                    .rejected {{ color: red; font-weight: bold; }}
                </style>
            </head>
            <body>
                <div class="form-container">
                    <div class="header">
                        <h2>Sick Leave Request Form</h2>
                    </div>

                    <div class="section">
                        <h3>Employee Information</h3>
                        <div class="field"><span class="label">Name:</span> <span class="value">{request_data['Name']}</span></div>
                        <div class="field"><span class="label">Employee ID:</span> <span class="value">{request_data['Employee ID']}</span></div>
                        <div class="field"><span class="label">Job Title:</span> <span class="value">{request_data['Job Title']}</span></div>
                        <div class="field"><span class="label">Leave Request Days:</span> <span class="value">{request_data['Leave Days']}</span></div>
                        <div class="field"><span class="label">Dates of Absence:</span> <span class="value">From {request_data['From']} To {request_data['To']}</span></div>
                    </div>

                    <div class="section">
                        <div class="field"><span class="label">Type of Leave:</span> <span class="value">{request_data['Leave Type']}</span></div>
                    </div>

                    <div class="section">
                        <h3>Sickness Description</h3>
                        <div class="reason-box">{request_data['Reason']}</div>
                    </div>

                    <div class="section">
                        <p class="note">I understand that this request is subject to approval by my employer.</p>
                        <br>
                        <div class="field">
                            <span class="label">Employee Signature:</span> 
                            <span class="signature-line"></span>
                        </div>
                        <div class="field">
                            <span class="label">Date:</span> 
                            <span class="signature-line"></span>

                        </div>
                    </div>

                    <div class="section">
                        <h3>Manager Approval</h3>
                        <div class="field">
                            <span class="label">Decision:</span>
                            <span class="value {'approved' if action == 'Approve' else 'rejected'}">{action}</span>
                        </div>
                        <br>
                        <div class="field">
                            <span class="label">Manager Signature:</span> 
                            <span class="signature-line"></span>
                        </div>
                        <div class="field">
                            <span class="label">Date:</span> 
                            <span class="signature-line"></span>

                        </div>
                    </div>

                    <div class="section">
                        <br>
                        <div class="field">
                            <span class="label">HR Department Signature:</span> 
                            <span class="signature-line"></span>
                        </div>
                        <div class="field">
                            <span class="label">Date:</span> 
                            <span class="value">___________________</span>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
    return html_content


def contract_form_html(contract_date, employee_name, national_id, agreed_terms):
    html_content = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 20px; font-size: 12pt; color: #333; }}
                        .form-container {{ max-width: 100%; margin: auto; padding: 0; }}
                        .header {{ background-color: #f0f0f0; padding: 20px; margin: -30px -30px 20px -30px; border-bottom: 2px solid #ddd; }}
                        h2 {{ font-size: 24pt; margin: 0; color: #2c3e50; }}
                        .section {{ max-width: 100%; margin-bottom: 5px; padding-bottom: 5px; border-bottom: 1px solid #eee; }}
                        .section {{max-width: 100%; background-color: #f0f0f0;padding: 10px;border: 1px solid #ccc;border-radius: 5px;margin-bottom: 10px;}}
                        .field {{ margin-bottom: 12px; display: flex; align-items: center; }}
                        .label {{ font-weight: bold; width: 200px; color: #34495e; }}
                        .value {{ flex: 1; }}
                        .signature-line {{ border-top: 1px solid #999; width: 300px; display: inline-block; margin-left: 10px; }}
                        h3 {{ font-size: 16pt; color: #2980b9; margin-bottom: 15px; }}
                        .note {{ font-style: italic; font-size: 10pt; color: #7f8c8d; }}
                        .terms {{ white-space: pre-wrap; }}
                    </style>
                </head>
                <body>
                    <div class="form-container">
                        <div class="header">
                            <h2>Employment Contract</h2>
                        </div>

                        <div class="section">
                            <p>On {contract_date}, an agreement has been made between:</p>
                            <div class="field"><span class="label">First party:</span> <span class="value">Real Energy Sources Contracting Establishment</span></div>
                            <div class="field"><span class="label">Second party:</span> <span class="value">{employee_name}</span></div>
                            <div class="field"><span class="label">National ID No.:</span> <span class="value">{national_id}</span></div>
                        </div>

                        <div class="section">
                            <h3>Terms of Agreement</h3>
                            <div class="terms">{agreed_terms}</div>
                        </div>

                        <div class="section">
                            <div class="field">
                                <span class="label">First party name:</span> 
                                <span class="value">Real Energy Sources Contracting Establishment</span>
                            </div>
                            <div class="field">
                                <span class="label">First party signature:</span> 
                                <span class="signature-line"></span>
                            </div>
                        </div>

                        <div class="section">
                            <div class="field">
                                <span class="label">Second party name:</span> 
                                <span class="value">{employee_name}</span>
                            </div>
                            <div class="field">
                                <span class="label">Second party signature:</span> 
                                <span class="signature-line"></span>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
            """
    return html_content