<template>
    <div class="container mdui-prose">
        <div v-if="isLoading" class="loading-container">
            <mdui-circular-progress></mdui-circular-progress>
        </div>
        <div v-else>
            <h2>{{ $t('shop.all_dishes.title') }}</h2>

            <mdui-li>
                <div v-for="(value, key) in categories" :key="key">
                    <mdui-list-subheader style="display:flex; align-items: center; justify-content: space-between;">
                        {{ categories[key] }}
                        <div style="display:flex; align-items: center; gap: 8px">
                            <mdui-button-icon @click="editCategory(key, value)">
                                <mdui-icon-edit></mdui-icon-edit>
                            </mdui-button-icon>
                            <mdui-button-icon @click="deleteCategory(key, value)">
                                <mdui-icon-clear></mdui-icon-clear>
                            </mdui-button-icon>

                        </div>
                    </mdui-list-subheader>
                    <div v-for="dish in dishes[value]" :key="dish.id">
                        <mdui-list-item rounded @click="showDetail(value, dish.id)">{{ dish.name }}</mdui-list-item>
                    </div>
                </div>
            </mdui-li>

            <mdui-button full-width variant="tonal" @click="addCategory" style='margin-top: 20px'>
                添加分类
                <mdui-icon-category slot="icon"></mdui-icon-category>
            </mdui-button>

        </div>

        
    </div>

    <mdui-dialog ref="dishDetail" close-on-overlay-click>
        <span slot="headline">{{ currentDish.name }}</span>
        <div slot="description" class="mdui-prose">
            <h2 style="font-size: 20px; margin-bottom: 10px; color: black">{{ $t('shop.all_dishes.detail.basic_title') }}</h2>

            <div class="detail-item">
                <div class="detail-label">{{ $t('shop.all_dishes.detail.dish_id') }}</div>
                {{ currentDish.id }}</div>  

            <div class="detail-item">
                <div class="detail-label">{{ $t('shop.all_dishes.detail.name') }}</div>
                {{ currentDish.name }}</div>

            <div class="detail-item">
                <div class="detail-label">{{ $t('shop.all_dishes.detail.description') }}</div>
                {{ currentDish.description }}</div>

            <div class="detail-item">
                <div class="detail-label">{{ $t('shop.all_dishes.detail.price') }}</div>
                {{ $t('shop.all_dishes.detail.price_value' , { price: currentDish.price }) }}</div>

            <div class="detail-item">
                <div class="detail-label">{{ $t('shop.all_dishes.detail.created_at') }}</div>
                {{ new Date(currentDish.created_at).toLocaleString() }}</div>
            
            <div class="detail-item">
                <div class="detail-label">{{ $t('shop.all_dishes.detail.available') }}</div>
                {{ currentDish.available ? $t('shop.all_dishes.detail.available_value') : $t('shop.all_dishes.detail.unavailable_value') }}</div>     
                    
            <h2 style="font-size: 20px; margin-bottom: 10px; color: black; margin-top: 10px">统计信息</h2>
            
            <div class="detail-item">
                <div class="detail-label">{{ $t('shop.all_dishes.detail.monthly_sales') }}</div>
                {{ currentDish.stat?.monthly_sales || $t('shop.all_dishes.detail.no_data') }}</div>  

            <div class="detail-item">
                <div class="detail-label">{{ $t('shop.all_dishes.detail.total_sales') }}</div>
                {{ currentDish.stat?.total_sales || $t('shop.all_dishes.detail.no_data') }}</div>  

            <div class="detail-item">
                <div class="detail-label">{{ $t('shop.all_dishes.detail.updated_at') }}</div>
                {{ new Date(currentDish.stat?.updated_at).toLocaleString() }}</div>

            <h2 style="font-size: 20px; margin-bottom: 10px; color: black; margin-top: 10px" v-if="currentDish.choices">{{ $t('shop.all_dishes.detail.choices') }}</h2>
            
            <div v-for="(value, key) in currentDish.choices" :key="key">
                <div class="detail-item" style="margin-bottom: 8px;">
                    <div class="detail-label">{{ key }}</div>
                    <mdui-segmented-button-group >
                        <mdui-segmented-button v-for="option in value" :key="option">{{ option }}</mdui-segmented-button>
                    
                    </mdui-segmented-button-group>
                </div>
            </div>

            

                

        </div>

        <mdui-button slot="action" variant="tonal" @click="deleteDish">
            {{ $t('shop.all_dishes.detail.delete_action') }}
            <mdui-icon-delete slot="icon" ></mdui-icon-delete>
        </mdui-button>


        <mdui-button slot="action" variant="tonal" @click="goEdit">
            {{ $t('shop.all_dishes.detail.edit_action') }}
            <mdui-icon-edit slot="icon" ></mdui-icon-edit>
        </mdui-button>
        <mdui-button slot="action" variant="text" @click="dishDetail.open = false">{{ $t('common.text.confirm') }}</mdui-button>

    </mdui-dialog>

    <mdui-fab size="normal" style="position: fixed; bottom: 40px; right: 30px;" @click="router.push('/shop/dishes/new')">
            <mdui-icon-add slot="icon"></mdui-icon-add>
            <!-- 添加菜品 -->
    </mdui-fab>

