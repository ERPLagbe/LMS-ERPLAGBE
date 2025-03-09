frappe.ui.form.on("LMS Quiz", {
	after_save: function (frm) {
		let duration_in_minutes = frm.doc.duration_in_minutes;
		let duration_in_ms = duration_in_minutes * 60 * 1000;
		frm.set_value("duration", duration_in_ms);
	},
});
