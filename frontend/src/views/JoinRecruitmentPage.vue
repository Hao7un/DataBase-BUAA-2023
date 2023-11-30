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
                                <th style="background-color: #e8e8e4">状态</th>
                                <th style="background-color: #e8e8e4">所属项目</th>
                                <th style="background-color: #e8e8e4">招募时间</th>
                                <th style="background-color: #e8e8e4">进行时间</th>
                                <th style="background-color: #e8e8e4">面向群体</th>
                                <th style="background-color: #e8e8e4">招募地点</th>
                                <th style="background-color: #e8e8e4">志愿时长</th>
                                <th style="background-color: #e8e8e4">招募人数</th>
                            </tr>
                            <tr>
                                <th style="width: 150px;">
                                    <el-select v-model="status" clearable placeholder="选择招募状态">
                                        <el-option key="招募中" value="招募中">招募中</el-option>
                                        <el-option key="结束招募" value="结束招募">结束招募</el-option>
                                    </el-select>
                                </th>
                                <th style="width: 180px;">
                                    <el-input v-model="keyword" placeholder="搜索项目名称" clearable></el-input>
                                </th>
                                <th style="width: 200px;">
                                    <el-date-picker v-model="date" type="date" placeholder="搜索招募时间"
                                        clearable></el-date-picker>
                                </th>
                                <th style="width: 150px;">
                                    <el-select v-model="type" placeholder="选择面向群体" clearable>
                                        <el-option key="面向公共招募" value="面向公共招募">面向公共招募</el-option>
                                        <el-option key="仅限团队内部" value="仅限团队内部">仅限团队内部</el-option>
                                    </el-select>
                                </th>
                                <th colspan="3" style="width: 500px;"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in displayedList" @click="openDialog(item.id)">
                                <td style="text-align:center">
                                    <div :class="item.isAttend ? 'green-status' : 'grey-status'"
                                        style="width: 75px; height: 25px; margin-left: 37px;">{{ showProjectType(item.projectType) }}</div>
                                </td>
                                <td style="text-align:center">{{ item.projectName }}</td>
                                <td style="text-align:center">{{ item.launchTime }}-{{ item.dueTime }}</td>
                                <td style="text-align:center">{{ item.startTime }}-{{ item.endTime }}</td>
                                <td style="text-align:center">
                                    <div :class="item.type === '公共' ? 'blue-type' : 'orange-type'"
                                        style="width: 120px; height: 25px; margin-left: 15px;">{{ showRecruitmentType(item.type) }}</div>
                                </td>
                                <td style="text-align:center">{{ item.location }}</td>
                                <td style="text-align:center">{{ item.volunteerHour }} 小时</td>
                                <td style="text-align:center"
                                    :class="item.currentNumber === item.maxNumber ? 'red-number' : 'green-number'">{{
                                        item.currentNumber }} / {{ item.maxNumber }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="pagination-container">
                    <el-pagination @current-change="handlePageChange" :page-size="20" :total="filteredList.length"
                        layout="prev, pager, next">
                    </el-pagination>
                </div>

                <el-dialog v-model="dialogVisible" title="注意" width="30%" align-center center draggable>
                    <span class="text-font">你即将报名此次招募。</span>
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
        </div>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus';


export default {
    created() {
        this.axios.post('http://localhost:8000/', {
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
            status: "",
            keyword: "",
            date: null,
            type: "",
            hours: null,
            recruitmentList: [
                { id: "00001", launchTime: "YYYY-MM-DD HH:MM", dueTime: "YYYY-MM-DD HH:MM", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", isAttend: true, type: "1", maxNumber: "50", currentNumber: "30", projectId: "00001", projectName: "志愿项目1", projectType: "1" },
            ],
            dialogVisible: false,
            attendId: "00001"
        }
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 20;
            let endIndex = startIndex + 20;
            let filteredList = this.recruitmentList;
            if (this.keyword != null && this.status != null && this.type != null) {
                filteredList = filteredList.filter(item => {
                    return item.projectName.includes(this.keyword) && item.type.includes(this.type)
                        && item.launchTime.includes(this.formatDateString);
                });
            }
            return filteredList.slice(startIndex, endIndex);
        },
        filteredList() {
            let list = this.recruitmentList;
            if (this.keyword != null && this.status != null && this.type != null) {
                list = list.filter(item => {
                    return item.projectName.includes(this.keyword) && item.type.includes(this.type)
                        && item.launchTime.includes(this.formatDateString);
                });
            }
            return list;
        },
        formatDateString() {
            if (this.date == null) return "";
            return this.formatDate(this.date);
        },
        userId() {
            return this.$store.state.userId;
        }
    },
    methods: {
        formatDate(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
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
        openDialog(id) {
            this.dialogVisible = true;
            this.attendId = id;
        },
        attendRecruitment() {
            this.axios.post('http://localhost:8000/', {
                userId: this.userId,
                recruitmentId: this.attendId
            })
                .then(res => {
                    console.log(res);
                    if (res.data.code === 0) {
                        this.dialogVisible = false;
                        ElMessage.success('报名成功');
                    }
                });
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

.content-container {
    display: flex;
    height: 1000px;
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
    margin-left: 130px;
    height: 700px;
    width: 1350px;
}

.table-container {
    width: 100%;
}

table tr:hover {
    cursor: pointer;
}

th,
td {
    border: 2px solid black;
    height: 35px;
}

.pagination-container {
    margin-top: 150px;
    margin-bottom: 50px;
}

.green-status {
    background: green;
    color: white;
    border-radius: 5px;
}

.grey-status {
    background: grey;
    color: white;
    border-radius: 5px;
}

.blue-type {
    background: rgb(78, 78, 249);
    color: white;
    border-radius: 5px;
}

.orange-type {
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
</style>