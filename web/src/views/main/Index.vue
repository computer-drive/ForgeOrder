<template>
    <div>
        <!-- 关键修改：Transition 直接包裹组件，不要多余的 div -->
        <Transition :name="transitionName" mode="out-in">
            <!-- 使用动态组件或 v-if/v-else 切换 -->
            <component :is="currentComponent" :key="index" />
        </Transition>
        
        <BottomBar ref="bottomBar" v-if="showBottomBar"/>
    </div>
</template>

<script setup>
    import BottomBar from '@/components/BottomBar.vue'
    import Home from './Home.vue'
    import Orders from './Orders.vue'
    import Me from './Me.vue'

    import { ref, watch, computed, onMounted, shallowRef } from 'vue'
    import { useRoute, onBeforeRouteUpdate, useRouter } from 'vue-router'

    const route = useRoute()
    const router = useRouter()

    const transitionName = ref('tabslide-left')
    const bottomBar = ref(null)

    const lastIndex = ref(0)

    const showBottomBar = ref(false)

    // 使用动态组件
    const currentComponent = computed(() => {
        const index = bottomBar.value?.index ?? 0
        const components = [Home, Orders, Me]
        return components[index] || Home
    })

    const index = computed(() => {
        return bottomBar.value?.index ?? 0
    })


    onMounted(() => {
        const queryIndex = route.query?.index
        
        if (queryIndex) {
            bottomBar.value?.updateIndex(Number(queryIndex))
        } else {
            bottomBar.value?.updateIndex(0)

        }
        bottomBar.value?.setSelected(index.value.toString() || '0')

        setTimeout(() => {
            showBottomBar.value = true
        }, 150)
    })

    // 监听 index 变化同步到 URL
    watch(
        () => bottomBar.value?.index ?? -1  , 
        (newVal) => {
            router.replace({
                query: {
                    ...router.currentRoute.value.query,
                    index: newVal
                }
            })
            // console.log(newVal, index.value)
            transitionName.value = newVal > lastIndex.value ? 'tabslide-left' : 'tabslide-right'
            lastIndex.value = newVal
        }
    )
</script>

<style>
.tabslide-left-enter-active,
.tabslide-left-leave-active,
.tabslide-right-enter-active,
.tabslide-right-leave-active {
    transition:
        transform .15s cubic-bezier(.22, 1, .36, 1),
        opacity .15s;
}

/* 前进 */
.tabslide-left-enter-from {
    transform: translateX(30px);
    opacity: 0;
}

.tabslide-left-leave-to {
    transform: translateX(-30px);
    opacity: 0;
}

/* 返回 */
.tabslide-right-enter-from {
    transform: translateX(-30px);
    opacity: 0;
}

.tabslide-right-leave-to {
    transform: translateX(30px);
    opacity: 0;
}


</style>