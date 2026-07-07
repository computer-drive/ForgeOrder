<template>
    <TopBar :showHome="true">
        <template #left>
            <mdui-button-icon @click="goBack">
                <mdui-icon-arrow-back></mdui-icon-arrow-back>
            </mdui-button-icon>
        </template>
    </TopBar>
</template> 

<script setup>
import TopBar from '@/components/TopBar.vue'
import { useRoute, useRouter } from 'vue-router'

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
</script>