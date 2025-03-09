import frappe
from frappe import _
import frappe.model
import frappe.model.rename_doc
from frappe.utils import validate_email_address, validate_phone_number
from frappe.utils.password import update_password
import requests
from datetime import datetime
import random
import string
from frappe.www.printview import validate_print_permission
from frappe.translate import print_language


def format_number(number):
    number_reduced = number / 1000
    if number_reduced < 1:
        return number
    return f"{frappe.utils.flt(number_reduced, 1)}k"


@frappe.whitelist(allow_guest=True)
def get_course_list(page=1, limit=10, fields=None, custom_category=None):
    # Convert page and limit to integers
    page = int(page)
    limit = int(limit)

    # Calculate the offset for pagination
    offset = (page - 1) * limit

    # Convert fields string to list if provided
    if fields:
        fields = frappe.parse_json(fields)
    else:
        # Default fields if none are provided
        fields = [
            "name",
            "title",
            "image",
            "course_price",
            "discount_price",
            "custom_average_rating",
            "custom_level",
            "custom_sorting_badge",
            "meta_title",
        ]

    # Set up filters
    filters = {"published": True}

    # Add custom_category filter if it's passed
    if custom_category:
        filters["custom_category"] = custom_category

    # Fetch course data with the required fields and filters
    courses = frappe.get_all(
        "LMS Course",
        fields=fields,
        filters=filters,
        limit=limit,
        start=offset,
        order_by="creation desc",
    )

    for course in courses:
        # Calculate discounted course price
        course_price = course.get("course_price", 0) or 0
        discount_price = course.get("discount_price", 0) or 0
        discounted_price = max(course_price - discount_price, 0)  # Ensure non-negative
        course["amount"] = discounted_price
        # Get the enrollment count for each course
        enrollment_count = frappe.db.count(
            "LMS Enrollment", {"course": course["name"], "member_type": "Student"}
        )
        # Add the enrollment count to the course dictionary
        course["custom_total_enrolled"] = format_number(enrollment_count)

    total_courses = frappe.db.count("LMS Course", filters=filters)
    total_pages = (total_courses + limit - 1) // limit

    # Format the response with course list
    response = {
        "courses": courses,
        "total_pages": total_pages,
        "pagination": {"page": page, "limit": limit},
    }

    return response


@frappe.whitelist(allow_guest=True)
def get_course_details(meta_title):
    """
    Fetch the details of a single course by its ID with custom fields.
    Extracts titles from custom_what_you_will_learn field.
    Also fetches reviews associated with the course, including the owner's profile picture,
    and the chapters with their respective lessons.
    Additionally, calculates the percentage of people who gave reviews above certain thresholds.
    """
    course_name = frappe.db.get_value("LMS Course", {"meta_title": meta_title}, "name")

    # Fetch the course document using the provided course_id
    course = frappe.get_doc("LMS Course", course_name)

    # Extract titles from custom_what_you_will_learn if it's a list or child table
    if hasattr(course, "custom_what_you_will_learn"):
        what_you_will_learn_titles = [
            item.title for item in course.custom_what_you_will_learn
        ]
    else:
        what_you_will_learn_titles = []

    # Fetch reviews linked to the specified course
    reviews = frappe.get_all(
        "LMS Course Review",
        filters={"course": course_name},  # Filter reviews by course
        fields=["rating", "review", "creation", "owner"],
        # Select relevant fields
        order_by="creation desc",  # Order reviews by latest first
    )

    # Add owner's profile picture to each review
    for review in reviews:
        # Fetch user's profile picture from the User doctype
        user_data = frappe.get_value("User", review["owner"], "user_image")
        review["owner_profile_picture"] = (
            user_data if user_data else None
        )  # Add profile picture or None if not set

    # Calculate percentage of reviews above specific thresholds
    total_reviews = len(reviews)
    if total_reviews > 0:
        # Initialize counts for each threshold
        # Initialize counts for each range
        count_above_0_8 = sum(1 for review in reviews if review["rating"] >= 0.8)
        count_between_0_8_and_0_6 = sum(
            1 for review in reviews if 0.6 <= review["rating"] < 0.8
        )
        count_between_0_6_and_0_4 = sum(
            1 for review in reviews if 0.4 <= review["rating"] < 0.6
        )
        count_between_0_4_and_0_3 = sum(
            1 for review in reviews if 0.3 <= review["rating"] < 0.4
        )
        count_between_0_3_and_0_2 = sum(
            1 for review in reviews if 0.2 <= review["rating"] < 0.3
        )
        count_between_0_2_and_0_1 = sum(
            1 for review in reviews if 0.1 <= review["rating"] < 0.2
        )

        # Calculate percentages
        percentages = {
            "above_0_8": (count_above_0_8 / total_reviews) * 100,
            "above_0_6": (count_between_0_8_and_0_6 / total_reviews) * 100,
            "above_0_4": (count_between_0_6_and_0_4 / total_reviews) * 100,
            "above_0_3": (count_between_0_4_and_0_3 / total_reviews) * 100,
            "above_0_2": (count_between_0_3_and_0_2 / total_reviews) * 100,
            "above_0_1": (count_between_0_2_and_0_1 / total_reviews) * 100,
        }
    else:
        percentages = {
            "above_0_8": 0,
            "above_0_6": 0,
            "above_0_4": 0,
            "above_0_3": 0,
            "above_0_2": 0,
            "above_0_1": 0,
        }

    # Fetch chapters and their respective lessons
    chapters = frappe.get_all(
        "Course Chapter",
        filters={"course": course_name},  # Filter chapters by course
        fields=["title", "name"],  # Select relevant fields
        order_by="creation asc",  # Ensure correct order of chapters
    )

    for chapter in chapters:
        # Fetch lessons linked to each chapter
        lessons = frappe.get_all(
            "Course Lesson",
            filters={"chapter": chapter["name"]},  # Filter lessons by chapter
            fields=["title", "custom_duration"],  # Select relevant fields
            order_by="creation asc",  # Ensure correct order of lessons
        )
        chapter["lessons"] = lessons  # Add lessons to their respective chapters
    amount = course.course_price
    if course.discount_price:
        amount = course.course_price - course.discount_price
    # Return the relevant fields along with percentage data
    course_data = {
        "id": course.name,
        "title": course.title,
        "image": course.image,
        "meta_title": course.meta_title,
        "discount_price": course.discount_price,
        "course_price": course.course_price,
        "amount": amount,
        "custom_average_rating": course.custom_average_rating,
        "custom_level": course.custom_level,
        "custom_total_enrolled": course.custom_total_enrolled,
        "custom_sorting_badge": course.custom_sorting_badge,
        "custom_course_duration": course.custom_course_duration,
        "custom_what_you_will_learn": what_you_will_learn_titles,
        "description": course.description,
        "custom_total_videos": course.custom_total_videos,
        "custom_total_quizes": course.custom_total_quizes,
        "reviews": reviews,  # Include the reviews with profile pictures in the response
        "chapters": chapters,  # Include the chapters with their respective lessons
        "total_reviews": total_reviews,
        "review_percentages": percentages,  # Include the percentage breakdown of reviews
    }

    return course_data


