<template>
    <div class="page-container mdui-prose" ref="pageContainer">
        <div style="text-align: center;">   

            <mdui-icon-error class="icon"></mdui-icon-error>

            <p class="title">{{  title  }}</p>

            <p class="message">{{ message }}</p>
            
            <div v-if="detail">
                <mdui-button class="detail-button" variant="text" @click="showDetail" >{{ pages.error.actions.detail }}</mdui-button>
            </div>


            <mdui-button class="home-button" @click="backHome" v-if="showHome">{{ pages.error.actions.back_home }}</mdui-button>

            
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

    import { pages } from './locales/index.js';

    const router = useRouter();
    const props = defineProps({
        title: {
            type: String,
            default: pages.error.default.t
        },
        message: {
            type: String,
            default: pages.error.default.message
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
            headline: pages.error.dialog.headline,
            description: detail.value,
            actions: [
                {
                    text: pages.error.dialog.actions.clickboard,
                    onClick: async () => {
                        try {
                            await navigator.clipboard.writeText(detail.value);
                            snackbar({
                                'message': pages.error.snackbar.copy_success,
                            })
                        } catch (error) {
                            snackbar({
                                'message': pages.error.snackbar.copy_failed
                            })
                            console.error(error);
                        } 
                    }
                },
                {
                    text: pages.common.text.confirm,
                    
                },
            ]
        })
    }

    onMounted(() => {
        if (props.hasTopbar) {
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

<style scoped>

    .page-container{
        height: calc(100vh - 80px);
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
    
    .title {
        font-size: 24px;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .message {
        font-size: 16px;
    }

    .detail-button {
        margin-top: 12px;
    }

    .home-button {
        margin-top: 12px;
    }
</style>