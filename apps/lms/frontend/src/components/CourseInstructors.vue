<template>
	<span v-if="instructors.length == 1">
		<router-link
			:to="{
				name: 'Profile',
				params: { username: instructors[0].username },
			}"
		>
			<p class="text-sm md:text-lg font-medium">
				{{ instructors[0].full_name }}
			</p>
		</router-link>
	</span>
	<span v-if="instructors.length == 2">
		<router-link
			:to="{
				name: 'Profile',
				params: { username: instructors[0].username },
			}"
		>
			{{ instructors[0].first_name }}
		</router-link>
		and
		<router-link
			:to="{
				name: 'Profile',
				params: { username: instructors[1].username },
			}"
		>
			{{ instructors[1].first_name }}
		</router-link>
	</span>
	<span v-if="instructors.length > 2">
		<router-link
			:to="{
				name: 'Profile',
				params: { username: instructors[0].username },
			}"
		>
			{{ instructors[0].first_name }}
		</router-link>
		and {{ instructors.length - 1 }} others
	</span>
</template>
<script setup>
const props = defineProps({
	instructors: {
		type: Array,
		required: true,
	},
})
</script>
