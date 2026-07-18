<template>
    <TopProgressBar v-model="isLoading"/>

    <NumberKeyboardDialog
     ref="priceInputDialog" 
    :money_input="true"
    @confirm="dishData.price = $event"
     ></NumberKeyboardDialog>
    
    <div v-if="isLoading"   style="
    position: fixed;
    inset: 0;
    background-color: rgba(230, 230, 230, 0.1);
    z-index: 2100;
">

    </div>

    <div class="container mdui-prose" v-if="!isError">

        <h2 v-if="!isNew">{{ $t('shop.dish_edit.title', {name: dishData.name}) }}</h2> 
        <h2 v-else>{{ $t('shop.new_dish.title') }}</h2> 

        <div style="margin-bottom: 24px; font-size: 18px">
            <span v-if="isNew">{{ $t('shop.new_dish.description') }}</span>
            <span v-else>{{ $t('shop.dish_edit.description') }}</span>
        </div>

        <div>

            <div class="setting-item">
                <div class="setting-item-key">{{ $t('shop.dish_edit.dish_name') }}</div>
                <div class="setting-item-value">
                    
                    <mdui-text-field 
                    ref="nameInput"
                    v-model="dishData.name"
                    :disabled="isLoading"
                    variant="outlined" ></mdui-text-field>
            
                </div>
            </div>

            <div class="setting-item">
                <div class="setting-item-key">{{ $t('shop.dish_edit.dish_description') }}</div>
                <mdui-text-field 
                    class="setting-item-value"
                    autosize
                    min-rows="1"
                    max-rows="3"
                    v-model="dishData.description"
                    :disabled="isLoading"
                    variant="outlined"></mdui-text-field>
            </div>

            <div class="setting-item">
                <div class="setting-item-key">{{ $t('shop.dish_edit.dish_price') }}</div>
                <mdui-text-field 
                    ref="priceInput"    
                    class="setting-item-value"
                    variant="outlined" 
                    @click="priceInputDialog.open(dishData.price)"
                    :disabled="isLoading"
                    v-model="dishData.price"
                    
                    > 
                    <div slot="icon">￥</div>
                </mdui-text-field>
            </div>

            <div class="setting-item">
                <div class="setting-item-key">{{ $t('shop.dish_edit.dish_available') }}</div>
                <mdui-switch :checked="dishData.is_available" ref="isAvailableSwitch" :disabled="isLoading"></mdui-switch>
            </div>

            <div class="setting-item">
                <div class="setting-item-key">{{ $t('shop.dish_edit.category') }}</div>
                <mdui-select 
                    ref="categoryInput"
                    variant="outlined" 
                    class="setting-item-value"
                    :disabled="isLoading"
                    
                >
                    <mdui-menu-item 
                        v-for="category in categories" 
                        :key="category.id"
                        :value="category.id"
                    >{{ category.name }}</mdui-menu-item>
                    <mdui-icon-arrow-drop-down slot="end-icon"></mdui-icon-arrow-drop-down>
                </mdui-select>
                <!-- <div v-else>加载中</div> -->
            </div>

            <div class="setting-item">
                <div class="setting-item-key">{{ $t('shop.dish_edit.choices') }}</div>
                <mdui-button-icon @click="addNewChoices">
                    <mdui-icon-add></mdui-icon-add>
                </mdui-button-icon>
            </div>    

            <mdui-list>
                    <div v-for="(options, name) in dishData.choices">

                        <mdui-list-item nonclickable rounded class="choices-item">

                            <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px">    
                               
                                <div style="flex-shrink: 0;">{{ name }}</div>
                                
                                <div style="display: flex; align-items: center; gap: 6px">
                                    
                                    <div style="display:flex; flex-wrap: wrap; gap: 6px;">
                                        <mdui-chip v-for="option in options" @click="deleteOption(name, option)">{{ option }}</mdui-chip>
                                    </div>
 

                                </div>

                                <div style="display: flex; gap: 8px">
                                    <mdui-button-icon variant="tonal" @click="addNewOption(name)">
                                            <mdui-icon-add></mdui-icon-add>
                                    </mdui-button-icon>

                                    
                                </div>

                            </div>

                        </mdui-list-item>
                    </div>

             </mdui-list>    


        </div>
    </div>
    
    <div v-else>
        <Error :hasTopbar="true" ref="errorPage" :showHome="false">
        </Error>
    </div>

    
