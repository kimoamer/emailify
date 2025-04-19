frappe.ui.form.on('Notification', {
    refresh(frm) {
        // Hide message field when email template is selected
        frm.toggle_display('message', !frm.doc.email_template);
    },
    
    email_template(frm) {
        // Toggle message field visibility
        frm.toggle_display('message', !frm.doc.email_template);
        
        // Load template preview if available
        if (frm.doc.email_template) {
            frm.add_custom_button(__('Preview Template'), () => {
                if (!frm.doc.email_template || !frm.doc.document_type) {
                    frappe.msgprint(__('Please select both Email Template and Document Type.'));
                    return;
                }
            
                frappe.call({
                    method: 'frappe.client.get_list',
                    args: {
                        doctype: frm.doc.document_type,
                        fields: ['name'],
                        limit_page_length: 1,
                        order_by: 'RAND()'
                    },
                    callback({ message }) {
                        if (!message?.length) {
                            frappe.msgprint(__('No records found for {0}', [frm.doc.document_type]));
                            return;
                        }
            
                        frappe.call({
                            method: 'frappe.client.get',
                            args: {
                                doctype: frm.doc.document_type,
                                name: message[0].name
                            },
                            callback({ message: doc }) {
                                console.log(doc)
                                frappe.call({
                                    method: 'frappe.email.doctype.email_template.email_template.get_email_template',
                                    args: {
                                        template_name: frm.doc.email_template,
                                        doc: doc
                                    },
                                    callback({ message: template }) {
                                        if (!template) {
                                            frappe.msgprint(__('Could not fetch the email template preview.'));
                                            return;
                                        }
                                        
            
                                        const dialog = new frappe.ui.Dialog({
                                            title: __('Email Template Preview'),
                                            fields: [
                                                { fieldname: 'subject', label: __('Subject'), fieldtype: 'Data', read_only: 1 },
                                                { fieldname: 'message', label: __('Message'), fieldtype: 'HTML' }
                                            ]
                                        });
            
                                        dialog.set_values({
                                            subject: template.subject,
                                            message: template.message
                                        });
            
                                        dialog.show();
                                    }
                                });
                            }
                        });
                    }
                });
            });
            
            
        }
    },
    
    channel(frm) {
        // Show/hide email template field based on channel
        frm.toggle_display('email_template', frm.doc.channel === 'Email');
    }
});