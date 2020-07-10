import yagmail

def send_emails(e):
# type up the template email her    
    body = "Hi! This is a test email."   
    yag = yagmail.SMTP("heyyougotmail2020@gmail.com")
    
    
    for email in e:
        yag.close()
        yag.send(
            to=email,
            subject="Hey, you got mail!",
            contents=f"hi {email}! this is a test email", 
        )
    
    return e