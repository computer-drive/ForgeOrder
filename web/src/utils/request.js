import axios from 'axios'
import router from '@/router'

import { createLogger } from './log.js'
import { snackbar } from 'mdui'

const request = axios.create({
    baseURL: '/api',
    timeout: 10000,
})

// 请求拦截，自动添加Authorization头
request.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token')

        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => Promise.reject(error)

)


// 响应拦截
request.interceptors.response.use(
    response => response,
    error => {
        const logger = createLogger("Auth")
        // 处理401错误
        if (error.response?.status === 401) {
            
            // 识别status
            const status = error.response.data.status

            let msg = ''
            if (status == 2002) {
                // 对于权限不足的api，应不跳转到登录页
                logger.error("权限不足")
                msg = t('Ulogin.error.no_permission')
            } else if (status == 2003) {
                logger.error("Token无效")
                msg = t('Ulogin.error.invalid_token')
            } else if (status == 2004) {
                logger.error("Token过期")
                msg = t('Ulogin.error.expired_token')
            } else if (status == 2005) {
                logger.error("旧设备")
                msg = t('Ulogin.error.old_device')
            } else {
                logger.error("未知错误")
                logger.error(error.response.data)
                msg = t('Ulogin.error.unknown', { status: status })
            }

            // 跳转登录页
            if (status != 2002) {
                router.push({
                    name: 'Login',
                    state: {
                        msg: msg
                    }
                })
                // 清除本地的token
                localStorage.removeItem("token")
                return
                
            } else {
                // 对于权限不足的api，应不跳转到登录页
            }
        } else if (error.response.status === 400) {
            const status = error.response.data?.status || -1
            if (status == 1001) {
                snackbar({
                    message:"请求错误，请联系开发者。"
                })
            }
        } else if (error.response.status == 503) {
            snackbar({
                message:"服务器繁忙，请稍后再试。"
            })
        }

        return Promise.reject(error)
    }
)

export default request