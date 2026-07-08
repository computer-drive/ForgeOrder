<template>
    <div class="container mdui-prose">
        <div v-if="isLoading" class="loading-container">
            <mdui-circular-progress></mdui-circular-progress>
        </div>
        <div v-else>
            <h2>所有菜品</h2>

            <mdui-li>
                <div v-for="(value, key) in categories" :key="key">
                    <mdui-list-subheader>{{ categories[key] }}</mdui-list-subheader>
                    <div v-for="dish in dishes[value]" :key="dish.id">
                        <mdui-list-item rounded @click="showDetail(value, dish.id)">{{ dish.name }}</mdui-list-item>
                    </div>

                </div>
            </mdui-li>

        </div>


    </div>

    <mdui-dialog ref="dishDetail" close-on-overlay-click>
        <span slot="headline">{{ currentDish.name }}</span>
        <div slot="description" class="mdui-prose">
            <h2 style="font-size: 20px; margin-bottom: 10px; color: black">基本信息</h2>

            <div class="detail-item">
                <div class="detail-label">菜品ID</div>
                {{ currentDish.id }}</div>  

            <div class="detail-item">
                <div class="detail-label">名称</div>
                {{ currentDish.name }}</div>

            <div class="detail-item">
                <div class="detail-label">描述</div>
                {{ currentDish.description }}</div>

            <div class="detail-item">
                <div class="detail-label">价格</div>
                ￥ {{ (currentDish.price  / 100).toFixed(2) }}</div>

            <div class="detail-item">
                <div class="detail-label">创建时间</div>
                {{ new Date(currentDish.created_at).toLocaleString() }}</div>
            
            <div class="detail-item">
                <div class="detail-label">是否可用</div>
                {{ currentDish.available ? "是" : "否" }}</div>     
                    
            <h2 style="font-size: 20px; margin-bottom: 10px; color: black; margin-top: 10px">统计信息</h2>
            
            <div class="detail-item">
                <div class="detail-label">当月销量</div>
                {{ currentDish.stat?.monthly_sales || '无数据' }}</div>  

            <div class="detail-item">
                <div class="detail-label">总销量</div>
                {{ currentDish.stat?.total_sales || '无数据' }}</div>  

            <div class="detail-item">
                <div class="detail-label">更新时间</div>
                {{ new Date(currentDish.stat?.updated_at).toLocaleString() }}</div>

            <h2 style="font-size: 20px; margin-bottom: 10px; color: black; margin-top: 10px">选项信息</h2>
            
            <div v-for="(value, key) in currentDish.choices" :key="key">
                <div class="detail-item" style="margin-bottom: 8px;">
                    <div class="detail-label">{{ key }}</div>
                    <mdui-segmented-button-group >
                        <mdui-segmented-button v-for="option in value" :key="option">{{ option }}</mdui-segmented-button>
                    
                    </mdui-segmented-button-group>
                </div>
            </div>

            

                

        </div>

        <mdui-button slot="action" variant="tonal" @click="goEdit">
            编辑
            <mdui-icon-edit slot="icon" ></mdui-icon-edit>
        </mdui-button>
        <mdui-button slot="action" variant="text" @click="dishDetail.open = false">确定</mdui-button>

    </mdui-dialog>

</template> 

<script setup>
import TopProgressBar from '@/components/TopProgressBar.vue'

import 'mdui/components/list.js';
import 'mdui/components/list-item.js';
import 'mdui/components/list-subheader.js';
import 'mdui/components/dialog.js';
import 'mdui/components/segmented-button-group.js';
import 'mdui/components/segmented-button.js';

import { inject, h, onMounted, ref, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

import '@mdui/icons/add.js';
import '@mdui/icons/edit.js';

import request from '@/utils/request.js'

const router = useRouter()

const { setRightComponent, clearRightComponent } = inject('rightComponent')

const dishes = ref([])
const categories = ref([])

const isLoading=  ref(true)

const currentDish = ref({})
const dishDetail = ref(null)


const addDish = () => {}

onMounted(() => {

    setRightComponent(h('mdui-button-icon', {
        onClick: addDish
    }, [
        h('mdui-icon-add')
    ]))

    request.get("/shop/dishes/getAll").then(res => {
        // console.log(res)
        if (res.status == 200) {
            // console.log(res.data.data)
            dishes.value = res.data.data.dishes
            categories.value = res.data.data.categories
            console.log(dishes.value, categories.value)
        }
        isLoading.value = false 
    })

    
})

const showDetail = (category_name, dish_id) => {
    currentDish.value = { 
        ...dishes.value[category_name].find(dish => dish.id == dish_id) 
    }
    
    
    dishDetail.value.open = true;

    console.log(currentDish.value.stat)
}

const goEdit = () => {
    router.push(`/shop/dishes/${currentDish.value.id}`)
}

onBeforeUnmount(() => {
    clearRightComponent()
})





</script>

<style>
    .loading-container {
        height: calc(100vh - 65px);
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .detail-item {
        display: flex;
        gap: 12px;
        align-items: center;
    }
    .detail-label {
        width: 4.1em;
        text-align: justify;
        text-justify: inter-ideograph;
        text-align-last: justify;
        flex-shrink: 0;
    }
</style>