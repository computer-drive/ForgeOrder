<template>

    <mdui-navigation-bar label-visibility="selected" ref="bottomBar">
        <mdui-navigation-bar-item @click="handleClick(0)" value="0">
          {{ $t('Cbottom_bar.text.main') }}
         <mdui-icon-home--outlined slot="icon"></mdui-icon-home--outlined>
         <mdui-icon-home slot="active-icon"></mdui-icon-home>
        </mdui-navigation-bar-item>

        <mdui-navigation-bar-item @click="handleClick(1)" value="1">
          {{  $t('Cbottom_bar.text.orders') }}
          <mdui-icon-list-alt slot="icon"></mdui-icon-list-alt>
        </mdui-navigation-bar-item>


        <mdui-navigation-bar-item @click="handleClick(2)" value="2">
          {{ $t('Cbottom_bar.text.me') }}
          <mdui-icon-account-circle--outlined slot="icon"></mdui-icon-account-circle--outlined>
          <mdui-icon-account-circle slot="active-icon"></mdui-icon-account-circle>
        </mdui-navigation-bar-item>
      </mdui-navigation-bar>

</template>

<script setup>
import 'mdui/components/navigation-bar.js';
import 'mdui/components/navigation-bar-item.js';

import '@mdui/icons/home.js';
import '@mdui/icons/home--outlined.js';
import '@mdui/icons/list-alt.js';
import '@mdui/icons/account-circle--outlined.js'; 
import '@mdui/icons/account-circle.js';

import { ref, onMounted, computed, watch } from 'vue';

const index = ref(0)
const bottomBar = ref(null)

const handleClick = (newVal) => {
  // console.log(newVal)
  updateIndex(newVal)

  // const url = new URL(window.location.href)
  // url.searchParams.set('index', index.value?.toString() || '0')

}
const updateIndex = (newVal) => {
  index.value = newVal
}

const setSelected = (newVal) => {
  bottomBar.value.setAttribute('value', newVal)
}




defineExpose({
  updateIndex,
  index,
  setSelected,
})

// onMounted(() => {
//   // 根据当前路由设置底部导航栏的选中项
//   if (route.path === '/') {
//     bottomBar.value.setAttribute('value', 'home')
    
//   } else if (route.path === '/orders') {
//     bottomBar.value.setAttribute('value', 'orders')
//   } else if (route.path === '/me') {
//     bottomBar.value.setAttribute('value', 'me')
//   }
// })




</script>