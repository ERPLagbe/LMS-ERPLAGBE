<template>{{ props.type }}{{ props.name }}</template>

<script setup>
import { createResource } from 'frappe-ui'
console.log('Checkout')
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
console.log(props.name)
console.log(props.type)

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

console.log(orderSummary.data, 'orderSummary.data')
</script>
