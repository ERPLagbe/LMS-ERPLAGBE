<template>
	<div v-if="isVisible" class="flex">
		<div
			class="bg-white rounded-lg shadow-lg p-6 w-full max-w-3xl relative overflow-y-auto max-h-[80vh] sm:max-h-[90vh]"
		>
			<!-- Form -->
			<form
				@submit.prevent="submitForm"
				class="grid grid-cols-1 gap-4 sm:grid-cols-2"
			>
				<!-- Name -->
				<div>
					<label class="block text-sm font-semibold text-gray-700 mb-1"
						>নাম</label
					>
					<input
						type="text"
						v-model="form.name"
						placeholder="আপনার পুরো নাম লিখুন"
						class="w-full border border-gray-300 rounded-lg p-2 text-sm"
					/>
				</div>

				<!-- Email -->
				<div>
					<label class="block text-sm font-semibold text-gray-700 mb-1">
						ইমেইল
					</label>
					<input
						type="email"
						v-model="form.email"
						placeholder="আপনার ইমেইল লিখুন"
						class="w-full border border-gray-300 rounded-lg p-2 text-sm"
						:readonly="user.email.startsWith('user_') ? false : true"
					/>
				</div>

				<!-- Mobile Number -->
				<div>
					<label class="block text-sm font-semibold text-gray-700 mb-1"
						>মোবাইল নাম্বার</label
					>
					<input
						type="text"
						v-model="form.mobile"
						placeholder="অনুগ্রহ করে আপনার 11 সংখ্যার ফোন নম্বর দিন"
						class="w-full border border-gray-300 rounded-lg p-2 text-sm"
						:readonly="user.mobile_no ? true : false"
					/>
				</div>

				<!-- Gender -->
				<div class="col-span-1 sm:col-span-2">
					<label class="block text-sm font-semibold text-gray-700 mb-1"
						>লিঙ্গ</label
					>
					<div class="flex space-x-2">
						<button
							type="button"
							@click="setGender('Male')"
							:class="genderClass('Male')"
							class="px-4 py-2 rounded-lg"
						>
							পুরুষ
						</button>
						<button
							type="button"
							@click="setGender('Female')"
							:class="genderClass('Female')"
							class="px-4 py-2 rounded-lg"
						>
							মহিলা
						</button>
						<button
							type="button"
							@click="setGender('Other')"
							:class="genderClass('Other')"
							class="px-4 py-2 rounded-lg"
						>
							অন্যান্য
						</button>
					</div>
				</div>

				<!-- Birth Date -->
				<div>
					<label class="block text-sm font-semibold text-gray-700 mb-1"
						>জন্ম তারিখ</label
					>
					<input
						type="date"
						v-model="form.birthDate"
						class="w-full border border-gray-300 rounded-lg p-2 text-sm"
					/>
				</div>

				<!-- District -->
				<div>
					<label class="block text-sm font-semibold text-gray-700 mb-1"
						>জেলা</label
					>
					<select
						v-model="form.district"
						class="w-full border border-gray-300 rounded-lg p-2 text-sm"
					>
						<option value="" disabled>জেলা নির্বাচন করুন</option>
						<option
							v-for="district in districts"
							:key="district"
							:value="district"
						>
							{{ district }}
						</option>
					</select>
				</div>

				<!-- Detailed Address -->
				<div class="col-span-1 sm:col-span-2">
					<label class="block text-sm font-semibold text-gray-700 mb-1"
						>বিস্তারিত ঠিকানা</label
					>
					<textarea
						v-model="form.address"
						placeholder="বাড়ি, রাস্তা, শহর, এলাকা, ইত্যাদি"
						class="w-full border border-gray-300 rounded-lg p-2 text-sm"
					></textarea>
				</div>

				<!-- Submit Button -->
				<div class="col-span-1 sm:col-span-2">
					<button
						type="submit"
						:disabled="isSubmitting"
						class="bg-[#004341] text-white w-full py-2 rounded-lg text-sm font-medium"
						:class="{ 'opacity-50 cursor-not-allowed': isSubmitting }"
					>
						<span v-if="isSubmitting">Loading...</span>
						<span v-else>Save</span>
					</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		isVisible: {
			type: Boolean,
			required: true,
		},
	},
	data() {
		return {
			isSubmitting: false,
			user: null,
			form: {
				name: '',
				mobile: '',
				email: '',
				gender: '',
				birthDate: '',
				district: '',
				address: '',
				newPassword: '',
				confirmPassword: '',
			},
			districts: [
				'ঢাকা',
				'চট্টগ্রাম',
				'রাজশাহী',
				'খুলনা',
				'বরিশাল',
				'সিলেট',
				'ময়মনসিংহ',
				'রংপুর',
				'বাগেরহাট',
				'বান্দরবান',
				'বগুড়া',
				'বরগুনা',
				'ভোলা',
				'চাঁদপুর',
				'চাঁপাইনবাবগঞ্জ',
				'চুয়াডাঙ্গা',
				'কুমিল্লা',
				'কক্সবাজার',
				'দিনাজপুর',
				'ফরিদপুর',
				'ফেনী',
				'গাইবান্ধা',
				'গাজীপুর',
				'গোপালগঞ্জ',
				'হবিগঞ্জ',
				'জামালপুর',
				'যশোর',
				'ঝালকাঠি',
				'ঝিনাইদহ',
				'জয়পুরহাট',
				'খাগড়াছড়ি',
				'কিশোরগঞ্জ',
				'কুড়িগ্রাম',
				'কুষ্টিয়া',
				'লক্ষ্মীপুর',
				'লালমনিরহাট',
				'মাদারীপুর',
				'মাগুরা',
				'মানিকগঞ্জ',
				'মেহেরপুর',
				'মৌলভীবাজার',
				'নওগাঁ',
				'নড়াইল',
				'নেত্রকোনা',
				'নীলফামারী',
				'নোয়াখালী',
				'পাবনা',
				'পঞ্চগড়',
				'পটুয়াখালী',
				'পিরোজপুর',
				'রাঙ্গামাটি',
				'সাতক্ষীরা',
				'শরীয়তপুর',
				'শেরপুর',
				'সুনামগঞ্জ',
				'টাঙ্গাইল',
				'ঠাকুরগাঁও',
			],
		}
	},
	methods: {
		async fetchUserDetails() {
			try {
				const response = await fetch('/api/method/lms.lms.api.get_user_info', {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
					},
				})

				if (!response.ok) {
					throw new Error('Failed to fetch user info')
				}

				const data = await response.json()
				this.user = data.message
				if (data.message) {
					this.form.name =
						data.message.full_name &&
						!data.message.full_name.startsWith('User_')
							? data.message.full_name
							: ''
					this.form.email =
						data.message.email && !data.message.email.startsWith('user_')
							? data.message.email
							: ''
					this.form.mobile = data.message.mobile_no || ''
					this.form.gender = data.message.gender || ''
					this.form.birthDate = data.message.birth_date || ''
					this.form.district = data.message.location || ''
					this.form.address = data.message.address || ''
				}
			} catch (error) {
				console.error('Error fetching user details:', error)
				alert('ব্যবহারকারীর তথ্য আনতে সমস্যা হয়েছে।')
			}
		},
		setGender(gender) {
			this.form.gender = gender
		},
		genderClass(gender) {
			return this.form.gender === gender
				? 'bg-[#004341] text-white'
				: 'bg-gray-200 text-gray-800'
		},
		async submitForm() {
			// Ensure all required fields are filled
			if (!this.form.name || !this.form.mobile || !this.form.gender) {
				alert('অনুগ্রহ করে সব ফিল্ড পূরণ করুন।')
				return
			}

			// Set submitting state
			this.isSubmitting = true

			try {
				// Construct the payload
				const payload = {
					name: this.form.name,
					mobile: this.form.mobile,
					email: this.form.email,
					gender: this.form.gender,
					birthDate: this.form.birthDate,
					district: this.form.district,
					address: this.form.address,
					newPassword: this.form.newPassword,
					confirmPassword: this.form.confirmPassword,
				}
				// Call the API
				const response = await fetch(
					'/api/method/lms_api.api.update_user_profile',
					{
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
						},
						body: JSON.stringify(payload),
					},
				)

				const data = await response.json()
				if (!response.ok) {
					let serverMessages = data._server_messages

					try {
						// Parse the JSON string to extract messages
						let messages = JSON.parse(serverMessages)

						if (messages.length > 0) {
							// Parse and log only the first message
							let parsedMessage = JSON.parse(messages[0]) // Parse the first individual message
							alert(parsedMessage.message) // Log the "message" field
						}
					} catch (error) {
						console.error('Failed to parse server messages:', error)
					}
					throw new Error('Network response was not ok')
				} else {
					// Check if the email has changed
					if (data.message && data.message.emailChanged) {
						// Redirect to login if the email has changed
						window.location.href = '/login'
					} else {
						window.location.reload(true)
					}
				}
			} catch (error) {
				console.error('Error updating profile:', error)
			} finally {
				// Reset submitting state
				this.isSubmitting = false
			}
		},
	},
	mounted() {
		this.fetchUserDetails()
	},
}
</script>

<style scoped>
div[role='dialog'] {
	overflow-y: auto;
	max-height: 90vh; /* For better accessibility on mobile devices */
}
</style>
