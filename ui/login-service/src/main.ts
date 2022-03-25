import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import 'flowbite'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faEye, faEyeSlash } from '@fortawesome/free-regular-svg-icons'

localStorage.setItem('theme', 'dark')
library.add(faEye, faEyeSlash)

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