@frappe.whitelist(allow_guest=True)  # This allows guests to access it
def get_course_category_data():
    categories = frappe.get_all(
        "Course Category LMS",
        fields=["custom_name", "custom_thumbnail_image"],
        order_by="creation desc",
    )

    for category in categories:
        # Count the number of courses linked to each category
        category["total_courses"] = frappe.db.count(
            "LMS Course", {"custom_category": category["custom_name"]}
        )

    return categories


def update_course_enrollment_count(doc):
    if doc.course:  # Ensure there is a course linked to the enrollment
        # Fetch the course document
        course = frappe.get_doc("LMS Course", doc.course)

        # Increment the custom_total_enrolled field
        course.custom_total_enrolled += 1

        # Save the updated course document
        course.save()


def decrement_course_enrollment_count(doc):
    if doc.course:
        course = frappe.get_doc("LMS Course", doc.course)
        course.custom_total_enrolled -= 1
        course.save()


@frappe.whitelist(allow_guest=True)
def get_blog_list(page=1, limit=10, fields=None, blog_category=None, tag=None):
    """
    Fetch blog posts with pagination, including ID, title, thumbnail image, date, and category.
    If 'fields' parameter is provided, fetch the data accordingly; otherwise, use default fields.
    Allows filtering by blog_category and tag.
    """
    # Convert page and limit to integers
    page = int(page)
    limit = int(limit)

    # Calculate the offset for pagination
    offset = (page - 1) * limit

    # Default fields if not provided
    default_fields = [
        "name",
        "title",
        "custom_image",
        "creation",
        "blog_category as category",
        "meta_title",
    ]

    # Use the fields provided in the request or default fields if not given
    fields = frappe.parse_json(fields) if fields else default_fields

    # Set up filters
    filters = {}

    # Apply blog_category filter if provided
    if blog_category:
        filters["blog_category"] = blog_category

    # Fetch blog posts by tag using frappe's 'Tag Link' doctype if tag is provided
    if tag:
        blogs_with_tag = frappe.get_all(
            "Tag Link",
            filters={"tag": tag, "document_type": "Blog Post"},
            fields=["document_name"],
        )
        # Get the names of blog posts associated with the tag
        blog_names = [blog.document_name for blog in blogs_with_tag]

        # Add to the filters to fetch only blogs with these names
        if blog_names:
            filters["name"] = ["in", blog_names]
        else:
            # Return empty if no blogs are associated with the tag
            return {"blogs": [], "pagination": {"page": page, "limit": limit}}

    # Fetch blog post data with the required fields and filters
    blogs = frappe.get_all(
        "Blog Post",
        fields=fields,
        filters=filters,
        limit=limit,
        start=offset,
        order_by="creation desc",
    )

    total_blogs = frappe.db.count("Blog Post", filters=filters)
    total_pages = (total_blogs + limit - 1) // limit

    # Format the response with blog list and pagination details
    response = {
        "blogs": blogs,
        "total_pages": total_pages,
        "pagination": {"page": page, "limit": limit},
    }

    return response


