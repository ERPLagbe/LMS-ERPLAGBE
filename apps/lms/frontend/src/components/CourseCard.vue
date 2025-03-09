<template>
	<div
		v-if="course.title"
		class="flex flex-col h-full shadow-md text-base overflow-auto"
		style="min-height: 350px"
	>
		<div
			class="course-image"
			:class="{ 'default-image': !course.image }"
			:style="{ backgroundImage: 'url(\'' + encodeURI(course.image) + '\')' }"
		>
			<div
				class="flex items-center flex-wrap space-y-1 space-x-1 relative top-4 px-2 w-fit"
			>
				<Badge v-if="course.featured" variant="subtle" theme="green" size="md">
					{{ __('Featured') }}
				</Badge>
				<Badge
					variant="outline"
					theme="gray"
					size="md"
					v-for="tag in course.tags"
				>
					{{ tag }}
				</Badge>
			</div>
			<div v-if="!course.image" class="image-placeholder">
				{{ course.title[0] }}
			</div>
		</div>
		<div class="flex flex-col flex-auto p-4">
			<div class="flex items-center gap-2 mb-2">
				<div v-if="course.lesson_count" class="bg-[#00434133] px-2 py-1">
					<Tooltip :text="__('Lessons')">
						<span class="flex items-center text-sm text-[#004341]">
							<BookOpen class="h-4 w-4 stroke-1.5 text-[#004341] mr-1" />
							{{ course.lesson_count }}টি
						</span>
					</Tooltip>
				</div>

				<div v-if="course.enrollment_count" class="bg-[#00434133] px-2 py-1">
					<Tooltip :text="__('Enrolled Students')">
						<span class="flex items-center text-sm text-[#004341]">
							<Users class="h-4 w-4 stroke-1.5 text-[#004341] mr-1" />
							{{ course.enrollment_count }}জন
						</span>
					</Tooltip>
				</div>
			</div>

			<div class="border-b border-dashed my-3 border-[#DFDFDF]"></div>

			<div class="text-xl font-semibold leading-6 mb-3">
				{{ course.title }}
			</div>

			<ProgressBar
				v-if="user && course.membership"
				:progress="course.membership.progress"
			/>

			<div v-if="user && course.membership" class="text-sm mb-4">
				{{ Math.ceil(course.membership.progress) }}% completed
			</div>

			<div class="flex items-center justify-between mt-auto">
				<div class="flex avatar-group overlap">
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
				<div v-if="user && course.membership">
					<Badge theme="red">Purchased</Badge>
				</div>
				<div v-else>
					<div class="font-semibold">
						{{ course.price }}
					</div>
					<div
						v-if="course.discount_price > 0"
						class="font-semibold line-through text-red-500"
					>
						৳ {{ course.course_price }}
					</div>
				</div>
			</div>
		</div>
		<button
			:class="{
				'mt-2 px-4 py-2 text-white text-sm md:text-lg': true,
				'bg-blue-500 hover:bg-blue-800': user && course.membership,
				'bg-[#004341] hover:bg-[#004341d8]': !user || !course.membership,
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
	height: 168px;
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
