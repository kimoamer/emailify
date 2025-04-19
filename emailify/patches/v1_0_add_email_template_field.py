import frappe

def execute():
    # Add email_template & Sender Name fields to Notification doctype
    fields = [
        {
            "doctype": "Custom Field",
            "dt": "Notification",
            "fieldname": "email_template",
            "label": "Email Template",
            "fieldtype": "Link",
            "options": "Email Template",
            "insert_after": "channel",
            "depends_on": "eval:doc.channel == 'Email'",
            "description": "Select an Email Template to use instead of the Message field"
        },
        {
            "doctype": "Custom Field",
            "dt": "Notification",
            "fieldname": "sender_name",
            "label": "Sender Name",
            "fieldtype": "Data",
            "insert_after": "sender_email",
            "depends_on": "eval:doc.sender",
            "description": "This name will appear in email message."
        }
    ]
    for field in fields:
        if not frappe.db.exists("Custom Field", {"fieldname":field.get("fieldname"), "dt": field.get("dt")}):
            frappe.get_doc(field).insert(ignore_permissions=True)