import frappe
from frappe.utils import nowdate
from frappe.model.document import Document
import json
import requests
from frappe.utils import cstr

@frappe.whitelist(allow_guest=True)
def ping():
    return 'ping'

@frappe.whitelist(allow_guest=True)
def handle_sns_notification():
    try:
        # Get the data from the request
        data = json.loads(frappe.request.data)
        frappe.log_error(message=cstr(data), title="SNS Notification Data")

        if data.get('Type') == 'SubscriptionConfirmation':
            # Handle subscription confirmation request
            confirm_subscription(data.get('SubscribeURL'))
        elif data.get('Type') == 'Notification':
            # Process the notification
            handle_notification(json.loads(data.get('Message')))
    except Exception as e:
        frappe.log_error(message=cstr(e), title="Error in SNS Notification Handling")

def handle_notification(message):
    # Get the necessary details from the message
    notification_type = message.get('notificationType')
    mail = message.get('mail')
    email_id = mail.get('messageId')

    if notification_type == 'Bounce':
        handle_bounce(mail, message.get('bounce'))
    elif notification_type == 'Complaint':
        handle_complaint(mail, message.get('complaint'))
    elif notification_type == 'Delivery':
        handle_delivery(mail, message.get('delivery'))
    else:
        # For simplicity, we assume that any other type of notification is an 'Open' or 'Click' event
        # In practice, you should check the specific type and handle it accordingly
        handle_open_or_click(mail, message)

def handle_bounce(mail, bounce):
    # Find or create the email status document for this email
    email_status_name = frappe.get_value('Email Status', {'aws_message_id': mail['messageId']}, 'name')
    if email_status_name:
        email_status = frappe.get_doc('Email Status', email_status_name)
    else:
        email_status = frappe.new_doc('Email Status')
        email_status.aws_message_id = mail['messageId']
    email_status.status = 'Bounced'
    email_status.save(ignore_permissions=True)
    frappe.db.commit()

    # Create a new Email Bounce document
    email_bounce = frappe.new_doc('Email Bounce')
    email_bounce.email_id = email_status.name
    email_bounce.bounce_type = bounce['bounceType']
    email_bounce.bounce_sub_type = bounce['bounceSubType']
    email_bounce.bounced_recipients = ', '.join([recipient['emailAddress'] for recipient in bounce['bouncedRecipients']])
    email_bounce.timestamp = nowdate()
    email_bounce.insert()
    frappe.db.commit()

def handle_complaint(mail, complaint):
    # Find or create the email status document for this email
    email_status_name = frappe.get_value('Email Status', {'aws_message_id': mail['messageId']}, 'name')
    if email_status_name:
        email_status = frappe.get_doc('Email Status', email_status_name)
    else:
        email_status = frappe.new_doc('Email Status')
        email_status.aws_message_id = mail['messageId']
    email_status.status = 'Complained'
    email_status.save(ignore_permissions=True)
    frappe.db.commit()

    email_complaint = frappe.new_doc('Email Complaint')
    email_complaint.email_id = email_status.name
    email_complaint.complaint_feedback_type = complaint['complaintFeedbackType']
    email_complaint.complained_recipients = ', '.join([recipient['emailAddress'] for recipient in complaint['complainedRecipients']])
    email_complaint.timestamp = nowdate()
    email_complaint.insert()
    frappe.db.commit()

def handle_delivery(mail, delivery):
    # Find or create the email status document for this email
    email_status_name = frappe.get_value('Email Status', {'aws_message_id': mail['messageId']}, 'name')
    if email_status_name:
        email_status = frappe.get_doc('Email Status', email_status_name)
    else:
        email_status = frappe.new_doc('Email Status')
        email_status.aws_message_id = mail['messageId']
    email_status.status = 'Delivered'
    email_status.save(ignore_permissions=True)
    frappe.db.commit()

def handle_open_or_click(mail, event):
    # Find or create the email status document for this email
    email_status_name = frappe.get_value('Email Status', {'aws_message_id': mail['messageId']}, 'name')
    if email_status_name:
        email_status = frappe.get_doc('Email Status', email_status_name)
    else:
        email_status = frappe.new_doc('Email Status')
        email_status.aws_message_id = mail['messageId']

    if 'open' in event:
        email_status.status = 'Opened'
        email_status.save(ignore_permissions=True)

        email_open_event = frappe.new_doc('Email Open Event')
        email_open_event.email_id = email_status.name
        email_open_event.opened_by_recipient = event['open']['ipAddress']
        email_open_event.opened_date_and_time = nowdate()
        email_open_event.insert()
        email_open_event.submit()
        frappe.db.commit()

    elif 'click' in event:
        email_status.status = 'Clicked'
        email_status.save(ignore_permissions=True)

        email_click_event = frappe.new_doc('Email Click Event')
        email_click_event.email_id = email_status.name
        email_click_event.clicked_by_recipient = event['click']['ipAddress']
        email_click_event.clicked_link = event['click']['link']
        email_click_event.clicked_date_and_time = nowdate()
        email_click_event.insert()
        email_click_event.submit()
        frappe.db.commit()

def confirm_subscription(url):
    """
    Confirm the SNS subscription by calling the provided URL.
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            frappe.log_error(message=f"Error confirming subscription: {response.text}", title="AWS SNS Subscription Error")
    except Exception as e:
        frappe.log_error(message=cstr(e), title="Error in SNS Subscription Confirmation")
