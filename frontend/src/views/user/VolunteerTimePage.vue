<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="volunteerTime"
                style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="info" @click="changeToUserInfoPage">
                    <span class="item-font" style="font-weight: bold;">个人信息</span>
                </el-menu-item>
                <el-menu-item index="volunteerTime" @click="changeToVolunteerTimePage">
                    <span class="item-font" style="font-weight: bold;">志愿统计</span>
                </el-menu-item>
            </el-menu>
        </div>
        <v-btn class="back-button" @click="handleBack">
            <template v-slot:prepend>
                <el-icon>
                    <Back />
                </el-icon>
            </template>
            返回
        </v-btn>
    </div>
</template>

<script>
export default {
    computed: {
        userId() {
            return this.$store.state.userId;
        },
        lastMenu() {
            return this.$store.state.lastMenu;
        }
    },
    methods: {
        changeToUserInfoPage() {
            this.$router.push({
                path: '/user/info'
            })
        },
        changeToVolunteerTimePage() {
            this.$router.push({
                path: '/user/volunteer-time'
            })
        },
        handleBack() {
            this.$store.commit("setActiveMenu", this.lastMenu);
            this.$router.go(-1);
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

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.back-button {
    font-weight: bold;
    font-size: 16px;
}
</style>