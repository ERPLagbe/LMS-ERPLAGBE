<template>
	<div v-if="quiz.data">
		<div class="bg-blue-100 py-2 px-2 mb-4 rounded-md text-sm text-blue-800">
			<div class="leading-relaxed">
				{{
					__('This quiz consists of {0} questions.').format(questions.length)
				}}
			</div>
			<div v-if="quiz.data.passing_percentage" class="leading-relaxed">
				{{
					__(
						'You will have to get {0}% correct answers in order to pass the quiz.',
					).format(quiz.data.passing_percentage)
				}}
			</div>
			<div v-if="quiz.data.max_attempts" class="leading-relaxed">
				{{
					__('You can attempt this quiz {0}.').format(
						quiz.data.max_attempts == 1
							? '1 time'
							: `${quiz.data.max_attempts} times`,
					)
				}}
			</div>
			<div v-if="quiz.data.time" class="leading-relaxed">
				{{
					__(
						'The quiz has a time limit. For each question you will be given {0} seconds.',
					).format(quiz.data.time)
				}}
			</div>
		</div>
		<div v-if="activeQuestion == 0">
			<div class="border text-center p-20 rounded-md">
				<div class="font-semibold text-lg">
					{{ quiz.data.title }}
				</div>
				<Button
					v-if="
						!quiz.data.max_attempts ||
						attempts.data?.length < quiz.data.max_attempts
					"
					@click="startQuiz"
					class="mt-2"
				>
					<span>
						{{ __('Start') }}
					</span>
				</Button>
				<div v-else>
					{{
						__(
							'You have already exceeded the maximum number of attempts allowed for this quiz.',
						)
					}}
				</div>
			</div>
		</div>
		<div v-else-if="!quizSubmission.data">
			<div class="flex items-center justify-center mb-5">
				<div class="bg-white py-3 rounded-lg shadow-lg w-80 text-center">
					<div
						v-if="remainingTime > 0"
						class="text-xl font-semibold text-gray-700"
					>
						<p class="text-4xl font-bold text-blue-600">
							{{ formatTime(remainingTime) }}
						</p>
						<p class="mt-2 text-sm text-gray-500">Time Remaining</p>
					</div>

					<div v-else class="text-xl font-semibold text-gray-700">
						<p class="text-4xl font-bold text-red-600">Time's Up!</p>
						<p class="mt-2 text-sm text-gray-500">Submitting the quiz...</p>
					</div>
				</div>
			</div>
			<div v-for="(question, qtidx) in questions">
				<div
					v-if="qtidx == activeQuestion - 1 && questionDetails.data"
					class="border rounded-md p-5"
				>
					<div class="flex justify-between">
						<div class="text-sm">
							<span class="mr-2">
								{{ __('Question {0}').format(activeQuestion) }}:
							</span>
							<span v-if="questionDetails.data.type == 'User Input'">
								{{ __('Type your answer') }}
							</span>
							<span v-else>
								{{
									questionDetails.data.multiple
										? __('Choose all answers that apply')
										: __('Choose one answer')
								}}
							</span>
						</div>
						<div class="text-gray-900 text-sm font-semibold item-left">
							{{ question.marks }}
							{{ question.marks == 1 ? __('Mark') : __('Marks') }}
						</div>
					</div>
					<div
						class="text-gray-900 font-semibold mt-2 leading-5"
						v-html="questionDetails.data.question"
					></div>
					<div v-if="questionDetails.data.type == 'Choices'" v-for="index in 4">
						<label
							v-if="questionDetails.data[`option_${index}`]"
							class="flex items-center bg-gray-200 rounded-md p-3 mt-4 w-full cursor-pointer focus:border-blue-600"
						>
							<input
								v-if="!showAnswers.length && !questionDetails.data.multiple"
								type="radio"
								:name="encodeURIComponent(questionDetails.data.question)"
								class="w-3.5 h-3.5 text-gray-900 focus:ring-gray-200"
								@change="markAnswer(index)"
							/>

							<input
								v-else-if="!showAnswers.length && questionDetails.data.multiple"
								type="checkbox"
								:name="encodeURIComponent(questionDetails.data.question)"
								class="w-3.5 h-3.5 text-gray-900 rounded-sm focus:ring-gray-200"
								@change="markAnswer(index)"
							/>

							<div
								v-else-if="quiz.data.show_answers"
								v-for="(answer, idx) in showAnswers"
							>
								<div v-if="index - 1 == idx">
									<CheckCircle v-if="answer" class="w-4 h-4 text-green-500" />
									<MinusCircle
										v-else-if="questionDetails.data[`is_correct_${index}`]"
										class="w-4 h-4 text-green-500"
									/>
									<XCircle
										v-else-if="answer == 0"
										class="w-4 h-4 text-red-500"
									/>
									<MinusCircle v-else class="w-4 h-4" />
								</div>
							</div>
							<span
								class="ml-2"
								v-html="questionDetails.data[`option_${index}`]"
							>
							</span>
						</label>
						<div
							v-if="questionDetails.data[`explanation_${index}`]"
							class="mt-2 text-xs"
							v-show="showAnswers.length"
						>
							{{ questionDetails.data[`explanation_${index}`] }}
						</div>
					</div>
					<div v-else>
						<FormControl
							v-model="possibleAnswer"
							type="textarea"
							:disabled="showAnswers.length ? true : false"
							class="my-2"
						/>
						<div v-if="showAnswers.length">
							<Badge v-if="showAnswers[0]" :label="__('Correct')" theme="green">
								<template #prefix>
									<CheckCircle class="w-4 h-4 text-green-500 mr-1" />
								</template>
							</Badge>
							<Badge v-else theme="red" :label="__('Incorrect')">
								<template #prefix>
									<XCircle class="w-4 h-4 text-red-500 mr-1" />
								</template>
							</Badge>
						</div>
					</div>
					<div class="flex items-center justify-between mt-5">
						<div>
							{{
								__('Question {0} of {1}').format(
									activeQuestion,
									questions.length,
								)
							}}
						</div>
						<Button
							v-if="quiz.data.show_answers && !showAnswers.length"
							@click="checkAnswer()"
						>
							<span>
								{{ __('Check') }}
							</span>
						</Button>
						<Button
							v-else-if="activeQuestion != questions.length"
							@click="nextQuetion()"
						>
							<span>
								{{ __('Next') }}
							</span>
						</Button>
						<Button v-else @click="submitQuiz()">
							<span>
								{{ __('Submit') }}
							</span>
						</Button>
					</div>
				</div>
			</div>
		</div>
		<div v-else class="border rounded-md p-20 text-center">
			<div v-if="quizSubmission.data.pass">
				<div
					:key="quizSubmission.data.certificate.name"
					class="bg-white shadow rounded-lg p-3 cursor-pointer"
					@click="openCertificate(quizSubmission.data.certificate)"
				>
					<div class="font-medium leading-5">
						{{ quizSubmission.data.certificate.course_title }}
					</div>
					<div class="mt-2">
						<span class="text-xs text-gray-700"> {{ __('issued on') }}: </span>
						{{ quizSubmission.data.certificate.issue_date }}
					</div>
				</div>
			</div>
			<div v-else>
				<div class="text-lg font-semibold">
					{{ __('Quiz Summary') }}
				</div>
				<div>
					{{
						__(
							'You got {0}% correct answers with a score of {1} out of {2}',
						).format(
							Math.ceil(quizSubmission.data.percentage),
							quizSubmission.data.score,
							quizSubmission.data.score_out_of,
						)
					}}
				</div>
				<Button
					@click="resetQuiz()"
					class="mt-2"
					v-if="
						!quiz.data.max_attempts ||
						attempts?.data.length < quiz.data.max_attempts
					"
				>
					<span>
						{{ __('Try Again') }}
					</span>
				</Button>
			</div>
		</div>
		<div
			v-if="quiz.data.show_submission_history && attempts?.data"
			class="mt-10"
		>
			<ListView
				:columns="getSubmissionColumns()"
				:rows="attempts?.data"
				row-key="name"
				:options="{ selectable: false, showTooltip: false }"
			>
			</ListView>
		</div>
	</div>
