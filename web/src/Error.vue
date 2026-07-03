<template>
    <div class="page-container mdui-prose">
        <div style="text-align: center;">   

            <mdui-icon-error class="icon"></mdui-icon-error>

            <p style="font-size: 24px; margin-top: 8px; margin-bottom: 8px;">{{  title  }}</p>

            <p style="font-size: 16px">{{ message }}</p>
            
            <div class="button-container" v-if="detail">
                <mdui-button style="margin-top: 12px" variant="text" @click="showDetail" >详细信息</mdui-button>
                <mdui-button style="margin-top: 12px" @click="backHome">返回首页</mdui-button>
            </div>

            <mdui-button style="margin-top: 12px" @click="backHome" v-else>返回首页</mdui-button>

            
        </div>
    </div>
</template>

<script setup>
    import '@mdui/icons/error.js';
    import 'mdui/components/button.js';
    import { dialog } from 'mdui/functions/dialog.js'
    import { snackbar } from 'mdui/functions/snackbar.js';
    import { useRouter } from 'vue-router';

    const router = useRouter();
    const props = defineProps({
        title: {
            type: String,
            default: '错误'
        },
        message: {
            type: String,
            default: '发生了未知错误'
        },
        detail: {
            type: String,
            default: null
        },
    })

    const backHome = () => {
        router.push("/");
    }

    const showDetail = () => {
        dialog({
            headline: '详细信息',
            description: props.detail,
            actions: [
                {
                    text: '复制到剪切板',
                    onClick: async () => {
                        try {
                            await navigator.clipboard.writeText(props.detail);
                            snackbar({
                                'message': '复制成功',
                                placement: 'bottom-end'
                            })
                        } catch (error) {
                            snackbar({
                                'message': '复制失败'
                            })
                            console.error(error);
                        } 
                    }
                },
                {
                    text: '确定',
                },
            ]
        })
    }
    

</script>

<style>
    /* body {
        padding: 0;
        margin: 0;  
    } */

    .page-container{
        height: calc(100vh - 16px);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .icon {
        font-size: 60px;
    }

    .button-container {
        display: flex;
        justify-content: space-between;
        gap:20px
    }
</style>



