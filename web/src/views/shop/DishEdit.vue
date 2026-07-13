<template>
    <TopProgressBar v-model="isLoading"/>

    <NumberKeyboardDialog
     ref="priceInputDialog" 
    :money_input="true"
    @confirm="dishData.price = $event"
     ></NumberKeyboardDialog>

    <div class="container mdui-prose" v-if="!isError">
        <h2>编辑“{{ dishData.name }}”</h2>  
        <div style="margin-bottom: 24px; font-size: 18px">在下方更改菜品信息，点击右上角的“保存”按钮以应用更改。    </div>

        <div>

            <div class="setting-item" ref="nameInput">
                <div class="setting-item-key">菜品名称</div>
                <div class="setting-item-value">
                    
                    <mdui-text-field 
                    v-model="dishData.name"
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
                    v-model="dishData.description"
                    variant="outlined"></mdui-text-field>
            </div>

            <div class="setting-item">
                菜品价格
                <mdui-text-field 
                    class="setting-item-value"
                    variant="outlined" 
                    readonly 
                    @click="priceInputDialog.open(dishData.price)"

                    v-model="dishData.price"
                    > 
                    <div slot="icon">￥</div>
                </mdui-text-field>
            </div>

            <div class="setting-item">
                启用此菜品
                <mdui-switch :checked="dishData.is_available" ref="isAvailableSwitch"></mdui-switch>
            </div>

            <div class="setting-item">
                分类
                <mdui-select 
                    ref="categoryInput"
                    variant="outlined" 
                    class="setting-item-value"
                    
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
                选项
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
    
    import request from '@/utils/request.js'

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

    const route = useRoute()
    const router = useRouter()

    const { setRightComponent, clearRightComponent } = inject('rightComponent')

    const isLoading = ref(false)
    const isError= ref(false)

    const priceInputDialog = ref(null)
    const errorPage = ref(null)

    const categoryInput = ref(null)
    const nameInput = ref(null)
    const isAvailableSwitch = ref(null)
    const saveButton = ref(null)

    const dishData = ref({})
    let originDishData = {}
    const categories = ref([])
    let choicesChanging = []
    


    // 右上角的按钮
    const handleSave = async (event) => {
        // 通过事件对象获取按钮元素
        const button = event?.currentTarget
    
        if (button) {
            button.loading = true
        }
        
        // 保存菜品数据
        let dishData_ = {...dishData.value,}

        dishData_.price *= 100 // 转换为分
        dishData_.is_available = isAvailableSwitch.value.checked

        if (typeof categoryInput.value.value == 'string') {
            let category = -1 
            for ( let i = 0; i < categories.value.length; i++) {
                if (categories.value[i].name == categoryInput.value.value) {
                    category = i
                    break
                }
            }
            if (category == -1) {
                snackbar({
                    message: '分类不存在'
                })
                return
            }
            dishData_.category = category
        } else {
            dishData_.category = Number(categoryInput.value.value)
        }

        // 获取被修改的项
        let changed = {}

        // 名称
        if (dishData_.name == '') {
            nameInput.setCustomValidity("名称不能为空")
        } else if (dishData_.name !== originDishData.name) {
            changed.name = dishData_.name
        }

        // 描述
        if (dishData_.description !== originDishData.description) {
            changed.description = dishData_.description
        }

        // 价格
        if (dishData_.price <= 0) {
            priceInputDialog.value.setCustomValidity("价格必须大于0")
        } else if (dishData_.price !== originDishData.price) {
            changed.price = dishData_.price
        }

        // 是否启用
        if (dishData_.is_available !== originDishData.is_available) {
            changed.is_available = dishData_.is_available
        }

        // 分类
        if (dishData_.category !== originDishData.category) {
            changed.category = dishData_.category
        }

        console.log(changed, choicesChanging)

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
                    message: '修改成功'
                })
                router.push("/shop/dishes")
            } else {
                alert({
                    headline: '修改失败',
                    description: '' + res.data.data,
                    confirmText: '确定'
                })
            }
             
        } catch (error) {
            if (error.response.status === 401 && error.response.data?.status == 2002) {
                alert({
                headline: '修改失败',
                description: '权限不足，仅管理员用户可修改菜品数据',
                confirmText: '确定'
            })

            } else if (error.response.status == 400 && error.response.data?.status == 3001) {
                snackbar({
                    message: '未更改任何内容。'
                })
            } else {
                alert({
                headline: '修改失败',
                description: '网络错误：' + error,
                confirmText: '确定'
            })
            }
            
        } finally {
            button.loading = false
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

        const dishId = route.params.id

        try {
            // 获取菜品数据
            let res = await request.post(`/shop/dishes/get`, {
                id: Number(dishId),
            })
            if (res.data.status == 0) {
                dishData.value = res.data.data

                originDishData = {...res.data.data}

                dishData.value.price /= 100 // 转换为元
            }

            // 获取分类信息
            res = await request.get(`/shop/dishes/getAllCategories`)
            if (res.data.status == 0) {
                categories.value = res.data.data
                // console.log(categories.value)
                // console.log(categories.value[dishData.value.category].name)
                categoryInput.value.value = categories.value[dishData.value.category].name
            }


        } catch (error) {
            isError.value = true;

            clearRightComponent()

            await nextTick()

            // console.log(error.message)
            errorPage.value.setInfo(
                "加载失败",
                "无法获取菜品信息",
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
            headline: '添加选项',
            description: '请输入新选项的名称',
            confirmText: '确定',
            cancelText: '取消',
            onConfirm: (name) => {
                if (name == '') {
                    snackbar({
                        message: '选项名称不能为空'
                    })
                } else if (dishData.value.choices[name]) {
                    snackbar({
                        message: '选项已存在'
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
            headline: `添加“${name}”的项目`,
            description: '请输入新项目的名称',
            confirmText: '确定',
            cancelText: '取消',
            onConfirm: (option) => {
                if (option == '') {
                    snackbar({
                        message: '项目名称不能为空'
                    })
                } else if (dishData.value.choices[name].includes(option)) {
                    snackbar({
                        message: '项目已存在'
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
            headline = `删除“${name}”`
            description = `选项${name}将剩余一个项目，删除${option}将删除该选项，确定继续吗？`
        } else {
            // headline和description显示为删除项目
            headline = `删除“${name}”的项目`
            description = `确定删除项目“${option}”吗？`
        }

        dialog({
            headline: headline,
            description: description,
            actions: [
                {
                    text: "取消",
                },
                {
                    text: "确定",
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