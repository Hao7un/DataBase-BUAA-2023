<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="my" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="join" @click="changeToJoinRecruitmentPage">
                    <span class="item-font" style="font-weight: bold;">参与招募</span>
                </el-menu-item>
                <el-menu-item index="my" @click="changeToMyRecruitmentPage">
                    <span class="item-font" style="font-weight: bold;">招募统计</span>
                </el-menu-item>
            </el-menu>
        </div>
        
    </div>
</template>


<script>
export default {

    methods: {
        handlePageChange(currentPage) {
            this.currentPage = currentPage;
        },
        changeToJoinRecruitmentPage() {
            this.$router.push({
                path: '/recruitment/join'
            })
        },
        changeToMyRecruitmentPage() {
            this.$router.push({
                path: '/recruitment/my'
            })
        }
    },
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

.item-font {
    font-size: 18px;
    margin-left: 10px;
}
</style>
