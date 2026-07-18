<template>
    
    <mdui-top-app-bar
        scroll-behavior="elevate shrink"
        class="topbar"
      >
        
        <slot name="left"></slot>

        <mdui-button-icon v-if="showBack" @click="goBack">
          <mdui-icon-arrow-back></mdui-icon-arrow-back>
        </mdui-button-icon>
        

        <mdui-button-icon v-if="isNotHomePage && showHome" @click="goHome">
          <mdui-icon-home></mdui-icon-home>
        </mdui-button-icon>
        
        <mdui-top-app-bar-title>{{ barTitle }}</mdui-top-app-bar-title>

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
    import { locale } from '@/locales/index.js'

    import { goBack } from '@/utils/routerHelper';


    const route = useRoute();
    const router = useRouter();

    const props = defineProps({
      title: {
        type: String,
        default: null
      },
      showHome: {
        type: Boolean,
        default: false
      },
      showBack: {
        type: Boolean,
        default: false
      }
    })

    const barTitle  = computed(() => {
        let title = ''
        if (props.title) {
            title = props.title
        } else if (route.meta.title) {
            title = route.meta.title
        } else {
            title = 'ForgeOrder'
        }
        
        return locale(title)
    
    })

    // 主页按钮 
    const isNotHomePage = computed(() => {
      return route.path !== '/';
    });

    function goHome() {
    if (route.path === '/') {
        return
    } else {
        router.push('/');
    } 
    }

    // 返回按钮 
    // function goBack() {
    //     if (route.matched == 1) {
    //       router.push('/')
    //     } else {
    //       router.push(
    //         route.path.split('/').slice(0, -1).join('/') || '/'
    //       )
    //     }
    // }
</script>

<style>
.topbar {
  align-items: center;
  position: sticky;
}
</style>