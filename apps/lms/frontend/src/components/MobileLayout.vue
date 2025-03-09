<template>
	<div class="flex h-full flex-col">
		<div class="h-full pb-10" id="scrollContainer">
			<slot />
		</div>
		<div
			v-if="sidebarSettings.data"
			class="fixed flex justify-around border-t border-gray-300 bottom-0 z-10 w-full bg-white standalone:pb-4 shadow-md"
			:style="{
				gridTemplateColumns: `repeat(${sidebarLinks.length}, minmax(0, 1fr))`,
			}"
		>
			<button
				v-for="tab in sidebarLinks"
				:key="tab.label"
				:class="isVisible(tab) ? 'block' : 'hidden'"
				class="flex flex-row gap-2 items-center justify-center py-3 transition active:scale-95"
				@click="handleClick(tab)"
			>
				<component
					:is="icons[tab.icon]"
					class="h-4 w-4 stroke-1.5"
					:class="[isActive(tab) ? 'text-gray-900' : 'text-gray-600']"
				/>
				<span class="text-sm">{{ tab.label }}</span>
			</button>
		</div>
	</div>
</template>
<script setup>
import { getSidebarLinks } from '../utils'
import { useRouter } from 'vue-router'
import { computed, ref, onMounted } from 'vue'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/user'
import * as icons from 'lucide-vue-next'

const { logout, user, sidebarSettings } = sessionStore()
let { isLoggedIn } = sessionStore()
const router = useRouter()
let { userResource } = usersStore()
const sidebarLinks = ref(getSidebarLinks())

onMounted(() => {
	sidebarSettings.reload(
		{},
		{
			onSuccess(data) {
				Object.keys(data).forEach((key) => {
					if (!parseInt(data[key])) {
						sidebarLinks.value = sidebarLinks.value.filter(
							(link) => link.label.toLowerCase().split(' ').join('_') !== key,
						)
					}
				})
				addAccessLinks()
			},
		},
	)
})

const addAccessLinks = () => {
	if (user) {
		sidebarLinks.value.push({
			label: 'প্রোফাইল',
			icon: 'UserRound',
			activeFor: [
				'Profile',
				'ProfileAbout',
				'ProfileCertification',
				'ProfileEvaluator',
				'ProfileRoles',
			],
		})
		sidebarLinks.value.push({
			label: 'লগ আউট',
			icon: 'LogOut',
		})
	} else {
		sidebarLinks.value.push({
			label: 'লগ ইন',
			icon: 'LogIn',
		})
	}
	if (userResource?.data?.is_instructor) {
		sidebarLinks.value.push({
			label: 'App',
			icon: 'Box',
			to: '/app/lms',
		})
	}
}

let isActive = (tab) => {
	return tab.activeFor?.includes(router.currentRoute.value.name)
}

const handleClick = (tab) => {
	if (tab.label == 'লগ ইন') window.location.href = '/login'
	else if (tab.label == 'লগ আউট')
		logout.submit().then(() => {
			isLoggedIn = false
		})
	else if (tab.label == 'প্রোফাইল')
		window.location.href = `/lms/user/${userResource.data?.username}`
	// router.push({
	// 	name: 'Profile',
	// 	params: {
	// 		username: userResource.data?.username,
	// 	},
	// })
	// else router.push({ name: tab.to });
	else window.location.href = `/lms/${tab.to}`
}

const isVisible = (tab) => {
	if (tab.label == 'লগ ইন') return !isLoggedIn
	else if (tab.label == 'লগ আউট') return isLoggedIn
	else return true
}
</script>
