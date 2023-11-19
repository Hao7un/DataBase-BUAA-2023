<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="my" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="join" @click="changeToJoinTeamPage">
                    <span class="item-font" style="font-weight: bold;">加入团队</span>
                </el-menu-item>
                <el-menu-item index="my" @click="changeToMyTeamPage">
                    <span class="item-font" style="font-weight: bold;">我的团队</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content-container">
            
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            dateRange: null,
            keyword: null,
            currentPage: 1,
            selectedTotalIndex: null,
            totalList: [
                {name: "志愿团队1"},
                {name: "志愿团队2"},
                {name: "志愿团队3"},
                {name: "志愿团队4"},
                {name: "志愿团队5"},
                {name: "志愿团队6"},
                {name: "志愿团队7"},
                {name: "志愿团队8"},
                {name: "志愿团队9"},
                {name: "志愿团队10"},
                {name: "志愿团队11"},
                {name: "志愿团队12"},
            ]
        }
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 9;
            return this.totalList.slice(startIndex, startIndex + 9);
        }
    },
    methods: {
        changeToJoinTeamPage() {
            this.$router.push({
                path: '/team/join'
            })
        },
        changeToMyTeamPage() {
            this.$router.push({
                path: '/team/myteam'
            })
        },

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
    height: 1200px;
    flex-direction: column;
    padding-top: 20px;
    margin-left: 20px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.selector-container {
    height: 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
    margin-left: 50px;
}

.content-container {
    display: flex;
    flex-direction: column;
    margin-left: 50px;
}

.date-container {
    display: flex;
    width: 590px;
    margin-left: 30px;
}

.search-container {
    display: flex;
    justify-content: center;
    margin-left: 150px;
    margin-right: 30px;
}


</style>