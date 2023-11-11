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
                                    <el-select v-model="type" placeholder="选择面向群体" clearable>
                                        <el-option key="面向公共招募" value="面向公共招募">面向公共招募</el-option>
                                        <el-option key="仅限团队内部" value="仅限团队内部">仅限团队内部</el-option>
                                    </el-select>
                                </th>
                                <th colspan="3" style="width: 450px;"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in displayedList" @click="handleClickRow(item)">
                                <td style="text-align:center"><div :class="item.status === '招募中' ? 'green-status' : 'grey-status' " style="width: 75px; height: 25px; margin-left: 37px;">{{ item.status }}</div></td>
                                <td style="text-align:center">{{ item.project }}</td>
                                <td style="text-align:center">{{ item.date }}</td>
                                <td style="text-align:center"><div :class="item.type === '面向公共招募' ? 'blue-type' : 'orange-type' " style="width: 120px; height: 25px; margin-left: 15px;">{{ item.type }}</div></td>
                                <td style="text-align:center">{{ item.location }}</td>
                                <td style="text-align:center">{{ item.hours }} 小时</td>
                                <td style="text-align:center" :class="item.number === item.totalNumber ? 'red-number' : 'green-number' ">{{ item.number }} / {{ item.totalNumber }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="pagination-container">
                    <el-pagination 
                        @current-change="handlePageChange"
                        :page-size="20"
                        :total="filteredList.length"
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
            status: "",
            keyword: "",
            date: null,
            type: "",
            hours: null,
            totalList: [
                {status: "招募中", project: "项目1", date: "2023-10-21 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 1, totalNumber: 11},
                {status: "招募中", project: "项目2", date: "2023-10-22 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 12, totalNumber: 12},
                {status: "招募中", project: "项目3", date: "2023-10-23 23:59", location: "田径场", type: "仅限团队内部", hours: 16, number: 3, totalNumber: 13},
                {status: "招募中", project: "项目4", date: "2023-10-24 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 4, totalNumber: 14},
                {status: "招募中", project: "项目5", date: "2023-10-25 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 15},
                {status: "招募中", project: "项目6", date: "2023-10-26 23:59", location: "田径场", type: "仅限团队内部", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目7", date: "2023-10-27 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目8", date: "2023-10-28 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目9", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 10, totalNumber: 10},
                {status: "结束招募", project: "项目10", date: "2023-10-30 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 10, totalNumber: 10},
                {status: "结束招募", project: "项目11", date: "2023-10-31 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目12", date: "2023-10-29 23:59", location: "田径场", type: "仅限团队内部", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目13", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目14", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目15", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目16", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目17", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目18", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目19", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目20", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目21", date: "2023-10-29 23:59", location: "田径场", type: "仅限团队内部", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目22", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目23", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目24", date: "2023-10-29 23:59", location: "田径场", type: "面向公共招募", hours: 16, number: 5, totalNumber: 10},
            ],
            selectedRow: null,
        }
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 20;
            let endIndex = startIndex + 20;
            let filteredList = this.totalList;
            if (this.keyword != null && this.status != null && this.type != null) {
                filteredList = filteredList.filter(item => {
                    return item.project.includes(this.keyword) && item.status.includes(this.status) && item.type.includes(this.type) && item.date.includes(this.formatDateString);
                });
            }
            return filteredList.slice(startIndex, endIndex);
        },
        filteredList() {
            let list = this.totalList;
            if (this.keyword != null && this.status != null && this.type != null) {
                list = list.filter(item => {
                    return item.project.includes(this.keyword) && item.status.includes(this.status) && item.type.includes(this.type) && item.date.includes(this.formatDateString);
                });
            }
            return list;
        },
        formatDateString() {
            if (this.date == null) return "";
            return this.formatDate(this.date);
        },
    },
    methods: {
        formatDate(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
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

th, td {
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