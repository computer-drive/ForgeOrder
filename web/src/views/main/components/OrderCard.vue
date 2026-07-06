<template>
    <div class="card-container">
            <mdui-card class="order-card" variant="outlined" clickable>
                <!-- 顶部信息-->
                <div class="card-header">
                    <div class="header-left">

                        <div>
                            <span class="header-left-item-key">订单</span>
                            <span class="header-left-item-value">{{ orderDisplayId }}</span>
                        </div>

                        <div v-if="orderType == 0">
                            <span class="header-left-item-key">桌号</span>
                            <span class="header-left-item-value">{{ tableNo }}</span>
                        </div>
                        <div v-if="orderType == 0">
                            <span class="header-left-item-key">人数</span>
                            <span class="header-left-item-value">{{ people }}</span>
                        </div>
                        
                    </div>

                    <div class="header-right">{{  state  }}</div>
                </div>

                <!--进度信息-->
                <div class="progress-content">
                    <div class="progress-label">{{ finishedCount }}/ {{ totalCount }}</div>
                    <mdui-linear-progress :value="finishedCount" :max="totalCount" class="progress-bar"></mdui-linear-progress>
                </div>
            
                <div class="unfinished-dishes">
                    待完成：    
                    <span v-for="(dish, index) in unfinishedDishes" :key="dish">
                        <span v-if="index < 3">
                            {{ dish.name }}x{{ dish.count }}
                            <span v-if="index < unfinishedDishes.length - 1">
                                ,
                            </span>
                        </span>
                        
                    </span>
                    <span v-if="unfinishedDishes.length > 3">
                        ...
                    </span>
                </div>

                <!--标签区域-->
                <div class="tags-content">
                    <div v-for="tag in tags" :key="tag" >
                        <mdui-card class="tag-card tag-card-red" variant="outlined">{{ tag }}</mdui-card>
                    </div>

                    
                    <div v-if="orderType == 0">
                        <mdui-card class="tag-card tag-card-blue" variant="outlined">堂食</mdui-card>
                    </div>

                    <div v-else>
                        <mdui-card class="tag-card tag-card-green" variant="outlined">外送</mdui-card>
                    </div>
                </div>

                <!-- 底部信息-->
                <div class="footer-content">
                    <div>
                        <span class="footer-item">{{ formatDateInTime(createTime) }}</span>
                        （已等{{ formatWaitTime }}）
                    </div>
                    <div class="footer-item">
                        ￥ {{ (totalPrice / 100).toFixed(2) }}
                    </div>
                </div>

                
            </mdui-card>
            <!--操作区域-->
            <div class="action-content">
                <mdui-button-icon @click="router.push(`/order/${orderId}/unfinished`)">
                    <mdui-icon-done-outline></mdui-icon-done-outline>
                </mdui-button-icon>

                <mdui-button-icon @click="router.push(`/order/${orderId}/checkout`)">
                    <mdui-icon-payment></mdui-icon-payment>
                </mdui-button-icon>

                <mdui-button-icon @click="router.push(`/printer/print/${orderId}`)">
                    <mdui-icon-print></mdui-icon-print>
                </mdui-button-icon>

                <mdui-button-icon>
                    <mdui-icon-more-vert></mdui-icon-more-vert>
                </mdui-button-icon>

            </div>
        </div>

</template> 

<script setup>
    import { computed } from 'vue'

    import 'mdui/components/card.js';
    import 'mdui/components/fab.js';
    import 'mdui/components/linear-progress.js';
    import 'mdui/components/divider.js';
    import 'mdui/components/button-icon.js';

    import '@mdui/icons/done-outline.js';
    import '@mdui/icons/payment.js';
    import '@mdui/icons/print.js';
    import '@mdui/icons/more-vert.js';
    import '@mdui/icons/edit.js';

    import { formatDateInTime, getSub } from '@/utils/date.js';
    import { useRouter } from 'vue-router';
;
    const router = useRouter();



    const props = defineProps({
        orderId: {  // 订单在系统内的唯一id
            type: Number,
            default: 0
        },
        orderDisplayId: { // 订单号
            type: Number,
            default: 0
        },
        tableNo: { // 桌号
            type: String,
            default: 'A1'
        },
        people: {  // 人数
            type: Number,
            default: 0
        },
        state: { // 状态
            type: Number,
            default: 0
        },
        finishedCount: { // 已完成的菜品
            type: Number,
            default: 0
        },
        totalCount: { // 总菜品数
            type: Number,
            default: 0
        },
        unfinishedDishes: { // 待完成的菜品
            type: Array,
            default: []
        },
        tags: { // 标签
            type: Array,
            default: []
        },
        orderType: { // 订单类型(0: 堂食, 1: 外带)
            type: Number,
            default: 0
        },
        createTime: { // 创建时间
            type: Date,
            default: new Date()
        },
        totalPrice: { // 总金额（单位：分）
            type: Number,
            default: 0
        }
    })

    const orderDisplayId = computed(() => {
        // 补齐4位数字
        return props.orderDisplayId.toString().padStart(4, '0')
    })

    const state = computed(() => {
        if (props.state === 0) {
            return '已下单'
        } else if (props.state === 1) {
            return '制作中'
        } else if (props.state === 2) {
            return '待结账'
        } else if (props.state === 3) {
            return '已结账'
        }
        
    })

    const formatWaitTime = computed(() => {
        const waitTime = getSub(new Date(), props.createTime)
        
        if (waitTime.hour > 0) {
            return `${waitTime.hour}小时${waitTime.minute}分钟`
        } else if (waitTime.minute > 0) {
            return `${waitTime.minute}分钟`
        } else {
            return `${waitTime.second}秒`
        }
    })
</script>

<style>
    .container .card-container {
        margin-bottom: 24px ;
    }

    .order-card {
        width: 100%;  
        padding: 12px; 
        margin-bottom: 0
    }
    
    .card-header {
        display: flex; 
        justify-content: space-between; 
        align-items: center;
    }

    .header-left {
        display: flex;
        gap:8px
    }

    .header-left-item-key {
        margin-right: 5px;
    }

    .header-left-item-value {
        font-size: 20px;
    }

    .header-right {
        text-align: right;
         font-size: 20px;
    }

    .progress-content {
        display: flex;
         align-items: center;
    }

    .progress-label {
        font-size: 14px;
         flex-shrink: 0;
          white-space: nowrap;
           margin-right: 8px
    }

    .progress-bar {
        flex: 1;
    }

    .unfinished-dishes {
        font-size: 14px;
    }

    .tags-content {
        display: flex;
         gap: 8px;
    }

    .tag-card {
        font-size: 14px;
        padding-top: 2px;
        padding-bottom: 2px;
        padding-left: 6px;
        padding-right: 6px;
        
    }

    .tag-card-red {
        border: 1px solid #BB1614;
        color: #BB1614;
    }

    .tag-card-blue {
        border: 1px solid #18489c;
        color: #18489c;
    }

    .tag-card-green {
        border: 1px solid #189C25;
        color: #189C25;
    }

    .footer-content {
        display: flex;
         justify-content: space-between;
    }

    .footer-item {
        font-size: 20px;
    }

    .action-content {
        display: flex; 
        justify-content: flex-end;
    }


</style>