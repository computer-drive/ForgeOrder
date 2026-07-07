<template>
    <TopBar :showHome="true">
        <template #left>
            <mdui-button-icon @click="goBack">
                <mdui-icon-arrow-back></mdui-icon-arrow-back>
            </mdui-button-icon>
        </template>

        <template #right>
            <slot name="customRight">
                <component :is="rightComponent" />
            </slot>
        </template>
    </TopBar>

    <router-view/>
</template> 

<script setup>
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
        if (backPath == '/shop') {
            router.push('/')
        }
        else {
            router.push(backPath)
        }
    }
}

const rightComponent = ref(null)

const setRightComponent = (component) => {
    rightComponent.value = component
}

provide('setRightComponent', setRightComponent)


</script>