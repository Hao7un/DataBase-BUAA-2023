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
        <div class="content-container">
            <h1>TO BE DONE</h1>
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
    height: 1000px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.content-container {
    display: block;
    flex-direction: column;
    margin-left: 300px;
}

.item-font {
  font-size: 18px;
  margin-left: 10px;
}
</style>