from flask import Flask, request, redirect, url_for, render_template
import os
from datetime import datetime
from waitress import serve

# Create the Flask server
server = Flask(__name__)

# Main folder where all reports are stored
BASE_REPORTS_FOLDER = "Crime Reports"

# Ensure the main "Crime Reports" folder exists
if not os.path.exists(BASE_REPORTS_FOLDER):
    os.makedirs(BASE_REPORTS_FOLDER)

# Route to handle form submission (Flask route)
@server.route('/submit', methods=['POST'])
def submit():
    try:
        # Retrieve form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phonenumber = request.form.get('phonenumber')
        crimetype = request.form.get('crimetype')
        description = request.form.get('message')  # Fix the field name
        uploaded_file = request.files.get('uploadedphoto')

        # Create a new folder for the report
        report_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_folder = os.path.join(BASE_REPORTS_FOLDER, f"Report_{report_time}")
        os.makedirs(report_folder, exist_ok=True)

        # Save uploaded file
        if uploaded_file and uploaded_file.filename:
            file_path = os.path.join(report_folder, uploaded_file.filename)
            uploaded_file.save(file_path)
        else:
            file_path = "No file uploaded"

        # Save form data as a text file
        report_data = f"""
        --- Crime Report ---
        Submitted at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        First Name: {firstname}
        Last Name: {lastname}
        Email: {email}
        Phone Number: {phonenumber}
        Crime Type: {crimetype}
        Description: {description}
        Uploaded File: {uploaded_file.filename if uploaded_file else 'None'}
        ----------------------------
        """
        report_text_file = os.path.join(report_folder, "report.txt")
        with open(report_text_file, "w") as file:
            file.write(report_data)

        # Redirect to the thankyou.html page
        return redirect(url_for('thank_you'))

    except Exception as e:
        return f"An error occurred: {e}", 500

# Route to serve your custom thankyou.html (Flask route)
@server.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')  # This will render your custom thankyou.html

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Use the port Render provides
    server.run(debug=True, host='0.0.0.0', port=port)
