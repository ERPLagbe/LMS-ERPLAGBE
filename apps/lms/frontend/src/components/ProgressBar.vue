<template>
	<div class="w-full bg-white rounded-full h-[10px] my-2">
		<div
			class="bg-[#004341] h-[10px] rounded-full"
			:style="{ width: progressBarWidth }"
		></div>
	</div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
	progress: {
		type: Number,
		default: 0,
	},
})

const progressBarWidth = computed(() => {
	const formattedPercentage = Math.min(Math.ceil(props.progress), 100)
	return `${formattedPercentage}%`
})
</script>
