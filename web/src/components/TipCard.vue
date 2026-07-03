    <template>
        <mdui-card 
        class="tip" 
        :variant="props.variant" 
        style="margin-top: 16px;"
        ref="card"
        >
            <div style="display: flex; align-items: center; gap: 8px;">
                <slot> </slot>
            
            </div>
        </mdui-card>
    </template>

    <script setup>
    import { onMounted, ref } from 'vue'
    import 'mdui/components/card.js'

    const props = defineProps({
    variant: String,
    backgroundColor: String,
    color : String
    })

    const card = ref(null)

    onMounted(() => {
        if (props.backgroundColor) {
            card.value.style.backgroundColor = props.backgroundColor
        }
        if (props.color) {
            card.value.style.color = props.color
        }
    })

        
    </script>

        


    <style>
    .tip {
        padding-left: 12px;
        padding-right: 12px;
        padding-top: 16px;
        padding-bottom: 16px;
        width: 100%;
    }
    </style>