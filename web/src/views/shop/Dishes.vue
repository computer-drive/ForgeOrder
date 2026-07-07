<template>
    <div class="container mdui-prose">
        <h2>所有菜品</h2>
    </div>

    
</template> 

<script setup>
import { inject, h, onMounted } from 'vue'

import '@mdui/icons/add.js';


const setRightComponent = inject('setRightComponent')

const addDish = () => {}

onMounted(() => {
    setRightComponent(h('mdui-button-icon', {
        onClick: addDish
    }, [
        h('mdui-icon-add')
    ]))
})


</script>