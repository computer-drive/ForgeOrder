<template>

    <div class="mdui-prose">
      <div style="font-size: 24px">欢迎回来，{{ currentUser }}。</div>
    

      <div v-if="!isBusiness">
        <TipCard variant="filled" background-color="#BB1614" color="#fff">
          <mdui-icon-warning></mdui-icon-warning>
            店铺已打样。
        </TipCard>
      </div>

      <mdui-card variant="outlined" style="width: 100% ;margin-top:4px">
        <div style="margin: 8px">

          <div style="display: flex">
            <div style="font-size: 24px; margin-left: 12px;">今日订单</div>
            <mdui-button-icon style="margin-left: auto;" @click="refreshOrders">
              <mdui-icon-refresh></mdui-icon-refresh>
            </mdui-button-icon>
          </div>

          <div class="stats_content">
            <div class="stats_item">
              <div class="stats_label">订单数量</div>
              <div class="stats_value">0</div>
            </div>

            <div class="stats_item">
                <div class="stats_label">总金额（元）</div>
                <div class="stats_value">0</div>
            </div>
          </div>
          
        </div>
      </mdui-card>
    </div>

</template> 

<script setup>
import TipCard from '@/components/TipCard.vue'



import 'mdui/components/card.js';
import '@mdui/icons/warning.js';
import '@mdui/icons/refresh.js';

import { ref, onMounted } from 'vue'

const currentUser = ref('用户'); // 

const isBusiness = ref(false); // 是否营业

const refreshOrders = () => {
  console.log('刷新订单');
  // 在这里添加刷新订单的逻辑
};

</script>

<style>
  .stats_content {
    display: flex;
    align-items: center;
    justify-content: center;

  }

  .stats_item {
    width: 50%
  }


  .stats_label {
    font-size: 16px;
    text-align: center;

  }

  .stats_value {
    font-size: 24px;
    text-align: center;
  }
</style>