@frappe.whitelist(allow_guest=True)
def get_blog_categories():
    """
    Fetch blog categories along with their ID, name, and the count of blog posts in each category.
    """
    # Fetch all blog categories with their names
    categories = frappe.get_all(
        "Blog Category", fields=["name", "title"], order_by="creation desc"
    )

    # Loop through each category to get the count of blog posts
    for category in categories:
        # Count the number of blog posts in this category
        category["count"] = frappe.db.count(
            "Blog Post", filters={"blog_category": category["name"]}
        )

    # Return the categories with count
    response = {"categories": categories}

    return response


@frappe.whitelist(allow_guest=True)
def get_blog_details(meta_title):
    """
    Fetch blog details including ID, thumbnail image, title, description, tags, and comments.
    """
    blog_name = frappe.db.get_value("Blog Post", {"meta_title": meta_title}, "name")
    # Fetch the blog post document using the provided blog_id
    blog = frappe.get_doc("Blog Post", blog_name)

    # Fetch tags associated with the blog post
    tags = [
        tag.tag
        for tag in frappe.get_all(
            "Tag Link",
            filters={"document_type": "Blog Post", "document_name": blog_name},
            fields=["tag"],
        )
    ]

    # Fetch comments linked to the blog post
    comments = frappe.get_all(
        "Comment",
        filters={"reference_doctype": "Blog Post", "reference_name": blog_name},
        fields=["owner", "content", "creation"],
        order_by="creation desc",
    )

    # Format the response with the required fields
    blog_data = {
        "id": blog.name,
        "thumbnail_image": blog.custom_image,
        "title": blog.title,
        "description": blog.content,
        "meta_title": blog.meta_title,
        "tags": tags,
        "comments": comments,
    }

    return blog_data


@frappe.whitelist(allow_guest=True)
def get_blog_tags():
    """
    Fetch blog tags including ID and name.
    """
    # Fetch all blog tags from the Tag doctype
    tags = frappe.get_all(
        "Tag",
        fields=["name as id", "name as tag_name"],
        # Using 'name' as both ID and tag name
        order_by="creation desc",
    )

    # Format the response with tag details
    response = {"tags": tags}

    return response


@frappe.whitelist(allow_guest=True)
def get_gallery_list():
    """
    Fetches a list of galleries with their titles and associated images from the child doctype.
    """
    # Fetch all gallery documents
    galleries = frappe.get_all("Gallery", fields=["name", "title"])
    # Initialize an empty list for gallery data
    gallery_list = []

    # Iterate over each gallery and fetch associated images from the child doctype
    for gallery in galleries:
        # Fetch the gallery document
        gallery_doc = frappe.get_doc(
            "Gallery", gallery["name"], order_by="creation desc"
        )
        # Initialize dictionary to store gallery details
        gallery_data = {
            "name": gallery_doc.name,
            "title": gallery_doc.title,  # Get gallery title
            "images": [],  # Placeholder for child images
        }
        # Fetch child table data (Gallery Image)
        for (
            image
        ) in (
            gallery_doc.images
        ):  # 'images' is the fieldname for the child table in the parent doctype
            gallery_data["images"].append(
                {
                    "image": image.image  # Fieldname for the image path in the child doctype
                }
            )

        # Add the gallery and its images to the list
        gallery_list.append(gallery_data)

    # Return the list of galleries with their images
    return gallery_list


@frappe.whitelist(allow_guest=True)
def get_gallery_with_images(gallery_id):
    """
    Fetches the gallery title from the parent doctype and the images from the child doctype.
    """
    # Fetch the gallery document using the provided gallery_id
    gallery = frappe.get_doc("Gallery", gallery_id)

    # Initialize response dictionary with gallery details
    gallery_data = {
        "name": gallery.name,
        "title": gallery.title,
        "images": [],  # Placeholder for images from the child doctype
    }

    # Fetch child table data (Gallery Image)
    for (
        image
    ) in (
        gallery.images
    ):  # 'images' is the fieldname for the child table in the parent doctype
        gallery_data["images"].append(
            {"image": image.image}  # Fieldname for the image in the child doctype
        )

    # Return the gallery details with images
    return gallery_data


# Bkash Payment API Integration


def get_client():
    settings = frappe.get_single("LMS Settings")

    return {
        "api_url": settings.url,
        "razorpay_key": settings.razorpay_key,
        "razorpay_secret": settings.get_password(
            "razorpay_secret", raise_exception=True
        ),
        "merchant_number": settings.merchant_number,
        "merchant_password": settings.merchant_password,
        "payment_token_id": settings.payment_token_id,
        "payment_refresh_token_id": settings.payment_refresh_token_id,
        "razorpay_key": settings.razorpay_key,
        "merchant_association_info": settings.merchant_association_info,
    }


