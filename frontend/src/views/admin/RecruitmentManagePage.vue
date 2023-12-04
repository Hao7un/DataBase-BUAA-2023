<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="list" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="info" @click="changeToProjectManagePage">
                    <span class="item-font" style="font-weight: bold;">项目详情</span>
                </el-menu-item>
                <el-menu-item index="list" @click="changeToRecruitmentManangePage">
                    <span class="item-font" style="font-weight: bold;">招募管理</span>
                </el-menu-item>
            </el-menu>
        </div>  
        <div class="content-container">
            <div class="selector-container">
                <div class="left">
                    <el-input v-model="locationKey" clearable placeholder="输入活动地点" size="large">
                        <template #prefix>
                            <el-icon><Location /></el-icon>
                        </template>
                    </el-input>
                </div>
                <div class="middle1">
                    <el-select v-model="statusKey" clearable placeholder="选择招募状态" size="large">
                        <template #prefix>
                            <el-icon><Clock /></el-icon>
                        </template>
                        <el-option label="即将招募" key="即将招募" value="即将招募"></el-option>
                        <el-option label="招募中" key="招募中" value="招募中"></el-option>
                        <el-option label="招募结束" key="招募结束" value="招募结束"></el-option>
                    </el-select>
                </div>
                <div class="middle2">
                    <el-select v-model="typeKey" clearable placeholder="选择面向人群" size="large">
                        <template #prefix>
                            <el-icon><Unlock /></el-icon>
                        </template>
                        <el-option label="面向公共招募" key="面向公共招募" value="面向公共招募"></el-option>
                        <el-option label="仅限团队内部" key="仅限团队内部" value="仅限团队内部"></el-option>
                    </el-select>
                </div>
                <div class="right">
                    <el-select v-model="sortKey" clearable placeholder="选择排序方式" size="large">
                        <template #prefix>
                            <el-icon><Sort /></el-icon>
                        </template>
                        <el-option label="按招募发布时间排序" key="按招募发布时间排序" value="按招募发布时间排序"></el-option>
                        <el-option label="按招募结束时间排序" key="按招募结束时间排序" value="按招募结束时间排序"></el-option>
                        <el-option label="按活动开始时间排序" key="按活动开始时间排序" value="按活动开始时间排序"></el-option>
                        <el-option label="按活动结束时间排序" key="按活动结束时间排序" value="按活动结束时间排序"></el-option>
                        <el-option label="按志愿时长降序排序" key="按志愿时长降序排序" value="按志愿时长降序排序"></el-option>
                    </el-select>
                </div>
            </div>
            <el-divider style="margin-left: 50px;"></el-divider>
            <div class="recruitments-container">
                <div style="display: flex; justify-content: center; margin-left: 50px">
                    <v-btn size="large" @click="createRecruitmentDialogVisible">发布招募</v-btn>
                </div>
                <div class="recruitments-list-container">
                    <v-card v-for="(card, index) in displayedList" class="card">
                        <v-card-title>
                            {{ card.state }}
                        </v-card-title>

                        <v-btn @click="showRecruitmentDetails(index)">
                            {{ card.showDetails ? "展开详情" : "收起详情"}}
                        </v-btn>

                        <v-expand-transition>
                            <div v-show="card.showDetails">
                                99999
                            </div>
                        </v-expand-transition>
                    </v-card>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
    computed: {
        recruitmentList() {
            let recruitmentList = [];
            for (let i = 0; i < this.recruitements.length; i++) {
                let item = this.recruitements[i];
                let element = {
                    state: "",
                    showDetails: false,
                    launchTime: item.launchTime,
                    deadline: item.deadline,
                    startTime: item.startTime,
                    endTime: item.endTime,
                    location: item.location,
                    type: item.type,
                    hours: item.hours,
                    number: item.number,
                }
                if (Date.now() < new Date(item.launchTime)) {
                    element.state = "即将招募";
                }
                else if (Date.now() < new Date(item.deadline)) {
                    element.state = "招募中";
                }
                else {
                    element.state = "招募结束";
                }
                recruitmentList.push(element);
            }
            return recruitmentList;
        },
        displayedList() {
            let displayedRecruitments = this.recruitmentList;
            if (this.typeKey != null && this.locationKey != null && this.statusKey != null) {
                displayedRecruitments = displayedRecruitments.filter(item => {
                    return item.state.includes(this.statusKey) && item.type.includes(this.typeKey) && item.location.includes(this.locationKey);
                })
            }
            if (this.sortKey === "按招募发布时间排序" || this.sortKey === "") {
                displayedRecruitments = displayedRecruitments.sort((a, b) => {
                    return new Date(a.launchTime) - new Date(b.launchTime);
                })
            }
            else if (this.sortKey === "按招募结束时间排序") {
                displayedRecruitments = displayedRecruitments.sort((a, b) => {
                    return new Date(a.deadline) - new Date(b.deadline);
                })
            }
            else if (this.sortKey === "按活动开始时间排序") {
                displayedRecruitments = displayedRecruitments.sort((a, b) => {
                    return new Date(a.startTime) - new Date(b.startTime);
                })
            }
            else if (this.sortKey === "按活动结束时间排序") {
                displayedRecruitments = displayedRecruitments.sort((a, b) => {
                    return new Date(a.endTime) - new Date(b.endTime);
                })
            }
            else if (this.sortKey === "按志愿时长降序排序") {
                displayedRecruitments = displayedRecruitments.sort((a, b) => {
                    return new Date(a.hours) - new Date(b.hours);
                })
            }
            return displayedRecruitments;
        },
    },
    data() {
        return {
            projectId: this.$route.query.projectId,
            teamId: this.$route.query.teamId,
            locationKey: "",
            statusKey: "",
            typeKey: "",
            sortKey: "",
            recruitements: [
                {
                    launchTime: "2023-11-24 12:22",
                    deadline: "2023-11-24 13:00",
                    startTime: "2023-11-25 16:08",
                    endTime: "2023-11-25 17:00",
                    location: "校医院",
                    type: "面向公共招募",
                    hours: 16,
                    number: 10,
                },
                {
                    launchTime: "2023-11-23 12:23",
                    deadline: "2023-11-28 14:00",
                    startTime: "2023-11-24 16:09",
                    endTime: "2023-11-24 18:00",
                    location: "田径场",
                    type: "面向公共招募",
                    hours: 4,
                    number: 20,
                },
                {
                    launchTime: "2023-11-29 12:24",
                    deadline: "2023-11-23 15:00",
                    startTime: "2023-11-24 16:10",
                    endTime: "2023-11-24 17:30",
                    location: "晨兴音乐厅",
                    type: "仅限团队内部",
                    hours: 8,
                    number: 100,
                },
            ],
        }
    },
    methods: {
        showRecruitmentDetails(index) {
            console.log(this.displayedList[index].showDetails);
            this.displayedList[index].showDetails = !this.displayedList[index].showDetails;
        },
        changeToProjectManagePage() {
            this.$router.push({
                path: '/admin/projectinfo',
                query: {
                    projectId: this.projectId,
                    teamId: this.teamId,
                }
            })
        },
        changeToRecruitmentManangePage() {
            this.$router.push({
                path: '/admin/recruitment',
                query: {
                    projectId: this.projectId,
                    teamId: this.teamId,
                }
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

.selector-container {
    width: 1200px;
    margin-top: 40px;
    margin-left: 100px;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.recruitments-list-container {
    margin-left: 230px;
    margin-bottom: 50px;
    width: 70%;   
}

.card {
    margin-top: 15px;
}


</style>