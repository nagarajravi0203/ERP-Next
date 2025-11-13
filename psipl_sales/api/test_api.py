import frappe
import traceback

@frappe.whitelist(allow_guest=False)
def update_next_step(docname, new_status, reason=None, doctype="Lead Entry"):
    """Safely update next_step (or payment_status) even if submitted."""
    try:
        doc = frappe.get_doc(doctype, docname)
        doc.flags.ignore_permissions = True
        doc.flags.ignore_validate_update_after_submit = True
        doc.db_set("next_step", new_status, update_modified=True)

        comment = f"Next Step updated to '{new_status}'"
        if reason:
            comment += f" (Reason: {reason})"
        doc.add_comment("Comment", comment)

        frappe.db.commit()
        return {"status": "success", "message": f"{doctype} updated to {new_status}"}

    except Exception:
        frappe.log_error(message=traceback.format_exc(), title="update_next_step_error")
        return {"status": "failed", "message": "Error while updating next_step"}