def grant_token():
    if frappe.session.user == "Guest":
        frappe.throw("You must be logged in to access this API", frappe.PermissionError)

    client = get_client()

    url = client["api_url"] + "/token/grant"

    payload = {
        "app_key": client["razorpay_key"],
        "app_secret": client["razorpay_secret"],
    }

    headers = {
        "accept": "application/json",
        "username": client["merchant_number"],
        "password": client["merchant_password"],
        "content-type": "application/json",
    }

    token_response = requests.post(url, json=payload, headers=headers)
    print(token_response.json())
    if token_response.status_code == 200:
        token_data = token_response.json()

        settings = frappe.get_doc("LMS Settings")
        settings.payment_token_id = token_data.get("id_token")
        settings.payment_refresh_token_id = token_data.get("refresh_token")
        settings.save(ignore_permissions=True)
        frappe.db.commit()

    else:
        frappe.throw(
            f"Error fetching token: {token_response.status_code} - {token_response.text}"
        )


def refresh_token():
    client = get_client()
    url = client["api_url"] + "/token/refresh"
    # if not client["payment_refresh_token_id"]:
    grant_token()
    client = get_client()

    payload = {
        "app_key": client["razorpay_key"],
        "app_secret": client["razorpay_secret"],
        "refresh_token": client["payment_refresh_token_id"],
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "username": client["merchant_number"],
        "password": client["merchant_password"],
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        # Save the new token details
        new_token_data = response.json()
        client["payment_token_id"] = new_token_data["id_token"]
        client["refresh_token"] = new_token_data["refresh_token"]

        settings = frappe.get_doc("LMS Settings")
        settings.payment_token_id = new_token_data["id_token"]
        settings.payment_refresh_token_id = new_token_data["refresh_token"]
        settings.save(ignore_permissions=True)
        frappe.db.commit()
        client = get_client()

    elif response.status_code == 401 and "expired" in response.text.lower():
        # If the refresh token has expired, call the grant_token function
        grant_token()

    else:
        frappe.throw(
            f"Error during token refresh: {response.status_code} - {response.text}"
        )


@frappe.whitelist()
def get_payment_options(doctype, docname, billing_name):
    current_user = frappe.session.user  # Get the logged-in user
    user_doc = frappe.get_doc("User", current_user)  # Fetch the User document
    user_doc.first_name = billing_name  # Update the first_name field
    user_doc.save()  # Save changes to the database
    frappe.db.commit()  # Commit changes to the database (if needed)
    # if not frappe.db.exists(doctype, docname):
    #     frappe.throw(_("Invalid document provided."))

    # validate_phone_number(phone, True)
    details = get_details(doctype, docname)

    options = {
        "key_id": frappe.db.get_single_value("LMS Settings", "razorpay_key"),
        "name": frappe.db.get_single_value("Website Settings", "app_name"),
        "description": _("Payment for {0} course").format(details["title"]),
        "order_id": f"Order-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "amount": details.amount,
        "currency": details.currency,
        "prefill": {
            "name": frappe.db.get_value("User", frappe.session.user, "full_name"),
            "email": frappe.session.user,
            "contact": frappe.db.get_value("User", frappe.session.user, "mobile_no"),
        },
    }
    response = checkout_payment(options, doctype, docname)
    return response


def checkout_payment(options, doctype, docname):
    client = get_client()

    url = client["api_url"] + "/create"

    if client["payment_token_id"] == None:
        print("REFRESH TOKEN")
        refresh_token()
        client = get_client()

    cache_key = f"checkout_{frappe.session.user}"

    frappe.cache().set_value(cache_key, {"doctype": doctype, "docname": docname})

    payload = {
        "mode": "0011",
        "payerReference": options["prefill"]["contact"],
        "callbackURL": frappe.utils.get_url() + "/lms/payment-status",
        "merchantAssociationInfo": client["merchant_association_info"],
        "amount": options["amount"],
        "currency": options["currency"],
        "merchantInvoiceNumber": options["order_id"],
        "intent": "sale",
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {client['payment_token_id']}",
        "X-App-Key": client["razorpay_key"],
    }

    checkout_response = requests.post(url, json=payload, headers=headers)

    if checkout_response.status_code == 200:
        return checkout_response.json()

    else:
        refresh_token()

        client = get_client()
        headers["Authorization"] = f"Bearer {client['payment_token_id']}"
        checkout_response = requests.post(url, json=payload, headers=headers)

        if checkout_response.status_code == 200:
            return checkout_response.json()

        else:
            grant_token()

            client = get_client()
            headers["Authorization"] = f"Bearer {client['payment_token_id']}"
            checkout_response = requests.post(url, json=payload, headers=headers)

            if checkout_response.status_code == 200:
                return checkout_response.json()

        frappe.throw(
            f"Error during checkout creation after retry: {checkout_response.status_code} - {checkout_response.text}"
        )


def get_details(doctype, docname):
    if doctype == "LMS Course":
        details = frappe.db.get_value(
            "LMS Course",
            {"meta_title": docname},
            [
                "name",
                "title",
                "paid_course",
                "currency",
                "discount_price",
                "course_price as amount",
                "amount_usd",
            ],
            as_dict=True,
        )
        if not details.paid_course:
            frappe.throw(_("This course is free."))
    else:
        details = frappe.db.get_value(
            "LMS Batch",
            docname,
            ["name", "title", "paid_batch", "currency", "amount", "amount_usd"],
            as_dict=True,
        )
        if not details.paid_batch:
            frappe.throw(_("To join this batch, please contact the Administrator."))
    if details.discount_price:
        details.amount = details.amount - details.discount_price
    return details


def save_address(address):
    filters = {"email_id": frappe.session.user}
    exists = frappe.db.exists("Address", filters)
    if exists:
        address_doc = frappe.get_last_doc("Address", filters=filters)
    else:
        address_doc = frappe.new_doc("Address")

    address_doc.update(address)
    address_doc.update(
        {
            "address_title": frappe.db.get_value(
                "User", frappe.session.user, "full_name"
            ),
            "address_type": "Billing",
            "is_primary_address": 1,
            "email_id": frappe.session.user,
            "address_line1": address.address_line1,
            "city": address.state,
        }
    )
    address_doc.save(ignore_permissions=True)
    return address_doc.name


@frappe.whitelist(allow_guest=False)
def execute_payment():
    payment_id = frappe.form_dict.get("paymentID")

    cache_key = f"checkout_{frappe.session.user}"
    cached_data = frappe.cache().get_value(cache_key)

    if not cached_data:
        frappe.throw("Cached data not found for this payment.")

    # Access the cached doctype, docname, and address
    doctype = cached_data.get("doctype")
    docname = cached_data.get("docname")
    details = get_details(doctype, docname)

    client = get_client()

    url = client["api_url"] + "/execute"

    settings = frappe.get_doc("LMS Settings")

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {settings.payment_token_id}",
        "X-App-Key": f"{settings.razorpay_key}",
    }

    payload = {"paymentID": payment_id}

    execute_response = requests.post(url, json=payload, headers=headers)

    frappe.log_error(execute_response.json(), "Payment Execution Response")
    response = execute_response.json()
    if response.get("statusMessage") == "Successful":
        docname = details["name"]
        payment = record_payment(response, doctype, docname, details)
        verify_payment(
            response=response,
            doctype=doctype,
            docname=docname,
            details=details,
            payment=payment,
        )
        course_name = details.get("title")  # Extract course name
        return {
            "status": "success",
            "course_name": course_name,
            "payment_response": response,
            "payment": payment,
        }
    else:
        return {
            "status": "failure",
            "message": response.get("message", "Payment failed"),
        }


