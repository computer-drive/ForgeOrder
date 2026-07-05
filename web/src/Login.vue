<template>
  <div>
    
    <TopBar title="登录" showHome="false" />
    <TopProgressBar ref="topProgressbar"/>

    <div class="container">
        <div class="mdui-prose">
            <div style="text-align: center">
              <!-- <mdui-icon-lock style="font-size: 32px; padding-left: 12px; text-align: center"></mdui-icon-lock> -->
            </div>
            
            <!-- <div style="font-size: 24px; margin-bottom: 16px; margin-top: 16px; margin-left: 12">登录至ForgeOrder</div>
            <div style="margin-bottom: 16px;">输入用户名、密码以登录至ForgeOrder。</div> -->

            <h1>登录</h1>
            <div style="margin-bottom: 24px; font-size: 18px">输入用户名、密码以登录至ForgeOrder。</div>
            
            <form @submit.prevent="handleSubmit(false)">
              <mdui-text-field 
              autofocus="true"
              label="用户名" 
              variant="outlined" 
              style="margin-bottom: 24px;" 
              v-model="username"
              ref="usernameInput">
                <mdui-icon-account-circle slot="icon"></mdui-icon-account-circle>
              </mdui-text-field>

              <mdui-text-field 
              label="密码" 
              variant="outlined" 
              style="margin-bottom: 24px;" 
              type="password" 
              v-model="password"
              toggle-password
              ref="passwordInput">
                <mdui-icon-password slot="icon"></mdui-icon-password>
              </mdui-text-field>


              <div style="text-align: right; padding-right: 8px" >
                <mdui-button type="submit" ref="loginButton">登录</mdui-button>
              </div>
              
            </form>
        </div>
        

    </div>
  </div>
</template>

<script setup>

import TopBar from './components/TopBar.vue'
import TopProgressBar from './components/TopProgressBar.vue';
import { useAuth } from './composables/auth.js'

import 'mdui/components/text-field.js';
import { alert } from 'mdui/functions/alert.js';
import { snackbar } from 'mdui/functions/snackbar.js'
import { dialog } from 'mdui/functions/dialog.js';

import { ref, onMounted } from 'vue' 
import { useRouter } from 'vue-router'

import '@mdui/icons/account-circle.js';
import '@mdui/icons/password.js';

const topProgressbar = ref(null)

const username = ref('')
const password = ref('')

const usernameInput = ref(null)
const passwordInput = ref(null)
const loginButton = ref(null)

const router = useRouter()
const { login } = useAuth()

let errorMsg = history.state.msg



onMounted(() => {
    topProgressbar.value.hide()

    // window.history.replaceState()

    if (errorMsg) {
      history.replaceState({}, document.title)
      alert({
        headline: '登录状态失效',
        description: errorMsg,
        confirmText: '确定',
      })
    }
})

const handleSubmit = async (coverLogin = false) => {
    topProgressbar.value.show()
    usernameInput.value.disabled = true
    passwordInput.value.disabled = true
    usernameInput.value.setCustomValidity('')
    passwordInput.value.setCustomValidity('')
    loginButton.value.disabled = true


     let isError = false
    // 验证表单数据是否有效
    if (username.value === '') {
        isError = true
        usernameInput.value.setCustomValidity('用户名不能为空')

    }

    if (password.value === '') {
        isError = true
        passwordInput.value.setCustomValidity('密码不能为空')
    }

    if (isError) {
        topProgressbar.value.hide()
        usernameInput.value.disabled = false
        passwordInput.value.disabled = false
        loginButton.value.disabled = false
        return
    }




    let result = null

    try {
      result = await login(username.value, password.value, coverLogin)

      if (result.status == 0) {
        // 登录成功
        
      } else if (result.status == 3001) {
        // 用户名或密码错误
        passwordInput.value.setCustomValidity('用户名或密码错误')
      } else if (result.status == 3002) {
        // 服务器错误
        passwordInput.value.setCustomValidity('该用户未启用')
      } else if (result.status == 3003) {
        // 重复登录
        snackbar({
          message: '重复登录',
        })
        router.push("/")

      } else if (result.status == 3004) {
  
        dialog({
          headline: '新设备登录',
          description: `已有一个设备（${result.data.old_device_ip}）登录，是否覆盖它的登录？`,
          actions: [
            {
              text: '否',
            },
            {
              text: '是',
              onClick: () => {
                handleSubmit(true)
              }
            },
            
          ]
        })
      } else {
        // 其他错误
        console.error(result)
        alert({
          headline: '登录失败',
          description: `未知错误（${result.status}）：${result.data}`,
          confirmText: '确定'
        })
      }
    } 
    
    catch(error) {
      alert({
        headline: '登录失败',
        description: `网络错误：${error.message}`,
        confirmText: '确定'
      })
    } 
    finally {
      if (result !== null && result.status !== 3004) {
            topProgressbar.value.hide()
            usernameInput.value.disabled = false
            passwordInput.value.disabled = false
            loginButton.value.disabled = false
          }
    }
}
</script>

