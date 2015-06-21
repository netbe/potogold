import sendgrid
import os

def send_email_notification(email):
  sg = sendgrid.SendGridClient(os.environ.get('SENGRID_USERNAME'), os.environ.get('SENGRID_PASSWORD'))
  message = sendgrid.Mail()
  message.add_to(email)
  message.set_subject('Example1')
  message.set_text('')
  # message.add_filter('templates', 'enable', '1')
  message.add_filter('templates', 'template_id', 'c3929ae4-4c32-4e05-a0f5-c37b5b85359a')
  # mail.add_substitution('#recipient#', emails[0][0])
  status, msg = sg.send(message)
  # rep_name
  # fix_name
  print status
  print msg

if __name__ == "__main__":
  sendmail()