def verify_payment(response, doctype, docname, details, payment):
    if doctype == "LMS Course":
        return create_membership(docname, payment)
    else:
        return add_student_to_batch(docname, payment)


def create_membership(course, payment):
    # Check if the user is already enrolled in the course
    existing_membership = frappe.db.exists(
        "LMS Enrollment", {"member": frappe.session.user, "course": course}
    )

    if existing_membership:
        return f"/lms/courses/{course}/learn/1-1"

    # Create a new LMS Enrollment document
    membership = frappe.new_doc("LMS Enrollment")
    membership.update(
        {"member": frappe.session.user, "course": course, "payment": payment.name}
    )
    membership.save(ignore_permissions=True)

    # Redirect to the course page
    return f"/lms/courses/{course}/learn/1-1"


def add_student_to_batch(batchname, payment):
    student = frappe.new_doc("Batch Student")
    current_count = frappe.db.count("Batch Student", {"parent": batchname})
    student.update(
        {
            "student": frappe.session.user,
            "payment": payment.name,
            "source": payment.source,
            "parent": batchname,
            "parenttype": "LMS Batch",
            "parentfield": "students",
            "idx": current_count + 1,
        }
    )
    student.save(ignore_permissions=True)
    return f"/batches/{batchname}"


def record_payment(response, doctype, docname, details):
    # address = frappe._dict(address)
    # address_name = save_address(address)

    payment_details = get_payment_details(doctype, docname)
    payment_doc = frappe.new_doc("LMS Payment")
    payment_doc.update(
        {
            "billing_name": frappe.db.get_value(
                "User", frappe.session.user, "full_name"
            ),
            "posting_date": datetime.now(),
            "member": frappe.session.user,
            "number": response["payerReference"],
            "payment_received": 1 if response["statusMessage"] == "Successful" else 0,
            "order_id": response["merchantInvoiceNumber"],
            "payment_id": response["paymentID"],
            "amount": payment_details["amount"],
            "currency": payment_details["currency"],
            "payment_for_document_type": doctype,
            "payment_for_document": docname,
        }
    )
    payment_doc.save(ignore_permissions=True)
    create_course_enrollment(member=frappe.session.user, course=details.name)
    frappe.db.commit()

    return payment_doc


