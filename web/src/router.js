import { createBrowserRouter, createWebHashHistory } from 'vue-router'
import Home from './Home.vue'
import Login from './Login.vue'

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/login',
        component: Login
    }
]

const router = createBrowserRouter(routes, {
    history: createWebHashHistory()
})




