<template>
    <div class="container mdui-prose">
        <h1>编辑“{{ dishData.name }}”</h1>
        <div style="margin-bottom: 24px; font-size: 18px">在下方更改菜品信息，点击右上角的“保存”按钮以应用更改。    </div>

        <div class="setting-title">基本信息</div>
        <mdui-text-field label="菜品名称" class="setting-item" variant="outlined"></mdui-text-field>

        <mdui-text-field label="菜品描述" class="setting-item" autosize min-rows="1" max-rows="3" variant="outlined"></mdui-text-field>

        <mdui-text-field label="价格" class="setting-item" variant="outlined" readonly>
            <mdui-button-icon slot="end-icon" @click="priceInputDialog.open = true">
                <mdui-icon-edit></mdui-icon-edit>
            </mdui-button-icon>
        </mdui-text-field>
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
    import { ref } from 'vue'

    import 'mdui/components/text-field.js';
    import 'mdui/components/dialog.js';

    import '@mdui/icons/edit.js';
    import '@mdui/icons/backspace.js';
    import '@mdui/icons/clear.js';
    import '@mdui/icons/keyboard-return.js';

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

    const dishData = ref({})
    const price = ref(0)

    const priceInputDialog = ref(null)
    const currentText = ref('0')

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
        currentText.value = '0'
    }

   </script>

<style>
.setting-item {
    margin-bottom: 24px;
}

.setting-title {
    font-size: 30px;
     margin-top: 16px;
      margin-bottom: 16px
}



.panel .has-default {
    position: fixed;
    left: 0;
    bottom: 0;
}



.price-content {
    border-radius: var(--mdui-shape-corner-extra-large);
    background-color: rgb(var(--mdui-color-primary-container));
    font-size: 28px;
    color : rgb(var(--mdui-color-on-primary-container));
    padding-top: 16px;
    padding-bottom: 16px;
    padding-left: 24px;
    padding-right: 24px;
    text-align: right;
    margin-bottom: 16px;
}

.price-input-container {
    /* display: flex; */
    justify-content: center;
    align-items: center;
}

.price-input {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    /* grid-auto-rows: 70px; */
    /* gap: 8px */
    place-items: center;
    grid-template-rows: 80px 80px;

}

.price-num-button {
    font-size: 22px;
    height: 100%;
    width: 100%;
}

.price-big-button {
    font-size: 22px;
    grid-row: 3 / 5;
    grid-column: 4;
    height: 160px;
    text-align: center;
    writing-mode: vertical-lr;
    line-height: 20px; 
    letter-spacing: 5px;
    /* width: 60px; */
    /* border-radius: var(--mdui-shape-corner-extra-large); */
}

 mdui-dialog.price-input-dialog::part(panel) {
  position: fixed;
  left: 0;
  bottom: 0;
  min-width: 100vw;
  border-radius: var(--mdui-shape-corner-extra-large) var(--mdui-shape-corner-extra-large) 0 0;
}

</style>