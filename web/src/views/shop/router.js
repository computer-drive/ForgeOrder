import Index from './Index.vue'
import Dishes from './Dishes.vue'

export default {
    path: '/shop',
    component: Index,
    meta: {
        title: 'ShopDefaultPage'
    },
    children: [
        {
            path: '/shop/dishes',
            component: Dishes,
            meta: {
                title: '菜品'
            }
        }
    ]
}