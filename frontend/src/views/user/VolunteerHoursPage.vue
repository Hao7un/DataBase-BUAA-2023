<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="volunteerHours"
                style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="info" @click="changeToUserInfoPage">
                    <span class="item-font" style="font-weight: bold;">个人信息</span>
                </el-menu-item>
                <el-menu-item index="password" @click="changeToPasswordPage">
                    <span class="item-font" style="font-weight: bold;">修改密码</span>
                </el-menu-item>
                <el-menu-item index="volunteerHours" @click="changeToVolunteerHoursPage">
                    <span class="item-font" style="font-weight: bold;">志愿统计</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="grid-container">
            <div class="grid-item">1</div>
            <div class="grid-item">2</div>
            <div class="grid-item">3</div>
            <div class="grid-item">4</div>
            <div class="grid-item">5</div>
            <div class="grid-item">6</div>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        changeToUserInfoPage() {
            this.$router.push({
                path: '/user/info'
            })
        },
        changeToPasswordPage() {
            this.$router.push({
                path: '/user/password'
            })
        },
        changeToVolunteerHoursPage() {
            this.$router.push({
                path: '/user/volunteer-hours'
            })
        }
    }
}
</script>

<style scoped>
.main-container {
    display: flex;
}

.sidebar-container {
    display: flex;
    width: 180px;
    flex-direction: column;
    padding-top: 20px;
    margin-left: 20px;
    height: auto;
    min-height: 750px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.grid-container {
  display: grid;
  grid-template-columns: auto auto auto; /* 定义了三列，每列的宽度为 auto */
  grid-gap: 10px; /* 定义了网格线之间的间距 */
}

.grid-item {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  font-size: 30px;
  text-align: center;
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}
</style>