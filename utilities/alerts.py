# alerts.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertSystem:
    def __init__(self, email_server, sender_email, sender_password):
        self.email_server = email_server
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email, subject, message):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP(self.email_server, 587)
        server.starttls()
        server.login(self.sender_email, self.sender_password)
        text = msg.as_string()
        server.sendmail(self.sender_email, recipient_email, text)
        server.quit()

# Example usage:
if __name__ == "__main__":
    alert_system = AlertSystem('smtp.example.com', 'your_email@example.com', 'your_password')
    alert_system.send_email('recipient@example.com', 'Urgent Market Update', 'Significant market movement detected.')
