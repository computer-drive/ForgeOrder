<template>

    <mdui-navigation-bar label-visibility="selected" ref="bottomBar">
        <mdui-navigation-bar-item @click="goHome" value="home">
          主页
         <mdui-icon-home--outlined slot="icon"></mdui-icon-home--outlined>
         <mdui-icon-home slot="active-icon"></mdui-icon-home>
        </mdui-navigation-bar-item>

        <mdui-navigation-bar-item @click="goOrders" value="orders">
          订单
          <mdui-icon-list-alt slot="icon"></mdui-icon-list-alt>
        </mdui-navigation-bar-item>


        <mdui-navigation-bar-item @click="goMe" value="me">
          我的
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

import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

function goHome() {
  if (route.path === '/') {
    return
  } else {
    router.push('/');
  } 
}

function goOrders() {
  if (route.path === '/orders') {
    return
  } else {
    router.push('/orders');
  } 
}

function goMe() {
  if (route.path === '/me') {
    return
  } else {
    router.push('/me');
  } 
}


// 底部导航栏
const bottomBar = ref(null);





onMounted(() => {
  // 根据当前路由设置底部导航栏的选中项
  if (route.path === '/') {
    bottomBar.value.setAttribute('value', 'home')
    
  } else if (route.path === '/orders') {
    bottomBar.value.setAttribute('value', 'orders')
  } else if (route.path === '/me') {
    bottomBar.value.setAttribute('value', 'me')
  }
})




</script>