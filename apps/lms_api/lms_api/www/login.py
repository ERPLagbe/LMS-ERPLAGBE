import frappe


def get_context(context):
    lms_settings = frappe.get_single("LMS Settings")
    return context
