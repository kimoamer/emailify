from frappe.email.doctype.notification.notification import Notification
from collections import namedtuple
import json
import os
import frappe
from frappe import _
from frappe.utils import nowdate, validate_email_address
from frappe.utils.jinja import validate_template
from frappe.utils.safe_exec import get_safe_globals
from frappe.email.doctype.email_template.email_template import get_email_template


class CustomNotification(Notification):
    def validate(self):
        # Original validation
        if self.channel in ("Email", "Slack", "System Notification"):
            validate_template(self.subject)
        
        if self.event in ("Days Before", "Days After") and not self.date_changed:
            frappe.throw(_("Please specify which date field must be checked"))
            
        if self.event == "Value Change" and not self.value_changed:
            frappe.throw(_("Please specify which value field must be checked"))
            
        self.validate_forbidden_document_types()
        self.validate_condition()
        self.validate_standard()
        
        # New validation for email template
        if self.channel == "Email" and self.email_template:
            if not frappe.db.exists("Email Template", self.email_template):
                frappe.throw(_("Email Template {0} does not exist").format(self.email_template))
                
        frappe.cache.hdel("notifications", self.document_type)

    def send_an_email(self, doc, context):
        """Override email sending to use template if specified"""
        from email.utils import formataddr
        from frappe.core.doctype.communication.email import _make as make_communication

        # Get subject - use template if available
        if self.email_template:
            doc = context.get("doc", {})
            template = get_email_template(self.email_template, doc)
            subject = template.get("subject")
            message = template.get("message")
        else:
            subject = self.subject
            if "{" in subject:
                subject = frappe.render_template(self.subject, context)
            message = frappe.render_template(self.message, context)

        attachments = self.get_attachment(doc)
        recipients, cc, bcc = self.get_list_of_recipients(doc, context)
        
        if not (recipients or cc or bcc):
            return

        sender = None
        if self.sender and self.sender_email:
            sender = formataddr((self.sender_name or self.sender, self.sender_email))

        communication = None
        if doc.doctype != "Communication":
            communication = make_communication(
                doctype=self.get_reference_doctype(doc),
                name=self.get_reference_name(doc),
                content=message,
                subject=subject,
                sender=sender,
                recipients=recipients,
                communication_medium="Email",
                send_email=False,
                attachments=attachments,
                cc=cc,
                bcc=bcc,
                communication_type="Automated Message",
            ).get("name")

        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            sender=sender,
            cc=cc,
            bcc=bcc,
            message=message,
            reference_doctype=self.get_reference_doctype(doc),
            reference_name=self.get_reference_name(doc),
            attachments=attachments,
            expose_recipients="header",
            print_letterhead=((attachments and attachments[0].get("print_letterhead")) or False),
            communication=communication,
        )

    def get_reference_doctype(self, doc):
        return doc.parenttype if getattr(doc, 'meta', {}).get('istable') else doc.doctype

    def get_reference_name(self, doc):
        return doc.parent if getattr(doc, 'meta', {}).get('istable') else doc.name