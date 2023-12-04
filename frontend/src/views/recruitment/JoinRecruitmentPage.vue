<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="join" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="join" @click="changeToJoinRecruitmentPage">
                    <span class="item-font" style="font-weight: bold;">参与招募</span>
                </el-menu-item>
                <el-menu-item index="my" @click="changeToMyRecruitmentPage">
                    <span class="item-font" style="font-weight: bold;">我的活动</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content-container">
            <div class="table-container">
                <h2 class="title">招募列表</h2>
                <div class="recruitments-container">
                    <table class="table-style" border>
                        <thead>
                            <tr>
                                <th style="background-color: #e8e8e4">所属项目</th>
                                <th style="background-color: #e8e8e4">项目类别</th>
                                <th style="background-color: #e8e8e4">活动时间</th>
                                <th style="background-color: #e8e8e4">活动地点</th>
                                <th style="background-color: #e8e8e4">面向群体</th>
                                <th style="background-color: #e8e8e4">志愿时长</th>
                                <th style="background-color: #e8e8e4">招募时间</th>
                                <th style="background-color: #e8e8e4">招募人数</th>
                                <th style="background-color: #e8e8e4">状态</th>
                            </tr>
                            <tr>
                                <th style="width: 250px;">
                                    <el-input v-model="keyword" placeholder="输入项目名称" clearable></el-input>
                                </th>
                                <th style="width: 130px;">
                                    <el-select v-model="typeP" placeholder="选择项目类别" clearable>
                                        <el-option key="1" value="社区服务">社区服务</el-option>
                                        <el-option key="2" value="科技科普">科技科普</el-option>
                                        <el-option key="3" value="支教助学">支教助学</el-option>
                                        <el-option key="4" value="体育赛事">体育赛事</el-option>
                                        <el-option key="5" value="大型演出">大型演出</el-option>
                                        <el-option key="6" value="其它">其它</el-option>
                                    </el-select>
                                </th>
                                <th style="width: 160px;">
                                    <el-date-picker v-model="date" type="date" placeholder="选择活动日期"
                                        clearable></el-date-picker>
                                </th>
                                <th style="width: 140px;">
                                    <el-input v-model="place" placeholder="输入活动地点" clearable></el-input>
                                </th>
                                <th style="width: 130px;">
                                    <el-select v-model="typeR" placeholder="选择面向群体" clearable>
                                        <el-option key="1" value="面向公共招募">面向公共招募</el-option>
                                        <el-option key="2" value="仅限团队内部">仅限团队内部</el-option>
                                    </el-select>
                                </th>
                                <th style="width: 100px;">
                                </th>
                                <th style="width: 160px;">
                                </th>
                                <th style="width: 100px;">
                                    <el-button type="success" @click="refresh(true)">
                                        <span style="font-weight: bold; font-size: 14px; color:whitesmoke">刷新</span>
                                    </el-button>
                                </th>
                                <th style="width: 130px;">
                                    <el-select v-model="status" placeholder="选择招募状态" clearable>
                                        <el-option key="1" value="可报名">可报名</el-option>
                                        <el-option key="2" value="未开始">未开始</el-option>
                                        <el-option key="3" value="已截止">已截止</el-option>
                                    </el-select>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in displayedList">
                                <td style="text-align:center">
                                    <el-button text><strong style="color: #110f0f; font-size: 17px;"
                                            @click="changeToProjectInfoPage(item.projectId)">{{ item.projectName }}
                                        </strong></el-button>
                                </td>
                                <td style="text-align:center">{{ showProjectType(item.projectType) }}</td>
                                <td style="text-align:center">开始<br>{{ item.startTime }}<br>结束<br>{{ item.endTime }}</td>
                                <td style="text-align:center">{{ item.location }}</td>
                                <td style="text-align:center">
                                    <div :class="item.type === '1' ? 'public-type' : 'private-type'">
                                        {{ showRecruitmentType(item.type) }}</div>
                                </td>
                                <td style="text-align:center">{{ item.volunteerHour }} 小时</td>
                                <td style="text-align:center;">开始<br>{{ item.launchTime }}<br>结束<br>{{ item.dueTime }}</td>
                                <td style="text-align:center;"
                                    :class="item.currentNumber >= item.maxNumber ? 'red-number' : 'green-number'">
                                    {{ item.currentNumber }} / {{ item.maxNumber }}
                                </td>
                                <td style="text-align:center">
                                    <el-button :class="showRecruitmentStatus(item.id)" size="large"
                                        :disabled="shouldDisableButton(item.id)"
                                        style="font-weight: bold; font-size: 14px; color:whitesmoke"
                                        @click="openDialog(item.id)">
                                        {{ showRecruitmentStatus(item.id) }}
                                    </el-button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="pagination-container">
                    <el-pagination @current-change="handlePageChange" :page-size="10" :total="filteredList.length"
                        layout="prev, pager, next">
                    </el-pagination>
                </div>
            </div>
        </div>
        <el-dialog v-model="dialogVisible" title="注意" width="30%" align-center center draggable>
            <span class="text-font">请确认此次志愿活动的时间与地点，报名后无法退出。</span>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="attendRecruitment">
                        <span style="color:whitesmoke">确认</span>
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus';

