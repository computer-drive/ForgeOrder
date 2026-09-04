<template>
    <div >
        <TopBar :title="$t('orders.topbar.text')" :showHome="false">
            <template #right >
                <mdui-text-field variant="outlined" :placeholder="$t('orders.topbar.search.text')" style="width: auto; height: 100%">
                </mdui-text-field>
                <mdui-button-icon >
                    <mdui-icon-search></mdui-icon-search>
                </mdui-button-icon>
            </template>
        </TopBar>

        <div class="container mdui-prose main-container" ref="contentContainer">
            <h2>{{$t('orders.main.today')}}</h2>

            <div v-for="order in unfinishedOrders" :key="order.id">
                <OrderCard 
            :displayCode="order.displayCode"
            :orderId="order.id" 
            :tableId="order.tableId" 
            :partySize="order.partySize" 
            :status="order.status"
            :orderType="order.type"
            :createTime="new Date(order.createdAt)"
            :totalPrice="order.totalAmount"
            />
            </div>


            <div class="loading-container" v-if="isLoading">
                <mdui-circular-progress></mdui-circular-progress>
            </div>

            <div v-if="!hasMore" class="loading-container">没有更多了。</div>
            
        </div>

        <mdui-fab 
                class="create-order-button" 
                @click="pushWithFrom('/order/new')" 
                extended
                >
                <mdui-icon-edit slot="icon"></mdui-icon-edit>
                {{ $t('orders.main.add') }}
            </mdui-fab>

    </div>

</template>

<script setup>
    import '@/assets/transition.css'

    import TopBar from '@/components/TopBar.vue'
    import OrderCard from './components/OrderCard.vue'
    
    import { pushWithFrom } from '@/utils/routerHelper'
    import reqeust from '@/utils/request.js'

    import 'mdui/components/text-field.js'
    import 'mdui/components/button-icon.js'

    import '@mdui/icons/search.js'

    import { useRouter } from 'vue-router'
    import { onMounted, ref } from 'vue'
    import { useInfiniteScroll } from '@vueuse/core'

    const router = useRouter();

    const PAGE_SIZE = 10

    const currentPage = ref(0)

    const isLoading = ref(false)
    const hasMore = ref(true)

    const unfinishedOrders = ref([])
    const finishedOrders = ref([])

    const contentContainer = ref(null)

    const fetchData = async (page) => {
        const res = await reqeust.post('/order/getToday', {
            "offset": PAGE_SIZE * page
        })

        if (res.data.status == 0) {
            return {unfinished: res.data.data.unfinished, finished: res.data.data.finished}
        }
        
    }

    const loadMore = async () => {
        if (isLoading.value || !hasMore.value)  return

        isLoading.value = true

        try {
            const { unfinished, finished } = await fetchData(currentPage.value)


            unfinishedOrders.value.push(...unfinished)
            finishedOrders.value.push(...finished)

            if (unfinished.length < PAGE_SIZE) {
                hasMore.value = false
            }
            
            currentPage.value ++
            
        } catch (error){
            console.error("加载失败", error)
            hasMore.value = false
        } finally {
            isLoading.value = false 
            
        }
    }

    onMounted(() => {
        loadMore()       
    })

    useInfiniteScroll(
        contentContainer,     
        loadMore,            
        {
            distance: 100,     
            direction: 'bottom',
            interval: 0
        }
    )


</script>


<style scoped>
    .create-order-button {
        position: fixed;
        bottom: 120px;
        right: 20px;
        transform: translateX(0);

    }

    .main-container {
        height: calc(100dvh - 64px - 80px - 24px)
    }

    .loading-container {
        display: flex;
        justify-content: center
    }
    
    

</style>