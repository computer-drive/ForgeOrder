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
      },
  server : {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        configure: (proxy) => {
          // 获取真实ip并设置header
          proxy.on('proxyReq', (proxyReq, req, res, options) => {
            const ip = req.socket?.remoteAddress || req.connection?.remoteAddress || 'unknown';
            const realIP = ip.replace(/^::ffff:/, '');
            proxyReq.setHeader('X-Real-IP', realIP);
            proxyReq.setHeader('X-Forwarded-For', realIP);
          })
        }
      }
    }
  },
  build: {
    outDir: '../server/static',
  },
};