<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="join" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="join" @click="changeToJoinProjectPage">
                    <span class="item-font" style="font-weight: bold">查看项目</span>
                </el-menu-item>
                <el-menu-item index="my" @click="changeToMyProjectPage">
                    <span class="item-font" style="font-weight: bold">我的收藏</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content-container">
            <div class="selector-container">
                <div class="menu-container">
                    <!-- <el-select v-model="statusRadio" placeholder="项目状态" clearable size="large" class="select-container">
                        <template #prefix>
                            <el-icon class="icon-container"><Open /></el-icon>
                        </template>
                        <el-option
                            v-for="item in option2"
                            :key="item.value"
                            :value="item.value"
                            
                        ></el-option>
                    </el-select> -->
                </div>
                <div class="search-container">
                    <div class="search-item-container">
                        <el-select v-model="typeRadio" placeholder="项目类别" clearable size="large">
                            <template #prefix>
                                <el-icon class="icon-container"><FolderOpened /></el-icon>
                            </template>
                            <el-option
                                v-for="item in option1"
                                :key="item.value"
                                :value="item.value"
                                size="large"
                            ></el-option>
                        </el-select>
                    </div>
                    <div class="search-item-container">
                        <el-input v-model="keyword" placeholder="输入项目名称" clearable size="large" style="width: 200px"></el-input>
                    </div>
                </div>
            </div>
            <div class="recruitments-container">
                <div class="info-container">
                    <div class="card" v-for="(item, index) in displayedList" >
                        <el-card shadow="hover" class="inner-card" @click="showRecruitmentTable(index, this.currentPage)">
                            <div class="img-container">
                                <img src="../assets/images/project.png">
                            </div>
                            <div class="card-info">
                                <div class="info-item">项目名称：{{ item.name }}</div>
                                <div class="info-item">项目类别：{{ item.type }}</div>
                                <div class="info-item">所属团队：{{ item.team }}</div>
                            </div>
                          </el-card>
                    </div>
                </div>
                <div class="pagination-container">
                    <el-pagination 
                        @current-change="handlePageChange"
                        :page-size="9"
                        :total="filteredList.length"
                        layout="prev, pager, next">
                    </el-pagination>
                </div>
            </div>
        </div>
        
        <div class="recruitment-table" v-if="recruitmentTableVisible">
            <div class="quit-container">
                <el-button round @click="quitRecruitmentTable()">
                    <el-icon><CloseBold /></el-icon>
                </el-button>
            </div>
            <div class="recruitment-content">
                <div class="recruitment-top">
                    <div class="recruitment-img">
                        <img src="../assets/images/project.png">
                    </div>
                    <div class="recruitment-info">
                        <div class="inner-info-item">
                            项目名称：{{ this.totalList[this.selectedTotalIndex].name }}
                        </div>
                        <div class="inner-info-item">
                            项目时间：{{ this.totalList[this.selectedTotalIndex].time }}
                        </div>
                        <div class="inner-info-item">
                            志愿时长：{{ this.totalList[this.selectedTotalIndex].hours }} 小时
                        </div>
                        <div class="inner-info-item">
                            项目地点：{{ this.totalList[this.selectedTotalIndex].location }}
                        </div>
                        <div class="inner-info-item">
                            项目状态：{{ this.totalList[this.selectedTotalIndex].state }}
                        </div>
                    </div>
                </div>
                <div class="recruitment-intro">
                    {{ this.totalList[this.selectedTotalIndex].intro }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            typeRadio: "",
            authRadio: "",
            statusRadio: "",
            date: "",
            keyword: "",
            currentPage: 1,
            selectedTotalIndex: null,
            totalList: [
                {name: "志愿项目1", hours: 1, type: "社区服务", intro: "这是一段介绍", team: "志愿团队1"},
                {name: "志愿项目2", hours: 2, type: "科技科普", intro: "这是一段介绍", team: "志愿团队2"},
                {name: "志愿项目3", hours: 3, type: "支教助学", intro: "这是一段介绍", team: "志愿团队3"},
                {name: "志愿项目4", hours: 4, type: "体育赛事", intro: "这是一段介绍", team: "志愿团队4"},
                {name: "志愿项目5", hours: 5, type: "大型演出", intro: "这是一段介绍", team: "志愿团队5"},
                {name: "志愿项目6", hours: 6, type: "其它", intro: "这是一段介绍", team: "志愿团队6"},
                {name: "志愿项目7", hours: 7, type: "社区服务", intro: "这是一段介绍", team: "志愿团队7"},
                {name: "志愿项目8", hours: 8, type: "科技科普", intro: "这是一段介绍", team: "志愿团队8"},
                {name: "志愿项目9", hours: 9, type: "支教助学", intro: "这是一段介绍", team: "志愿团队9"},
                {name: "志愿项目10", hours: 10, type: "体育赛事", intro: "这是一段介绍", team: "志愿团队10"},
                {name: "志愿项目11", hours: 11, type: "大型演出", intro: "这是一段介绍", team: "志愿团队1"},
                {name: "志愿项目12", hours: 12, type: "其它", intro: "这是一段介绍", team: "志愿团队2"},
                {name: "志愿项目13", hours: 13, type: "社区服务", intro: "这是一段介绍", team: "志愿团队3"},
                {name: "志愿项目14", hours: 14, type: "科技科普", intro: "这是一段介绍", team: "志愿团队4"},
                {name: "志愿项目15", hours: 15, type: "支教助学", intro: "这是一段介绍", team: "志愿团队5"},
            ],
            recruitmentTableVisible: false,
            option1: [
                {name: "社区服务", value: "社区服务"},
                {name: "科技科普", value: "科技科普"},
                {name: "支教助学", value: "支教助学"},
                {name: "体育赛事", value: "体育赛事"},
                {name: "大型演出", value: "大型演出"},
                {name: "其它", value: "其它"},

            ],
            option2: [
                {name: "正在招募", value: "正在招募"},
                {name: "已结项", value: "已结项"},
            ]
        };
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 9;
            let endIndex = startIndex + 9;
            let filteredList = this.totalList;
            if (this.keyword != null && this.typeRadio != null) {
                filteredList = filteredList.filter( item => {
                        return item.name.includes(this.keyword) && item.type.includes(this.typeRadio);
                    }
                )
            }
            return filteredList.slice(startIndex, endIndex);
        },
        filteredList() {
            let list = this.totalList;
            if (this.keyword != null && this.typeRadio != null) {
                list = list.filter( item => {
                        return item.name.includes(this.keyword) && item.type.includes(this.typeRadio);
                    }
                )
            }
            return list;
        },
    },
    methods: {
        handlePageChange(currentPage) {
            this.currentPage = currentPage;
        },
        changeToMyProjectPage() {
            this.$router.push({
            path: '/project/my'
        })
        },
        changeToJoinProjectPage() {
            this.$router.push({
            path: '/project/join'
        })
        },
        showRecruitmentTable(index, currentPage) {
            this.selectedTotalIndex = (this.currentPage - 1) * 9 + index;
            this.recruitmentTableVisible = true;
        },
        quitRecruitmentTable() {
            this.recruitmentTableVisible = false;
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

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.icon-container {
    font-size: 25px;
}

.content-container {
    display: flex;   
    flex-direction: column;
}

.selector-container {
    height: 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 25px;
}

.menu-container {
    display: flex;
    width: 590px;
}

.search-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 190px;
    margin-right: 100px;
}

.search-item-container {
    margin-left: 10px;
    margin-right: 30px;
}

.recruitments-container {
    display: flex;
    align-items: center;
    flex-direction: column;
}

.info-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-content: flex-start;
    margin-top: 15px;
    margin-left: 50px;
    height: 1000px;
    width: 1350px;
}

.card {
    width: calc(33.33% - 10px);
    height: 300px;
    margin-top: 20px;
    margin-right: 8px;
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
    margin-left: 10px;
    justify-content: center;
    align-items: center;
}

.card-info {
    display: flex;
    flex-direction: column;
}

.recruitment-table {
    width: 800px;
    height: 800px;
    top: 50%;
    left: 50%;
    background: rgba(235, 233, 233, 0.8);
    position: fixed;
    z-index: 1;
    transform: translate(-50%, -50%);
    display: flex;
}

.pagination-container {
    margin-top: 50px;
    margin-bottom: 50px;
}

.recruitment-content {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.recruitment-top {
    flex: 1;
    display: flex;
}

.recruitment-img {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}

.recruitment-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
}

.inner-info-item {
    margin-bottom: 10px;
}

.recruitment-intro {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}

.quit-container {
  position: absolute;
  top: 10px;
  right: 10px;
}

.select-container {
    margin-left: 40px;
}

</style>