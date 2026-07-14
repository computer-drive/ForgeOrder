import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { t, locale } from './locales/index.js'

const app = createApp(App)

app.use(router)

app.config.globalProperties.$t = t
app.config.globalProperties.$locale = locale

app.mount('#app')
