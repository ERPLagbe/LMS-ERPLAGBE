<template>
	<div class="flex flex-col items-center justify-center h-screen">
		<div
			class="w-5/6 md:w-3/6 flex flex-col justify-center items-center gap-6 bg-white p-6 md:p-8 rounded-lg drop-shadow-[0px_0px_6px_rgba(0,0,0,0.25)]"
		>
			<!-- Status Icon -->
			<img
				v-if="statusMessage === 'Successful'"
				class="w-20"
				src="../assets/images/Success-Icon.png"
				alt="Success Icon"
			/>
			<img
				v-else
				class="w-20"
				src="../assets/images/Cross-Icon.png"
				alt="Error Icon"
			/>

			<!-- Status Message -->
			<p class="text-sm" v-if="statusMessage === 'Successful'">
				আপনি আমাদের <b>{{ courseName }}</b> কোর্সে ভর্তি সম্পন্ন করেছেন
			</p>
			<hr class="divide-y divide-dashed" />

			<!-- Details -->
			<div class="w-full flex justify-between">
				<p class="font-bold text-sm">নাম</p>
				<p class="text-sm">{{ user_name }}</p>
			</div>
			<div class="w-full flex justify-between">
				<p class="font-bold text-sm">ফোন নম্বর</p>
				<p class="text-sm">+88{{ phoneNumber }}</p>
			</div>
			<div class="w-full flex justify-between">
				<p class="font-bold text-sm">দাম</p>
				<p class="text-sm">৳ {{ coursePrice }}</p>
			</div>
			<div class="w-full flex justify-between">
				<p class="font-bold text-sm">পেমেন্ট স্টেটাস</p>
				<p class="text-sm" v-if="statusMessage === 'Successful'">Successful</p>
				<p class="text-sm" v-else>Failed</p>
			</div>

			<!-- Payment Date & Time -->
			<div class="w-full" v-if="statusMessage === 'Successful'">
				<div class="w-full flex justify-between">
					<p class="font-bold text-sm">তারিখ</p>
					<p class="text-sm">{{ formattedDate }}</p>
				</div>
				<div class="w-full flex justify-between">
					<p class="font-bold text-sm">সময়</p>
					<p class="text-sm">{{ formattedTime }}</p>
				</div>
			</div>

			<!-- Payment Method -->
			<div class="w-full flex justify-between">
				<p class="font-bold text-sm">পেমেন্ট মেথড</p>
				<p class="text-sm">বিকাশ</p>
			</div>

			<!-- Buttons (Only visible if status is Successful) -->
			<div
				class="w-full flex justify-center gap-4"
				v-if="statusMessage === 'Successful'"
			>
				<a
					v-if="paymentName"
					class="rounded-lg border border-[#004341] px-5 py-2"
					target="_blank"
					:href="`/api/method/lms_api.api.download_pdf?doctype=LMS Payment&name=${paymentName}`"
				>
					<p class="text-sm text-[#004341]">ইনভয়েস ডাউনলোড করুন</p>
				</a>
				<button
					v-if="courseName"
					@click="handleRoute"
					class="rounded-lg bg-[#004341] px-5 py-2"
				>
					<p class="text-white text-sm text-[#004341]">কোর্সটি শুরু করুন</p>
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import { inject } from 'vue'

export default {
	data() {
		return {
			user_name: inject('$user')?.data.full_name || '',
			courseName: '', // Course Name
			statusMessage: '', // Payment Status
			formattedDate: '', // Formatted Date
			formattedTime: '', // Formatted Time
			paymentName: '',
			phoneNumber: '',
			coursePrice: '',
		}
	},
	mounted() {
		this.setStatusFromURL() // Set status from URL
		this.fetchPaymentStatus() // Fetch payment details
		this.setCurrentDateTime() // Set current date and time
	},
	methods: {
		// Extract status from the URL
		setStatusFromURL() {
			const queryParams = new URLSearchParams(window.location.search)
			this.statusMessage =
				queryParams.get('status') === 'success' ? 'Successful' : 'Failed'
		},

		// Fetch payment details from the backend
		async fetchPaymentStatus() {
			try {
				const queryParams = new URLSearchParams(window.location.search)
				const response = await fetch(
					`/api/method/lms_api.api.execute_payment?${queryParams.toString()}`,
				)

				if (!response.ok) {
					throw new Error(`HTTP error! Status: ${response.status}`)
				}

				const data = await response.json()

				if (data.message.status !== 'failure') {
					this.courseName = data?.message?.course_name
					this.paymentName = data?.message?.payment.name
					this.phoneNumber = data?.message?.payment.number
					this.coursePrice = data?.message?.payment.amount
				}

				// Set the payment execution date and time
				this.setCurrentDateTime()
			} catch (error) {
				console.error('Failed to fetch payment details:', error)
				this.statusMessage = 'Failed'
			}
		},

		// Route to the course learning page
		handleRoute() {
			if (this.courseName) {
				window.location.href = '/lms/courses'
			}
		},

		// Set the current date and time in Bengali locale
		setCurrentDateTime() {
			const now = new Date()
			const optionsDate = { year: 'numeric', month: 'short', day: 'numeric' }
			const optionsTime = { hour: '2-digit', minute: '2-digit', hour12: true }

			this.formattedDate = now.toLocaleDateString('bn-BD', optionsDate)
			this.formattedTime = now.toLocaleTimeString('bn-BD', optionsTime)
		},
	},
}
</script>

<style>
.status-message {
	margin-top: 20px;
	padding: 15px;
	border: 1px solid #ccc;
	border-radius: 5px;
	background-color: #f9f9f9;
	color: #333;
	font-size: 16px;
	text-align: center;
}
</style>
