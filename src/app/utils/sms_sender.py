import boto3

from app import config

sns_client = boto3.client('sns', region_name=config.SNS_REGION)


def send_sms(phones, subject, message, sender_id='WhoAmI'):
    sns_client.set_sms_attributes(
        attributes={
            'DefaultSenderID': sender_id
        }
    )
    for phone in phones:
        if not phone.startswith('+'):
            phone = '+65' + phone
        # print(phone)

        try:
            sns_client.publish(
                PhoneNumber=phone,
                Message=message,
                Subject=subject
            )
        except Exception as e:
            print(f'Failed to send SMS to {phone}: {str(e)}')