</template>
<script setup>
import { Badge, Button, createResource, ListView } from 'frappe-ui'
import { ref, watch, reactive, inject, onMounted, onBeforeUnmount } from 'vue'
import { createToast } from '@/utils/'
import { CheckCircle, XCircle, MinusCircle } from 'lucide-vue-next'
import { timeAgo } from '@/utils'
import FormControl from 'frappe-ui/src/components/FormControl.vue'
const user = inject('$user')

const activeQuestion = ref(0)
const currentQuestion = ref('')
const selectedOptions = reactive([0, 0, 0, 0])
const showAnswers = reactive([])
let questions = reactive([])
const possibleAnswer = ref(null)
const remainingTime = ref(0)
const timer = ref(null)

const props = defineProps({
	quizName: {
		type: String,
		required: true,
	},
})

const quiz = createResource({
	url: 'frappe.client.get',
	makeParams(values) {
		return {
			doctype: 'LMS Quiz',
			name: props.quizName,
		}
	},
	cache: ['quiz', props.quizName],
	auto: true,
	onSuccess(data) {
		populateQuestions()
	},
})

const populateQuestions = () => {
	let data = quiz.data
	if (data.shuffle_questions) {
		questions = shuffleArray(data.questions)
		if (data.limit_questions_to) {
			questions = questions.slice(0, data.limit_questions_to)
		}
	} else {
		questions = data.questions
	}
}

