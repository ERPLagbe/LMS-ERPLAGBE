<template>
	<div v-if="access?.data" class="flex flex-col items-center justify-center">
		<div
			class="navbar w-full flex justify-center items-center p-2 shadow-md bg-white z-50"
		>
			<img
				src="../assets/images/jobayer-academy-logo.png"
				alt="Logo"
				class="w-24 h-10"
			/>
		</div>

		<!-- Stepper -->
		<div class="flex items-center justify-between w-5/6 my-8">
			<div
				v-for="(step, index) in steps"
				:key="index"
				:class="[
					'flex items-center',
					index === steps.length - 1 ? '' : 'w-full',
				]"
			>
				<div class="flex flex-col items-center w-[40px]">
					<p class="-translate-y-4 text-xs font-semibold text-[#004341]">
						{{ steps[index] }}
					</p>
					<!-- Step Number -->
					<div
						:class="[
							'w-4 h-4 flex items-center justify-center rounded-full border-2',
							currentStep === index
								? 'bg-[#004341] text-white border-[#004341]'
								: index < currentStep
									? 'bg-[#004341] text-white border-[#004341]'
									: 'bg-white text-gray-500 border-[#004341]',
						]"
					></div>
				</div>

				<!-- Connector Line -->
				<div
					v-if="index < steps.length - 1"
					class="flex-1 h-0.5 mr-2 translate-y-2 w-[40px]"
					:class="[index < currentStep ? 'bg-[#004341]' : 'bg-gray-300']"
				></div>
			</div>
		</div>
		<!-- Step Content -->
		<div class="w-5/6">
			<div
				class="grid grid-cols-1 gap-8 md:grid-cols-3"
				v-if="currentStep === 0"
			>
				<div class="col-span-1 md:col-span-2">
					<!-- Course Details Section -->
					<OrderSummary :orderSummary="orderSummary" />
				</div>
				<!-- Login Section -->
				<div
					class="bg-white p-6 md:p-8 rounded-lg drop-shadow-[0px_0px_6px_rgba(0,0,0,0.25)]"
				>
					<h2 class="text-[#004341] text-lg md:text-xl font-bold mb-6 md:mb-5">
						লগ ইন
					</h2>
					<p class="text-sm">
						পেমেন্ট সম্পন্ন করতে মোবাইল নাম্বার দিয়ে এগিয়ে যান
					</p>
					<input
						type="tel"
						v-model="phoneNumber"
						class="w-full p-2 border border-gray-300 rounded-lg my-6 md:my-14"
						placeholder="মোবাইল নাম্বার"
					/>
					<button
						@click="sendSms"
						class="w-full bg-[#004341] text-white p-2 rounded-lg text-[#C3E31F]"
					>
						এগিয়ে যান
					</button>
				</div>
			</div>
			<div
				class="grid grid-cols-1 gap-8 md:grid-cols-3"
				v-if="currentStep === 1"
			>
				<div class="col-span-1 md:col-span-2">
					<!-- Course Details Section -->
					<OrderSummary :orderSummary="orderSummary" />
				</div>

				<div class="relative">
					<!-- Navigation Buttons -->
					<div class="flex justify-between my-2 absolute top-3 right-3 z-10">
						<button
							v-if="currentStep === 1"
							@click="prevStep"
							:disabled="currentStep === 0"
							class="px-2 py-1 bg-green-800 text-white rounded hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								width="24"
								height="24"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
								class="lucide lucide-arrow-big-left"
							>
								<path d="M18 15h-6v4l-7-7 7-7v4h6v6z" />
							</svg>
						</button>
						<!-- <button
				@click="nextStep"
				:disabled="currentStep === steps.length - 1"
				class="px-4 py-2 bg-[#004341] text-white rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
			>
				Next
			</button> -->
					</div>

					<!-- OTP Section -->
					<div
						v-if="isPassword"
						class="bg-white p-6 md:p-8 rounded-lg drop-shadow-[0px_0px_6px_rgba(0,0,0,0.25)]"
					>
						<h2
							class="text-[#004341] text-lg md:text-xl font-bold mb-6 md:mb-5"
						>
							পাসওয়ার্ড
						</h2>
						<div class="flex gap-4 justify-start mt-6">
							<div class="relative">
								<input
									:type="showPassword ? 'text' : 'password'"
									class="border border-gray-300 rounded-lg text-center text-lg focus:outline-none focus:border-[#004341] focus:ring-[#004341]"
									v-model="password"
									placeholder="পাসওয়ার্ড"
								/>
								<button
									type="button"
									class="absolute right-3 top-1/2 transform -translate-y-1/2"
									@click="togglePasswordVisibility"
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										width="24"
										height="24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
										stroke-linecap="round"
										stroke-linejoin="round"
										class="feather feather-eye"
									>
										<path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z" />
										<circle cx="12" cy="12" r="3" />
									</svg>
								</button>
							</div>
						</div>
						<button
							class="text-right text-sm my-4 text-[#FF8D4D] cursor-pointer"
							@click="resetPassword"
						>
							পাসওয়ার্ড রিসেট
						</button>
						<button
							@click="loginWithPassword"
							class="w-full bg-[#004341] text-white p-2 rounded-lg mt-6 text-[#C3E31F]"
						>
							এগিয়ে যান
						</button>
					</div>

					<!-- OTP Section -->
					<div
						v-else
						class="bg-white p-6 md:p-8 rounded-lg drop-shadow-[0px_0px_6px_rgba(0,0,0,0.25)] relative"
					>
						<h2
							class="text-[#004341] text-lg md:text-xl font-bold mb-6 md:mb-5"
						>
							ভেরিফিকেশন কোড
						</h2>
						<p class="text-sm">
							+88{{ mobileNo }} মোবাইল নম্বরে পাঠানো ৪ সংখ্যার কোডটি এখানে
							লিখুন।
						</p>

						<div class="flex gap-4 justify-start mt-6">
							<input
								v-for="(digit, index) in otp"
								:key="index"
								type="text"
								maxlength="1"
								class="w-12 h-12 border border-gray-300 rounded-lg text-center text-lg focus:outline-none focus:border-[#004341] focus:ring-[#004341]"
								@input="handleInput($event, index)"
								@keydown.backspace="handleBackspace($event, index)"
							/>
						</div>
						<button
							class="text-right text-sm my-4 text-[#FF8D4D] cursor-pointer"
							@click="resendOtp"
						>
							আবার কোড পাঠান
						</button>
						<button
							@click="loginWithOtp"
							class="w-full bg-[#004341] text-white p-2 rounded-lg mt-6 text-[#C3E31F]"
						>
							এগিয়ে যান
						</button>
					</div>
				</div>
			</div>
			<div
				class="grid grid-cols-1 gap-4 lg:gap-8 md:grid-cols-3"
				v-if="currentStep === 2"
			>
				<div class="col-span-1 md:col-span-2">
					<!-- Course Details Section -->
					<OrderSummary :orderSummary="orderSummary" />
				</div>
				<!-- Payment Section -->
				<div
					class="bg-white p-6 md:p-8 rounded-lg drop-shadow-[0px_0px_6px_rgba(0,0,0,0.25)]"
				>
					<p class="text-md font-bold mb-2">নাম</p>
					<input
						type="text"
						class="w-full p-2 border border-gray-300 rounded-lg"
						placeholder="নাম"
						v-model="billingDetails.billing_name"
					/>
					<h2 class="text-[#004341] text-lg md:text-xl font-bold my-6 md:my-5">
						পেমেন্ট মেথড
					</h2>
					<!-- I want here one check box  with an image -->
					<div
						class="flex justify-between mb-4 bg-white p-2 md:p-4 rounded-lg drop-shadow-[0px_0px_6px_rgba(0,0,0,0.25)]"
					>
						<div class="flex gap-2">
							<input
								type="radio"
								name="payment-method"
								class="mr-2 accent-[#004341]"
								checked
							/>
							<label
								for="card"
								class="w-full flex justify-between items-center text-sm font-bold"
								>বিকাশ <img class="w-20" src="" alt=""
							/></label>
						</div>
						<img src="../assets/images/bkash.png" class="w-14 h-4" />
					</div>
					<button
						@click="generateBkashPaymentLink()"
						class="w-full bg-[#004341] text-white p-2 rounded-lg text-[#C3E31F]"
					>
						এগিয়ে যান
					</button>
				</div>
			</div>
			<div
				class="w-full my-2 bg-[#F0F0F0] flex flex-col gap-4 p-5 justify-center items-center rounded"
			>
				<p class="text-2xl text-[#004341] font-bold">সাহায্য প্রয়োজন?</p>
				<p class="text-center">
					কাস্টোমার কেয়ারের সাথে কথা বলতে কল করুন
					<a href="tel:01780440087" class="text-underline text-blue-500"
						>০১৭৮০৪৪০০৮৭</a
					>
					নাম্বারে
				</p>
			</div>
		</div>
	</div>
