import axios from 'axios'
import router from '@/router'

const request = axios.create({
    baseURL: '/api',
    timeout: 10000,
})

// 请求拦截，自动添加Authorization头
request.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token')
        // console.log(token)
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => Promise.reject(error)

)


// 相应拦截
request.interceptors.response.use(
    response => response,
    error => {
        // 处理401错误
        if (error.response.status === 401) {
            
            // 识别status
            const status = error.response.data.status

            let msg = ''
            if (status == 2002) {
                // 对于权限不足的api，应不跳转到登录页
                msg = '权限不足'
            } else if (status == 2003) {
                msg = 'Token无效，请重新登录。'
            } else if (status == 2004) {
                
                msg = 'Token过期，请重新登录。'
            } else if (status == 2005) {
                msg = '有新的设备覆盖了你的登录状态，请重新登录。'
            } else {
                msg = '未知错误，请重新登录。'
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
            } else {
                // 对于权限不足的api，应不跳转到登录页
            }
        } else if (error.response.status === 400) {
            const status = error.response.data?.status || -1
            if (status == 1001) {
                let detail = JSON.stringify(error.response.data?.data)
                
                // console.log(error.response.data?.data)
                router.push({
                    name: 'Error',
                    query: {
                        title: '请求错误',
                        message: '请求错误，此问题通常不是由您的操作引起的。请复制详细信息并联系开发者。',
                        detail: detail
                    }
                })

            }
        }

        return Promise.reject(error)
    }
)

export default request