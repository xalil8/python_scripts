import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class RAMMonitor:
    def __init__(self):
        self.sender_email = "sender@example.com"
        self.threshold_percentage = 66  # Example threshold: 80%
        self.receiver_emails = ["email_1@example.com", "email_2@example.com"]  # List of email addresses to receive notifications


        self.smtp_username = "username"
        self.smtp_password = "pw"

        self.smtp_host = "adress"
        self.smtp_port = 2525

    def send_notification_email(self, ram_usage):
        # Compose the email message
        subject = 'High RAM Usage Alert'
        message = f'The RAM usage has exceeded the threshold.\nCurrent RAM usage: {ram_usage}%'

        for receiver_email in self.receiver_emails:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message))

            # Connect to the SMTP server and send the email
            try:
                with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password) #optional

                    server.sendmail(self.sender_email, receiver_email, msg.as_string())
                print(f'Notification email sent successfully to {receiver_email}.')
            except Exception as e:
                print(f'Error occurred while sending email to {receiver_email}: {str(e)}')

    def check_ram_usage(self):
        ram_usage = psutil.virtual_memory().percent

        if ram_usage > self.threshold_percentage:
            self.send_notification_email(ram_usage)

def main():
    ram_monitor = RAMMonitor()
    ram_monitor.check_ram_usage()

if __name__ == '__main__':
    main()
