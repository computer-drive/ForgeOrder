<template>

    <div class="page">
      <TopBar :title="$t('home.topbar.text')">
        <template #right>
          <!-- <!-- 右上角的按钮 -->
          <mdui-dropdown trigger="click">
            <div slot="trigger">
              <mdui-button-icon >
                <mdui-icon-more-vert></mdui-icon-more-vert>
              </mdui-button-icon>
            </div>

            <mdui-menu>
              
            
              <div v-if="isAdmin">
                <mdui-menu-item @click="pushWithFrom('/shop/settings')">{{$t('home.topbar.menu.shop')}}
                  <mdui-icon-shopping-cart slot="icon"></mdui-icon-shopping-cart>
                </mdui-menu-item>

                <mdui-menu-item @click="changeBusinessState">
                  <span v-if="isBusiness">{{$t('home.topbar.menu.business_end')}}</span>
                  <span v-else>{{$t('home.topbar.menu.business_start')}}</span>
                  <mdui-icon-door-back slot="icon"></mdui-icon-door-back>
                  </mdui-menu-item>
                
              </div>

              <mdui-menu-item @click="pushWithFrom('/develop')">{{$t('home.topbar.menu.develop')}}
                
              </mdui-menu-item>
              <mdui-divider></mdui-divider>


              <mdui-menu-item  @click="pushWithFrom('/scan')">扫描
                <mdui-icon-qr-code-scanner slot="icon"></mdui-icon-qr-code-scanner>
              </mdui-menu-item>
              <mdui-menu-item @click="pushWithFrom('/me/settings')">选项
                <mdui-icon-settings slot="icon" ></mdui-icon-settings>
              </mdui-menu-item>

              <mdui-divider></mdui-divider>

              <mdui-menu-item @click="pushWithFrom('/dashboard')">{{$t('home.topbar.menu.dashboard')}}
                <mdui-icon-open-in-new slot="icon"></mdui-icon-open-in-new>
              </mdui-menu-item>
            </mdui-menu>

          </mdui-dropdown>
          
        </template>
      </TopBar>

      <!-- 主体内容 -->
      <div class="mdui-prose container">
        <!-- <div style="font-size: 24px">欢迎回来，{{ currentUser }}。</div> -->
        <h2>{{$t('home.main.welcome.text', {user: currentUser})}}</h2>
      
        <!-- 打样信息 -->
        <div v-if="!isBusiness">
          <TipCard variant="filled" background-color="#BB1614" color="#fff">
            <mdui-icon-warning></mdui-icon-warning>
              {{$t('home.main.not_business.text')}}
          </TipCard>
        </div>

        <!-- 统计信息 -->
        <mdui-card variant="outlined" style="width: 100% ;margin-top:4px; border: 0">
          <div style="margin: 8px">

            <div style="display: flex">
              <div style="font-size: 24px; margin-left: 12px;">{{$t('home.today.title')}}</div>
              <mdui-button-icon style="margin-left: auto;" @click="refreshOrders" ref="refreshOrdersButton">
                <mdui-icon-refresh></mdui-icon-refresh>
              </mdui-button-icon>
            </div>

            <div class="stats_content">
              <div class="stats_item">
                <div class="stats_label">{{$t('home.today.count.text')}}</div>
                <div class="stats_value">0</div>
              </div>

              <div class="stats_item">
                  <div class="stats_label">{{$t('home.today.amount.text')}}</div>
                  <div class="stats_value">0</div>
              </div>
              
              <div class="stats_item">
                  <div class="stats_label">{{$t('home.today.people.text')}}</div>
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
              <div style="font-size: 24px; margin-left: 0px;">{{$t('home.table.title')}}</div>
              <mdui-button-icon style="margin-left: auto;" @click="refreshTables" ref="refreshTablesButton">
                <mdui-icon-refresh></mdui-icon-refresh>
              </mdui-button-icon>
            </div>
            
            <div class="table_scroll">
              <div class="table_content">
                <div v-for="i in 12" :key="i" class="table_item">
                  <div class="table_label">{{$t('home.table.key', {name: i})}}</div>
                  <div class="table_value">{{$t('home.table.value.free')}}</div>
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
                <div style="font-size: 16px">{{$t('home.actions.serve.text')}}</div>
              </div>
            
            </mdui-button>
          </div>
          
          <div class="action_item">
            <mdui-button full-width variant="outlined" style="height: 70px;"
            @click="router.push('/shop')">

              <div style="font-size: 24px; display: block">
                <mdui-icon-list></mdui-icon-list>
                <div style="font-size: 16px">{{$t('home.actions.dishes.text')}}</div>
              </div>

            </mdui-button>
          </div>

          <div class="action_item">
            <mdui-button full-width variant="outlined" style="height: 70px;">

              <div style="font-size: 24px; display: block">
                <mdui-icon-add></mdui-icon-add>
                <div style="font-size: 16px">{{$t('home.actions.order.text')}}</div>
              </div>

            </mdui-button>
          </div>

        
        </div>
        


      </div>
      
      <!-- 切换营业状态对话框-->
    <mdui-dialog
      :headline="t('home.dialog.change_business_state.headline')"
      :description="t('home.dialog.change_business_state.description')"
      ref="changeBusinessStateDialog"
      style="height: auto;"
    >
    <div v-if="changeBusinessStateisLoading" style="text-align: center; overflow-y: hidden;">
      <mdui-circular-progress></mdui-circular-progress>
    </div>

  
    <mdui-button v-if="!changeBusinessStateisLoading" slot="action" variant="text" @click="changeBusinessStateDialog.open=false">{{ $t("common.text.cancel") }}</mdui-button>
    <mdui-button v-if="!changeBusinessStateisLoading" slot="action" variant="text" @click="changeBusinessStateConfirmClick" ref="changeBusinessStateConfirmButton">{{ $t("common.text.confirm") }}</mdui-button>
  </mdui-dialog>
  
    </div>

    


</template> 

<script setup>
// 导入home.css
import '@/assets/home.css'

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

import { useAuth } from '@/composables/auth.js'
import request from '@/utils/request.js'
import { pushWithFrom } from '@/utils/routerHelper'
import { t } from '@/locales/index.js'

const router = useRouter();
const currentUser = ref('用户'); // 当前用户

const isBusiness = ref(true); // 是否营业

const isAdmin = ref(false); // 是否管理员

onMounted(async () => {
  const userInfo = JSON.parse(localStorage.getItem('userInfo'));
  if (userInfo) {
    currentUser.value = userInfo.username;

    isAdmin.value = userInfo.is_admin;
    // console.log(isAdmin.value)

    const response = await request.get('/shop/getBusinessState');
    isBusiness.value = response.data.data;

  }
})

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




const changeBusinessStateDialog = ref(null);
const changeBusinessStateConfrim = ref(null);
const changeBusinessStateisLoading = ref(false);


const changeBusinessState = () => {
  changeBusinessStateDialog.value.open = true;
}

const changeBusinessStateConfirmClick = async () => {
  changeBusinessStateisLoading.value = true;

  changeBusinessStateDialog.value.description = t('home.dialog.change_business_state.changing.text');
  

  const response = await request.post('/shop/setBusinessState', {
    is_business: !isBusiness.value,
  })

  if (response.data.status == 0) {
    // console.log("切换营业状态成功")
    isBusiness.value = !isBusiness.value;
  }
  
  changeBusinessStateisLoading.value = false;


  changeBusinessStateDialog.value.open = false
}





</script>

