<template>
    
   <BasicInfo v-show="index == 0" v-model:index ="index" v-model:orderInfo="orderBasicInfo"/>
   <Dishes v-show="index == 1" v-model:index ="index" v-model:dishInfo="dishInfo"/>
   <Confirm v-show="index == 2" v-model:index ="index" v-model:orderInfo="orderBasicInfo" v-model:dishInfo="dishInfo"/>

</template> 


<script setup>
    import '@/assets/transition.css'
    import { ref, watch, defineAsyncComponent } from 'vue'

    const BasicInfo = defineAsyncComponent(
  () => import('@/views/order/views/BasicInfo.vue')
)

    const Dishes = defineAsyncComponent(
  () => import('@/views/order/views/Dishes.vue')
)
     const Confirm = defineAsyncComponent(
  () => import('@/views/order/views/Confirm.vue')
)

    const index= ref(0)

    const orderBasicInfo = ref({})
    const dishInfo = ref({})

    const nextPage = () => {
        index.value++
    }

    watch(
        () => index.value,
        (newlVal, oldVal) => {
            console.log(orderBasicInfo.value)
            console.log(dishInfo.value)
        }
    )


    
</script>

<style>
    /* .bottom-bar {
        position:   ;
    } */

</style>