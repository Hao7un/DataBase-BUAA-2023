<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="join">
                <el-menu-item index="join" @click="changeToJoinRecruitmentPage">
                    <span class="item-font" style="font-weight: bold;">参与招募</span>
                </el-menu-item>
                <el-menu-item index="my" @click="changeToMyRecruitmentPage">
                    <span class="item-font" style="font-weight: bold;">招募统计</span>
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
                                <th style="width: 150px;">
                                    <el-input v-model="keyword" placeholder="搜索项目名称" clearable></el-input>
                                </th>
                                <th style="width: 200px;">
                                    <el-date-picker
                                    v-model="date"
                                    type="date"
                                    placeholder="搜索招募时间"
                                    clearable
                                ></el-date-picker>
                                </th>
                                <th style="width: 150px;">
                                    <el-select v-model="type" placeholder="面向对象" clearable>
                                        <el-option key="面向公共招募" value="面向公共招募">面向公共招募</el-option>
                                        <el-option key="仅限团队内部" value="仅限团队内部">仅限团队内部</el-option>
                                    </el-select>
                                </th>
                                <th colspan="3" style="width: 450px;"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in displayedList" @click="handleClickRow(item)">
                                <td style="text-align:center">{{ item.status }}</td>
                                <td style="text-align:center">{{ item.project }}</td>
                                <td style="text-align:center">{{ item.date }}</td>
                                <td style="text-align:center">{{ item.type }}</td>
                                <td style="text-align:center">{{ item.location }}</td>
                                <td style="text-align:center">{{ item.hours }} 小时</td>
                                <td style="text-align:center">{{ item.number }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="pagination-container">
                    <el-pagination 
                        @current-change="handlePageChange"
                        :page-size="20"
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
            currentPage: 1,
            status: null,
            keyword: null,
            date: null,
            type: null,
            hours: null,
            totalList: [
                {status: "招募中", project: "项目1", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目2", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目3", date: "2023-10-29 23:59", location: "田径场", type: "仅限团队内部", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目4", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目5", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目6", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目7", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目8", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目9", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目10", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目11", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目12", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目13", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目14", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目15", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目16", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目17", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目18", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目19", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目20", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目21", date: "2023-10-29 23:59", location: "田径场", type: "仅限团队内部", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目22", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目23", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
            ],
            selectedRow: null,
        }
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 20;
            return this.totalList.slice(startIndex, startIndex + 20);
        },
        filterdList() {
            
        }
    },
    methods: {
        getStatusClass(status) {
            return status === '招募中' ? "green-border" : "red-border";
        },
        handleClickRow(row) {
            console.log(row.status, row.project, row.date, row.location, row.type, row.hours, row.number);
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
    height: 900px;
    flex-direction: column;
    padding-top: 20px;
    margin-left: 20px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.content-container {
    display: flex;
    height: 600px;
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

.pagination-container {
    margin-top: 50px;
    margin-bottom: 50px;
}

.green-border {
  border: 2px solid green;
}

.red-border {
  border: 2px solid red;
}

</style>