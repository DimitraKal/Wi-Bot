import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(from_address, to_address, subject, message):
    passw = "w3bInt3lB0t1"  # TODO πρέπει να αλλάξω θέση στα credentials
    msg = MIMEMultipart()

    msg['From'] = from_address
    msg['To'] = to_address

    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    # filename = "/home/ashish/Downloads/webinar_rasa2_0.png"
    # attachment = open(filename, "rb")
    #
    # # instance of MIMEBase and named as p
    # p = MIMEBase('application', 'octet-stream')
    #
    # # To change the payload into encoded form
    # p.set_payload((attachment).read())
    #
    # # encode into base64
    # encoders.encode_base64(p)
    #
    # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    #
    # # attach the instance 'p' to instance 'msg'
    # msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    try:
        s.login(from_address, passw)
        text = msg.as_string()
        s.sendmail(from_address, to_address, text)
    except:
        print("Παρουσιάστηκε κάποιο σφάλμα :/")
    finally:
        s.quit()
