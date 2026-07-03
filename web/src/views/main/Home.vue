<template>

    <div class="mdui-prose">
      <div style="font-size: 24px">欢迎回来，{{ currentUser }}。</div>
    

      <div v-if="!isBusiness">
        <TipCard variant="filled" background-color="#BB1614" color="#fff">
          <mdui-icon-warning></mdui-icon-warning>
            店铺已打样。
        </TipCard>
      </div>

      <mdui-card variant="outlined" style="width: 100% ;margin-top:4px; border: 0">
        <div style="margin: 8px">

          <div style="display: flex">
            <div style="font-size: 24px; margin-left: 12px;">今日订单</div>
            <mdui-button-icon style="margin-left: auto;" @click="refreshOrders" ref="refreshOrdersButton">
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
            
            <div class="stats_item">
                <div class="stats_label">接待人数</div>
                <div class="stats_value">0</div>
            </div>

          </div>
          
        </div>
      </mdui-card>

      <mdui-divider style="margin: 9px;"></mdui-divider>

      <div class="table_conatiner">
        <div style="margin: 8px">

          <div style="display: flex">
            <div style="font-size: 24px; margin-left: 12px;">餐桌状态</div>
            <mdui-button-icon style="margin-left: auto;" @click="refreshTables" ref="refreshTablesButton">
              <mdui-icon-refresh></mdui-icon-refresh>
            </mdui-button-icon>
          </div>
          
          <div class="table_scroll">
            <div class="table_content">
              <div v-for="i in 12" :key="i" class="table_item">
                <div class="table_label">餐桌 {{ i }}</div>
                <div class="table_value">空闲</div>
              </div>
            </div>
          </div>
          
        </div>
      </div>



      <mdui-button full-width style="height: 50px;">
          <div style="font-size: 16px">出餐</div>
          <mdui-icon-done slot="icon" ></mdui-icon-done>
      </mdui-button>


    </div>

</template> 

<script setup>
import TipCard from '@/components/TipCard.vue'

import 'mdui/components/card.js'
import 'mdui/components/divider.js';
import 'mdui/components/button.js'
import 'mdui/components/collapse.js';
import 'mdui/components/collapse-item.js';
import 'mdui/components/list.js'


import '@mdui/icons/warning.js'
import '@mdui/icons/refresh.js'
import '@mdui/icons/done.js';

import { ref, onMounted } from 'vue'

const currentUser = ref('用户'); // 

const isBusiness = ref(false); // 是否营业

const refreshOrdersButton = ref(null);
const refreshTablesButton = ref(null);



const refreshOrders = async () => {
  refreshOrdersButton.value.loading = true;

  await new Promise(resolve => setTimeout(resolve, 1000));
  refreshOrdersButton.value.loading = false;

};

const refreshTables = async () => {
  refreshTablesButton.value.loading = true;

  await new Promise(resolve => setTimeout(resolve, 1000));
  refreshTablesButton.value.loading = false;
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
    font-size: 14px;
    text-align: center;

  }

  .stats_value {
    font-size: 24px;
    text-align: center;
  }

  .table_conatiner {
    width: 100% ;
    margin-top:4px;
    border: 0;
    
  }


  .table_scroll {
    overflow-x: auto;
    overflow-y: hidden;
    width: 100%
  }

  .table_content {
    display: flex;
    justify-content: center;
    min-width: max-content;
    gap: 8px;

  
  
  }

  .table_item {
    /* width: 25%; */
  }

  .table_label {
    font-size: 14px;
    text-align: center;
  }

  .table_value {
    font-size: 18px;
    text-align: center;
  }

</style>
