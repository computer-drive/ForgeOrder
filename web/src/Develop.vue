<template>
    <TopBar title="开发人员选项"/>
    <div class="mdui-prose container">
        <p>这些设置仅供开发人员使用。</p>

        <mdui-list>
            <mdui-list-subheader>用户认证</mdui-list-subheader>
            <mdui-list-item 
            headline="测试登录状态"
            description="调用API测试。若未登录将跳转到登录页面。" nonclickable>
            <mdui-button slot="end-icon" @click="testApi">Test</mdui-button>
        </mdui-list-item>

            <mdui-list-item>Item 2</mdui-list-item>
        </mdui-list>


    </div>
</template>

<script setup>
    import TopBar from '@/components/Topbar.vue'

    import 'mdui/components/list.js';
    import 'mdui/components/list-item.js';
    import 'mdui/components/list-subheader.js';
    import 'mdui/components/button.js';
    import { snackbar } from 'mdui/functions/snackbar.js';
    import request from '@/utils/request.js'
    
    const testApi = async () => {

    const response = await request.get("/auth/test")
    snackbar({
        message: response.data.data,
    })
}
</script>