import yagmail

def send_emails(e):
# type up the template email her    
    body = "Hi! This is a test email."   
    yag = yagmail.SMTP("heyyougotmail2020@gmail.com")
    yag.send(
        bcc=e,
        subject="Hey, you got mail!",
        contents=body, 
    )
    return e