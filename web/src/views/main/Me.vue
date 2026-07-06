<template>
    <TopBar title="我的" showHome="false">
    </TopBar>

    <TipCard variant="filled" background-color="#BB1614" color="#fff" v-if="isDevelopment">
        <mdui-icon-warning style="flex-shrink: 0"></mdui-icon-warning>
        系统运行在“开发环境”上，可能影响性能与数据安全，请勿在生产环境中使用。
    </TipCard>


    <div class="container mdui-prose" >
        <div style="display: flex; padding: 12px; gap: 16px; align-items: center;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 32px; color: grey">
                <mdui-icon-manage-accounts v-if="isAdmin">
                </mdui-icon-manage-accounts>
                <mdui-icon-account-circle v-else>
                </mdui-icon-account-circle>
                </div>
            </div>

            <div>
                <div style="font-size: 24px">{{username}}</div>
                <div>{{isAdmin ? '管理员' : '服务员' }}</div>
            </div>
        </div>
        <mdui-divider></mdui-divider>

        <mdui-list>
            <mdui-list-item rounded @click="router.push('/printer/queue')">
                打印队列
                <mdui-icon-print slot="icon"></mdui-icon-print>
                <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right>
            </mdui-list-item>

            <mdui-list-item rounded @click="router.push('/me/settings')">
                用户与偏好设置
                <mdui-icon-app-settings-alt slot="icon"></mdui-icon-app-settings-alt>
                <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right>
            </mdui-list-item>

            <mdui-list-item rounded @click="router.push('/shop/settings')">
                店铺设置
                <mdui-icon-shopping-cart slot="icon"></mdui-icon-shopping-cart>
                <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right>
            </mdui-list-item>

            <mdui-list-item rounded @click="router.push('/system/logs')">
                系统日志
                <mdui-icon-receipt slot="icon"></mdui-icon-receipt>
                <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right>
            </mdui-list-item>

            <mdui-list-item rounded @click="router.push('/system/about')">
                关于系统
                <mdui-icon-info slot="icon"></mdui-icon-info>
                <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right>
            </mdui-list-item>


            <mdui-list-item rounded @click="handleLogout">
                退出登录
                <mdui-icon-logout slot="icon"></mdui-icon-logout>
                <!-- <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right> -->
            </mdui-list-item>
            
        </mdui-list>
    </div>

    <div class="footer">
        <div style="font-size: 11px; display: flex; justify-content: center; gap: 12px;">
            <span>IP Address: {{ ipAddress }}</span>
            <span>Version: {{ version }} ({{ isDevelopment ? 'develop' : 'product' }})</span>
        </div>
    </div>
    
</template>
    
<script setup>
    import TopBar from '@/components/TopBar.vue'
    import TipCard from '@/components/TipCard.vue'

    import 'mdui/components/card.js'
    import 'mdui/components/list.js'
    import 'mdui/components/list-item.js'
    import 'mdui/components/divider.js'
    import { snackbar } from 'mdui/functions/snackbar.js';

    import '@mdui/icons/account-circle.js'
    import '@mdui/icons/manage-accounts.js'
    import '@mdui/icons/print.js'
    import '@mdui/icons/chevron-right.js'
    import '@mdui/icons/app-settings-alt.js'
    import '@mdui/icons/logout.js'
    import '@mdui/icons/shopping-cart.js'
    import '@mdui/icons/receipt.js'
    import '@mdui/icons/info.js'

    import { ref, computed } from 'vue'
    import { useRouter } from 'vue-router'

    import { useAuth } from '@/composables/auth.js'

    const { logout } = useAuth()

    const router = useRouter()

    const isDevelopment = ref(false)

    const username = computed(() => JSON.parse(localStorage.getItem('userInfo')).username)

    const isAdmin = computed(() => JSON.parse(localStorage.getItem('userInfo')).is_admin)

    const ipAddress = ref('192.168.1.5')

    const version = ref('1.0.0')

    const handleLogout = async () => {
        await logout()
        
        snackbar({
            message: '退出登录成功',
        })
        
        router.push('/login')

        

    }



    


</script>

<style>
    .footer {
        position: fixed;
        bottom: 90px;
        left: 0;
        width: 100%
    }
</style>
