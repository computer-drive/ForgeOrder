<template>
    <mdui-linear-progress v-if="isShow" class="top-progress-bar"></mdui-linear-progress>
</template>

<script setup>
    import 'mdui/components/linear-progress.js'
    import { ref } from 'vue'

    const isShow = ref(false)

    const show = () => {
        isShow.value = true
    }
    const hide = () => {
        isShow.value = false
    }

    defineExpose({
        show,
        hide
    })
</script>

<style>
    .top-progress-bar {
         position: fixed; 
         top: 0; 
         left: 0; 
         z-index: 10000;
        /* opacity: 0; */
    }
</style>