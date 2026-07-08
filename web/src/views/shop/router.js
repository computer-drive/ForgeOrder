import Index from './Index.vue'
import Dishes from './Dishes.vue'
import DishEdit from './DishEdit.vue'

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
        },
        {
            path: '/shop/dishes/:id',
            component: DishEdit,
            meta: {
                title: '编辑菜品'
            },
            props: true
        },
        {
            path: '/shop/dishes/new',
            component: DishEdit,
            meta: {
                title: '新增菜品'
            },
            props: {
                isNew: true
            }
        }
    ]
}