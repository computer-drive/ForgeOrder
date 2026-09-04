<template>
    <div>
        <div class="container mdui-prose">
            <div v-if="isLoading" class="loading-container">
                <mdui-circular-progress></mdui-circular-progress>
            </div>
            <div v-else>
                <h2>订单 {{ orderInfo.displayCode }}</h2>

                <div class="order-id-container">
                    <p class="order-id">唯一标识符：{{ id }}</p>
                    <mdui-button-icon @click="copyOrderId">
                        <mdui-icon-content-copy></mdui-icon-content-copy>
                    </mdui-button-icon>
                </div>
                
                <mdui-linear-progress :value="orderStatus" max="4"></mdui-linear-progress>
                
                <div class="state-container">
                    <div class="state-item">
                        已下单
                        {{ String(createdAt?.getHours()).padStart(2, '0') }}:{{ String(createdAt?.getMinutes()).padStart(2, '0') }}
                    </div>
                    <div class="state-item">制作中
                        <span v-if="orderStatus == 2">
                            {{ String(updatedAt?.getHours()).padStart(2, '0') }}:{{ String(updatedAt?.getMinutes()).padStart(2, '0') }}
                        </span>
                    </div>
                    <div class="state-item">待结账
                        <span v-if="orderStatus == 3">
                            {{ String(updatedAt?.getHours()).padStart(2, '0') }}:{{ String(updatedAt?.getMinutes()).padStart(2, '0') }}
                        </span>
                    </div>
                    <div class="state-item">
                        已结账
                        <span v-if="payAt !== null">
                            {{ String(payAt?.getHours()).padStart(2, '0') }}:{{ String(payAt?.getMinutes()).padStart(2, '0') }}
                        </span>
                        <!-- <span v-else>未结账</span> -->
                    </div>
                </div>

                <mdui-list>
                    <mdui-list-item nonclickable>
                        创建者
                        <div class="order-info-value" slot="end-icon">
                            <mdui-circular-progress class="order-info-progress"></mdui-circular-progress>

                            (ID:{{ orderInfo.creator }})

                            <mdui-button-icon @click="router.push(`/user/${orderInfo.creator}`)">
                                <mdui-icon-open-in-new></mdui-icon-open-in-new>
                            </mdui-button-icon>
                        </div>
                    </mdui-list-item>

                    <mdui-list-item nonclickable>
                        订单类型
                        <div class="order-info-value" slot="end-icon">
                            {{ orderInfo.type === 0 ? "堂食" : "打包" }}
                        </div>
                    </mdui-list-item>

                    <mdui-list-item nonclickable> 
                        就餐人数
                        <div class="order-info-value" slot="end-icon">
                            {{ orderInfo.partySize }}
                        </div>
                    </mdui-list-item>

                    <mdui-list-item v-if="orderInfo.type === 0" nonclickable>
                        卓台信息
                        <div class="order-info-value" slot="end-icon" >
                            <mdui-circular-progress class="order-info-progress"></mdui-circular-progress>

                            (ID:{{ orderInfo.tableId }})

                            <mdui-button-icon @click="router.push(`/shop/tables`)">
                                <mdui-icon-open-in-new></mdui-icon-open-in-new>
                            </mdui-button-icon>
                        </div>
                    </mdui-list-item>

                    <mdui-list-item v-if="orderInfo.type === 0" nonclickable>
                        总金额
                        <div class="order-info-value" slot="end-icon" >

                            ￥{{ orderInfo.totalAmount / 100 }}

                        </div>
                    </mdui-list-item>



                    <mdui-collapse ref="collapseRef" @change="() => { $forceUpdate(); count ++ }">
                        <mdui-collapse-item value="checkoutInfo">

                            <mdui-list-item slot="header" rounded >
                                结账信息
                                <mdui-icon-expand-more   pand-more 
                                    slot="end-icon" 
                                    v-if="count && collapseRef?.value && collapseRef.value.indexOf('checkoutInfo') == -1">
                                    <!--test变量的用处，用于让Vue检测到折叠状态的变化-->
                                </mdui-icon-expand-more>

                                <mdui-icon-expand-less slot="end-icon" v-else></mdui-icon-expand-less>
                            </mdui-list-item>

                            <div style="margin-left: 1rem">
                                <mdui-list-item nonclickable rouneded>
                                    收银员
                                    <div class="order-info-value" slot="end-icon">
                                        <mdui-circular-progress class="order-info-progress"></mdui-circular-progress>

                                        (ID:{{ orderInfo.creator }})

                                        <mdui-button-icon @click="router.push(`/user/${orderInfo.creator}`)">
                                            <mdui-icon-open-in-new></mdui-icon-open-in-new>
                                        </mdui-button-icon>
                                    </div>

                                </mdui-list-item>

                                <mdui-list-item nonclickable rouneded>
                                    结账时间

                                    <div class="order-info-value" slot="end-icon">
                                        {{ dayjs(payAt).format('YYYY-MM-DD HH:mm:ss') }}
                                    </div>

                                </mdui-list-item>


                                <mdui-list-item nonclickable rouneded>
                                     优惠信息
                                    <div class="order-info-value" slot="end-icon">
                                        <div v-if="orderInfo.discount === null">无</div>
                                        <div class="order-info-value" slot="end-icon" v-else>
                                            {{ orderInfo.discoutType }}
                                            ￥{{ orderInfo.discout / 100 }}
                                        </div>
                                    </div>

                                </mdui-list-item>

                                <mdui-list-item nonclickable rouneded>
                                    支付方式
                                    <div class="order-info-value" slot="end-icon">
                                        {{ orderInfo.payMethod }}
                                    </div>

                                </mdui-list-item>

                                
                            </div>

                        </mdui-collapse-item>

                        <mdui-collapse-item value="orderInfo">
                            <mdui-list-item slot="header" value="orderInfo">Item 2</mdui-list-item>

                            <mdui-list-item>Item 2 - subitem</mdui-list-item>

                        </mdui-collapse-item>

                    </mdui-collapse>

                    

                </mdui-list>




            </div>
            
            
        </div>
    </div>
