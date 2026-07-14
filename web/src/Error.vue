<template>
    <div class="page-container mdui-prose" ref="pageContainer">
        <div style="text-align: center;">   

            <mdui-icon-error class="icon"></mdui-icon-error>

            <p style="font-size: 24px; margin-top: 8px; margin-bottom: 8px;">{{  title  }}</p>

            <p style="font-size: 16px">{{ message }}</p>
            
            <div v-if="detail">
                <mdui-button style="margin-top: 12px" variant="text" @click="showDetail" >{{$t("error.actions.detail")}}</mdui-button>
            </div>

            <!-- <mdui-button style="margin-top: 12px" variant="text" @click="showDetail" v-else-if="detail">详细信息</mdui-button> -->



            <mdui-button style="margin-top: 12px" @click="backHome" v-if="showHome">{{$t("error.actions.back_home")}}</mdui-button>

            
        </div>
    </div>
</template>

<script setup>
    import '@mdui/icons/error.js';
    import 'mdui/components/button.js';
    import { dialog } from 'mdui/functions/dialog.js'
    import { snackbar } from 'mdui/functions/snackbar.js';
    import { useRouter } from 'vue-router';
    import { onMounted, ref } from 'vue';
    import { t } from './locales/index.js';

    const router = useRouter();
    const props = defineProps({
        title: {
            type: String,
            default: t("error.default.title")
        },
        message: {
            type: String,
            default: t("error.default.message")
        },
        detail: {
            type: String,
            default: null
        },
        hasTopbar: {
            type: Boolean,
            default: false
        },
        showHome: {
            type: Boolean,
            default: true
        }
    })

    const pageContainer = ref(null)

    const title = ref(props.title)
    const message = ref(props.message)
    const detail = ref(props.detail)

    const backHome = () => {
        router.push("/");
    }

    const showDetail = () => {
        dialog({
            headline: t("error.dialog.headline"),
            description: detail.value,
            actions: [
                {
                    text: t("error.dialog.actions.clickboard"),
                    onClick: async () => {
                        try {
                            await navigator.clipboard.writeText(detail.value);
                            snackbar({
                                'message': t("error.snackbar.copy_success"),
                                placement: 'bottom-end'
                            })
                        } catch (error) {
                            snackbar({
                                'message': t("error.snackbar.copy_failed")
                            })
                            console.error(error);
                        } 
                    }
                },
                {
                    text: t("common.text.confirm"),
                    onClick: () => {
                        dialog.close();
                    }
                },
            ]
        })
    }

    onMounted(() => {
        if (props.hasTopbar) {
            // pageContainer.value.style['padding-top'] = '64px'
            pageContainer.value.style['height'] = 'calc(100vh - 80px)'
        }
    })

    const setInfo = (title_, message_, detail_) => {
        title.value = title_
        message.value = message_
        detail.value = detail_
    }

    defineExpose({
        setInfo
    })
    
    

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