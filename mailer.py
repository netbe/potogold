import sendgrid
import os

def send_email_notification(email, username, fixer_name):
  sg = sendgrid.SendGridClient(os.environ.get('SENGRID_USERNAME'), os.environ.get('SENGRID_PASSWORD'))
  message = sendgrid.Mail()
  message.add_to(email)
  message.set_subject(username + ' - ')
  message.set_from("Potogold")
  message.set_html("   ")
  message.add_filter('templates', 'enable', '1')
  message.add_filter('templates', 'template_id', 'c3929ae4-4c32-4e05-a0f5-c37b5b85359a')
  # # mail.addSubstitution('-rep_name-', process.env.FROM_NAME);
  message.add_substitution(':fix_name', fixer_name)
  # message.add_substitution('-body-', '');
  status, msg = sg.send(message)
  # rep_name
  # fix_name
  print status
  print msg

if __name__ == "__main__":
  print "uncomment"
  # send_email_notification("email", "francois", "ben")