</template> 

<script setup>
    import '@/assets/shop.dish_edit.css'

    import { ref, inject, h, onMounted, onBeforeUnmount, nextTick } from 'vue'
    import { useRoute, useRouter } from 'vue-router'

    import 'mdui/components/text-field.js'
    import 'mdui/components/dialog.js'
    import 'mdui/components/list.js'
    import 'mdui/components/list-item.js'
    import 'mdui/components/list-subheader.js'
    import 'mdui/components/switch.js'
    import 'mdui/components/select.js'
    import 'mdui/components/menu-item.js'
    
    import 'mdui/components/chip.js'

    import { prompt } from 'mdui/functions/prompt.js'
    import { dialog } from 'mdui/functions/dialog.js'
    import { alert } from 'mdui/functions/alert.js'
    import { snackbar } from 'mdui/functions/snackbar.js'

    import '@mdui/icons/edit.js'
    
    import '@mdui/icons/arrow-drop-down.js'
    import '@mdui/icons/add.js'
    import '@mdui/icons/save.js'
    import '@mdui/icons/delete.js'

    import TopProgressBar from '@/components/TopProgressBar.vue'
    import NumberKeyboardDialog from '@/components/NumberKeyboardDialog.vue'
    import Error from '@/Error.vue'


    import { t } from '@/locales/index.js'    
    import request from '@/utils/request.js'

    import { pushWithFrom } from '@/utils/routerHelper'


    const props = defineProps({
        id: {
            type: String,
            default: ''
        },
        isNew: {
            type: Boolean,
            default: false
        }
    })

    const route = useRoute()
    const router = useRouter()

    const { setRightComponent, clearRightComponent } = inject('rightComponent')

    const isLoading = ref(false)
    const isError= ref(false)

    const priceInputDialog = ref(null)
    const errorPage = ref(null)

    const categoryInput = ref(null)
    const nameInput = ref(null)
    const priceInput = ref(null)
    const isAvailableSwitch = ref(null)
    const saveButton = ref(null)

    const dishData = ref({})
    let originDishData = {}
    const categories = ref([])
    let choicesChanging = []
    


    const saveChanged = async(changed, choicesChanging) => {
        try {
            const dishId = route.params.id
            // console.log(dishId)

            const res = await request.post(`/shop/dishes/update`, {
                dish_id: Number(dishId),
                changed_items: changed,
                changed_choices: choicesChanging,
            })

    
            if (res.data.status == 0) {
                // 刷新菜品数据
                snackbar({
                    message: t("shop.dish_edit.snackbar.success")
                })
                pushWithFrom("/shop/dishes")
            } else {
                alert({
                    headline: t("shop.dish_edit.error_alert.headline"),
                    description: '' + res.data.data,
                    confirmText: t("common.text.confirm")
                })
            }
             
        } catch (error) {
            if (error.response.status === 401 && error.response.data?.status == 2002) {
                alert({
                headline: t("shop.dish_edit.save_error_alert.headline"),
                description: t("shop.dish_edit.save_error_alert.description_permission"),
                confirmText: t("common.text.confirm")
            })

            } else if (error.response.status == 400 && error.response.data?.status == 3001) {
                snackbar({
                    message: t("shop.dish_edit.snackbar.no_change")
                })
            } else {
                alert({
                headline: t("shop.dish_edit.save_error_alert"),
                description: t("shop.dish_edit.save_error_alert.message", {error: error.message}),
                confirmText: t("common.text.confirm")
            })
            }
            
        } 
    }

    const saveNew = async(dishData_) => {
        console.log(dishData_)
        try {
            const res = await request.post(`/shop/dishes/new`, dishData_)
            if (res.data.status == 0) {
                snackbar({
                    message: t("shop.new_dish.snackbar.success")
                })
                router.push("/shop/dishes")
            } else if (res.data.data?.status == 3001) {
                snackbar({
                    message: t("shop.new_dish.snackbar.no_category")
                })
            }
        } catch(error) {
            alert({
                headline: t("shop.new_dish.error_alert.headline"),
                description: t("shop.new_dish.error_alert.message", {error: error.message}),
                confirmText: t("common.text.confirm")
            })
        }
    }


    const handleSave = async (event) => {
        isLoading.value = true

        nameInput.value.setCustomValidity('')

        // 通过事件对象获取按钮元素
        const button = event?.currentTarget
    
        if (button) {
            // button.loading = true
        }
        
        // 保存菜品数据
        let dishData_ = {...dishData.value,}

        dishData_.price *= 100 // 转换为分
        dishData_.is_available = isAvailableSwitch.value.checked

        if (typeof categoryInput.value.value == 'string') {
            let category = -1 
            for ( let i = 0; i < categories.value.length; i++) {
                if (categories.value[i].name == categoryInput.value.value) {
                    category = categories.value[i].id
                    break
                }
            }
            if (category == -1) {
                snackbar({
                    message: t("shop.dish_edit.snackbar.no_category")
                })
                isLoading.value = false
                return
            }

            dishData_.category = category

        } else {
            dishData_.category = Number(categoryInput.value.value)
        }

        // 获取被修改的项
        let changed = {}

        // 名称
        // console.log(dishData_.name)
        if (!dishData_.name) {
            nameInput.value.setCustomValidity(t("shop.dish_edit.error_info.name"))
            isLoading.value = false
            return

        } else if (dishData_.name !== originDishData.name) {
            changed.name = dishData_.name
        }

        // 描述
        if (dishData_.description !== originDishData.description) {
            changed.description = dishData_.description
        }   

        // 价格
        if (!dishData_.price) {
            priceInput.value.setCustomValidity(t("shop.dish_edit.error_info.price"))
            isLoading.value = false
            return 
        }
        if (dishData_.price <= 0) {
            // console.log("价格错误", priceInput.value.setCustomValidity)
            priceInput.value.setCustomValidity(t("shop.dish_edit.error_info.price"))
            isLoading.value = false
            return 

        } else if (dishData_.price !== originDishData.price) {
            changed.price = dishData_.price
        }

        // 是否启用
        if (!dishData_.is_available) {
            dishData_.is_available = false
        }

        if (dishData_.is_available !== originDishData.is_available) {
            changed.is_available = dishData_.is_available
        }

        // 分类
        if (dishData_.category !== originDishData.category) {
            changed.category = dishData_.category
        }

        try {
            if (props.isNew) {
                await saveNew(dishData_)
            } else {
                await saveChanged(changed, choicesChanging)
            }
        } finally {
            isLoading.value = false
        }


    
    }

    const getAllCategorires = async () => {
            const res = await request.get(`/shop/category/getAll`)
                if (res.data.status == 0) {
                    categories.value = res.data.data
                    // console.log(categories.value)
                    // console.log(categories.value[dishData.value.category].name)
                }
    }

    const getDish = async(dishId) => {
            // 获取菜品数据
            let res = await request.post(`/shop/dishes/get`, {
                id: Number(dishId),
            })
            if (res.data.status == 0) {
                dishData.value = res.data.data

                originDishData = {...res.data.data}

                dishData.value.price /= 100 // 转换为元
            }


    }


    onMounted( async () => {
        // 设置居右的保存按钮组件
        setRightComponent(h('mdui-button-icon', {
            onClick: handleSave,
            ref: (el) => {saveButton.value = el}
        }, [
            h('mdui-icon-save')
        ]))

        
        // 获取菜品数据和分类信息
        isLoading.value = true


        try {
            await getAllCategorires()

            if (!props.isNew) {
                await getDish(route.params.id)

                categoryInput.value.value = categories.value.find(category => category.id == dishData.value.category).name
            } else {
                dishData.value = {
                    'name': '',
                    'price': 0,
                    'description': '',
                    'image': '',
                    'category': '',
                    'choices': {},
                    'is_available': 0
                }
            }
            
            
            


        } catch(error) {
            console.error(error)
            isError.value = true;

            clearRightComponent()

            await nextTick()

            errorPage.value.setInfo(
                t("shop.dish_edit.load_error.title"),
                t("shop.dish_edit.load_error.message"),
                error.message
            )
        } finally {
            isLoading.value = false
        }
    
    })    

    onBeforeUnmount(() => {
        clearRightComponent()
    })

    // 添加选项
    const addNewChoices = () => {
        prompt({
            headline: t("shop.dish_edit.new_choice.headline"),
            description: t("shop.dish_edit.new_choice.description"),
            confirmText: t("common.text.confirm"),
            cancelText: t("common.text.cancel"),
            onConfirm: (name) => {
                if (name == '') {
                    snackbar({
                        message: t("shop.dish_edit.new_choice.error.none")
                    })
                } else if (dishData.value.choices[name]) {
                    snackbar({
                        message: t("shop.dish_edit.new_choice.error.exist")
                    })
                } else {
                    dishData.value.choices[name] = []

                    choicesChanging.push({
                        type: "new_choice",
                        name: name,
                    })
                }
            }
        })
    }

    // 添加选项的选项
    const addNewOption = (name) => {
        prompt({
            headline: t("shop.dish_edit.new_option.headline", {name: name}),
            description: t("shop.dish_edit.new_option.description"),
            confirmText: t("common.text.confirm"),
            cancelText: t("common.text.cancel"),
            onConfirm: (option) => {
                if (option == '') {
                    snackbar({
                        message: t("shop.dish_edit.new_option.error.none")
                    })
                } else if (dishData.value.choices[name].includes(option)) {
                    snackbar({
                        message: t("shop.dish_edit.new_option.error.exist")
                    })
                } else {
                    dishData.value.choices[name].push(option)
                    
                    choicesChanging.push({
                        type: "new_option",
                        name: name,
                        option: option,
                    })
                }
            }
        })
    }

    // 删除选项的选项
    const deleteOption = (name, option) => {
        let headline = ''
        let description = ''

        // 判断长度是否为一
        if (dishData.value.choices[name].length == 1) {
            // headline和description显示为删除Choices
            headline = t("shop.dish_edit.delete_option.headline", {name: name}),
            description = t("shop.dish_edit.delete_option.only_one", {name: name, option: option})
        } else {
            // headline和description显示为删除项目
            headline = t("shop.dish_edit.delete_option.headline", {name: name, option: option}),
            description = t("shop.dish_edit.delete_option.description", {name: name, option: option})
        }

        dialog({
            headline: headline,
            description: description,
            actions: [
                {
                    text: t("common.text.cancel"),
                },
                {
                    text: t("common.text.confirm"),
                    onClick: () => {
                        const index = dishData.value.choices[name].indexOf(option)
                        dishData.value.choices[name].splice(index, 1)

                        // 删除项目
                        choicesChanging.push({
                            type: "delete_option",
                            name: name,
                            option: option,
                        })

                        if (dishData.value.choices[name].length == 0) {
                            // 选项中没有项目了，删除选项
                            delete dishData.value.choices[name]
                            
                            choicesChanging.push({
                            type: "delete_choice",
                            name: name,
                            option: option,
                            })
                        }
                    },
                },
                
            ]
        })
    }

   </script>