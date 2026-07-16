<template>
    <div class="mdui-prose container">
        <h2>{{ $t("shop.title.tables") }}</h2>
        <mdui-list >
            <mdui-list-item rounded>餐桌1</mdui-list-item>
            <mdui-list-item rounded>餐桌2</mdui-list-item>
        </mdui-list>
    </div>
</template>

<script setup>
    import 'mdui/components/list.js'
    import 'mdui/components/list-item.js'
    import 'mdui/components/list-subheader.js'

</script>