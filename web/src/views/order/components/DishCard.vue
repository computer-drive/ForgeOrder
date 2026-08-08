<template>
    <mdui-card class="dish-card" variant="outlined">
        <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 18px; margin-bottom: 16px;">{{ props.dish.name }}</div>

                    <div style="margin-left: auto; display: flex; align-items: flex-end; gap: 4px; color: rgba(var(--mdui-color-primary))">
                        <span style="font-size: 16px; line-height: 1;">¥</span>
                        <span style="font-size: 24px; line-height: 1;">{{ props.dish.price / 100}}</span>
                    </div>

                </div>

                <mdui-button-icon style="margin-left: auto;" @click="addDishes">
                    <mdui-icon-add-shopping-cart></mdui-icon-add-shopping-cart>
                </mdui-button-icon>

        </div>

        


        <div style="display: flex; align-items: center;">
        
            

        </div>
    </mdui-card>

    <mdui-dialog
        ref="addDishDialog"
        :headline="props.dish.name"

        close-on-esc 
        class="add-dish-dialog"
    >
        <div style="box-sizing: border-box; ">
            <div>
                {{props.dish.description}}
            </div>
            <mdui-list>
                <mdui-list-item nonclickable>
                    <div style="display: flex; align-items: center;">
                        数量
                        <mdui-text-field v-model="dishCount" variant="outlined" type="number" style="margin-left: auto; max-width: 50%">
                            <mdui-button-icon slot="icon" @click="dishCount - 1  > 1 ? dishCount-- : dishCount = 1"><mdui-icon-remove></mdui-icon-remove></mdui-button-icon>
                            <mdui-button-icon slot="end-icon" @click="dishCount++"><mdui-icon-add></mdui-icon-add></mdui-button-icon>
                        </mdui-text-field>
                    </div>
                </mdui-list-item>

                
                <mdui-list-item v-for="(options, name) in dish.choices" :key="name" nonclickable>
                    <div style="margin-bottom: 16px">{{name}}</div>
                    <mdui-segmented-button-group selects="single" full-width :value="currentChoices[name] || options[0]" @change="currentChoices[name] = $event.target.value">

                        <mdui-segmented-button v-for="(option, id) in options" :key="id" :value="option" >{{option}}</mdui-segmented-button>
                    </mdui-segmented-button-group>
                </mdui-list-item>
            </mdui-list>
            
            <div style="display: flex; justify-content: center; width:100%; gap:8px; box-sizing: border-box;">
                <mdui-button variant="text" style="height: 50px" @click="addDishDialog.open = false">取消</mdui-button>  
                <mdui-button style="width: 70%; height: 50px" @click="addDishToShoppingCart">
                    <mdui-icon-add-shopping-cart slot="icon"></mdui-icon-add-shopping-cart>
                    添加到购物车
                </mdui-button>
                
            </div>
            
        </div>
    </mdui-dialog>
</template>

<script setup>
    import 'mdui/components/card.js'
    import 'mdui/components/button-icon.js'
    import 'mdui/components/dialog.js'
    import 'mdui/components/list.js'
    import 'mdui/components/list-item.js'
    import 'mdui/components/list-subheader.js'
    import 'mdui/components/text-field.js'
    import 'mdui/components/segmented-button-group.js'
    import 'mdui/components/segmented-button.js'

    import '@mdui/icons/add-shopping-cart.js'

    import { onMounted, ref } from 'vue'

    const props = defineProps({
        'dish': {
            type: Object,
            default : () => ({})
        }
    })

    const emit = defineEmits(['update'])

    const addDishDialog = ref(null)

    const dishCount = ref(1)

    const currentChoices = ref({})

    const addDishes = () => {
        addDishDialog.value.open = true
    }

    const addDishToShoppingCart = () => {
        setDefaultChoice()

        // console.log(currentChoices.value)
        emit('update', {
            id: props.dish.id,
            dishInfo: props.dish,
            count: dishCount.value,
            choices: currentChoices.value
        })

        currentChoices.value = {}
        dishCount.value = 1


        addDishDialog.value.open = false
    }

    const setDefaultChoice = () => {

        if (Object.keys(currentChoices.value).length > 0) {
            return
        }

        if (props.dish.choices) {
            const defaults = {}
            for (const [name, options] of Object.entries(props.dish.choices)) {
                defaults[name] = options[0] || ''
            }
            currentChoices.value = defaults
        }
    }

    onMounted(() => {
        setDefaultChoice()
    })

</script>

<style>

    .dish-card {
        width: 100%;
        padding: 12px
    }

    mdui-dialog.add-dish-dialog::part(panel) {
        min-width: 90vw;
        max-width: 100vw;

    }
</style>