</template>
<script setup>
import NotPermitted from '@/components/NotPermitted.vue'
import { createToast } from '@/utils/'
import { Button, createResource, Input } from 'frappe-ui'
import { inject, onMounted, reactive, ref, nextTick, watch } from 'vue'
import OrderSummary from '../components/OrderSummary.vue'

const user = inject('$user')

const currentStep = ref(0)
const isPassword = ref(false)
const showPassword = ref(false)
const mobileNo = ref('')
const password = ref('')
const fullName = ref('')
const steps = ['লগ ইন', 'ভেরিফিকেশন', 'পেমেন্ট']
const otp = reactive(['', '', '', ''])

function togglePasswordVisibility() {
	showPassword.value = !showPassword.value
}

onMounted(() => {
	fullName.value = user.data.full_name.startsWith('User_')
		? ''
		: user.data.full_name
	if (user.data) {
		currentStep.value = 2
	} else {
		currentStep.value = 0
	}
})

function nextStep() {
	if (currentStep.value < steps.length - 1) {
		currentStep.value++
	}
}

// Navigate to the previous step
function prevStep() {
	if (currentStep.value > 0) {
		currentStep.value--
	}
}

// Handle input in OTP fields
function handleInput(event, index) {
	const input = event.target
	const value = event.target.value
	otp[index] = value // Store the digit
	if (index < otp.length - 1) {
		const nextInput = input.nextElementSibling
		if (nextInput) nextInput.focus()
	}
}

