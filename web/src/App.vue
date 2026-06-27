<style>
    h1 {
        font-size: 36px;
    }

    .container {
        margin-top: 20vh;
    }

    label, input, button {
        font-size: 22px;
    }

    input {
        padding: 5px 5px;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    button {
        padding: 10px 20px;
        margin-top: 10px;
    }

    .submit_container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

</style>
<template>
    <div class="container">
        <h1 style="text-align: center">登录</h1>
        <hr/>

        <form  @submit.prevent="handleLogin" style="text-align: center">
            <label style="display: inline-block; width: 100px; text-align: right;">用户名：</label>
            <input type="text" placeholder="用户名" v-model="username">

            <br>
            <label style="display: inline-block; width: 100px; text-align: right;">密码：</label>
            <input type="password" placeholder="密码" v-model="password">

            <br>
            

            <div class="submit_container">
                <label class="error_message" v-if="error_message !== ''">{{ error_message }}</label>
                <label class="error_message" v-else> </label>

                <button type="submit">{{ login_button_text }}</button>
            </div>
            

        </form>
    </div>
    

</template> 
    
<script setup>    
    import { ref } from 'vue'

    const username = ref('')
    const password = ref('')
    const error_message = ref('')
    const login_button_text = ref('登录')

    const handleLogin = () => {
        error_message.value = ''
        login_button_text.value = '加载...'

        if (username.value && password.value) {
            
        } else {
            error_message.value = '请输入用户名和密码'

        }

        login_button_text.value = '登录'
    }
</script>   