import boto3

from app import config

CHARSET = 'utf8'


def send_emails(emails, subject, from_address, message_text, message_html=''):
    ses_client = boto3.client('ses', region_name=config.SES_REGION)
    try:
        resp = ses_client.send_email(
            Source=from_address,
            Destination={
                'ToAddresses': emails
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': CHARSET
                },
                'Body': {
                    'Text': {
                        'Data': message_text,
                        'Charset': CHARSET
                    },
                    'Html': {
                        'Charset': CHARSET,
                        'Data': message_html,
                    },
                }
            },
            ReplyToAddresses=[from_address]
        )
        print(resp['MessageId'])
    except Exception as e:
        raise Exception('Error in sending email:', str(e))
    return True


def email_otp(otp, email, name='', duration='5 minutes', from_address=None):
    # The subject line for the email.
    subject = f'OTP to CapDev Portal'

    # The email body for recipients with non-HTML email clients.
    body_text = (f"Hi {name},\r\n"
                 f"Your OTP is {otp} \r\n"
                 f"Login in {duration}.")

    # The HTML body of the email.
    body_html = f"""<html>
    <head></head>
    <body>
      <h2>Your OTP is {otp}</h2>
      <p>It will expire in {duration}.</p>
    </body>
    </html>
    """

    if from_address is None:
        from_address = config.EMAIL_ADMIN

    send_emails(email, subject, from_address, body_text, body_html)
