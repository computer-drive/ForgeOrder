<template>

    <mdui-dialog ref="numberKeyboArdDialog" class="number-keyboard-dialog" close-on-overlay-click>
            <div class="number-content">
                {{ currentText }}
            </div>
            <div class="input-container">
                <div class="input-number-container">
                    <mdui-button variant="text" class="input-number-button" @click="inputText('1')">1</mdui-button>
                    <mdui-button variant="text" class="input-number-button" @click="inputText('2')">2</mdui-button>
                    <mdui-button variant="text" class="input-number-button" @click="inputText('3')">3</mdui-button>
                    <mdui-button variant="text" class="input-number-button" @click="backspace">
                        <mdui-icon-backspace></mdui-icon-backspace>
                    </mdui-button>

                    <mdui-button variant="text" class="input-number-button" @click="inputText('4')">4</mdui-button>
                    <mdui-button variant="text" class="input-number-button" @click="inputText('5')">5</mdui-button>
                    <mdui-button variant="text" class="input-number-button" @click="inputText('6')">6</mdui-button>
                    <mdui-button variant="text" class="input-number-button" @click="clear">
                        <mdui-icon-clear></mdui-icon-clear>
                    </mdui-button>

                    <mdui-button variant="text" class="input-number-button" @click="inputText('7')">7</mdui-button>
                    <mdui-button variant="text" class="input-number-button" @click="inputText('8')">8</mdui-button>
                    <mdui-button variant="text" class="input-number-button" @click="inputText('9')">9</mdui-button>
                    <mdui-button class="input-confrim-button" variant="filled" @click="submit">
                        <mdui-icon-keyboard-return></mdui-icon-keyboard-return>
                    </mdui-button>

                    <mdui-button variant="text" class="input-number-button" style="visibility: hidden;">9</mdui-button>
                    <mdui-button variant="text" class="input-number-button" @click="inputText('0')">0</mdui-button>
                    <mdui-button variant="text" class="input-number-button" @click="inputText('.')">.</mdui-button>
                </div>
            </div>
    </mdui-dialog>
</template> 

<script setup>
    import '@/assets/component.number_keyboard_dialog.css'

    import 'mdui/components/button.js'
    
    import '@mdui/icons/backspace.js'
    import '@mdui/icons/clear.js'
    import '@mdui/icons/keyboard-return.js'

    import { ref } from 'vue'

    // 定义事件
    const emit = defineEmits(['confirm'])


    // 定义参数
    const props = defineProps({
        money_input: { // 是否为金额输入（小数点只允许后两位）
            type: Boolean,
            default: false
        }
    })


    // console.log(props.money_input)

    const currentText = ref('0')

    const numberKeyboArdDialog = ref(null)

    const inputText = (text) => {
        if (currentText.value === '0') {
            currentText.value = text
        } else {
            if (text == '.') {
                // 判断是否已经存在小数点
                if (currentText.value.indexOf('.') !== -1) {
                    return 
                }
                
            }

            // 判断是否是金额输入
                if (props.money_input) {
                    // 判断小数点后的数字是否超过两位
                    if (currentText.value.length - currentText.value.indexOf('.') > 2) {
                        return
                    }
                }

            // 合并当前输入的数字
            currentText.value += text
        }
    }

    const clear = () => {
        currentText.value = '0'
    }

    const backspace = () => {
        if (currentText.value.length > 1) {
            currentText.value = currentText.value.slice(0, -1)
        } else {
            currentText.value = '0'
        }
    }

    const submit = () => {
        numberKeyboArdDialog.value.open = false
        emit('confirm', Number(currentText.value))
    }

    const open = (default_number = 0) => {
        numberKeyboArdDialog.value.open = true
        currentText.value = String(default_number)
    }

    defineExpose({
  open
})
</script>