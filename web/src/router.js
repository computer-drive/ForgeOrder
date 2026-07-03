import { createRouter ,createWebHashHistory } from 'vue-router'
import mainRouter from './views/main/router.js'


const routes = [
    mainRouter
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router


