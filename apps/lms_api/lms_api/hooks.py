app_name = "lms_api"
app_title = "Lms Api"
app_publisher = "Tariqul Islam"
app_description = "Lms Api"
app_email = "tariqmolla8@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "lms_api",
# 		"logo": "/assets/lms_api/logo.png",
# 		"title": "Lms Api",
# 		"route": "/lms_api",
# 		"has_permission": "lms_api.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/lms_api/css/styles.css"
app_include_js = [
    "/assets/lms_api/js/lms_course.js",
    "/assets/lms_api/js/lms_quiz.js",
    "/assets/lms_api/js/navbar.js",
    "/assets/lms_api/js/permission_student.js",
]

# include js, css files in header of web template
# web_include_css = "/assets/lms_api/css/lms_api.css"
# web_include_js = "/assets/lms_api/js/lms_api.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lms_api/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "lms_api/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "lms_api.utils.jinja_methods",
# 	"filters": "lms_api.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "lms_api.install.before_install"
# after_install = "lms_api.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "lms_api.uninstall.before_uninstall"
# after_uninstall = "lms_api.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "lms_api.utils.before_app_install"
# after_app_install = "lms_api.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "lms_api.utils.before_app_uninstall"
# after_app_uninstall = "lms_api.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lms_api.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "LMS Enrollment": {
        # "after_insert": "lms_api.api.update_course_enrollment_count",
        "after_insert": "lms_api.api.update_user_enrolled_field",
        # "on_trash": "lms_api.api.decrement_course_enrollment_count",
        # "before_update": "lms_api.api.update_course_enrollment_count"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"lms_api.tasks.all"
# 	],
# 	"daily": [
# 		"lms_api.tasks.daily"
# 	],
# 	"hourly": [
# 		"lms_api.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lms_api.tasks.weekly"
# 	],
# 	"monthly": [
# 		"lms_api.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "lms_api.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    "lms_api.api.get_course_list": "lms_api.api.get_course_list",
    "lms_api.api.get_course_details": "lms_api.api.get_course_details",
    "lms_api.api.get_course_category_data": "lms_api.api.get_course_category_data",
    "lms_api.api.get_blog_list": "lms_api.api.get_blog_list",
    "lms_api.api.get_blog_categories": "lms_api.api.get_blog_categories",
    "lms_api.api.get_blog_details": "lms_api.api.get_blog_details",
    "lms_api.api.get_blog_tags": "lms_api.api.get_blog_tags",
    "lms_api.api.get_gallery_list": "lms_api.api.get_gallery_list",
    "lms_api.api.get_gallery_with_images": "lms_api.api.get_gallery_with_images",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lms_api.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["lms_api.utils.before_request"]
# after_request = ["lms_api.utils.after_request"]

# Job Events
# ----------
# before_job = ["lms_api.utils.before_job"]
# after_job = ["lms_api.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"lms_api.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
