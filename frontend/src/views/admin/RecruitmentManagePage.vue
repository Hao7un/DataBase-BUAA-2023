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
            <v-btn class="back-button" @click="handleBack">
                <template v-slot:prepend>
                    <el-icon>
                        <Back />
                    </el-icon>
                </template>
                返回
            </v-btn>
            <div class="selector-container">
                <div class="left">
                    <el-input v-model="locationKey" clearable placeholder="输入活动地点" size="large" style="width: 250px;">
                        <template #prefix>
                            <el-icon>
                                <Location />
                            </el-icon>
                        </template>
                    </el-input>
                </div>
                <div class="middle1">
                    <el-select v-model="statusKey" clearable placeholder="选择招募状态" size="large" style="width: 250px;">
                        <template #prefix>
                            <el-icon>
                                <Clock />
                            </el-icon>
                        </template>
                        <el-option label="即将招募" key="即将招募" value="即将招募"></el-option>
                        <el-option label="招募中" key="招募中" value="招募中"></el-option>
                        <el-option label="招募结束" key="招募结束" value="招募结束"></el-option>
                    </el-select>
                </div>
                <div class="middle2">
                    <el-select v-model="typeKey" clearable placeholder="选择面向人群" size="large">
                        <template #prefix>
                            <el-icon>
                                <Unlock />
                            </el-icon>
                        </template>
                        <el-option label="面向公共招募" key="面向公共招募" value="面向公共招募"></el-option>
                        <el-option label="仅限团队内部" key="仅限团队内部" value="仅限团队内部"></el-option>
                    </el-select>
                </div>
                <div class="right">
                    <el-select v-model="sortKey" clearable placeholder="选择排序方式" size="large">
                        <template #prefix>
                            <el-icon>
                                <Sort />
                            </el-icon>
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
                    <v-btn size="large" @click="createRecruitmentVisible = true">发布招募</v-btn>
                </div>
                <div class="recruitments-list-container">
                    <v-expansion-panels v-model="panel" multiple>
                        <v-expansion-panel v-for="(card, index) in displayedList" class="panel">
                            <v-expansion-panel-title @click="card.showDetails = !card.showDetails" style="height: 70px;">
                                <div style="display: flex; justify-content: space-between; width: 99%;">
                                    <div>招募编号: &nbsp;{{ card.id }}</div>
                                    <div><el-icon>
                                            <Clock />
                                        </el-icon>&nbsp;招募状态: &nbsp;{{ card.state }}</div>
                                    <div v-if="card.type === '1'"><el-icon>
                                            <Unlock />
                                        </el-icon>&nbsp;面向群体: &nbsp;面向公共招募</div>
                                    <div v-else="card.type === '2'"><el-icon>
                                            <Unlock />
                                        </el-icon>&nbsp;面向群体: &nbsp;仅限团队内部</div>
                                    <div><el-icon>
                                            <Calendar />
                                        </el-icon>&nbsp;发布时间: &nbsp;{{ card.startTime }}</div>
                                </div>
                                <span v-if="!card.showDetails" style="margin-left: 20px;"><el-icon>
                                        <ArrowDownBold />
                                    </el-icon></span>
                                <span v-else style="margin-left: 20px;"><el-icon>
                                        <ArrowUpBold />
                                    </el-icon></span>
                            </v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div style="display: flex; justify-content: center; flex-direction: column">
                                    <el-descriptions :column="6" :row="3" border>
                                        <el-descriptions-item :span="2" label-align="center" align="center">
                                            <template #label>
                                                <el-icon>
                                                    <Clock />
                                                </el-icon>
                                                &nbsp;
                                                招募状态:
                                            </template>
                                            <span v-if="card.state === '招募结束'" style="color: red;">{{ card.state }}</span>
                                            <span v-else-if="card.state === '招募中'" style="color: orange;">{{ card.state
                                            }}</span>
                                            <span v-else style="color: green;">{{ card.state }}</span>
                                        </el-descriptions-item>
                                        <el-descriptions-item :span="1" label-align="center" align="center">
                                            <template #label>
                                                <el-icon>
                                                    <Coin />
                                                </el-icon>
                                                &nbsp;
                                                志愿时长:
                                            </template>
                                            {{ card.hours }} 小时
                                        </el-descriptions-item>
                                        <el-descriptions-item :span="2" label-align="center" align="center">
                                            <template #label>
                                                <el-icon>
                                                    <Location />
                                                </el-icon>
                                                &nbsp;
                                                活动地点:
                                            </template>
                                            {{ card.location }}
                                        </el-descriptions-item>
                                        <el-descriptions-item :span="1" label-align="center" align="center">
                                            <template #label>
                                                <el-icon>
                                                    <User />
                                                </el-icon>
                                                &nbsp;
                                                招募人数:
                                            </template>
                                            {{ card.number }} / {{ card.maxNumber }}
                                        </el-descriptions-item>
                                        <el-descriptions-item :span="3" label-align="center" align="center">
                                            <template #label>
                                                <el-icon>
                                                    <Calendar />
                                                </el-icon>
                                                &nbsp;
                                                招募发布时间:
                                            </template>
                                            {{ card.launchTime }}
                                        </el-descriptions-item>
                                        <el-descriptions-item :span="3" label-align="center" align="center">
                                            <template #label>
                                                <el-icon>
                                                    <Calendar />
                                                </el-icon>
                                                &nbsp;
                                                招募结束时间:
                                            </template>
                                            {{ card.deadline }}
                                        </el-descriptions-item>
                                        <el-descriptions-item :span="3" label-align="center" align="center">
                                            <template #label>
                                                <el-icon>
                                                    <Calendar />
                                                </el-icon>
                                                &nbsp;
                                                活动开始时间:
                                            </template>
                                            {{ card.startTime }}
                                        </el-descriptions-item>
                                        <el-descriptions-item :span="3" label-align="center" align="center">
                                            <template #label>
                                                <el-icon>
                                                    <Calendar />
                                                </el-icon>
                                                &nbsp;
                                                活动结束时间:
                                            </template>
                                            {{ card.endTime }}
                                        </el-descriptions-item>
                                    </el-descriptions>
                                    <el-button size="large" @click="viewRecruits(card)"
                                        style="margin-top: 5px;">查看应募人员</el-button>
                                </div>
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                    </v-expansion-panels>
                </div>
            </div>
        </div>
    </div>
    <v-dialog v-model="viewRecruitsVisible">
        <div style="width: 800px; height: 600px; background: white; position: relative; padding: 10px; margin-left: 500px;">
            <h3 style="text-align: center; margin-top: 35px">应募人员</h3>
            <el-button style="position: absolute; top: 10px; right: 10px"
                @click="viewRecruitsVisible = false">退出</el-button>
            <div style="margin-top: 20px; text-align: center;">
                <el-table :data="this.displayedRecruits" border max-height="500">
                    <template #empty>
                        无匹配信息
                    </template>
                    <el-table-column prop="collegeId" label="学工号" align="center" width="120px">
                        <template #header>
                            <div>学工号</div>
                            <el-input v-model="collegeIdKey" clearable placeholder="输入学工号"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="name" label="姓名" align="center" width="120px">
                        <template #header>
                            <div>姓名</div>
                            <el-input v-model="nameKey" clearable placeholder="输入姓名"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="telephone" label="电话" align="center" width="170px">
                        <template #header>
                            <div>电话</div>
                            <el-input v-model="telephoneKey" clearable placeholder="输入电话"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="email" label="邮箱" align="center">
                        <template #header>
                            <div>邮箱</div>
                            <el-input v-model="emailKey" clearable placeholder="输入邮箱"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="time" label="应募时间" align="center" sortable></el-table-column>
                </el-table>
            </div>
        </div>
    </v-dialog>
    <el-dialog v-model="createRecruitmentVisible" width="600px" style="z-index: 6;">
        <div class="create-recruitment-dialog-container">
            <div class="create-item">
                <h3 style="margin-bottom: 10px;">活动地点</h3>
                <el-input v-model="location" clearable style="width: 250px;">
                    <template #prefix>
                        <el-icon>
                            <Location />
                        </el-icon>
                    </template>
                </el-input>
            </div>
            <div class="create-item">
                <h3 style="margin-bottom: 10px;">活动开始时间</h3>
                <el-date-picker v-model="startTime" type="datetime" format="YYYY-MM-DD HH:mm"
                    value-format="YYYY-MM-DD HH:mm" :disabled-date="disabledDates" @focus="this.focus"
                    @confirm="handleDateConfirm"></el-date-picker>
            </div>
            <div class="create-item">
                <h3 style="margin-bottom: 10px;">活动结束时间</h3>
                <el-date-picker v-model="endTime" type="datetime" format="YYYY-MM-DD HH:mm" value-format="YYYY-MM-DD HH:mm"
                    :disabled-date="disabledDates" @focus="this.focus"></el-date-picker>
            </div>
            <div class="create-item">
                <h3 style="margin-bottom: 10px;">招募结束时间</h3>
                <el-date-picker v-model="deadline" type="datetime" format="YYYY-MM-DD HH:mm" value-format="YYYY-MM-DD HH:mm"
                    :disabled-date="disabledDates" @focus="this.focus"></el-date-picker>
            </div>
            <div class="create-item">
                <h3 style="margin-bottom: 10px;">面向群体</h3>
                <el-radio-group v-model="type">
                    <el-radio label="1" border size="middle">面向公共招募</el-radio>
                    <el-radio label="2" border size="middle">仅限团队内部</el-radio>
                </el-radio-group>
            </div>
            <div class="create-item">
                <h3 style="margin-bottom: 10px;">招募人数上限</h3>
                <el-input-number v-model="maxNumber" size="small" :min="1"></el-input-number>
            </div>
            <div class="create-item">
                <h3 style="margin-bottom: 10px;">志愿时长</h3>
                <el-input-number v-model="hours" size="small" :min="1"></el-input-number>
            </div>
            <div style="margin-left: 240px; margin-top: 30px; margin-bottom: 20px;">
                <el-button size="large" @click="handleCreateRecruitmentSubmit">提交</el-button>
            </div>
        </div>
    </el-dialog>
