<template>
    <div class="container mdui-prose">
        <h2>系统设置</h2>
        <mdui-list>
            <!-- <mdui-list-subheader>Subheader</mdui-list-subheader> -->
            <mdui-list-item rounded @click="router.push('/system/logs')">系统日志
                <mdui-icon-receipt slot="icon"></mdui-icon-receipt>
                <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right>
            </mdui-list-item>

            <mdui-list-item rounded @click="router.push('/system/about')">关于系统
                <mdui-icon-info slot="icon"></mdui-icon-info>
                <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right>
            </mdui-list-item>
        </mdui-list>
        
    </div>
    </template> 


<script setup>
import 'mdui/components/list.js';
import 'mdui/components/list-item.js';
import 'mdui/components/list-subheader.js';

import '@mdui/icons/receipt.js'
import '@mdui/icons/info.js'
import '@mdui/icons/chevron-right.js'

import { useRouter } from 'vue-router'

const router = useRouter()
</script>