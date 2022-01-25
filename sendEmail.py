import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_with_file(from_address, to_address, subject, message, file_to_send):
    passw = "w3bInt3lB0t1"
    msg = MIMEMultipart()

    msg['From'] = from_address
    msg['To'] = to_address

    msg['Subject'] = subject
    info = " \n\n Αυτό το email στάλθηκε μέσω του WiBot"
    body = message + info
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = file_to_send
    attachment = open(filename, "rb")
    #
    # # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    #
    # # To change the payload into encoded form
    p.set_payload(attachment.read())
    #
    # # encode into base64
    encoders.encode_base64(p)
    #
    p.add_header('Content-Disposition', 'attachment', filename=filename)

    # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    #
    # # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    try:
        s.login(from_address, passw)
        text = msg.as_string()
        s.sendmail(from_address, to_address, text)
    except:
        error = "Παρουσιάστηκε κάποιο σφάλμα..🤔"
        print(error)
        return error
    finally:
        s.quit()


def send_email(from_address, to_address, subject, message):
    passw = "w3bInt3lB0t1"  # TODO πρέπει να αλλάξω θέση στα credentials
    msg = MIMEMultipart()

    msg['From'] = from_address
    msg['To'] = to_address

    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    try:
        s.login(from_address, passw)
        text = msg.as_string()
        s.sendmail(from_address, to_address, text)
    except:
        error = "Παρουσιάστηκε κάποιο σφάλμα..🤔"
        print(error)
        return error
    finally:
        s.quit()
#  try:
#      s.login(from_address, passw)
#      text = msg.as_string()
#      s.sendmail(from_address, to_address, text)
#  except SMTPResponseException as e:
#      error_code = e.smtp_code
#      error_message = e.smtp_error
#      print("Error code:" + error_code + "Message:" + error_message)
#      if error_code == 422:
#          error_message = "Recipient Mailbox Full"
#      elif error_code == 431:
#          error_message = "Server out of space"
#      elif error_code == 447:
#          error_message = "Timeout. Try reducing number of recipients"
#      elif error_code == 510 or error_code == 511:
#          error_message = "One of the addresses in your TO, CC or BBC line doesn't exist. Check again your recipients' accounts and correct any possible misspelling."
#      elif error_code == 512:
#          error_message = "Check again all your recipients' addresses: there will likely be an error in a domain name  like mail@domain.coom instead of mail@domain.com "
#      elif error_code == 541 or error_code == 554:
#          error_message = "Your message has been detected and labeled as spam. You must ask the recipient to whitelist you"
#      elif error_code == 550:
#          error_message = "Though it can be returned also by the recipient's firewall  or when the incoming server is down , the great majority of errors 550 simply tell that the recipient email address doesn't exist. You should contact the recipient otherwise and get the right address."
#      elif error_code == 553:
#          error_message = "Check all the addresses in the TO, CC and BCC field. There should be an error or a misspelling somewhere."
#      else:
#          print(error_code + ": " + error_message)
#          # except:
#          #    error = "Παρουσιάστηκε κάποιο σφάλμα..🤔"
#          #    print(error)
#      return error_message
#  finally:
#      s.quit()
