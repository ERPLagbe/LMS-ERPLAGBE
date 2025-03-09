console.log("Hello");

$(document).ready(function () {
	if (frappe.session && frappe.session.user) {
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "User",
				name: frappe.session.user,
			},
			callback: function (response) {
				const roles = response.message.roles.map((role) => role.role);
				if (roles.length === 0 || roles.includes("LMS Student")) {
					window.location.href = "/lms/courses";
				}
			},
		});
	} else {
		console.log("Frappe session user is not available.");
	}
});
