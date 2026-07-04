<template>

    <TopBar title="首页">
      <template #right>
        <!-- 右上角的按钮 -->
        <mdui-dropdown trigger="click">
          <div slot="trigger">
            <mdui-button-icon >
              <mdui-icon-more-vert></mdui-icon-more-vert>
            </mdui-button-icon>
          </div>

          <mdui-menu>
            
          
            <div v-if="isAdmin">
              <mdui-menu-item @click="goShopSettings">店铺设置
                <mdui-icon-shopping-cart slot="icon"></mdui-icon-shopping-cart>
              </mdui-menu-item>

              <mdui-menu-item @click="changeBusinessState">
                <span v-if="isBusiness">结束营业</span>
                <span v-else>开始营业</span>
                <mdui-icon-door-back slot="icon"></mdui-icon-door-back>
                </mdui-menu-item>
              
            </div>

            <mdui-divider></mdui-divider>


            <mdui-menu-item  @click="goScanQR">扫描
              <mdui-icon-qr-code-scanner slot="icon"></mdui-icon-qr-code-scanner>
            </mdui-menu-item>
            <mdui-menu-item @click="goSettings">选项
              <mdui-icon-settings slot="icon" ></mdui-icon-settings>
            </mdui-menu-item>

            <mdui-divider></mdui-divider>

            <mdui-menu-item @click="goDashboard">数据看板
              <mdui-icon-open-in-new slot="icon"></mdui-icon-open-in-new>
            </mdui-menu-item>
          </mdui-menu>

        </mdui-dropdown>
        
      </template>
    </TopBar>

    <!-- 主体内容 -->
    <div class="mdui-prose">
      <div style="font-size: 24px">欢迎回来，{{ currentUser }}。</div>
    
      <!-- 打样信息 -->
      <div v-if="!isBusiness">
        <TipCard variant="filled" background-color="#BB1614" color="#fff">
          <mdui-icon-warning></mdui-icon-warning>
            店铺已打样。
        </TipCard>
      </div>

      <!-- 统计信息 -->
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
      <!-- 餐桌状态 -->
      <div class="table_conatiner">
        <div style="margin: 14px">

          <div style="display: flex">
            <div style="font-size: 24px; margin-left: 0px;">餐桌状态</div>
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

      <mdui-divider style="margin: 9px;"></mdui-divider>


      <!-- 操作按钮 -->
      <div class="actions_container">
        <div class="action_item">
          <mdui-button full-width variant="outlined" style="height: 70px">

            <div style="font-size: 24px; display: block">
              <mdui-icon-done></mdui-icon-done>
              <div style="font-size: 16px">出餐</div>
            </div>
          
          </mdui-button>
        </div>
        
        <div class="action_item">
          <mdui-button full-width variant="outlined" style="height: 70px;">

            <div style="font-size: 24px; display: block">
              <mdui-icon-list></mdui-icon-list>
              <div style="font-size: 16px">全部菜品</div>
            </div>

          </mdui-button>
        </div>

        <div class="action_item">
          <mdui-button full-width variant="outlined" style="height: 70px;">

            <div style="font-size: 24px; display: block">
              <mdui-icon-add></mdui-icon-add>
              <div style="font-size: 16px">添加订单</div>
            </div>

          </mdui-button>
        </div>

      
      </div>
      
      <p>{{  isLoggedIn }}</p>


    </div>

    <!-- 切换营业状态对话框-->
    <mdui-dialog
      headline="切换营业状态"
      description="确认切换营业状态吗？"
      close-on-overlay-click
      ref="changeBusinessStateDialog"
      style="height: auto;"
    >
    <div v-if="changeBusinessStateisLoading" style="text-align: center; overflow-y: hidden;">
      <mdui-circular-progress></mdui-circular-progress>
    </div>

  
    <mdui-button v-if="!changeBusinessStateisLoading" slot="action" variant="text" @click="changeBusinessStateDialog.open=false">否</mdui-button>
    <mdui-button v-if="!changeBusinessStateisLoading" slot="action" variant="text" @click="changeBusinessStateConfirmClick" ref="changeBusinessStateConfrim">是</mdui-button>
  </mdui-dialog>


</template> 

<script setup>
// 导入自定义组件
import TipCard from '@/components/TipCard.vue'
import TopBar from '@/components/TopBar.vue'

// 导入mdui组件
import 'mdui/components/card.js'
import 'mdui/components/divider.js';
import 'mdui/components/button.js'
import 'mdui/components/collapse.js';
import 'mdui/components/collapse-item.js';
import 'mdui/components/list.js'
import 'mdui/components/dropdown.js';
import 'mdui/components/menu.js'
import 'mdui/components/menu-item.js';
import 'mdui/components/dialog.js';
import 'mdui/components/circular-progress.js';

// 导入mdui图标
import '@mdui/icons/warning.js'
import '@mdui/icons/refresh.js'
import '@mdui/icons/done.js';
import '@mdui/icons/more-vert.js';
import '@mdui/icons/qr-code-scanner.js';
import '@mdui/icons/settings.js';
import '@mdui/icons/open-in-new.js';
import '@mdui/icons/add.js';
import '@mdui/icons/shopping-cart.js';
import '@mdui/icons/door-back.js';
import '@mdui/icons/list.js';

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter();
const currentUser = ref('用户'); // 当前用户

const isBusiness = ref(false); // 是否营业

const isAdmin = ref(true); // 是否管理员

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

const goNewOrder = () => {
  router.push("/orders/new");
}

const goScanQR = () => {
  router.push("/scan");
}

const goSettings = () => {
  router.push("/account/settings");
}

const goDashboard = () => {
  router.push("/dashboard");
}

const goShopSettings = () => {
  router.push("/shop/settings");
}

const changeBusinessStateDialog = ref(null);
const changeBusinessStateConfrim = ref(null);
const changeBusinessStateisLoading = ref(false);



const changeBusinessState = () => {
  changeBusinessStateDialog.value.open = true;
}

const changeBusinessStateConfirmClick = async () => {
  changeBusinessStateisLoading.value = true;
  changeBusinessStateDialog.value.description = '正在切换营业状态';
  

  await new Promise(resolve => setTimeout(resolve, 1000));
  changeBusinessStateisLoading.value = false;

  

  changeBusinessStateDialog.value.open = false
}


const isLoggedIn = ref(false);

onMounted( async () => {
  let token = localStorage.getItem("token");

  const response = await fetch("/api/verify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "token": token
    })
  });

  const data = await response.json()
  if (data["status"] == 0) {
    // 登录成功
    isLoggedIn.value = "已登录";
  } else {
    // 登录失败
    isLoggedIn.value = "未登录";
  }

})



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

  .actions_container {
    display: flex; 
    width: 100%; 
    flex: 1;
    justify-content: center;
    gap: 8px;
  }


  .action_item {
    width: calc(50% - 4px);
  }

</style>
