<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="join">
                <el-menu-item index="join" @click="changeToJoinProjectPage">
                    <span class="item-font" style="font-weight: bold">加入项目</span>
                </el-menu-item>
                <el-menu-item index="my" @click="changeToMyProjectPage">
                    <span class="item-font" style="font-weight: bold">我的项目</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content-container">
            <div class="selector-container">
                <div class="menu-container">
                    <el-menu mode="horizontal">
                        <el-sub-menu index="type">
                            <template #title>
                                <el-icon class="icon-container"><FolderOpened /></el-icon>
                                <p class="item-font">服务类别</p>
                            </template>
                            <el-radio-group v-model="typeRadio" class="radio-container">
                                <div class="radio-item-container">
                                    <el-radio :label="1" class="radio-spacer">社区服务</el-radio>
                                </div>
                                <div class="radio-item-container">
                                    <el-radio :label="2" class="radio-spacer">科技科普</el-radio>
                                </div>
                                <div class="radio-item-container">
                                    <el-radio :label="3" class="radio-spacer">支教助学</el-radio>
                                </div>
                                <div class="radio-item-container">
                                    <el-radio :label="4" class="radio-spacer">体育赛事</el-radio>
                                </div>
                                <div class="radio-item-container">
                                    <el-radio :label="5" class="radio-spacer">大型演出</el-radio>
                                </div>
                                <div class="radio-item-container">
                                    <el-button size="small" @click="clearTypeRadio()">撤销</el-button>
                                </div>                                
                            </el-radio-group>
                        </el-sub-menu>
                        <el-sub-menu index="status">
                            <template #title>
                                <el-icon class="icon-container"><Open /></el-icon>
                                <p class="item-font">项目状态</p>                                
                            </template>
                            <el-radio-group v-model="statusRadio" class="radio-container">
                                <div class="radio-item-container">
                                    <el-radio :label="1" class="radio-spacer">招募中</el-radio>
                                </div>
                                <div class="radio-item-container">
                                    <el-radio :label="2" class="radio-spacer">运行中</el-radio>
                                </div>
                                <div class="radio-item-container">
                                    <el-radio :label="3" class="radio-spacer">已结项</el-radio>
                                </div>
                                <div class="radio-item-container">
                                    <el-button size="small" @click="clearStatusRadio()">撤销</el-button>
                                </div>
                            </el-radio-group>
                        </el-sub-menu>
                        <el-sub-menu index="people">
                            <template #title>
                                <el-icon class="icon-container"><User /></el-icon>
                                <p class="item-font">招募人群</p> 
                            </template>
                            <el-radio-group v-model="authRadio" class="radio-container">
                                <div class="radio-item-container">
                                    <el-radio :label="1" class="radio-spacer">面向公共招募</el-radio>
                                </div>
                                <div class="radio-item-container">
                                    <el-radio :label="2" class="radio-spacer">仅团队内招募</el-radio>
                                </div>
                                <div class="radio-item-container">
                                    <el-button size="small" @click="clearAuthRadio()">撤销</el-button>
                                </div>
                            </el-radio-group>  
                        </el-sub-menu>
                    </el-menu>
                </div>
                <div class="search-container">
                    <div class="search-item-container">
                        <el-date-picker v-model="date" placeholder="请选择项目开始日期" size="large"></el-date-picker>
                    </div>
                    <div class="search-item-container">
                        <el-input v-model="keyword" placeholder="请输入项目名称" clearable size="large"></el-input>
                    </div>
                    <el-button size="large" type="primary"><span style="font-weight: bold; font-size: 15px;">搜 索</span></el-button>
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
                                <div class="info-item">剩余招募人数：{{ item.remainingNumber }} 人</div>
                                <div class="info-item">距离招募截止：{{ item.remainingDays }} 天</div>
                            </div>
                          </el-card>
                    </div>
                </div>
                <div class="pagination-container">
                    <el-pagination 
                        @current-change="handlePageChange"
                        :page-size="9"
                        :total="totalList.length"
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

<!-- <style>
    .container {
      display: flex;
      flex-direction: column;
      height: 100vh; /* 设置容器高度为视口高度 */
    }
  
    .top {
      flex: 1; /* 上半层占据剩余空间 */
      display: flex;
    }
  
    .image {
      flex: 1; /* 左半边占据一半空间 */
    }
  
    .info {
      flex: 1; /* 右半边占据一半空间 */
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
  
    .info-item {
      margin-bottom: 10px; /* 调整每个信息文字之间的间距 */
    }
  
    .bottom {
      flex: 1; /* 下半层占据剩余空间 */
      display: flex;
      justify-content: center;
      align-items: center;
    }
  </style> -->
  
  <!-- <div class="container">
    <div class="top">
      <div class="image">

      </div>
      <div class="info">
        <div class="info-item">

        </div>
        <div class="info-item">

        </div>
        <div class="info-item">

        </div>
      </div>
    </div>
    <div class="bottom">

    </div>
  </div> -->


<script>

export default {
    data() {
        return {
            typeRadio: null,
            authRadio: null,
            statusRadio: null,
            date: null,
            keyword: null,
            currentPage: 1,
            selectedTotalIndex: null,
            totalList: [
                {name: "志愿项目1", hours: 1, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目2", hours: 2, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目3", hours: 3, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目4", hours: 4, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目5", hours: 5, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目6", hours: 6, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目7", hours: 7, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目8", hours: 8, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目9", hours: 9, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目10", hours: 10, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目11", hours: 11, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目12", hours: 12, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目13", hours: 13, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目14", hours: 14, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
                {name: "志愿项目15", hours: 15, number: 0, remainingNumber: 0, remainingDays: 0, time: "2023-10-9", location: "田径场", type: "社区服务", state: "正在招募", intro: "这是一段介绍"},
            ],
            recruitmentTableVisible: false
        };
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 9;
            return this.totalList.slice(startIndex, startIndex + 9);
        }
    },
    methods: {
        clearTypeRadio() {
            this.typeRadio = null;
        },
        clearAuthRadio() {
            this.authRadio = null;
        },
        clearStatusRadio() {
            this.statusRadio = null;
        },
        handlePageChange(currentPage) {
            this.currentPage = currentPage;
        },
        changeToMyProjectPage() {
            this.$router.push({
            path: '/project/myproject'
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
    height: 1200px;
    flex-direction: column;
    padding-top: 20px;
    margin-left: 20px;
    border-right: 2px solid black;
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
    margin-top: 15px;
}

.menu-container {
    width: 590px;
}

.search-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 160px;
    margin-right: 100px;
}

.search-item-container {
    margin-left: 10px;
    margin-right: 15px;
}

.radio-container {
    display: flex;
    flex-direction: column;
    width: 130px;
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
    margin-top: 40px;
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
    justify-content: center;
}

.info-item {
    margin-top: 10px;
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

</style>