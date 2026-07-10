<template>
    <mdui-linear-progress v-if="modelValue" class="top-progress-bar"></mdui-linear-progress>
</template>

<script setup>
    import 'mdui/components/linear-progress.js'
    import { ref } from 'vue'

    const props = defineProps({
        modelValue: {
            type: Boolean,
            default: false
        }
    })  

    const emit = defineEmits(['update:modelValue'])

    const show = () => {
        emit('update:modelValue', true)
    }
    const hide = () => {
        emit('update:modelValue', false)
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
         z-index: 2000; /* 这个值放在了topBar上，对话框的遮罩层之下*/
        /* opacity: 0; */
    }
</style>