// Handle backspace to move focus to the previous input
function handleBackspace(event, index) {
	const input = event.target
	if (event.key === 'Backspace') {
		// Clear the current field and move to the previous field if it's empty
		if (!input.value && index > 0) {
			const prevInput = input.previousElementSibling
			if (prevInput) {
				prevInput.focus()
				prevInput.value = '' // Clear the previous input field
				otp[index - 1] = ''
			}
		}
	}
}

// Send SMS via API
async function sendSms() {
	const phoneNumber = document.querySelector('input[type="tel"]').value
	mobileNo.value = phoneNumber
	// Remove non-numeric characters
	const cleaned = phoneNumber.replace(/\D/g, '')

	// Frappe API endpoint
	const frappeApiUrl =
		'/api/method/lms_api.api.create_user_with_mobile_or_email_and_generate_link'
	const frappeApiPayload = { identifier: cleaned } // Payload to send to Frappe API

	try {
		// Step 1: Call Frappe API to generate one-time login link
		const frappeResponse = await fetch(frappeApiUrl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(frappeApiPayload),
		})

		if (!frappeResponse.ok) {
			const errorText = await frappeResponse.text()
			console.error('Frappe API error response:', errorText)
			alert(
				'Failed to call Frappe API. Please check your server configuration.',
			)
			return
		}

		const frappeResult = await frappeResponse.json()
		if (!frappeResult.message.key) {
			isPassword.value = true
		}
		currentStep.value++
	} catch (error) {
		// Handle any network or other errors
		console.error('Error occurred:', error)
		alert('An error occurred while processing your request.')
	}
}

async function loginWithPassword() {
	const apiEndpoint = '/api/method/login' // Replace with your Frappe site URL

	// Prepare login payload
	const payload = {
		usr: mobileNo.value, // Use the phone number directly as the username
		pwd: password.value, // Password entered by the user
	}

	try {
		// Make a POST request to the login API
		const response = await fetch(apiEndpoint, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			},
			body: new URLSearchParams(payload),
		})

		if (!response.ok) {
			alert('Invalid credentials')
			throw new Error(`Login failed: ${response.statusText}`)
		}

		const result = await response.json()

		if (result && result.message === 'Logged In') {
			window.location.reload()
			currentStep.value++
			// Handle successful login here, such as storing session info or tokens
			return result
		} else {
			alert('Invalid credentials')
			throw new Error('Invalid credentials or unexpected response')
		}
	} catch (error) {
		console.error('Error during login:', error.message)
		// Handle login failure here
		return null
	}
}

async function loginWithOtp() {
	const loginResponse = await fetch(
		`/api/method/lms_api.api.login_via_key?key=${Number(otp.join(''))}`,
		{
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
		},
	)
	if (loginResponse.ok) {
		const loginResult = loginResponse.json()
		currentStep.value++ // Proceed to the next step
	} else {
		const errorText = loginResponse.text()
		console.error('Login API error response:', errorText)
		alert('Failed to log in. Please try again.')
	}
}

async function resendOtp() {
	if (mobileNo) {
		try {
			const response = await fetch(`/api/method/lms_api.api.resend_otp`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ identifier: mobileNo.value }),
			})

			const data = await response.json()
			console.log(data, 'resend otp')
			if (data.message.message.response_code === 202) {
				alert(data.message.message.message)
			}
		} catch (error) {
			alert('An error occurred. Please try again.')
		}
	} else {
		alert('Mobile number is missing.')
	}
}