const shuffleArray = (array) => {
	for (let i = array.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1))
		;[array[i], array[j]] = [array[j], array[i]]
	}
	return array
}

const attempts = createResource({
	url: 'frappe.client.get_list',
	makeParams(values) {
		return {
			doctype: 'LMS Quiz Submission',
			filters: {
				member: user.data?.name,
				quiz: quiz.data?.name,
			},
			fields: [
				'name',
				'creation',
				'score',
				'score_out_of',
				'percentage',
				'passing_percentage',
			],
			order_by: 'creation desc',
		}
	},
	transform(data) {
		data.forEach((submission, index) => {
			submission.creation = timeAgo(submission.creation)
			submission.idx = index + 1
		})
	},
})

watch(
	() => quiz.data,
	() => {
		if (quiz.data && quiz.data.max_attempts) {
			attempts.reload()
			resetQuiz()
		}
	},
)

const quizSubmission = createResource({
	url: 'lms.lms.doctype.lms_quiz.lms_quiz.quiz_summary',
	makeParams(values) {
		return {
			quiz: quiz.data.name,
			results: localStorage.getItem(quiz.data.title),
		}
	},
})

const questionDetails = createResource({
	url: 'lms.lms.utils.get_question_details',
	makeParams(values) {
		return {
			question: currentQuestion.value,
		}
	},
})

watch(activeQuestion, (value) => {
	if (value > 0) {
		currentQuestion.value = quiz.data.questions[value - 1].question
		questionDetails.reload()
	}
})

watch(
	() => props.quizName,
	(newName) => {
		if (newName) {
			quiz.reload()
		}
	},
)

const startQuiz = () => {
	activeQuestion.value = 1
	localStorage.removeItem(quiz.data.title)
	setupDurationWatcher()
}

const markAnswer = (index) => {
	if (!questionDetails.data.multiple)
		selectedOptions.splice(0, selectedOptions.length, ...[0, 0, 0, 0])
	selectedOptions[index - 1] = selectedOptions[index - 1] ? 0 : 1
}

const getAnswers = () => {
	let answers = []
	const type = questionDetails.data.type

	if (type == 'Choices') {
		selectedOptions.forEach((value, index) => {
			if (selectedOptions[index])
				answers.push(questionDetails.data[`option_${index + 1}`])
		})
	} else {
		answers.push(possibleAnswer.value)
	}

	return answers
}

const checkAnswer = () => {
	let answers = getAnswers()
	if (!answers.length) {
		createToast({
			title: 'Please select an option',
			icon: 'alert-circle',
			iconClasses: 'text-yellow-600 bg-yellow-100 rounded-full',
			position: 'top-center',
		})
		return
	}

	createResource({
		url: 'lms.lms.doctype.lms_quiz.lms_quiz.check_answer',
		params: {
			question: currentQuestion.value,
			type: questionDetails.data.type,
			answers: JSON.stringify(answers),
		},
		auto: true,
		onSuccess(data) {
			let type = questionDetails.data.type
			if (type == 'Choices') {
				selectedOptions.forEach((option, index) => {
					if (option) {
						showAnswers[index] = option && data[index]
					} else if (questionDetails.data[`is_correct_${index + 1}`]) {
						showAnswers[index] = 0
					} else {
						showAnswers[index] = undefined
					}
				})
			} else {
				showAnswers.push(data)
			}
			addToLocalStorage()
			if (!quiz.data.show_answers) {
				resetQuestion()
			}
		},
	})
}

