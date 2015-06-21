import sendgrid

import os



def sendmail():
  sg = sendgrid.SendGridClient(os.environ.get('SENGRID_USERNAME'), os.environ.get('SENGRID_PASSWORD'))
  message = sendgrid.Mail()
  message.add_to('becafoin@gmail.com')
  message.set_subject('Example1')
  message.set_text('Body')
  message.set_from('Doe John ')
  # message.add_filter('templates', 'enable', '1')
  # message.add_filter('templates', 'template_id', '8975824')
  message.add_filter('templates', 'template_id', 'Potogold_final')
  # mail.add_substitution('#recipient#', emails[0][0])
  status, msg = sg.send(message)
  # rep_name
  # fix_name
  print status
  print msg
if __name__ == "__main__":
  sendmail()
