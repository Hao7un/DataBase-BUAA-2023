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
                <div class="recruitments-container">
                    <el-table
                        :data="this.displayedList" border
                        :header-cell-style="{background:'#eef1f6', color:'#606266'}"
                        @row-click="handleRowClick"
                    >

                        <el-table-column prop="status" label="状态" align="center" ></el-table-column>
        
                        <el-table-column prop="project" label="所属项目" align="center"></el-table-column>
                        
                        <el-table-column prop="date" label="招募时间" align="center"></el-table-column>

                        <el-table-column prop="location" label="招募地点" align="center"></el-table-column>
        
                        <el-table-column prop="type" label="面向群体" align="center"></el-table-column>

                        <el-table-column prop="hours" label="志愿时长" align="center"></el-table-column>
        
                        <el-table-column prop="totalNumber" label="招募人数" align="center"></el-table-column>   
                               
                    </el-table>
                </div>
                <div class="pagination-container">
                    <el-pagination 
                        @current-change="handlePageChange"
                        :page-size="15"
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
            totalList: [
                {status: "招募中", project: "项目1", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目2", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目3", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目4", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目5", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目6", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目7", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目8", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目9", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目10", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目11", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目12", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目13", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目14", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目15", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目16", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "结束招募", project: "项目17", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目18", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
                {status: "招募中", project: "项目19", date: "2023-10-29 23:59", location: "田径场", type: "面向公共", hours: 16, number: 5, totalNumber: 10},
            ],
            selectedRow: null,
        }
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 15;
            return this.totalList.slice(startIndex, startIndex + 15);
        }
    },
    methods: {
        getStatusClass(status) {
            return status === '招募中' ? "green-border" : "red-border";
        },
        handleRowClick(row) {
            this.selectedRow = row;
            console.log("click!!!");
            console.log(this.selectedRow.status, 
                this.selectedRow.project, this.selectedRow.date, 
                this.selectedRow.location, this.selectedRow.type, 
                this.selectedRow.hours, this.selectedRow.number);
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

.recruitments-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-content: flex-start;
    margin-top: 30px;
    margin-left: 30px;
    height: 700px;
    width: 1350px;
}

.pagination-container {
    margin-top: 50px;
}

.green-border {
  border: 2px solid green;
}

.red-border {
  border: 2px solid red;
}

</style>