const addToLocalStorage = () => {
	let quizData = JSON.parse(localStorage.getItem(quiz.data.title))
	let questionData = {
		question_name: currentQuestion.value,
		answer: getAnswers().join(),
		is_correct: showAnswers.filter((answer) => {
			return answer != undefined
		}),
	}
	quizData ? quizData.push(questionData) : (quizData = [questionData])
	localStorage.setItem(quiz.data.title, JSON.stringify(quizData))
}

const nextQuetion = () => {
	if (!quiz.data.show_answers) {
		checkAnswer()
	} else {
		resetQuestion()
	}
}

const resetQuestion = () => {
	if (activeQuestion.value == quiz.data.questions.length) return
	activeQuestion.value = activeQuestion.value + 1
	selectedOptions.splice(0, selectedOptions.length, ...[0, 0, 0, 0])
	showAnswers.length = 0
	possibleAnswer.value = null
}

const submitQuiz = () => {
	if (!quiz.data.show_answers) {
		checkAnswer()
		setTimeout(() => {
			createSubmission()
		}, 500)
		return
	}
	createSubmission()
}

const createSubmission = () => {
	quizSubmission.reload().then(() => {
		if (quiz.data && quiz.data.max_attempts) attempts.reload()
	})
}

function setupDurationWatcher() {
	// Watch the duration and start the timer when it changes
	watch(
		() => quiz?.data?.duration,
		(newDuration) => {
			if (newDuration) {
				remainingTime.value = newDuration

				// Clear any existing timers
				if (timer.value) {
					clearInterval(timer.value)
				}

				// Start a new timer
				timer.value = setInterval(() => {
					if (remainingTime.value > 0) {
						remainingTime.value -= 1000 // Decrease by 1 second (1000ms)
					} else {
						clearInterval(timer.value) // Stop the timer when it reaches 0
						createSubmission() // Call the submission function
					}
				}, 1000) // Update every second
			}
		},
		{ immediate: true }, // Executes the watcher immediately if the value is already defined
	)

	return { remainingTime }
}

const formatTime = (time) => {
	const minutes = Math.floor(time / 60000)
	const seconds = Math.floor((time % 60000) / 1000)
	return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
}

function handleVisibilityChange() {
	if (document.visibilityState !== 'visible') {
		createSubmission()
	} else {
		console.log('Tab is inactive')
	}
}

onMounted(() => {
	// Add event listener to warn users before they refresh the page
	window.addEventListener('beforeunload', handleBeforeUnload)
	document.addEventListener('visibilitychange', handleVisibilityChange)
})

onBeforeUnmount(() => {
	// Clean up the event listener when the component is destroyed
	window.removeEventListener('beforeunload', handleBeforeUnload)
})

const handleBeforeUnload = (event) => {
	// Customize the message you want to display when the user tries to leave the page
	const message =
		'Your quiz will be submitted if you refresh. Are you sure you want to leave?'

	// The standard way to trigger a confirmation dialog is by setting a returnValue
	event.returnValue = message // For modern browsers
	// createSubmission()
	return message // For some older browsers
}

const resetQuiz = () => {
	activeQuestion.value = 0
	selectedOptions.splice(0, selectedOptions.length, ...[0, 0, 0, 0])
	showAnswers.length = 0
	quizSubmission.reset()
	populateQuestions()
}

const openCertificate = (certificate) => {
	window.open(
		`/api/method/frappe.utils.print_format.download_pdf?doctype=LMS Certificate&name=${certificate.name}&key=None`,
	)
}

const getSubmissionColumns = () => {
	return [
		{
			label: 'No.',
			key: 'idx',
		},
		{
			label: 'Date',
			key: 'creation',
		},
		{
			label: 'Score',
			key: 'score',
			align: 'center',
		},
		{
			label: 'Score out of',
			key: 'score_out_of',
			align: 'center',
		},
		{
			label: 'Percentage',
			key: 'percentage',
			align: 'center',
		},
	]
}
</script>
