import Plyr from 'plyr'

export default class YouTubeVideoTool {
	static get toolbox() {
		return {
			title: 'YouTube Video',
			icon: `
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24">
          <path d="M19.615 3.184c-1.19-.672-8.068-.672-9.258 0-1.392.78-1.409 2.398-1.412 2.406v4.82s.02 1.626 1.412 2.406c1.19.672 8.068.672 9.258 0 1.392-.78 1.409-2.398 1.412-2.406v-4.82s-.02-1.626-1.412-2.406zm-9.615 8.148v-4.148l3.665 2.074-3.665 2.074zm9-4.148c-.257 0-.54.039-.832.118-.538.142-.758.224-.91.316-.077.047-.108.063-.155.099v6.148c.047.035.077.052.155.099.152.091.372.174.91.316.293.079.575.118.832.118 1.202 0 1.48-1.536 1.482-1.548v-4.822c-.002-.012-.28-1.548-1.482-1.548z"/>
        </svg>
      `,
		}
	}

	// Indicate that this tool supports read-only mode
	static get isReadOnlySupported() {
		return true
	}

	constructor({ data, api, readOnly }) {
		this.api = api
		this.data = data || {}
		this.videoUrl = this.data.videoUrl || ''
		this.player = null
		this.readOnly = readOnly
	}

	render() {
		const container = document.createElement('div')

		// Only show the input field if not in read-only mode
		if (!this.readOnly) {
			this.input = document.createElement('input')
			this.input.type = 'url'
			this.input.placeholder = 'Enter YouTube URL...'
			this.input.value = this.videoUrl
			this.input.addEventListener('input', (event) => {
				this.videoUrl = event.target.value
				this.updateVideoEmbed()
			})
			container.appendChild(this.input)
		}

		// Player container
		this.embedContainer = document.createElement('div')
		this.embedContainer.className = 'youtube-video-embed'
		container.appendChild(this.embedContainer)

		// If there's a video URL, hide input and show player
		if (this.videoUrl) {
			this.updateVideoEmbed()
		}

		return container
	}

	save() {
		return {
			videoUrl: this.videoUrl,
		}
	}

	toggleInputDisplay(showInput) {
		if (this.input) {
			this.input.style.display = showInput ? 'block' : 'none'
		}
		this.embedContainer.style.display = showInput ? 'none' : 'block'
	}

	updateVideoEmbed() {
		if (this.embedContainer) {
			this.embedContainer.innerHTML = ''

			if (this.videoUrl) {
				const videoId = this.extractVideoId(this.videoUrl)
				if (videoId) {
					const videoElement = document.createElement('div')
					videoElement.setAttribute('data-plyr-provider', 'youtube')
					videoElement.setAttribute('data-plyr-embed-id', videoId)

					this.embedContainer.appendChild(videoElement)

					// Initialize Plyr on the video element
					if (this.player) {
						this.player.destroy() // Destroy any previous player instance
					}
					this.player = new Plyr(videoElement, {
						controls: ['play', 'progress', 'volume', 'fullscreen'],
						captions: { active: false },
						autoplay: 1,
					})
	// Attach full-screen change listener
	this.player.on('enterfullscreen', () => {
		if (screen.orientation && screen.orientation.lock) {
			screen.orientation.lock('landscape').catch((err) => {
				console.warn('Could not lock screen orientation:', err)
			})
		}
	})

	this.player.on('exitfullscreen', () => {
		if (screen.orientation && screen.orientation.lock) {
			screen.orientation.lock('portrait').catch((err) => {
				console.warn('Could not reset screen orientation:', err)
			})
		}
	})
					// Hide input after embedding video
					this.toggleInputDisplay(false)
				}
			}
		}
	}

	extractVideoId(url) {
		const regex =
			/(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/
		const match = url.match(regex)
		return match ? match[1] : null
	}
}