def create_course_enrollment(member, course):
    """
    Create an LMS Enrollment for a given member and course.
    """
    # Check if an enrollment already exists for this member and course
    enrollment = frappe.get_all(
        "LMS Enrollment", filters={"member": member, "course": course}, limit=1
    )

    if enrollment:
        # Enrollment already exists
        return "Enrollment already exists."

    # Create a new enrollment if not found
    enrollment_doc = frappe.new_doc("LMS Enrollment")
    enrollment_doc.update(
        {
            "member": member,
            "course": course,
            "status": "Enrolled",  # Adjust the status as needed
        }
    )

    # Save the enrollment document
    enrollment_doc.save(ignore_permissions=True)
    frappe.db.commit()
    course_doc = frappe.get_doc("LMS Course", course)
    if course_doc.custom_total_enrolled is None:
        course_doc.custom_total_enrolled = 0  # Set to 0 if it is None
    course_doc.custom_total_enrolled += 1
    course_doc.save(ignore_permissions=True)

    return enrollment_doc


def get_payment_details(doctype, docname):
    amount_field = "course_price" if doctype == "LMS Course" else "amount"
    amount = frappe.db.get_value(doctype, docname, amount_field)
    currency = frappe.db.get_value(doctype, docname, "currency")

    return {"amount": amount, "currency": currency}


def update_user_enrolled_field(doc, method):
    """
    Updates the 'enrolled' field in the User doctype when a new LMS Enrollment is created.
    """
    user_email = doc.member

    if user_email:
        try:
            user_doc = frappe.get_doc("User", user_email)

            user_doc.enrolled = True

            user_doc.save(ignore_permissions=True)

            frappe.db.commit()
        except frappe.DoesNotExistError:
            frappe.log_error(
                f"User with email {user_email} not found", "Enrollment Error"
            )
        except Exception as e:
            frappe.log_error(str(e), "Enrollment Update Error")


# Login


def send_otp(identifier, one_time_key):
    """
    Send an OTP to the provided identifier (mobile or email).
    - If identifier is a mobile number, send via SMS.
    - If identifier is an email address, send via email.
    """
    try:
        # Check if identifier is an email or mobile number
        if validate_email_address(identifier):  # It's an email
            print(identifier, "EMAIL IDENTIFIER")
            return send_email_otp(identifier, one_time_key)
        else:  # Assume it's a mobile number
            return send_sms_otp(identifier, one_time_key)
    except Exception as e:
        frappe.log_error(message=str(e), title="OTP Sending Error")
        return {"response_code": 500, "message": "Failed to send OTP."}


def send_sms_otp(mobile_no, one_time_key):
    """Send an OTP via SMS to the provided mobile number."""
    lms_settings = frappe.get_single("LMS Settings")
    api_key = lms_settings.api_key
    sender_id = lms_settings.sender_id
    message = f"Your login OTP: {one_time_key}"
    api_url = (
        f"https://bulksmsbd.net/api/smsapi"
        f"?api_key={api_key}&type=text&senderid={sender_id}"
        f"&number={mobile_no}&message={message}"
    )

    # Rate-limiting logic: Allow a maximum of 3 OTPs per mobile_no per hour
    otp_limit_key = f"otp_limit:{mobile_no}"
    otp_count = frappe.cache().get_value(otp_limit_key) or 0

    if int(otp_count) >= 3:
        return {
            "response_code": 429,
            "message": "OTP request limit exceeded. Try again after an hour.",
        }

    try:
        # Send SMS
        sms_response = requests.post(api_url)
        response_data = sms_response.json()

        if sms_response.status_code == 202:
            # Increment OTP request count
            frappe.cache().set_value(
                otp_limit_key, int(otp_count) + 1, expires_in_sec=60 * 60
            )

        return {"response_code": 202, "message": "OTP sent successfully via SMS."}

    except requests.RequestException as e:
        frappe.log_error(message=str(e), title="SMS Sending Error")
        return {"response_code": 500, "message": "Failed to send OTP via SMS."}


def send_email_otp(email, one_time_key):
    """Send an OTP via email to the provided email address."""
    subject = "Your OTP for Login"

    # Rate-limiting logic: Allow a maximum of 3 OTPs per email per hour
    otp_limit_key = f"otp_limit:{email}"
    otp_count = frappe.cache().get_value(otp_limit_key) or 0

    if int(otp_count) >= 10:
        return {
            "response_code": 429,
            "message": "OTP request limit exceeded. Try again after an hour.",
        }

    try:
        print(email, "SENDING EMAIL ..........")
        # Send email
        frappe.sendmail(
            recipients=[email],
            subject=subject,
            message=one_time_key,
        )
        print("EMAIL SENT ..........")

        # Increment OTP request count
        frappe.cache().set_value(
            otp_limit_key, int(otp_count) + 1, expires_in_sec=60 * 60
        )

        return {"response_code": 202, "message": "OTP sent successfully via email."}

    except Exception as e:
        frappe.log_error(message=str(e), title="Email Sending Error")
        return {"response_code": 500, "message": "Failed to send OTP via email."}


