<template>
    <TopBar :showHome="true">
        <template #left>
            <mdui-button-icon @click="goBack">
                <mdui-icon-arrow-back></mdui-icon-arrow-back>
            </mdui-button-icon>
        </template>
        
        <div style="flex-grow: 1"></div>
        
        <template #right>
            <slot name="customRight">
                <component :is="rightComponent" />
            </slot>
        </template>
    </TopBar>

    <router-view/>

    <Main v-if="route.path == '/system/' || route.path == '/system'"/>
</template> 

<script setup>
import Main from './Main.vue'
import TopBar from '@/components/TopBar.vue'
import { useRoute, useRouter } from 'vue-router'
import { ref, provide } from 'vue'

const route = useRoute()
const router = useRouter()

// 返回按钮 
const goBack = () => {
    if (route.matched == 1) {
        router.push('/')
    } else {
        const backPath = route.path.split('/').slice(0, -1).join('/') || '/'

        
        router.push(backPath)
        
    }
}

const rightComponent = ref(null)

const setRightComponent = (component) => {
    rightComponent.value = component
}

const clearRightComponent = () => {
    rightComponent.value = null
}

provide('rightComponent', {
    setRightComponent,
    clearRightComponent
})



</script>