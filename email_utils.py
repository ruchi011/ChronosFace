import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
sender_email = "yourgmail@gmail.com"
sender_password = "YOUR_16_CHARACTER_APP_PASSWORD"
def send_email(receiver_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )
        server.starttls()
        server.login(
            sender_email,
            sender_password
        )
        server.sendmail(
            sender_email,
            receiver_email,
            msg.as_string()
        )
        server.quit()
        print("Email Sent Successfully")
    except Exception as e:
        print("Email Error:", e)