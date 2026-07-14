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
            meta: { // 显示为TopbBar的标题，定义在TopBar组件的代码
                title: '$shop.title.dishes'
            }
        },
        {
            path: '/shop/dishes/:id',
            component: DishEdit,
            meta: {
                title: '$shop.title.edit_dish'
            },
            props: true
        },
        {
            path: '/shop/dishes/new',
            component: DishEdit,
            meta: {
                title: '$shop.title.add_dish'
            },
            props: {
                isNew: true
            }
        }
    ]
}