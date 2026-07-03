import { createRouter ,createWebHashHistory } from 'vue-router'
import Home from './Home.vue'
import Login from './Login.vue'
import Orders from './Orders.vue'
import Account from './Account.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/orders',
        name: 'Orders',
        component: Orders
    },
    {
        path: '/account',
        name: 'Account',
        component: Account
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router


