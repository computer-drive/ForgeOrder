import { createRouter ,createWebHashHistory } from 'vue-router'
import mainRouter from './views/main/router.js'


const routes = [
    mainRouter,
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('./Error.vue'),

        props: route => {

            return {
                title: '找不到页面',
                message: '您访问的页面不存在。',
                detail: null
            }
        }
        
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router


