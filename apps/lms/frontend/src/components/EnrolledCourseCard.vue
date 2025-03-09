<template>
	<div
		v-if="course"
		class="flex flex-col h-full rounded-md shadow-md text-base overflow-auto bg-[#00434126] px-5 py-3"
		style="min-height: 150px"
	>
		<div class="flex justify-between gap-5">
			<div class="flex flex-col gap-4 w-2/3 md:w-1/2">
				<div class="text-sm md:text-xl font-semibold leading-6">
					{{ course.title }}
				</div>
				<div class="flex items-center justify-between mb-2">
					<div class="flex flex-row gap-3">
						<div
							v-if="course.lesson_count"
							class="bg-[#00434133] text-sm px-2 py-1"
						>
							<Tooltip :text="__('Lessons')">
								<span class="flex items-center">
									<BookOpen class="h-4 w-4 stroke-1.5 text-gray-700 mr-1" />
									{{ course.lesson_count }}টি
								</span>
							</Tooltip>
						</div>

						<div
							v-if="course.enrollment_count"
							class="bg-[#00434133] text-sm px-2 py-1"
						>
							<Tooltip :text="__('Enrolled Students')">
								<span class="flex items-center">
									<Users class="h-4 w-4 stroke-1.5 text-gray-700 mr-1" />
									{{ course.enrollment_count }}জন
								</span>
							</Tooltip>
						</div>
					</div>
				</div>
			</div>
			<div class="w-1/3 md:w-1/2">
				<img
					:src="course.image"
					alt="Course Image"
					class="w-full h-full object-contain rounded-sm"
				/>
			</div>
		</div>
		<div class="flex flex-col flex-auto p-4">
			<div class="mb-4">
				<div v-if="user && course.membership" class="text-sm mb-1">
					{{ Math.ceil(course.membership.progress) }}%
				</div>
				<ProgressBar
					v-if="user && course.membership"
					:progress="course.membership.progress"
				/>
			</div>
			<div class="flex gap-5 items-center justify-between mt-auto">
				<div class="flex avatar-group overlap w-1/2">
					<div
						class="h-6 mr-1"
						:class="{ 'avatar-group overlap': course.instructors.length > 1 }"
					>
						<UserAvatar
							v-for="instructor in course.instructors"
							:user="instructor"
						/>
					</div>
					<CourseInstructors :instructors="course.instructors" />
				</div>
				<button
					:class="{
						'mt-2 px-4 py-2 text-sm md:text-lg': true,
						'bg-[#c2e31fd0] hover:bg-[#c2e31f] w-1/2 text-[#004341]':
							user && course.membership,
						'bg-[#004341da] hover:bg-[#004341] text-white':
							!user || !course.membership,
					}"
				>
					{{
						user && course.membership
							? course.membership.progress > 0
								? 'কোর্সটি চালিয়ে যান'
								: 'কোর্সটি শুরু করুন'
							: 'বিস্তারিত'
					}}
				</button>
			</div>
		</div>
	</div>
</template>
<script setup>
import { BookOpen, Users, Star } from 'lucide-vue-next'
import UserAvatar from '@/components/UserAvatar.vue'
import { sessionStore } from '@/stores/session'
import { Badge, Tooltip } from 'frappe-ui'
import CourseInstructors from '@/components/CourseInstructors.vue'
import ProgressBar from '@/components/ProgressBar.vue'

const { user } = sessionStore()

const props = defineProps({
	course: {
		type: Object,
		default: null,
	},
})
</script>
<style>
.course-image {
	height: 238px;
	width: 100%;
	background-size: cover;
	background-position: center;
	background-repeat: no-repeat;
}

.course-card-pills {
	background: #ffffff;
	margin-left: 0;
	margin-right: 0.5rem;
	padding: 3.5px 8px;
	font-size: 11px;
	text-align: center;
	letter-spacing: 0.011em;
	text-transform: uppercase;
	font-weight: 600;
	width: fit-content;
}

.default-image {
	display: flex;
	flex-direction: column;
	align-items: center;
	background-color: theme('colors.green.100');
	color: theme('colors.green.600');
}

.avatar-group {
	display: inline-flex;
	align-items: center;
}

.avatar-group .avatar {
	transition: margin 0.1s ease-in-out;
}
.image-placeholder {
	display: flex;
	align-items: center;
	flex: 1;
	font-size: 5rem;
	color: theme('colors.gray.700');
	font-weight: 600;
}
.avatar-group.overlap .avatar + .avatar {
	margin-left: calc(-8px);
}

.short-introduction {
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	text-overflow: ellipsis;
	width: 100%;
	overflow: hidden;
	margin: 0.25rem 0 1.25rem;
	line-height: 1.5;
}
</style>