</template>


<script>
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
    created() {
        this.fetch();
    },
    computed: {
        recruitmentList() {
            let recruitmentList = [];
            for (let i = 0; i < this.recruitments.length; i++) {
                let item = this.recruitments[i];
                let element = {
                    state: "",
                    id: item.id,
                    showDetails: false,
                    launchTime: item.launchTime,
                    deadline: item.deadline,
                    startTime: item.startTime,
                    endTime: item.endTime,
                    location: item.location,
                    type: item.type,
                    hours: item.hours,
                    number: item.number,
                    maxNumber: item.maxNumber,
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
                    return new Date(b.launchTime) - new Date(a.launchTime);
                })
            }
            else if (this.sortKey === "按招募结束时间排序") {
                displayedRecruitments = displayedRecruitments.sort((a, b) => {
                    return new Date(b.deadline) - new Date(a.deadline);
                })
            }
            else if (this.sortKey === "按活动开始时间排序") {
                displayedRecruitments = displayedRecruitments.sort((a, b) => {
                    return new Date(b.startTime) - new Date(a.startTime);
                })
            }
            else if (this.sortKey === "按活动结束时间排序") {
                displayedRecruitments = displayedRecruitments.sort((a, b) => {
                    return new Date(b.endTime) - new Date(a.endTime);
                })
            }
            else if (this.sortKey === "按志愿时长降序排序") {
                displayedRecruitments = displayedRecruitments.sort((a, b) => {
                    return b.hours - a.hours;
                })
            }
            return displayedRecruitments;
        },
        displayedRecruits() {
            let displayedRecruits = this.recruits;
            displayedRecruits = displayedRecruits.filter(item => {
                return item.collegeId.includes(this.collegeIdKey) && item.name.includes(this.nameKey) && item.telephone.includes(this.telephoneKey) && item.email.includes(this.emailKey);
            })
            return displayedRecruits;
        }
    },
    data() {
        return {
            projectId: this.$route.query.projectId,
            projectName: this.$route.query.projectName,
            teamId: this.$route.query.teamId,
            locationKey: "",
            statusKey: "",
            typeKey: "",
            sortKey: "",
            collegeIdKey: "",
            nameKey: "",
            telephoneKey: "",
            emailKey: "",
            panel: [],
            viewRecruitsVisible: false,
            createRecruitmentVisible: false,
            // 发布招募
            startTime: "",
            deadline: "",
            endTime: "",
            location: "",
            type: "",
            hours: "",
            maxNumber: 0,
            recruitments: [
                // {
                //     id: "1",
                //     launchTime: "2023-11-24 12:22",
                //     deadline: "2023-11-24 13:00",
                //     startTime: "2023-11-25 16:08",
                //     endTime: "2023-11-25 17:00",
                //     location: "校医院",
                //     type: "面向公共招募",
                //     hours: 16,
                //     number: 5,
                //     maxNumber: 10,
                // },
                // {
                //     id: "2",
                //     launchTime: "2023-11-23 12:23",
                //     deadline: "2023-11-28 14:00",
                //     startTime: "2023-11-24 16:09",
                //     endTime: "2023-11-24 18:00",
                //     location: "田径场",
                //     type: "面向公共招募",
                //     hours: 4,
                //     number: 6,
                //     maxNumber: 20,
                // },
                // {
                //     id: "3",
                //     launchTime: "2023-11-29 12:24",
                //     deadline: "2023-11-23 15:00",
                //     startTime: "2023-11-24 16:10",
                //     endTime: "2023-11-24 17:30",
                //     location: "晨兴音乐厅",
                //     type: "仅限团队内部",
                //     hours: 8,
                //     number: 10,
                //     maxNumber: 100,
                // }
            ],
            recruits: [
                // {
                //     collegeId: "1",
                //     name: "Kevin",
                //     telephone: "13700000000",
                //     email: "123@abc.com",
                //     time: "2023-12-04 23:02",
                // },
                // {
                //     collegeId: "2",
                //     name: "Bob",
                //     telephone: "13700000001",
                //     email: "456@abc.com",
                //     time: "2023-12-04 23:03"
                // },
                // {
                //     collegeId: "3",
                //     name: "Stuart",
                //     telephone: "13700000002",
                //     email: "789@abc.com",
                //     time: "2023-12-05 11:31"
                // }
            ]
        }
    },
    methods: {
        fetch() {
            const submitParams = {
                projectId: this.projectId,
            }

            this.axios({
                method: 'post',
                url: 'http://localhost:8000/admin_get_project_recruitments',
                data: submitParams,
            })
                .then((res) => {
                    console.log(res);
                    if (res.data.code === 0) {
                        console.log("获取项目下的招募列表成功");
                        this.recruitments = res.data.recruitments;
                    }
                    else {
                        console.log("获取失败, 错误码不是0");
                    }
                })
        },
        viewRecruits(recruitment) {
            const submitParams = {
                recruitmentId: recruitment.id
            }

            console.log(recruitment.id);

            this.axios({
                method: 'post',
                url: 'http://localhost:8000/admin_get_recruitment_applicants',
                data: submitParams,
            })
                .then((res) => {
                    console.log(res);
                    if (res.data.code === 0) {
                        console.log("获取应募人员列表成功");
                        this.recruits = res.data.recruits;
                    }
                    else {
                        console.log("获取失败, 错误码不是0");
                    }

                })
            // visible
            this.viewRecruitsVisible = true;
        },
        showRecruitmentDetails(index) {
            console.log(this.displayedList[index].showDetails);
            this.displayedList[index].showDetails = !this.displayedList[index].showDetails;
        },
        changeToProjectManagePage() {
            this.$router.push({
                path: '/admin/project-info',
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
                    projectName: this.projectName,
                    teamId: this.teamId,
                }
            })
        },
        handleBack() {
            this.$router.push({
                path: '/admin/team-info',
                query: {
                    teamId: this.teamId,
                },
            })
        },
        handleCreateRecruitmentSubmit() {
            console.log(typeof (this.type));
            if (this.startTime === "" || this.location === "" || this.type === "" || this.deadline === "" || this.endTime === "") {
                this.createRecruitmentVisible = false;
                ElMessageBox.alert("请填写完整的招募信息", "注意", {
                    confirmButtonText: 'OK',
                    type: 'warning'
                }).then(() => {
                    this.createRecruitmentVisible = true;
                })
            }
            else if (this.maxNumber === null) {
                this.createRecruitmentVisible = false;
                ElMessageBox.alert("招募人数上限不能为空", "注意", {
                    confirmButtonText: 'OK',
                    type: 'warning'
                }).then(() => {
                    this.createRecruitmentVisible = true;
                })
            }
            else if (this.hours === null) {
                this.createRecruitmentVisible = false;
                ElMessageBox.alert("志愿时长不能为空", "注意", {
                    confirmButtonText: 'OK',
                    type: 'warning'
                }).then(() => {
                    this.createRecruitmentVisible = true;
                })
            }
            else {
                const submitParams = {
                    projectId: this.projectId,
                    startTime: this.startTime,
                    deadline: this.deadline,
                    endTime: this.endTime,
                    location: this.location,
                    type: this.type,
                    hours: this.hours,
                    maxNumber: this.maxNumber,
                    message: {
                        title: "您收藏的项目发布了新的招募",
                        content: "您关注的 " + this.projectName + " 项目发布了新的招募, 招募开始时间为 " + this.startTime,
                    }
                };

                this.axios({
                    method: 'post',
                    url: 'http://localhost:8000/admin_create_recruitment',
                    data: submitParams,
                })
                    .then((res) => {
                        console.log(res);
                        if (res.data.code === 0) {
                            console.log("发布招募成功");
                            // 刷新招募列表
                            this.fetch();
                            this.createRecruitmentVisible = false;
                            ElMessage.success("创建成功")
                        }
                        else {
                            console.log("发布招募失败, 错误码不是0");
                        }
                    })
            }

        },
        focus() {
            this.$nextTick(() => {
                document.getElementsByClassName('el-picker-panel__link-btn')[0].setAttribute('style', 'display:none');
            })
        },
        disabledDates(date) {
            return date.getTime() < Date.now()
        },
        handleDateConfirm() {
            this.$nextTick(() => {
                this.dialogVisible = true;
            });
        }
    },
}
</script>


<style scoped>
.main-container {
    display: flex;
}

.back-button {
    margin-left: 25px;
    margin-top: 25px;
    font-weight: bold;
    font-size: 15px;
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

.selector-container {
    width: 1200px;
    margin-top: 10px;
    margin-left: 100px;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.recruitments-list-container {
    margin-left: 200px;
    margin-bottom: 50px;
    width: 1000px;
}

.panel {
    margin-top: 30px;
}

.create-recruitment-dialog-container {
    display: flex;
    height: auto;
    width: 550px;
    background-color: white;
    flex-direction: column;
}

.create-item {
    margin-top: 28px;
    margin-left: 50px;
    width: 99%;
}
</style>