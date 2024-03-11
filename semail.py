import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(html_file, sender_email, sender_password, receiver_email, subject):
    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Create HTML content
    html_content = MIMEText(open(html_file, "r").read(), "html")
    message.attach(html_content)

    # Attach HTML file
    with open(html_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {html_file}")
    message.attach(part)

    # Connect to SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Specify sender and receiver email addresses, subject, and HTML file
# sender_email = "interships1402@gmail.com"
# sender_password = 'ixhg xbdt bqcz igxr'
# receiver_email = "veininvein@proton.me"
# subject = "Daily Activity Report"

# Path to the HTML file to be attached
# html_file = "formatted_report.html"

# Send the email
# send_email(html_file, sender_email, sender_password, receiver_email, subject)