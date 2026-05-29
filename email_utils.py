import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
SENDER_EMAIL = "madichettysairuchita@gmail.com"
SENDER_PASSWORD = "ruchi@11"
def send_email(receiver_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )
        server.starttls()
        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )
        server.sendmail(
            SENDER_EMAIL,
            receiver_email,
            msg.as_string()
        )
        server.quit()
        print("Email Sent Successfully")
    except Exception as e:
        print("Email Error:", e)