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
        
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import("./Login.vue"),
        meta : {
            noAuth: true
        }
    },
    {
        path: '/develop',
        name: 'Develop',
        component: () => import("./Develop.vue"),
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

router.beforeEach((to, from) => {
    const token = localStorage.getItem('token')

    if (to.meta?.noAuth == true) {
        // 页面不需要认证。判断是否是登录页
        if (to.path == '/login' && token) {
            return '/'
        } else {
            return true
        }
        
    } else {
        if (!token) {
            // 未登录
            return {
                name: 'Login'
            }
        } else {
            return true
        }
    }


})

export default router


