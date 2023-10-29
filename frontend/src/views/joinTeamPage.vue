<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="join">
                <el-menu-item index="join" @click="changeToJoinTeamPage">
                    <span class="item-font" style="font-weight: bold;">加入团队</span>
                </el-menu-item>
                <el-menu-item index="my" @click="changeToMyTeamPage">
                    <span class="item-font" style="font-weight: bold;">我的团队</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content-container">
            <div class="selector-container">
                <div class="date-container">
                    <span style="display: flex; align-items: center;">团队注册日期</span> &nbsp;&nbsp;
                    <el-date-picker 
                        v-model="dateRange" 
                        type="daterange" 
                        unlink-panels 
                        range-separator="至" 
                        start-placeholder="开始日期"
                        end-placeholder="结束日期"
                        size="large"
                        clearable>
                    </el-date-picker>
                </div>
                <div class="search-container">
                    <el-input v-model="keyword" placeholder="请输入团队名称" clearable size="large" style="width: 200px"></el-input>
                </div> &nbsp;
                <el-button size="large" type="primary" @click="searchSubmit"><span style="font-weight: bold; font-size: 15px; color:whitesmoke">搜 索</span></el-button>
            </div>
            <div class="teams-container">
                <div class="info-container">
                    <div class="card" v-for="(item, index) in displayedList">
                        <el-card shadow="hover" class="inner-card">
                            <div class="img-container">
                                <img src="../assets/images/hand_shaking.png">
                            </div>
                            <div class="card-info">
                                <div class="info-item">团队名称：{{ item.name }}</div>
                            </div>
                        </el-card>
                    </div>
                </div>
                <div class="pagination-container">
                    <el-pagination 
                        @current-change="handlePageChange"
                        :page-size="6"
                        :total="totalList.length"
                        layout="prev, pager, next">
                    </el-pagination>
                </div>
            </div>
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
            ]
        }
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 6;
            return this.totalList.slice(startIndex, startIndex + 6);
        }
    },
    methods: {
        searchSubmit() {
            var date = new Date();
            console.log(date);
        },
        handlePageChange(currentPage) {
            this.currentPage = currentPage;
        },
        changeToJoinTeamPage() {
            this.$router.push({
                path: '/team/join'
            })
        },
        changeToMyTeamPage() {
            this.$router.push({
                path: '/team/myteam'
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
    align-items: center;
    margin-top: 15px;
    margin-left: 50px;
}

.content-container {
    display: flex;
    flex-direction: column;
    margin-left: 15px;
}

.date-container {
    display: flex;
    width: 590px;
    margin-left: 30px;
}

.teams-container {
    padding-left: 50px;
    display: flex;
    align-items: center;
    flex-direction: column;
}

.search-container {
    display: flex;
    justify-content: center;
    margin-left: 150px;
    margin-right: 30px;
}

.info-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-content: flex-start;
    margin-top: 15px;
    height: 1000px;
    width: 1350px;
}

.card {
    width: calc(50% - 150px);
    height: 300px;
    margin-top: 20px;
    margin-right: 50px;
    margin-left: 80px;
    cursor: pointer;
}

.inner-card {
    width: 100%;
    height: 100%;
}


.img-container {
    width: 100%;
    height: 66.6%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.info-item {
    margin-top: 10px;
    justify-content: center;
    align-items: center;
}

.info-item {
    margin-top: 10px;
    justify-content: center;
    align-items: center;
}

.pagination-container {
    margin-top: 50px;
    margin-bottom: 50px;
}

</style>