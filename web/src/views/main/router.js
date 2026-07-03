import Index from './Index.vue' 
import Home from './Home.vue'
import Orders from './Orders.vue'
import Account from './Account.vue'


export default {
    path: '/',
    component: Index,
    children: [
        {
            path: '/',
            component: Home
        },
        {
            path: '/orders',
            component: Orders
        },
        {
            path: '/account',
            component: Account
        }
    ]
}

