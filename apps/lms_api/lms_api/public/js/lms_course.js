frappe.ui.form.on('LMS Course', {
    after_save: function (frm) {
        // Trigger the redirect after saving the document
        window.location.href = `/lms/courses/${frm.doc.name}/edit`;
    }
});