@frappe.whitelist(allow_guest=True)
def create_user_with_mobile_or_email_and_generate_link(identifier: str):
    """
    Create a user with a given mobile number or email and generate a one-time login key.

    Args:
        identifier (str): Mobile number or email of the user.

    Returns:
        dict: A dictionary containing the key (if new user created) and password flag.
    """
    try:
        if not identifier:
            frappe.throw(
                "Identifier is mandatory. Please provide a valid email address or mobile number."
            )

        # Temporarily switch to Administrator to perform necessary actions
        frappe.set_user("Administrator")

        # Validate identifier and determine the search field
        if validate_email_address(identifier):
            search_field, value = "email", identifier
        elif validate_phone_number(identifier):
            search_field, value = "mobile_no", identifier
        else:
            frappe.throw("Please enter a valid email address or mobile number.")

        # Check for uniqueness
        existing_user = frappe.db.get_value(
            "User", {search_field: value}, ["email", "name", "enabled"]
        )
        if existing_user:
            return {"password": True, "key": None}  # User exists and has a password

        # Generate a unique one-time key
        one_time_key = random.randint(1000, 9999)

        # Handle SMS OTP for mobile numbers
        if search_field == "mobile_no":
            unique_suffix = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=8)
            )
            email = f"user_{unique_suffix}@example.com"
        else:
            email = identifier

        sms_response = send_otp(identifier, f"Your login otp: :{one_time_key}")
        print(sms_response)
        if sms_response["response_code"] == 202:

            # Create a new user
            user = frappe.get_doc(
                {
                    "doctype": "User",
                    "email": email,
                    "first_name": f"User_{email.split('@')[0]}",
                    "enabled": 1,
                    "mobile_no": identifier if search_field == "mobile_no" else None,
                    "send_welcome_email": 0,
                }
            )
            user.insert(ignore_permissions=True)
            user.add_roles("LMS Student")
            frappe.db.commit()

            # Cache the one-time key for 1 hour
            cache_key = f"one_time_login_key:{one_time_key}"
            frappe.cache().set_value(cache_key, value, expires_in_sec=60 * 60)

            return {"key": one_time_key, "password": False}
        else:
            return {"message": sms_response.message}

    except frappe.ValidationError as ve:
        frappe.log_error(message=str(ve), title="Validation Error")
        return {"message": str(ve), "status": "error"}

    except Exception as e:
        frappe.log_error(message=str(e), title="User Creation Error")
        return {
            "message": "An unexpected error occurred. Please try again.",
            "status": "error",
        }

    finally:
        # Revert to Guest user after processing
        frappe.set_user("Guest")


@frappe.whitelist(allow_guest=True)
def resend_otp(identifier: str):
    """
    Resends OTP to the given mobile number.

    Args:
        mobile (str): Mobile number to resend the OTP to.

    Returns:
        dict: Response message indicating success or failure.
    """
    try:
        if not identifier:
            frappe.throw("Mobile number is mandatory.")

        # Generate a new 4-digit OTP
        one_time_key = random.randint(1000, 9999)

        # Send the OTP via SMS
        sms_response = send_otp(identifier, f"Your login otp: {one_time_key}")

        if sms_response["response_code"] == 202:
            # Cache the OTP for 1 hour
            otp_key = f"one_time_login_key:{one_time_key}"
            frappe.cache().set_value(otp_key, identifier, expires_in_sec=3600)

            # Return success message
            return {"message": sms_response}
        else:
            frappe.throw(sms_response.get("message", "Failed to send OTP"))
    except frappe.ValidationError as ve:
        frappe.log_error(message=str(ve), title="OTP Resend Validation Error")
        return {"message": str(ve)}
    except Exception as e:
        frappe.log_error(message=str(e), title="OTP Resend Error")
        return {"message": "An error occurred while resending the OTP."}


@frappe.whitelist(allow_guest=True)
def login_via_key(key: str):
    cache_key = f"one_time_login_key:{key}"
    identifier = frappe.cache.get_value(cache_key)
    if identifier:
        frappe.cache.delete_value(cache_key)

        if "@" in identifier:
            # Identifier is an email
            user = frappe.db.get_value("User", {"email": identifier}, "email")
            username = frappe.db.get_value("User", {"email": identifier}, "username")
        else:
            # Identifier is a mobile number
            user = frappe.db.get_value("User", {"mobile_no": identifier}, "email")
            username = frappe.db.get_value(
                "User", {"mobile_no": identifier}, "username"
            )
        if not user:
            frappe.throw(_("User with this mobile number does not exist."))
        # Log in the user
        frappe.local.login_manager.login_as(user)
        # Return a success response or redirect
        return {"message": "Login successful", "user": user, "username": username}
    else:
        frappe.respond_as_web_page(
            _("Not Permitted"),
            _("The link you are trying to use is invalid or expired."),
            http_status_code=403,
            indicator_color="red",
        )