export default {
    created() {
        this.axios.post('http://localhost:8000/user_get_recruitment_list', {
            userId: this.userId
        })
            .then(res => {
                console.log(res);
                if (res.data.code === 0) {
                    this.recruitmentList = res.data.recruitmentList;
                }
            });
    },
    data() {
        return {
            currentPage: 1,
            keyword: "",
            place: "",
            date: null,
            typeP: "",
            typeR: "",
            status: "",
            recruitmentList: [
                { id: "5", launchTime: "2023-12-08 21:00", dueTime: "2023-12-09 21:00", startTime: "2023-12-26 19:00", endTime: "2023-12-26 21:00", location: "操场", volunteerHour: "5", isAttend: false, type: "1", maxNumber: "50", currentNumber: "30", projectId: "5", projectName: "志愿项目5", projectType: "1" },
                { id: "4", launchTime: "2023-12-01 21:00", dueTime: "2023-12-10 21:00", startTime: "2023-12-11 19:00", endTime: "2023-12-11 21:00", location: "新主楼G1000", volunteerHour: "5", isAttend: false, type: "1", maxNumber: "50", currentNumber: "30", projectId: "4", projectName: "志愿项目4", projectType: "2" },
                { id: "3", launchTime: "2023-12-01 12:00", dueTime: "2023-12-12 21:00", startTime: "2023-12-25 19:00", endTime: "2023-12-25 21:00", location: "操场", volunteerHour: "5", isAttend: true, type: "2", maxNumber: "50", currentNumber: "30", projectId: "3", projectName: "志愿项目3", projectType: "3" },
                { id: "2", launchTime: "2023-12-01 10:00", dueTime: "2023-12-02 11:00", startTime: "2023-12-02 19:00", endTime: "2023-12-02 21:00", location: "操场", volunteerHour: "5", isAttend: false, type: "2", maxNumber: "50", currentNumber: "50", projectId: "2", projectName: "志愿项目2", projectType: "4" },
                { id: "1", launchTime: "2023-11-01 21:00", dueTime: "2023-11-02 21:00", startTime: "2023-12-01 19:00", endTime: "2023-12-01 21:00", location: "操场", volunteerHour: "5", isAttend: false, type: "1", maxNumber: "50", currentNumber: "30", projectId: "1", projectName: "志愿项目1", projectType: "5" },
            ],
            dialogVisible: false,
            attendId: ""
        };
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 10;
            let endIndex = startIndex + 10;
            let filteredList = this.recruitmentList;
            if (this.keyword != null && this.place != null && this.typeP != null && this.typeR != null && this.status != null) {
                filteredList = filteredList.filter(item => {
                    let itemTypeP = this.showProjectType(item.projectType);
                    let itemTypeR = this.showRecruitmentType(item.type);
                    return item.projectName.includes(this.keyword) && item.location.includes(this.place) && itemTypeP.includes(this.typeP)
                        && itemTypeR.includes(this.typeR) && this.showRecruitmentStatus(item.id).includes(this.status) 
                        && item.startTime.includes(this.formatDateString);
                });
            }
            return filteredList.slice(startIndex, endIndex);
        },
        filteredList() {
            let list = this.recruitmentList;
            if (this.keyword != null && this.place != null && this.typeP != null && this.typeR != null && this.status != null) {
                list = list.filter(item => {
                    let itemTypeP = this.showProjectType(item.projectType);
                    let itemTypeR = this.showRecruitmentType(item.type);
                    return item.projectName.includes(this.keyword) && item.location.includes(this.place) && itemTypeP.includes(this.typeP)
                        && itemTypeR.includes(this.typeR) && this.showRecruitmentStatus(item.id).includes(this.status) 
                        && item.startTime.includes(this.formatDateString);
                });
            }
            return list;
        },
        formatDateString() {
            if (this.date == null)
                return "";
            return this.formatDate(this.date);
        },
        userId() {
            return this.$store.state.userId;
        }
    },
    methods: {
        refresh(showMessage) {
            this.axios.post('http://localhost:8000/user_get_recruitment_list', {
                userId: this.userId
            })
                .then(res => {
                    console.log(res);
                    if (res.data.code === 0) {
                        this.recruitmentList = res.data.recruitmentList;
                        if (showMessage) ElMessage.success('刷新成功');
                    }
                });
        },
        formatDate(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        handlePageChange(currentPage) {
            this.currentPage = currentPage;
            window.scrollTo(0, 0);
        },
        changeToJoinRecruitmentPage() {
            this.$router.push({
                path: '/recruitment/join'
            });
        },
        changeToMyRecruitmentPage() {
            this.$router.push({
                path: '/recruitment/my'
            });
        },
        changeToProjectInfoPage(id) {
            console.log('projectId:', id);
            this.$router.push({
                name: 'projectInfo',
                params: { projectId: id }
            });
        },
        showRecruitmentType(type) {
            switch (type) {
                case '1':
                    return '面向公共招募';
                case '2':
                    return '仅限团队内部';
            }
        },
        showProjectType(type) {
            switch (type) {
                case '1':
                    return '社区服务';
                case '2':
                    return '科技科普';
                case '3':
                    return '支教助学';
                case '4':
                    return '体育赛事';
                case '5':
                    return '大型演出';
                case '6':
                    return '其它';
            }
        },
        showRecruitmentStatus(id) {
            let recruitment = this.recruitmentList.find(item => item.id === id);
            if (recruitment.isAttend)
                return '已报名';
            else if (recruitment.currentNumber >= recruitment.maxNumber)
                return '已满员';
            else if (new Date(recruitment.dueTime) < new Date())
                return '已截止';
            else if (new Date(recruitment.launchTime) > new Date())
                return '未开始';
            else
                return '可报名';
        },
        shouldDisableButton(id) {
            let recruitment = this.recruitmentList.find(item => item.id === id);
            return recruitment.isAttend || recruitment.currentNumber >= recruitment.maxNumber
                || new Date(recruitment.dueTime) < new Date() || new Date(recruitment.launchTime) > new Date();
        },
        openDialog(id) {
            this.dialogVisible = true;
            this.attendId = id;
        },
        attendRecruitment() {
            this.axios.post('http://localhost:8000/user_apply_for_recruitment', {
                userId: this.userId,
                recruitmentId: this.attendId
            })
                .then(res => {
                    console.log(res);
                    if (res.data.code === 0) {
                        let recruitment = this.recruitmentList.find(item => item.id === this.attendId);
                        recruitment.currentNumber = parseInt(recruitment.currentNumber) + 1;
                        recruitment.isAttend = true;
                        ElMessage.success('报名成功');
                    } else if (res.data.code === 1) {
                        ElMessage.error('人数已满');
                        this.refresh(false);
                    } else if (res.data.code === 2) {
                        ElMessage.error('与已报名的活动时间冲突');
                        this.refresh(false);
                    }
                });
            this.dialogVisible = false;
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
    height: auto;
    min-height: 750px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.content-container {
    display: flex;
    flex-direction: column;
}

.table-container {
    display: flex;
    align-items: center;
    flex-direction: column;
}

.title {
    margin-top: 30px;
}

.table-style {
    border-collapse: collapse;
    border: 3px solid black;
}

.recruitments-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-content: flex-start;
    margin-top: 30px;
    margin-left: 60px;
}

th,
td {
    border: 2px solid black;
    height: 35px;
}

.pagination-container {
    margin-top: 80px;
    margin-bottom: 50px;
}

.public-type {
    background: rgb(12, 168, 53);
    color: white;
    border-radius: 5px;
}

.private-type {
    background: orange;
    color: white;
    border-radius: 5px;
}

.red-number {
    color: red;
}

.green-number {
    color: green;
}

.text-font {
    font-size: 16px;
    color: #000;
}

.dialog-footer button:first-child {
    margin-right: 10px;
}

.已报名 {
    background-color: green;
}

.已满员 {
    background-color: orange;
}

.已截止 {
    background-color: grey;
}

.未开始 {
    background-color: grey;
}

.可报名 {
    background-color: #409EFF;
}
</style>