<template>
    <div id="app">
        
        <!-- <div v-if="route.meta.transition">
            {{ route.meta.transition }}
                <router-view v-slot="{ Component, route }">
                    <Transition :name="route.meta.transition" mode="out-in">
                    <component :is="Component" :key="route.fullPath" />
                    </Transition>
                </router-view>
            </div>

        
            
        <div v-else>
            no-transition
            <router-view/>
        </div> -->

        <router-view v-slot="{ Component, route }">
            <Transition :name="route.meta.transition" mode="out-in">
                <component
                 :is="Component"
                 :key="route.meta.transition ? route.fullPath : route.matched[0]?.path"/>
            </Transition>
        </router-view>
        

        <!-- <RouterView v-slot="{ Component, route }">
            <component :is="Component" :key="route.fullPath" />
        </RouterView> -->
        <!-- <router-view /> -->
      
    </div>
</template>

<script setup>
  // 引入 mdui 组件库
  import 'mdui/mdui.css'

  import { useRoute } from 'vue-router'

  import { navigationKey } from '@/router'

  const route = useRoute()

  
</script> 

<style>
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
    transition:
        transform .15s cubic-bezier(.2, 0, 0, 1),
        opacity .15s cubic-bezier(.2, 0, 0, 1);
}

/* ---------- 前进 ---------- */

.slide-left-enter-from {
    transform: translateX(24px)  scale(.98);
    opacity: 0;
}

.slide-left-leave-to {
    transform: translateX(-16px) scale(.95);
    opacity: 0;
}

/* ---------- 返回 ---------- */

.slide-right-enter-from {
    transform: translateX(-16px) scale(.98);
    opacity: 0;
}

.slide-right-leave-to {
    transform: translateX(24px) scale(.95);
    opacity: 0;
}
</style>


