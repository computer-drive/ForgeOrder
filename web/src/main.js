import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { pages, utils, format } from './locales/index.js'

const app = createApp(App)

app.use(router)



app.mount('#app')