</template> 

<script setup>
import TopProgressBar from '@/components/TopProgressBar.vue'

import 'mdui/components/list.js'
import 'mdui/components/list-item.js'
import 'mdui/components/list-subheader.js'
import 'mdui/components/dialog.js'
import 'mdui/components/segmented-button-group.js'
import 'mdui/components/segmented-button.js'
import { dialog } from 'mdui/functions/dialog.js'
import { prompt } from 'mdui/functions/prompt.js'
import { snackbar } from 'mdui'

import { inject, h, onMounted, ref, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

import '@mdui/icons/add.js'
import '@mdui/icons/edit.js'
import '@mdui/icons/delete.js'
import '@mdui/icons/category.js';


import request from '@/utils/request.js'
import { t } from '@/locales/index.js'
import { pushWithFrom } from '@/utils/routerHelper'


const router = useRouter()

const { addRightComponent, clearRightComponent } = inject('rightComponent')

const dishes = ref([])
const categories = ref([])

const isLoading=  ref(true)

const currentDish = ref({})
const dishDetail = ref(null)


const addDish = () => {
    // router.push({name:'addDish1'})
    pushWithFrom("/shop/dishes/new")
}

onMounted( async() => {
    // <mdui-text-field variant="outlined" :placeholder="$t('orders.topbar.search.text')" style="width: auto; height: 100%">
    //         </mdui-text-field>
    //         <mdui-button-icon >
    //             <mdui-icon-search></mdui-icon-search>
    //         </mdui-button-icon>

    
    
    addRightComponent(h('mdui-text-field', {
            variant: 'outlined',
            placeholder: t('shop.all_dishes.search'),
            style: 'width: calc(100vw - 40px - 40px - 160px); height: 100%; align-items: center'
        }))

    // addRightComponent(h('mdui-button-icon', {}, [
    //         h('mdui-icon-search')
    //     ]))

    getDishes()
    

    
})

const getDishes = async () => {
    isLoading.value = true

    const res = await request.get("/shop/dishes/getAll")
        // console.log(res)
        if (res.status == 200) {
            // console.log(res.data.data)
            dishes.value = res.data.data.dishes
            categories.value = res.data.data.categories
            // console.log(dishes.value, categories.value)
        }
    
    isLoading.value = false 
}

const showDetail = (category_name, dish_id) => {
    currentDish.value = { 
        ...dishes.value[category_name].find(dish => dish.id == dish_id) 
    }
    
    
    dishDetail.value.open = true;

    // console.log(currentDish.value.stat)
}

const goEdit = () => {
    dishDetail.value.open = false;
    dishDetail.value.addEventListener('closed', () => {
        pushWithFrom(`/shop/dishes/${currentDish.value.id}`)
    })
    
}

const deleteDish = () => {
    dishDetail.value.open = false;
    dishDetail.value.addEventListener('closed', () => {
        dialog({
            headline: t('shop.all_dishes.delete_dialog.title'),
            description: t('shop.all_dishes.delete_dialog.description', { name: currentDish.value.name }),
            actions: [
                {
                    'text': t('common.text.cancel')
                },
                {
                    'text': t('common.text.confirm'),
                    onClick: async() => {
                        try{
                            const res = await request.post('/shop/dishes/delete', {
                                dish_id: currentDish.value.id
                            })

                            if (res.data.status == 0) {
                                snackbar({
                                    "message": t("shop.all_dishes.snackbar_delete_dish.success")
                                })
                                
                                getDishes()
                                
                                

                                // router.push(`/shop/dishes`)
                                
                            } else if (res.data.status == 3001) {
                                snackbar({
                                    "message": t("shop.all_dishes.snackbar_delete_dish.not_found")
                                })
                
                            } else if (res.data.status == 2002) {
                                snackbar({
                                    "message": t("shop.all_dishes.snackbar_delete_dish.permission")
                                })
                            } 
                            else {
                                console.log(res.data)
                                snackbar({
                                    "message": t("shop.all_dishes.snackbar_delete_dish.unknown")
                                })
                            }
                        } catch (error) {
                            console.log(error)
                            snackbar({
                                "message": t("shop.all_dishes.snackbar_delete_dish.unknown")
                            })
                        }
                    }
                },  
            ]
        })
    }, {once: true})
}

const deleteCategory = (category_id, category_name) => {
    let description = ''

    console.log(dishes.value[category_name].find(dish => dish.category  == category_id) != undefined)
    if (dishes.value[category_name].find(dish => dish.category  == category_id) != undefined) {
        // 分类下有菜品
        description = t('shop.all_dishes.delete_category_dialog.description_dish', { name: categories.value[category_id] })
    } else {
        console.log("1")
        // 分类下没有菜品
        description = t('shop.all_dishes.delete_category_dialog.description', { name: categories.value[category_id] })
    }

    dialog({
            headline: t('shop.all_dishes.delete_category_dialog.title'),
            description: description,
            actions: [
                {
                    'text': t('common.text.cancel'),
                },
                {
                    'text': t('common.text.confirm'),
                    onClick: async() => {
                        try{
                            const res = await request.post('/shop/category/delete', {
                                category_id: Number(category_id)
                            })

                            if (res.data.status == 0) {
                                snackbar({
                                    message: t("shop.all_dishes.snackbar_delete_category.success")
                                })
                                getDishes()
                            } else if (res.data.status == 3001) {
                                snackbar({
                                    message: t("shop.all_dishes.snackbar_delete_category.not_found")
                                })
                            } else if (res.data.status == 2002) {
                                snackbar({
                                    message: t("shop.all_dishes.snackbar_delete_category.permission")
                                })
                            } else {
                                snackbar({
                                    message: t("shop.all_dishes.snackbar_delete_category.unknown")
                                })
                            }
                        } catch (error) {
                            console.log(error)
                            snackbar({
                                message: t("shop.all_dishes.snackbar_delete_category.unknown")
                            })
                        }
                    } 
                }
            ]})
}

const editCategory = (category_id, category_name) => {
    prompt({
        headline: t('shop.all_dishes.edit_category_dialog.headline', { name: category_name }),
        description: t('shop.all_dishes.edit_category_dialog.description'),
        confirmText: t('common.text.confirm'),
        cancelText: t('common.text.cancel'),
        onConfirm: async (value) => {
            if (value == '') {
                snackbar({
                    message: t("shop.all_dishes.snackbar_edit_category.empty")
                })
                return
            }

            if (value.includes("_disabled")) {
                snackbar({
                    message: t("shop.all_dishes.snackbar_edit_category.invalid")
                })
                return
            }

            try{
                const res = await request.post('/shop/category/edit', {
                    category_id: Number(category_id),
                    category_name: value
                })

                if (res.data.status == 0) {
                    snackbar({
                        message: t("shop.all_dishes.snackbar_edit_category.success")
                    })
                    getDishes()
                } else if (res.data.status == 3001) {
                    snackbar({
                        message: t("shop.all_dishes.snackbar_edit_category.not_found")
                    })
                } else if (res.data.status == 2002) {
                    snackbar({
                        message: t("shop.all_dishes.snackbar_edit_category.permission")
                    })
                } else {
                    snackbar({
                        message: t("shop.all_dishes.snackbar_edit_category.unknown")
                    })
                }
            } catch (error) {
                console.log(error)
                snackbar({
                    message: t("shop.all_dishes.snackbar_edit_category.unknown")
                })
            }

        }
    })
}

const addCategory = () => {
    prompt({
        headline: t("shop.all_dishes.new_category_dialog.headline"),
        description: t("shop.all_dishes.new_category_dialog.description"),
        confirmText: t('common.text.confirm'),
        cancelText: t('common.text.cancel'),
        onConfirm: async (value) => {
            isLoading.value = true
            let res = null
            try {
                if (!value) {
                    snackbar({
                        message: t("shop.all_dishes.snackbar_new_category.empty")
                    })
                    isLoading.value = false
                    return
                }

                if (value.includes('_disabled')) {
                    snackbar({
                        message: t("shop.all_dishes.snackbar_new_category.invaild")
                    })
                    isLoading.value = false
                    return
                }

                res = await request.post('/shop/category/new', {
                    name: value
                })

                // console.log(res.data)

                if (res.data.status == 0) {
                    snackbar({
                        message: t("shop.all_dishes.snackbar_new_category.success")
                    })
                    getDishes()
                }          
            }
            catch (error) {
                console.log(error)

                if (error.response.data.status == 2002) {
                    snackbar({
                        message: t("shop.all_dishes.snackbar_new_category.permission")
                    })
                } else if (error.response.data.status == 3001) {
                    snackbar({
                        message: t("shop.all_dishes.snackbar_new_category.exist")
                    })
                } else {
                        snackbar({
                        message: t("shop.all_dishes.snackbar_new_category.unknown")
                    })
                }
                
            } finally {
                isLoading.value = false
            }
        }
})}

onBeforeUnmount(() => {
    clearRightComponent()
})





</script>

<style>
    .loading-container {
        height: calc(100vh - 65px);
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .detail-item {
        display: flex;
        gap: 12px;
        align-items: center;
    }
    .detail-label {
        width: 4.1em;
        text-align: justify;
        text-justify: inter-ideograph;
        text-align-last: justify;
        flex-shrink: 0;
    }
</style>