<template>
    <div class="mdui-prose container">
        <h2>{{ $t("shop.title.main") }}</h2>
        <mdui-list>
            <!-- <mdui-list-subheader>Subheader</mdui-list-subheader> -->
            <mdui-list-item rounded @click="router.push('/shop/dishes')">
                {{ $t("shop.title.dishes") }}
                <mdui-icon-list slot="icon"></mdui-icon-list>
                <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right>
            </mdui-list-item>

            <mdui-list-item rounded @click="router.push('/shop/tables')">
                {{  $t("shop.title.tables") }}
                <mdui-icon-table-restaurant slot="icon"></mdui-icon-table-restaurant>
                <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right>
            </mdui-list-item>

            <mdui-list-item rounded @click="router.push('/shop/users')">
                {{  $t("shop.title.users") }}
                <mdui-icon-account-circle slot="icon"></mdui-icon-account-circle>
                <mdui-icon-chevron-right slot="end-icon"></mdui-icon-chevron-right>
            </mdui-list-item>
        </mdui-list>
    </div>
    </template> 


<script setup>
    import '@mdui/icons/table-restaurant.js'
    import '@mdui/icons/chevron-right.js'
    import '@mdui/icons/list.js';
    import '@mdui/icons/account-circle.js';

    import 'mdui/components/list.js'
    import 'mdui/components/list-item.js'
    import 'mdui/components/list-subheader.js'

    import { useRouter } from 'vue-router'

    const router = useRouter()
</script>