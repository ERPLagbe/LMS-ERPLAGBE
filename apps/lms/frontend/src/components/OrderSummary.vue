<template>
	<div
		class="h-auto md:col-span-2 flex flex-col gap-4 lg:gap-8 bg-white p-6 md:p-8 rounded-lg drop-shadow-[0px_0px_6px_rgba(0,0,0,0.25)]"
	>
		<h1 class="text-lg md:text-xl font-semibold">অর্ডার</h1>
		<div class="h-auto md:h-[150px] flex flex-col md:flex-row gap-2 lg:gap-4">
			<div class="w-full md:w-1/3">
				<img
					class="w-full h-[180px] md:h-full object-cover rounded-lg"
					:src="orderSummary.data.image"
					alt="checkout"
				/>
			</div>
			<div class="flex flex-col justify-between mt-4 md:mt-0 w-full md:w-2/3">
				<h1 class="text-lg md:text-xl text-[#434242] font-semibold">
					{{ orderSummary.data.title }}
				</h1>
				<div class="flex justify-between mt-4 md:mt-0">
					<p class="text-sm text-[#434242]">কোর্সের মূল্য:</p>
					<p class="font-bold">
						{{ orderSummary.data.amount }}
					</p>
				</div>
			</div>
		</div>
		<hr class="divide-y divide-dashed" />
		<div class="flex justify-between">
			<h1 class="text-sm text-[#434242]">ডিসকাউন্ট মূল্য:</h1>
			<p class="text-sm font-bold">
				{{ orderSummary.data.discount_price }}
			</p>
		</div>
		<hr class="divide-y divide-dashed" />
		<div class="flex justify-between">
			<h1 class="text-sm text-[#434242]">সাব টোটাল</h1>
			<p class="text-sm font-bold">
				{{ orderSummary.data.total_amount_formatted }}
			</p>
		</div>
		<hr class="divide-y divide-dashed" />
		<div class="flex justify-between">
			<h1 class="text-xl text-[#434242]">সর্বমোট</h1>
			<p class="text-sm font-bold">
				{{ orderSummary.data.total_amount_formatted }}
			</p>
		</div>
	</div>
</template>

<script>
export default {
	name: 'OrderSummary',
	props: {
		orderSummary: {
			type: Object,
			required: true,
		},
	},
}
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