@frappe.whitelist(allow_guest=False)
def update_user_profile(
    name,
    mobile,
    email,
    gender,
    birthDate=None,
    district=None,
    address=None,
    newPassword=None,
    confirmPassword=None,
):
    try:
        errors = []

        # Validate required fields
        if not name:
            errors.append("Name is required.")
        if not mobile:
            errors.append("Mobile number is required.")
        elif not validate_phone_number(mobile):
            errors.append("Invalid mobile number format.")
        if not email:
            errors.append("Email address is required.")
        elif not validate_email_address(email):
            errors.append("Invalid email address format.")
        if not gender:
            errors.append("Gender is required.")
        if not birthDate:
            errors.append("Birth date is required.")
        if not district:
            errors.append("District is required.")
        if not address:
            errors.append("Address is required.")

        # Validate password fields
        if newPassword or confirmPassword:
            if newPassword != confirmPassword:
                errors.append("New password and confirm password do not match.")

        # If there are any validation errors, throw them
        if errors:
            frappe.throw("<br>".join(errors))

        # Get the current user
        user = frappe.session.user

        if user == "Guest":
            frappe.throw("You must be logged in to update your profile.")

        # Fetch the user document
        user_doc = frappe.get_doc("User", user)

        # Update the user fields
        user_doc.first_name = name
        user_doc.last_name = ""
        user_doc.mobile_no = mobile
        user_doc.gender = gender
        user_doc.birth_date = birthDate
        user_doc.address = address
        user_doc.location = district

        # Update password if provided
        if newPassword:
            update_password(user, newPassword)
        user_doc.save(ignore_permissions=True)

        # Check and update email if it has changed
        if user_doc.email != email:
            frappe.rename_doc("User", user_doc.name, email)
            user_doc = frappe.get_doc(
                "User", email
            )  # Reload the user doc after renaming
            # Clear session cache for the current user and email
            frappe.cache().delete_value(f"current_user:{user}")
            frappe.cache().delete_value(f"current_user:{email}")

            # Force logout to clear the session
            frappe.local.login_manager.logout()
            # Save the updated user document
            user_doc.save(ignore_permissions=True)

        frappe.db.commit()

        return {
            "message": "Profile updated successfully.",
            "emailChanged": user_doc.email != frappe.session.user,
        }

    except frappe.ValidationError as ve:
        frappe.log_error(message=str(ve), title="Profile Update Validation Error")
        frappe.throw(str(ve))
    except Exception as e:
        frappe.log_error(message=str(e), title="Profile Update Error")
        frappe.throw("An unexpected error occurred. Please try again.")


@frappe.whitelist(allow_guest=True)
def reset_otp(identifier: str):
    """
    Resets the OTP for a given mobile number and sends a new OTP via SMS.

    Args:
        mobile (str): Mobile number of the user.

    Returns:
        dict: A dictionary with the reset status and message.
    """
    try:
        # Validate mobile number
        if not identifier:
            frappe.throw("Mobile number is required.")

        if validate_email_address(identifier):
            search_field, value = "email", identifier
        elif validate_phone_number(identifier):
            search_field, value = "mobile_no", identifier

        # Check if the user exists
        user = frappe.db.get_value("User", {search_field: value}, "name")
        if not user:
            frappe.throw("No user found with the provided mobile number.")

        # Generate a new OTP
        new_otp = random.randint(1000, 9999)
        # Cache the OTP for 1 hour
        otp_key = f"one_time_login_key:{new_otp}"
        frappe.cache().set_value(otp_key, identifier, expires_in_sec=3600)
        print(otp_key, "otp_key")
        # Send the OTP via SMS
        sms_response = send_otp(identifier, otp_key)
        print(sms_response, "SMS RESPONSE")

        return {"message": sms_response}

    except frappe.ValidationError as ve:
        frappe.log_error(message=str(ve), title="OTP Reset Validation Error")
        return {
            "message": str(ve),
            "status": "error",
        }
    except Exception as e:
        frappe.log_error(message=str(e), title="OTP Reset Error")
        return {
            "message": "An unexpected error occurred while resetting the OTP. Please try again later.",
            "status": "error",
        }


@frappe.whitelist(allow_guest=True)
def download_pdf(
    doctype,
    name,
    format=None,
    doc=None,
    no_letterhead=0,
    language=None,
    letterhead=None,
):
    doc = doc or frappe.get_doc(doctype, name)
    validate_print_permission(doc)

    with print_language(language):
        pdf_file = frappe.get_print(
            doctype,
            name,
            format,
            doc=doc,
            as_pdf=True,
            letterhead=letterhead,
            no_letterhead=no_letterhead,
        )

    frappe.local.response.filename = "{name}.pdf".format(
        name=name.replace(" ", "-").replace("/", "-")
    )
    frappe.local.response.filecontent = pdf_file
    frappe.local.response.type = "pdf"
