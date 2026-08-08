<template>
    <div class="main-container" style="height: calc(100vh - 64px); width:100vw; display: flex; flex-direction: column; box-sizing: border-box;">    
        <div class="container mdui-prose " style="display:flex; flex-direction:column; flex:1; min-height:0; overflow-y: auto; width: calc(100% - 24px);">
            <h2>创建订单</h2>

            <h3>订单信息</h3>
            <mdui-list>
                <mdui-list-item rounded>
                    订单类型
                    <div slot="end-icon" style="font-size: 16px;">{{ props.orderInfo.order_type == '0' ? '堂食' : '外带' }}</div>
                </mdui-list-item>

                <mdui-list-item rounded v-if="props.orderInfo.order_type == '0'">
                    桌台
                    <div slot="end-icon" style="font-size: 16px;">{{ props.orderInfo.table_name }}</div>
                </mdui-list-item>

                <mdui-list-item rounded v-if="props.orderInfo.order_type == '0'">
                    人数
                    <div slot="end-icon" style="font-size: 16px;">{{ props.orderInfo.party_size }}</div>
                </mdui-list-item>

                <mdui-list-item rounded>
                    菜品
                </mdui-list-item>

                     
    
            </mdui-list>

            <div v-for="dish in dishInfo['dishes']" :key="dish" style="display: flex; justify-content: space-between; padding-left: 16px; padding-right: 16px; font-size: 14px">
        
                {{ dish.dishInfo.name }}
                <span v-for="(choice, name) in dish.choices">,{{ choice }}</span>
                <div style="margin-left: auto">x {{ dish.count }}</div>
            </div> 

            <mdui-divider style="margin-top: 10px; margin-bottom: 10px"></mdui-divider>

            <h3 style="margin-top: 0px">备注</h3>

            <mdui-text-field rows="5" variant="outlined" placeholder="无" v-model="note"></mdui-text-field>


        </div>

        <mdui-bottom-app-bar scroll-target=".main-container" style="position: relative; flex-shrink: 0;">
            
            <div style="flex-grow: 1"></div>
            <mdui-fab style="height: 56px; border-radius: var(--mdui-shape-corner-large)" @click="prevStep">
                    <mdui-icon-arrow-back slot="icon" style="width: 24px; height: 24px;"></mdui-icon-arrow-back>
                </mdui-fab>
                
            <mdui-button 
            style="height: 56px; border-radius: var(--mdui-shape-corner-large);"
            @click="nextStep"
            >   
                去下单
                <mdui-icon-done slot="icon" style="width: 24px; height: 24px;"></mdui-icon-done>
            </mdui-button>
        </mdui-bottom-app-bar>


    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'

    import '@mdui/icons/done.js'

    const props = defineProps(["orderInfo", "dishInfo", "index"])

    const emit = defineEmits(['update:index'])

    const note = ref('')


    const prevStep = () => {
            emit('update:index', props.index - 1)
    }

    const nextStep = () => {
        const orderInfo = props.orderInfo

        orderInfo.dishes = props.dishInfo['dishes']
        orderInfo.note = note.value

        console.log(orderInfo)
    }
</script>