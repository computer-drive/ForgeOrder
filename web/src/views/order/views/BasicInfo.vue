<template>
    <div class="main-container" style="height: calc(100vh - 64px); width:100vw; display: flex; flex-direction: column; box-sizing: border-box;">    
        <div class="container mdui-prose " style="display:flex; flex-direction:column; flex:1; min-height:0; overflow:hidden; width: calc(100% - 24px);">
            <h2>创建订单</h2>

            <mdui-list style="display:flex; flex-direction:column; flex:1; min-height:0; overflow:hidden">
                <mdui-list-item nonclickable>订单类型
                    <mdui-radio-group value="0" slot="end-icon" v-model="orderType">
                        <mdui-radio value="0">堂食</mdui-radio>
                        <mdui-radio value="1">外带</mdui-radio>
                    </mdui-radio-group>
                </mdui-list-item>

                <mdui-list-item nonclickable>
                    就餐人数
                        <NumberSelect slot="end-icon" v-model="partySize" :onChanged="onPartySizeChange"/>
                </mdui-list-item>

                <mdui-list-item nonclickable>
                    就餐桌台
                </mdui-list-item>
                
                <div v-if="orderType == '0'" style="flex: 1; min-height: 0; overflow-y: auto;">
                    <div class="loading-tables" v-if="loadingStatus == 1">
                        <mdui-circular-progress></mdui-circular-progress>
                        正在加载桌台信息
                    </div>

                    <div class="loading-tables" v-else-if="loadingStatus == 2">
                        <mdui-icon-error style="width: 48px; height: 48px;"></mdui-icon-error>
                        加载失败，请重试    
                    </div>
                    <TablesContainer :tables="tables" v-model="selectedTable" v-else />
                </div>
            </mdui-list>

        </div>

        <mdui-bottom-app-bar scroll-target=".main-container" style="position: relative; flex-shrink: 0;">
            
            <div style="flex-grow: 1"></div>
            <mdui-button 
            @click="nextStep" 
            style="height: 56px; border-radius: var(--mdui-shape-corner-large);"
            :disabled="orderType == '0' && selectedTable == -1"
            >
                下一步
                <mdui-icon-arrow-forward slot="icon" style="width: 24px; height: 24px;"></mdui-icon-arrow-forward>
            </mdui-button>
        </mdui-bottom-app-bar>


    </div>
</template>

<script setup> 
    import 'mdui/components/list.js';
    import 'mdui/components/list-item.js';
    import 'mdui/components/radio-group.js';
    import 'mdui/components/radio.js';
    import 'mdui/components/bottom-app-bar.js';

    import '@mdui/icons/error.js';
    import '@mdui/icons/arrow-forward.js';

    import NumberSelect from '@/components/NumberSelect.vue'
    
    import TablesContainer from '../components/TablesContainer.vue';
    import { ref, onMounted } from 'vue'
    import request from '@/utils/request.js'
    
    const props = defineProps(['index', 'orderInfo'])
    const emit = defineEmits(['update:index', 'update:orderInfo'])

    

    const partySize = ref(1)
    const orderType = ref('0')
    const tables = ref([])
    const loadingStatus = ref(1)
    const selectedTable = ref(-1)

    const onPartySizeChange = (oldVal, newVal) => {
        if (newVal > 0) {
            return true
        }
        return false
    }

    const loadTables = async () => {
        try {
            const res = await request.get('/shop/tables/getAll')
        
            if (res.data.status == 0) {
                tables.value = res.data.data
                loadingStatus.value = 0
            } else {
                loadingStatus.value = 2
            }
        } catch (error) {
            console.error(error)
            loadingStatus.value = 2
        } 
}

    onMounted(() => {
        loadTables()
    })

    const nextStep = () => {
        let tableName = ''
        if (orderType.value == '1') {
            selectedTable.value = -1
        } else {
            const index = tables.value.findIndex(table => table.id == selectedTable.value)
            if (index >= 0) {
                tableName = tables.value[index].name
            }
        }
        emit('update:index', props.index + 1)
        emit('update:orderInfo', {
            "order_type": orderType.value,
            "party_size": partySize.value,
            "table_id": selectedTable.value,
            "table_name": tableName
        })
    }

</script>

<style>
    .loading-tables {
        display: flex;
        flex-direction: column;
        gap: 20px;
        justify-content: center;
        align-items: center;
        height: 20vh;  
    }
</style>