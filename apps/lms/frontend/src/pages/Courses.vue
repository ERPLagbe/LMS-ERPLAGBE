<template>
	<div v-if="courses.data">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-white px-3 py-2.5 sm:px-5"
		>
			<div class="flex gap-4">
				<img src="../assets/images/jobayer-academy-logo.png" class="w-22 h-8" />
			</div>
			<div class="flex space-x-2 justify-end">
				<div class="w-36">
					<FormControl
						type="text"
						placeholder="Search"
						v-model="searchQuery"
						@input="courses.reload()"
					>
						<template #prefix>
							<Search class="w-4 h-4 stroke-1.5 text-gray-600" name="search" />
						</template>
					</FormControl>
				</div>
				<router-link
					:to="{
						name: 'CourseForm',
						params: {
							courseName: 'new',
						},
					}"
				>
					<Button v-if="user.data?.is_moderator" variant="solid">
						<template #prefix>
							<Plus class="h-4 w-4" />
						</template>
						{{ __('New Course') }}
					</Button>
				</router-link>
			</div>
		</header>
		<div class="">
			<Tabs
				v-model="tabIndex"
				tablistClass="overflow-x-visible flex-wrap !gap-3 md:flex-nowrap"
				:tabs="makeTabs"
			>
				<template #tab="{ tab, selected }" class="hidden">
					<div>
						<button
							class="hidden group -mb-px items-center gap-2 overflow-hidden border-b border-transparent py-2.5 text-base text-gray-600 duration-300 ease-in-out hover:border-gray-400 hover:text-gray-900"
							:class="{ 'text-gray-900': selected }"
						>
							<component v-if="tab.icon" :is="tab.icon" class="h-5 hidden" />
							{{ __(tab.label) }}
							<Badge theme="gray" class="hidden">
								{{ tab.count }}
							</Badge>
						</button>
					</div>
				</template>
				<template #default="{ tab }">
					<div class="flex justify-between">
						<h4
							class="text-3xl text-[#004341] font-bold my-6 text-underline mx-5"
						>
							আমার <span class="text-[#c3e31f]">কোর্স</span>সমূহ
						</h4>
						<a
							href="https://www.facebook.com/groups/jobayeracademybd/?ref=share&mibextid=NSMWBT"
							target="_blank"
							class="flex justify-center items-center gap-2 bg-[#0866FF] p-2 mt-3 h-10 mr-4"
						>
							<div class="bg-white">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									width="16"
									height="16"
									viewBox="0 0 24 24"
									fill="#0866FF"
									stroke="#FFFFFF"
									stroke-width="1"
									stroke-linecap="round"
									stroke-linejoin="round"
									class="lucide lucide-facebook"
								>
									<path
										d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"
									/>
								</svg>
							</div>
							<p class="text-sm text-white">Facebook Group</p>
						</a>
					</div>
					<div
						v-if="
							tab.courses &&
							tab.courses.value.filter((course) => course.membership).length
						"
						class="grid grid-cols-1 md:grid-cols-2 gap-5 my-5 mx-5"
					>
						<router-link
							v-for="course in tab.courses.value.filter(
								(course) => course.membership,
							)"
							:to="
								course.membership && course.current_lesson
									? {
											name: 'Lesson',
											params: {
												courseName: course.name,
												chapterNumber: course.current_lesson.split('-')[0],
												lessonNumber: course.current_lesson.split('-')[1],
											},
										}
									: course.membership
										? {
												name: 'Lesson',
												params: {
													courseName: course.name,
													chapterNumber: 1,
													lessonNumber: 1,
												},
											}
										: {
												name: 'CourseDetail',
												params: { courseName: course.name },
											}
							"
						>
							<EnrolledCourseCard :course="course" />
							<!-- <CourseCard :course="course" /> -->
						</router-link>
					</div>
					<div v-else class="my-5 mx-5 text-red-700 text-center">
						কোন কোর্স এনরোল করা হয়নি
					</div>
					<h4
						class="text-3xl text-[#004341] font-bold my-6 text-underline mx-5"
					>
						অন্যান্য <span class="text-[#c3e31f]">কোর্স</span>সমূহ
					</h4>
					<div
						v-if="tab.courses && tab.courses.value.length"
						class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 my-5 mx-5"
					>
						<!-- <router-link
							v-for="course in tab.courses.value.filter(
								(course) => !course.membership,
							)"
							:to="{
								name: 'CourseDetail',
								params: { courseName: course.name },
							}"
						>
							<CourseCard :course="course" />
						</router-link> -->
						<a
							v-for="course in tab.courses.value.filter(
								(course) => !course.membership,
							)"
							:href="`/lms/courses/${course.name}`"
							:key="course.name"
						>
							<CourseCard :course="course" />
						</a>
					</div>
					<div
						v-else
						class="grid flex-1 place-items-center text-xl font-medium text-gray-500"
					>
						<div class="flex flex-col items-center justify-center mt-4">
							<div>
								{{ __('No {0} courses found').format(tab.label.toLowerCase()) }}
							</div>
						</div>
					</div>
				</template>
			</Tabs>
		</div>
	</div>
	<ProfileInfoModal
		v-if="isModalVisible"
		:showCloseBtn="false"
		:isVisible="isModalVisible"
		:showPasswordModal="false"
		@close="toggleModal"
	/>
