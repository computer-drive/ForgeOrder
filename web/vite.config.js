import vue from '@vitejs/plugin-vue';
import { fileURLToPath, URL } from 'node:url'

export default {
  plugins: [
    vue({
      template: {
        compilerOptions: {
          // 所有以 mdui- 开头的标签名都是 mdui 组件
          isCustomElement: (tag) => tag.startsWith('mdui-'),
        },
      } 
    }),
  ],
  resolve: {
        alias: {
          '@': fileURLToPath(new URL('./src', import.meta.url)),
        }
      }
};