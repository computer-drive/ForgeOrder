<template>
  <div>
    
    <TopBar :title="$t('login.topbar.text')" :showHome="false" />
    <TopProgressBar v-model="isLoading"/>

    <div class="container">
        <div class="mdui-prose">
            <div style="text-align: center">
              <!-- <mdui-icon-lock style="font-size: 32px; padding-left: 12px; text-align: center"></mdui-icon-lock> -->
            </div>
            
            <!-- <div style="font-size: 24px; margin-bottom: 16px; margin-top: 16px; margin-left: 12">登录至ForgeOrder</div>
            <div style="margin-bottom: 16px;">输入用户名、密码以登录至ForgeOrder。</div> -->

            <h1>{{ $t('login.main.title') }}</h1>
            <div style="margin-bottom: 24px; font-size: 18px">{{ $t('login.main.description') }}</div>
            
            <form @submit.prevent="handleSubmit(false)">
              <mdui-text-field 
              autofocus="true"
              :label="$t('login.input.username.label')"
              variant="outlined" 
              style="margin-bottom: 24px;" 
              v-model="username"
              ref="usernameInput">
                <mdui-icon-account-circle slot="icon"></mdui-icon-account-circle>
              </mdui-text-field>

              <mdui-text-field 
              :label="$t('login.input.password.label')" 
              variant="outlined" 
              style="margin-bottom: 24px;" 
              type="password" 
              v-model="password"
              toggle-password
              ref="passwordInput">
                <mdui-icon-password slot="icon"></mdui-icon-password>
              </mdui-text-field>


              <div style="text-align: right; padding-right: 8px" >
                <mdui-button type="submit" ref="loginButton">{{ $t('login.button.submit.text') }}</mdui-button>
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
import { t } from '@/locales/index.js'

import 'mdui/components/text-field.js';
import { alert } from 'mdui/functions/alert.js';
import { snackbar } from 'mdui/functions/snackbar.js'
import { dialog } from 'mdui/functions/dialog.js';

import { ref, onMounted } from 'vue' 
import { useRouter } from 'vue-router'

import '@mdui/icons/account-circle.js';
import '@mdui/icons/password.js';

const isLoading = ref(false)

const username = ref('')
const password = ref('')

const usernameInput = ref(null)
const passwordInput = ref(null)
const loginButton = ref(null)

const router = useRouter()
const { login } = useAuth()

let errorMsg = history.state.msg



onMounted(() => {
    isLoading.value = false

    // window.history.replaceState()

    if (errorMsg) {
      history.replaceState({}, document.title)
      alert({
        headline: t('login.alert.session_expired.title'),
        description: errorMsg,
        confirmText: t('common.text.confirm'),
      })
    }
})

const handleSubmit = async (coverLogin = false) => {
    isLoading.value = true
    usernameInput.value.disabled = true
    passwordInput.value.disabled = true
    usernameInput.value.setCustomValidity('')
    passwordInput.value.setCustomValidity('')
    loginButton.value.disabled = true


     let isError = false
    // 验证表单数据是否有效
    if (username.value === '') {
        isError = true
        usernameInput.value.setCustomValidity(t('login.input.username.required'))

    }

    if (password.value === '') {
        isError = true
        passwordInput.value.setCustomValidity(t('login.input.password.required'))
    }

    if (isError) {
        isLoading.value = false
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
        passwordInput.value.setCustomValidity(t('login.error.invalid_credentials'))
      } else if (result.status == 3002) {
        // 服务器错误
        passwordInput.value.setCustomValidity(t('login.error.is_disabled'))
      } else if (result.status == 3003) {
        // 重复登录
        snackbar({
          message: t('login.error.repeat_login'),
        })
        router.push("/")

      } else if (result.status == 3004) {
  
        dialog({
          headline: t('login.dialog.new_device.title'),
          description: t("login.dialog.new_device.description", {ip: result.data.old_device_ip}),
          actions: [
            {
              text: t('common.text.cancel'),
              onClick: () => {
                isLoading.value = false
                usernameInput.value.disabled = false
                passwordInput.value.disabled = false
                loginButton.value.disabled = false
              }
            },
            {
              text: t('common.text.confirm'),
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
          headline: t("login.dialog.error.title"),
          description: `未知错误（${result.status}）：${result.data}`,
          confirmText: '确定'
        })
      }
    } 
    
    catch(error) {
      alert({
        headline: t("login.dialog.error.title"),
        description: `网络错误：${error.message}`,
        confirmText: '确定'
      })
    } 
    finally {
      if (result !== null && result.status !== 3004) {
            isLoading.value = false
            usernameInput.value.disabled = false
            passwordInput.value.disabled = false
            loginButton.value.disabled = false
          }
    }
}
</script>