</template>

<script setup>
import {
	Breadcrumbs,
	Tabs,
	Badge,
	Button,
	FormControl,
	createResource,
} from 'frappe-ui'
import CourseCard from '@/components/CourseCard.vue'
import { Plus, Search } from 'lucide-vue-next'
import { ref, computed, inject, onMounted } from 'vue'
import { updateDocumentTitle } from '@/utils'
import ProfileInfoModal from '../components/Modals/ProfileInfoModal.vue'
import EnrolledCourseCard from '../components/EnrolledCourseCard.vue'

const user = inject('$user')
const searchQuery = ref('')

// Check if all required fields exist
const hasRequiredData = !(
	user?.data?.address &&
	user?.data?.birth_date &&
	user?.data?.gender &&
	user?.data?.mobile_no &&
	user?.data?.location &&
	user?.data?.full_name
)

const isModalVisible = ref(user.data ? hasRequiredData : false)

function toggleModal() {
	isModalVisible.value = !isModalVisible.value
}

const courses = createResource({
	url: 'lms.lms.utils.get_courses',
	cache: ['courses', user.data?.email],
	auto: true,
})

const tabIndex = ref(0)
let tabs

const makeTabs = computed(() => {
	tabs = []
	addToTabs('Live')
	// addToTabs('New')
	// addToTabs('Upcoming')

	// if (user.data) {
	// 	addToTabs('Enrolled')

	// 	if (
	// 		user.data.is_moderator ||
	// 		user.data.is_instructor ||
	// 		courses.data?.created?.length
	// 	) {
	// 		addToTabs('Created')
	// 	}

	// 	if (user.data.is_moderator) {
	// 		addToTabs('Under Review')
	// 	}
	// }
	return tabs
})

const addToTabs = (label) => {
	let courses = getCourses(label.toLowerCase().split(' ').join('_'))
	tabs.push({
		label,
		courses: computed(() => courses),
		count: computed(() => courses.length),
	})
}

const getCourses = (type) => {
	if (searchQuery.value) {
		let query = searchQuery.value.toLowerCase()
		return courses.data[type].filter(
			(course) =>
				course.title.toLowerCase().includes(query) ||
				course.short_introduction.toLowerCase().includes(query) ||
				course.tags.filter((tag) => tag.toLowerCase().includes(query)).length,
		)
	}
	return courses.data[type]
}

const pageMeta = computed(() => {
	return {
		title: 'Courses',
		description: 'All Courses divided by categories',
	}
})

updateDocumentTitle(pageMeta)
</script>
