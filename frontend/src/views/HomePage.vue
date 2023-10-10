<template>
    <div>
        <HomeHeader></HomeHeader>
        <router-view></router-view>
    </div>
</template>

<script>
import HomeHeader from '../components/HomeHeader.vue'

export default {
    components: {
        HomeHeader,
    }
}
</script>


<style>

</style>