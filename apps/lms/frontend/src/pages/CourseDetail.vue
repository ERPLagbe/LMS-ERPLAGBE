<template>
	<div v-if="course.data">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-white px-3 py-2.5 sm:px-5"
		>
			<div class="flex gap-4">
				<img src="../assets/images/jobayer-academy-logo.png" class="w-22 h-8" />
			</div>
		</header>
		<div class="m-5">
			<div class="text-3xl font-semibold mb-5">
				{{ course.data.title }}
			</div>
			<div class="flex justify-between gap-5 w-full">
				<div class="w-full md:w-2/3">
					<div class="my-4">
						<img
							:src="course.data.image"
							alt="Course Image"
							class="w-full h-full object-contain rounded-sm shadow-md"
						/>
					</div>
					<div class="my-3 leading-6">
						{{ course.data.short_introduction }}
					</div>
					<div class="flex items-center">
						<Tooltip
							v-if="course.data.avg_rating"
							:text="__('Average Rating')"
							class="flex items-center"
						>
							<Star class="h-5 w-5 text-gray-100 fill-orange-500" />
							<span class="ml-1">
								{{ course.data.avg_rating }}
							</span>
						</Tooltip>
						<span v-if="course.data.avg_rating" class="mx-3">&middot;</span>
						<Tooltip
							v-if="course.data.enrollment_count"
							:text="__('Enrolled Students')"
							class="flex items-center"
						>
							<Users class="h-4 w-4 text-gray-700" />
							<span class="ml-1">
								{{ course.data.enrollment_count_formatted }}
							</span>
						</Tooltip>
						<span v-if="course.data.enrollment_count" class="mx-3"
							>&middot;</span
						>
						<div class="flex items-center">
							<span
								class="h-6 mr-1"
								:class="{
									'avatar-group overlap': course.data.instructors.length > 1,
								}"
							>
								<UserAvatar
									v-for="instructor in course.data.instructors"
									:user="instructor"
								/>
							</span>
							<CourseInstructors :instructors="course.data.instructors" />
						</div>
					</div>
					<div class="flex mt-3 mb-4 w-fit">
						<Badge
							theme="gray"
							size="lg"
							class="mr-2"
							v-for="tag in course.data.tags"
						>
							{{ tag }}
						</Badge>
					</div>
					<CourseCardOverlay :course="course" class="md:hidden mb-4" />
					<div
						v-html="course.data.description"
						class="course-description"
					></div>
					<div class="mt-10">
						<CourseOutline :courseName="course.data.name" :showOutline="true" />
					</div>
					<CourseReviews
						:courseName="course.data.name"
						:avg_rating="course.data.avg_rating"
						:membership="course.data.membership"
					/>
				</div>
				<div class="mt-3 hidden md:block">
					<CourseCardOverlay :course="course" />
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import { createResource, Breadcrumbs, Badge, Tooltip } from 'frappe-ui'
import { computed, ref } from 'vue'
import { Users, Star } from 'lucide-vue-next'
import CourseCardOverlay from '@/components/CourseCardOverlay.vue'
import CourseOutline from '@/components/CourseOutline.vue'
import CourseReviews from '@/components/CourseReviews.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import { updateDocumentTitle } from '@/utils'
import CourseInstructors from '@/components/CourseInstructors.vue'

const props = defineProps({
	courseName: {
		type: String,
		required: true,
	},
})

const course = createResource({
	url: 'lms.lms.utils.get_course_details',
	cache: ['course', props.courseName],
	params: {
		course: props.courseName,
	},
	auto: true,
})

const breadcrumbs = computed(() => {
	let items = [{ label: 'All Courses', route: { name: 'Courses' } }]
	items.push({
		label: course?.data?.title,
		route: { name: 'CourseDetail', params: { course: course?.data?.name } },
	})
	return items
})

const pageMeta = computed(() => {
	return {
		title: course?.data?.title,
		description: course?.data?.short_introduction,
	}
})

updateDocumentTitle(pageMeta)
</script>
<style>
.course-description p {
	margin-bottom: 1rem;
	line-height: 1.7;
}
.course-description li {
	line-height: 1.7;
}

.course-description ol {
	list-style: auto;
	margin: revert;
	padding: revert;
}

.course-description ul {
	list-style: disc;
	margin: revert;
	padding: revert;
}

.avatar-group {
	display: inline-flex;
	align-items: center;
}

.avatar-group .avatar {
	transition: margin 0.1s ease-in-out;
}
</style>
