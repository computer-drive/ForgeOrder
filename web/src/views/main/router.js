import Index from './Index.vue' 
import Home from './Home.vue'
import Orders from './Orders.vue'
import Me from './Me.vue'


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
            path: '/me',
            component: Me
        }
    ]
}