</template>

<script setup>
    import { alert } from 'mdui/functions/alert.js'
    import { snackbar } from 'mdui/functions/snackbar.js';

    import { ref, onMounted } from 'vue'
    import request from '@/utils/request.js'
    
    import { useRouter } from 'vue-router'

    import dayjs from 'dayjs'

    import 'mdui/components/button-icon.js'
    import 'mdui/components/circular-progress.js'
    import 'mdui/components/collapse.js'
    import 'mdui/components/collapse-item.js'
    import 'mdui/components/list.js'
    import 'mdui/components/list-item.js'

    import '@mdui/icons/content-copy.js'
    import '@mdui/icons/open-in-new.js'
    import '@mdui/icons/expand-more.js';
    import '@mdui/icons/expand-less.js';

    const props = defineProps({
        id: {
            type: String,
            default: ''
        }
    })

    const router = useRouter()

    const isLoading = ref(true)

    const orderInfo = ref({})

    const orderStatus = ref(0)

    const createdAt = ref(null)
    const payAt = ref(null)
    const updatedAt = ref(null)

    const collapseRef = ref(null)

    const count = ref(1) // 变量用于让Vue检测到折叠状态的变化

    const fetchData = async () => {
        const res = await request.post("/order/get", {
            id: props.id,
            queries: ["basicInfo"]
        })

        if (res.data.status == 0) {
            orderInfo.value = res.data.data.result.basicInfo
            
            createdAt.value = new Date(orderInfo.value.createdAt)
            updatedAt.value = new Date(orderInfo.value.updatedAt)
            if (orderInfo.value.payAt !== null) {
                payAt.value = new Date(orderInfo.value.payAt)
            }

            orderStatus.value = orderInfo.value.status + 1
        
        
        
        } else if (res.data.status == 3002) {
            // 找不到订单
            alert({
                headline: "找不到订单",
                description: `订单“${props.id}”不存在。`,
                confirmText: "确定",
                onConfirm: () => router.psuh("/?index=1"),
            })
        }

        isLoading.value = false
    }

    const copyOrderId = () => {
        try {
            navigator.clipboard.writeText(props.id)
            snackbar({
                "message": "复制到剪贴板成功",
            })
        } catch (error) {
            console.error(error)
            snackbar({
                "message": "复制到剪贴板失败",
            })
        }
    }

    onMounted(() => {
        fetchData()
    })
</script>

<style scoped>
    .loading-container {
        width: 100%;
        height: calc(100vh - 64px - 24px);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .state-container {
        display: flex;
    }

    .state-item {
        flex: 1;
        text-align: right;
        font-size: 12px
    }

    h2 {
        margin-bottom: 12px;
    }

    .order-id {
        display: flex;
        font-size: 12px;
        margin: 0
    }

    .order-id-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }



    .order-info-value {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px
    }

    .order-info-progress {
        width: 20px;
        height: 20px;

    }

    .order-info-button {
        margin-left: 12px;
    }



    
</style>