async function resetPassword() {
	const otpSection = document.getElementById('otp-section')
	const passwordSection = document.getElementById('password-section')

	if (mobileNo) {
		try {
			const response = await fetch(`/api/method/lms_api.api.reset_otp`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ identifier: mobileNo.value }),
			})

			const data = await response.json()
			console.log(data.message.message, 'reset password')
			isPassword.value = false
			if (data.message.message.response_code === 202) {
				alert(data.message.message.message)
			} else {
				alert('Password reset failed. Please try again.')
			}
		} catch (error) {
			alert('An error occurred. Please try again.')
		}
	} else {
		alert('Mobile number is missing.')
	}
}

onMounted(() => {
	access.submit()
})

const props = defineProps({
	type: {
		type: String,
		required: true,
	},
	name: {
		type: String,
		required: true,
	},
})

const access = createResource({
	url: 'lms.lms.api.validate_billing_access',
	params: {
		type: props.type,
		name: props.name,
	},
	onSuccess(data) {
		orderSummary.submit()
		setBillingDetails(data.address)
	},
})

const getImageUrl = (imagePath) => {
	const baseDomain = window.location.origin
	return `${baseDomain}/${imagePath}`
}

const orderSummary = createResource({
	url: 'lms.lms.utils.get_order_summary',
	makeParams(values) {
		return {
			doctype: props.type == 'course' ? 'LMS Course' : 'LMS Batch',
			docname: props.name,
			country: billingDetails.country,
		}
	},
	onError(err) {
		showError(err)
	},
})

const billingDetails = reactive({})

const setBillingDetails = (data) => {
	billingDetails.billing_name = fullName
	billingDetails.address_line1 = data.address_line1 || ''
	billingDetails.city = data.city || ''
	billingDetails.state = data.state || 'Dhaka'
	billingDetails.country = data.country || ''
	billingDetails.pincode = data.pincode || ''
	billingDetails.phone = data.phone || ''
	billingDetails.source = data.source || ''
	billingDetails.gstin = data.gstin || ''
	billingDetails.pan = data.pan || ''
}

const paymentOptions = createResource({
	url: 'lms_api.api.get_payment_options',
	makeParams(values) {
		return {
			doctype: props.type == 'course' ? 'LMS Course' : 'LMS Batch',
			docname: props.name,
			billing_name: billingDetails.billing_name,
		}
	},
})

const generateBkashPaymentLink = async () => {
	paymentOptions.submit(
		{},
		{
			validate(params) {
				return validateAddress()
			},
			onSuccess(data) {
				const bkashURL = data.bkashURL
				if (bkashURL) {
					window.location.href = bkashURL
				} else {
					console.error('Payment URL not found in the API response')
				}
			},
			onError(err) {
				showError(err)
			},
		},
	)
}

const generatePaymentLink = () => {
	paymentOptions.submit(
		{},
		{
			validate(params) {
				return validateAddress()
			},
			onSuccess(data) {
				data.handler = (response) => {
					let doctype = props.type == 'course' ? 'LMS Course' : 'LMS Batch'
					let docname = props.name
					handleSuccess(response, doctype, docname, data.order_id)
				}
				let rzp1 = new Razorpay(data)
				rzp1.open()
			},
			onError(err) {
				showError(err)
			},
		},
	)
}

const paymentResource = createResource({
	url: 'lms_api.api.verify_payment',
	makeParams(values) {
		return {
			response: values.response,
			doctype: props.type == 'course' ? 'LMS Course' : 'LMS Batch',
			docname: props.name,
			address: billingDetails,
			order_id: values.orderId,
		}
	},
})

const handleSuccess = (response, doctype, docname, orderId) => {
	paymentResource.submit(
		{
			response: response,
			orderId: orderId,
		},
		{
			onSuccess(data) {
				createToast({
					title: 'Success',
					text: 'Payment Successful',
					icon: 'check',
					iconClasses: 'bg-green-600 text-white rounded-md p-px',
				})
				setTimeout(() => {
					window.location.href = data
				}, 3000)
			},
		},
	)
}

const validateAddress = () => {
	let mandatoryFields = ['billing_name']
	for (let field of mandatoryFields) {
		if (!billingDetails[field])
			return (
				'Please enter a valid ' +
				field
					.replaceAll('_', ' ')
					.toLowerCase()
					.replace(/\b\w/g, (s) => s.toUpperCase())
			)
	}
}

const showError = (err) => {
	createToast({
		title: 'Error',
		text: err.messages?.[0] || err,
		icon: 'x',
		iconClasses: 'bg-red-600 text-white rounded-md p-px',
		position: 'top-center',
		timeout: 10,
	})
}

const changeCurrency = (country) => {
	billingDetails.country = country
	orderSummary.reload()
}
</script>

<style>
.sidebar {
	display: none;
}
</style>
