<template>
    <div>
        <TopBar :showHome="true">
        <template #left>
            <mdui-button-icon @click="goBack">
                <mdui-icon-arrow-back></mdui-icon-arrow-back>
            </mdui-button-icon>
        </template>
        <div style="flex-grow: 1"></div>
        
        <template #right>
            <slot name="customRight">
                <template v-for="(component, index) in rightComponents" :key="index">
                    <component :is="component" />
                </template>
            </slot>
        </template>
    </TopBar>

    <Main v-if="route.path == '/shop' || route.path == '/shop/' "/>
    <router-view/>
    
    </div>
</template> 

<script setup>
import Main from './Main.vue'
import TopBar from '@/components/TopBar.vue'
import { useRoute, useRouter } from 'vue-router'
import { ref, provide } from 'vue'

import { goBack } from '@/utils/routerHelper.js'



const route = useRoute()
const router = useRouter()

// 返回按钮 
// const goBack = () => {
//     router.push("/orders")
// }

const rightComponents = ref([])

const setRightComponent = (component) => {

    clearRightComponent()

    addRightComponent(component)
}

const clearRightComponent = () => {
    // 清除所有的右侧组件
    rightComponents.value = []
}

const addRightComponent = (component) => {
    // 添加右侧组件
    rightComponents.value.push(component)
}

provide('rightComponent', {
    setRightComponent,
    clearRightComponent,
    addRightComponent
})



</script>