<template>
    
    <mdui-top-app-bar
        scroll-behavior="elevate shrink"
        style="align-items: center;"
      >
        
        <mdui-button-icon v-if="canGoBack" @click="goBack">
          <mdui-icon-arrow-back></mdui-icon-arrow-back>
        </mdui-button-icon>
        

        <mdui-button-icon v-if="isNotHomePage && showHome === 'true'" @click="goHome">
          <mdui-icon-home></mdui-icon-home>
        </mdui-button-icon>
        
        <mdui-top-app-bar-title>{{ title }}</mdui-top-app-bar-title>

        <slot name="right"></slot> 

      </mdui-top-app-bar>
</template> 

<script setup>
    import 'mdui/components/top-app-bar.js'
    import 'mdui/components/top-app-bar-title.js'
    import 'mdui/components/button-icon.js';

    import '@mdui/icons/home.js';
    import '@mdui/icons/arrow-back.js';

    import { computed } from 'vue';
    import { useRoute, useRouter } from 'vue-router';


    const route = useRoute();
    const router = useRouter();

    const props = defineProps({
      title: {
        type: String,
        default: 'ForgeOrder'
      },
      showHome: {
        type: String,
        default: 'true'
      }
    })

    // 返回与主页按钮 
    const isNotHomePage = computed(() => {
    return route.path !== '/';
    });

    const canGoBack = computed(() => {
    });

    function goHome() {
    if (route.path === '/') {
        return
    } else {
        router.push('/');
    } 
    }
</script>
