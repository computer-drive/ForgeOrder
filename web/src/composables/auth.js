import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/utils/request.js'
// import { er } from 'vue-router/dist/index-BQLwgiyK.js'

export function useAuth() {
    const router = useRouter()

    const token = ref(localStorage.getItem('token') || '')
    const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

    const isLoggedIn = computed(() => token.value != '')

    const login = async(username, password, cover) => {
        try {
            const res = await request.post('/auth/login', {
                username,
                password,
                cover
            })
            
            console.log(res.status, res.data.status)
            if (res.status == 200) {
                if (res.data.status == 0 || res.data.status == 3003) {
                    // 登录成功
                    // console.log("登录成功")
                    token.value = res.data.data.token

                    userInfo.value = res.data.data.user_info
                    localStorage.setItem('token', token.value)
                    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))

                    console.log(token.value, userInfo.value)

                    router.push("/")

                    return res.data
                }
                // else 登录失败
            } // else 登录失败

                
            // 登录失败
            // console.log("登录失败")
            // console.log(res.data)
            return res.data
            

            
        } catch (error) {
            
            return {
                status: -1,
                data: error
            }
        }
    }

    const logout = async() => {
        try {
            const res = await request.post('/auth/logout')
            if (res.status == 200 && res.data.status == 0) {
                // 退出登录成功
                token.value = ''
                userInfo.value = null
                localStorage.removeItem('token')
                localStorage.removeItem('userInfo')

                router.push('/login')
                
                return res.data
            } 
        } catch (error) {
            // console.log(error)
            return {
                status: -1,
                data: error
            }
        }   
    }
    
    return {
        login,
        logout,
        token,
        userInfo,
        isLoggedIn
    }
}