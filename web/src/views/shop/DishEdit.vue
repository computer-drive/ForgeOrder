<template>
    <TopProgressBar v-model="isLoading"/>

    <div class="container mdui-prose">
        <h1>编辑“{{ dishData.name }}”</h1>
        <div style="margin-bottom: 24px; font-size: 18px">在下方更改菜品信息，点击右上角的“保存”按钮以应用更改。    </div>

        <div>

            <div class="setting-item">
                <div class="setting-item-key">菜品名称</div>
                <div class="setting-item-value">
                    
                    <mdui-text-field 
                    variant="outlined" ></mdui-text-field>
            
                </div>
            </div>

            <div class="setting-item">
                菜品描述
                <mdui-text-field 
                    class="setting-item-value"
                    autosize
                    min-rows="1"
                    max-rows="3"
                    variant="outlined"></mdui-text-field>
            </div>

            <div class="setting-item">
                菜品价格
                <mdui-text-field 
                    class="setting-item-value"
                    variant="outlined" 
                    readonly 
                    @click="openPriceInputDialog" 
                    :value="price"
                    > 
                    <div slot="icon">￥</div>
                </mdui-text-field>
            </div>

            <div class="setting-item">
                启用此菜品
                <mdui-switch></mdui-switch>
            </div>

            <div class="setting-item">
                分类
                <mdui-select value="1" variant="outlined" class="setting-item-value">
                    <mdui-menu-item value="1">Item 1</mdui-menu-item>
                    <mdui-menu-item value="2">Item 2</mdui-menu-item>
                    <mdui-icon-arrow-drop-down slot="end-icon"></mdui-icon-arrow-drop-down>
                </mdui-select>
            </div>

            <div class="setting-item">
                选项
                <mdui-button-icon>
                    <mdui-icon-add></mdui-icon-add>
                </mdui-button-icon>
            </div>    

            <mdui-list>
                    <mdui-list-item nonclickable rounded class="choices-item">
                        <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px">    
                            <div style="flex-shrink: 0;">是否可以   </div>
                            
                            <div style="display: flex; align-items: center; gap: 6px">
                                
                                <div style="display:flex; flex-wrap: wrap; gap: 6px;">
                                    <mdui-chip style="padding:0px">不辣</mdui-chip>
                                    <mdui-chip >不辣</mdui-chip>
                                    <mdui-chip >不辣</mdui-chip>
                                    <mdui-chip >不辣</mdui-chip>
                                </div>

                                <mdui-button-icon variant="filled">
                                    <mdui-icon-add></mdui-icon-add>
                                </mdui-button-icon>

                            </div>
                        </div>
                        

                    </mdui-list-item>

             </mdui-list>    


        </div>
    </div>

    <mdui-dialog ref="priceInputDialog" class="price-input-dialog" close-on-overlay-click>
        <div class="price-input-"></div>
        <div class="price-input-content">
            <div class="price-content">
                {{ currentText }}
            </div>
            <div class="price-input-container">
                <div class="price-input">
                    <mdui-button variant="text" class="price-num-button" @click="inputText('1')">1</mdui-button>
                    <mdui-button variant="text" class="price-num-button" @click="inputText('2')">2</mdui-button>
                    <mdui-button variant="text" class="price-num-button" @click="inputText('3')">3</mdui-button>
                    <mdui-button variant="text" class="price-num-button" @click="backspaceText">
                        <mdui-icon-backspace></mdui-icon-backspace>
                    </mdui-button>

                    <mdui-button variant="text" class="price-num-button" @click="inputText('4')">4</mdui-button>
                    <mdui-button variant="text" class="price-num-button" @click="inputText('5')">5</mdui-button>
                    <mdui-button variant="text" class="price-num-button" @click="inputText('6')">6</mdui-button>
                    <mdui-button variant="text" class="price-num-button" @click="clearText">
                        <mdui-icon-clear></mdui-icon-clear>
                    </mdui-button>

                    <mdui-button variant="text" class="price-num-button" @click="inputText('7')">7</mdui-button>
                    <mdui-button variant="text" class="price-num-button" @click="inputText('8')">8</mdui-button>
                    <mdui-button variant="text" class="price-num-button" @click="inputText('9')">9</mdui-button>
                    <mdui-button class="price-big-button" variant="filled" @click="handleSubmit">
                        <mdui-icon-keyboard-return></mdui-icon-keyboard-return>
                    </mdui-button>

                    <mdui-button variant="text" class="price-num-button" style="visibility: hidden;">9</mdui-button>
                    <mdui-button variant="text" class="price-num-button" @click="inputText('0')">0</mdui-button>
                    <mdui-button variant="text" class="price-num-button" @click="inputText('.')">.</mdui-button>
                </div>
            </div>
        </div>
    </mdui-dialog>
</template> 

<script setup>
    import '@/assets/shop.dish_edit.css'

    import { ref, inject, h, onMounted, onBeforeUnmount } from 'vue'

    import 'mdui/components/text-field.js'
    import 'mdui/components/dialog.js'
    import 'mdui/components/list.js'
    import 'mdui/components/list-item.js'
    import 'mdui/components/list-subheader.js'
    import 'mdui/components/switch.js'
    import 'mdui/components/select.js'
    import 'mdui/components/menu-item.js'
    import 'mdui/components/button.js'
    import 'mdui/components/chip.js'

    import '@mdui/icons/edit.js'
    import '@mdui/icons/backspace.js'
    import '@mdui/icons/clear.js'
    import '@mdui/icons/keyboard-return.js'
    import '@mdui/icons/arrow-drop-down.js'
    import '@mdui/icons/add.js'
    import '@mdui/icons/save.js'

    import TopProgressBar from '@/components/TopProgressBar.vue'

    defineProps({
        id: {
            type: String,
            default: ''
        },
        isNew: {
            type: Boolean,
            default: false
        }
    })

    const { setRightComponent, clearRightComponent } = inject('rightComponent')

    const isLoading = ref(false)

    const dishData = ref({})
    const price = ref(0)

    const priceInputDialog = ref(null)
    const currentText = ref('0')


    const openPriceInputDialog = () => {
        currentText.value = price.value.toString()
        priceInputDialog.value.open = true
        
    }

    const inputText = (text) => {
        if (currentText.value == '0') {
            currentText.value = text
        } else {
            if (text == '.' ) {
                if (currentText.value.indexOf('.') != -1) {
                    // 已存在小数点，不允许再输入
                    return 
                }
            }

            if (currentText.value.indexOf('.') != -1) {
                // 已存在小数点，判断小数点后的数字是否超过两位
                if (currentText.value.length - currentText.value.indexOf('.') > 2) {
                    // 小数点后的数字超过两位，不允许再输入
                    return 
                }
            }

            
            currentText.value += text
        }
    }

    const clearText = () => {
        currentText.value = '0'
    }

    const backspaceText = () => {
        if (currentText.value.length > 1) {
            currentText.value = currentText.value.slice(0, -1)
        } else {
            currentText.value = '0'
        }
    }

    const handleSubmit = () => {
        priceInputDialog.value.open = false
        price.value = Number(currentText.value)
        // currentText.value = '0'
    }

    const handleSave = () => {
        // 保存菜品数据
    }


    onMounted(() => {
        // 设置居右的保存按钮组件
        setRightComponent(h('mdui-button-icon', {
            onClick: handleSave
        }, [
            h('mdui-icon-save')
        ]))

        // 获取菜品数据
        isLoading.value = true


    })

    onBeforeUnmount(() => {
        clearRightComponent()
    })

   </script>
