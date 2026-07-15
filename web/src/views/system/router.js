import Index from './Index.vue'
import Logs from './Logs.vue'

export default {
    path: '/system/',
    component: Index,
    meta: {
        title: '$system.title.main'
    },
    children: [
        {
            path: '/system/logs',
            component: Logs,
            meta: { // 显示为TopbBar的标题，定义在TopBar组件的代码
                title: '$system.title.logs'
            }
        },
    ]
}