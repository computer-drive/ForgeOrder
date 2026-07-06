<template>
    <TopBar title="订单" showHome="false">
        <template #right >
            <mdui-text-field variant="outlined" placeholder="搜索" style="width: auto; height: 100%">
            </mdui-text-field>
            <mdui-button-icon >
                <mdui-icon-search></mdui-icon-search>
            </mdui-button-icon>
        </template>
    </TopBar>

    <div class="container mdui-prose" >
        <h2>今日订单</h2>

        <div v-for="i in 10" :key="i">
            <OrderCard 
        :orderId="2026114514" 
        :orderDisplayId="1"
        :tableNo="'A1'" 
        :people="4" 
        :state="0"
        :orderType="0"
        :createTime="new Date('2026-07-06 10:00:00')"
        :finishedCount="3"
        :totalCount="5"
        :unfinishedDishes="[{name:'鱼香肉丝',count:1},{name:'红烧肉',count:2},{name:'青椒肉丝',count:1}, {name:'红烧肉',count:2}, {name:'红烧肉',count:2}]"
        :tags="['有小孩']"
        :totalPrice="20000"
        />
        </div>

        <mdui-fab size="normal" style="position: fixed; bottom: 100px; right: 20px;" @click="router.push('/order/new')" extended>
            <mdui-icon-edit slot="icon"></mdui-icon-edit>
            添加订单
        </mdui-fab>

    </div>

    
    
</template>

<script setup>
    import TopBar from '@/components/TopBar.vue'
    import OrderCard from './components/OrderCard.vue'

    import 'mdui/components/text-field.js'
    import 'mdui/components/button-icon.js';

    import '@mdui/icons/search.js';
    import { useRouter } from 'vue-router';
    
    const router = useRouter();

</script>
