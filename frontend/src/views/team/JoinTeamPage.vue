<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="join" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
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
                    <span style="display: flex; align-items: center;">团队成立日期：</span> &nbsp;&nbsp;
                    <el-date-picker v-model="date" type="date" placeholder="输入日期" size="large" clearable>
                    </el-date-picker>
                    &nbsp; &nbsp; <span style="display: flex; align-items: center;">至今</span>
                </div>
                <div class="search-container">
                    <el-select v-model="number" placeholder="团队人数" clearable size="large" style="width: 200px">
                        <el-option key="1" value="10人以下">10人以下</el-option>
                        <el-option key="2" value="11至99人">11至99人</el-option>
                        <el-option key="3" value="100人以上">100人以上</el-option>
                    </el-select>
                    &nbsp; &nbsp; &nbsp;
                    <el-input v-model="keyword" placeholder="输入团队名称" clearable size="large" style="width: 200px"></el-input>
                </div>
            </div>
            <div class="teams-container">
                <div class="info-container">
                    <div class="card" v-for="(item, index) in displayedList">
                        <el-card shadow="hover" class="inner-card" @click="changeToTeamInfoPage(item.id)">
                            <div class="img-container">
                                <img src="../../assets/images/hand_shaking.png">
                            </div>
                            <div class="card-info">
                                <div class="team-name">{{ item.name }}</div>
                                <div class="team-details">
                                    <div class="detail-item"><el-icon>
                                            <User />
                                        </el-icon> 团队人数：{{ item.number }}</div>
                                    <el-divider border-style="solid" direction="vertical" />
                                    <div class="detail-item"><el-icon>
                                            <Clock />
                                        </el-icon> 总服务时长：{{ item.hours }} 小时</div>
                                </div>
                            </div>
                        </el-card>
                    </div>
                </div>
                <div class="pagination-container">
                    <el-pagination @current-change="handlePageChange" :page-size="8" :total="filteredList.length"
                        layout="prev, pager, next">
                    </el-pagination>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    created() {
        this.axios.get('http://localhost:8000/user_get_all_teams_info')
            .then(res => {
                console.log(res);
                if (res.data.code === 0) {
                    this.totalList = res.data.totalList;
                }
            });
    },
    data() {
        return {
            date: null,
            keyword: "",
            number: "",
            currentPage: 1,
            totalList: [
                { id: 1, name: "志愿团队1", date: "2023-11-01", number: 2, hours: 100 },
                { id: 2, name: "志愿团队2", date: "2023-11-02", number: 6, hours: 50 },
                { id: 3, name: "志愿团队3", date: "2023-11-03", number: 8, hours: 50 },
                { id: 4, name: "志愿团队4", date: "2023-11-04", number: 25, hours: 50 },
                { id: 5, name: "志愿团队5", date: "2023-11-05", number: 27, hours: 50 },
                { id: 6, name: "志愿团队6", date: "2023-11-06", number: 30, hours: 50 },
                { id: 7, name: "志愿团队7", date: "2023-11-07", number: 45, hours: 50 },
                { id: 8, name: "志愿团队8", date: "2023-11-08", number: 56, hours: 50 },
                { id: 9, name: "志愿团队9", date: "2023-11-09", number: 90, hours: 50 },
                { id: 10, name: "志愿团队10", date: "2023-11-10", number: 106, hours: 50 },
            ]
        }
    },
    computed: {
        range() {
            if (this.number === "10人以下") {
                return [1, 10];
            }
            else if (this.number === "11至99人") {
                return [11, 99];
            }
            else if (this.number === "100人以上") {
                return [100, Infinity];
            }
            else {
                return [0, Infinity];
            }
        },
        displayedList() {
            let startIndex = (this.currentPage - 1) * 8;
            let endIndex = startIndex + 8;
            let filteredList = this.totalList;
            if (this.keyword != null && this.number != null) {
                filteredList = filteredList.filter(item => {
                    let itemDate = new Date(item.date);
                    return item.name.includes(this.keyword) && (item.number >= this.range[0] && item.number <= this.range[1]) 
                    && itemDate >= this.date;
                }
                );
            }
            return filteredList.slice(startIndex, endIndex);
        },
        filteredList() {
            let list = this.totalList;
            if (this.keyword != null && this.number != null) {
                list = list.filter(item => {
                    let itemDate = new Date(item.date);
                    return item.name.includes(this.keyword) && (item.number >= this.range[0] && item.number <= this.range[1]) 
                    && itemDate >= this.date;
                }
                );
            }
            return list;
        },
    },
    methods: {
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
                path: '/team/my'
            })
        },
        changeToTeamInfoPage(id) {
            console.log('teamId:', id);
            this.$router.push({
                name: 'teamInfo',
                params: { teamId: id }
            });
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
    height: 1550px;
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
    margin-top: 30px;
    margin-left: 180px;
}

.content-container {
    display: flex;
    flex-direction: column;
    margin-left: 15px;
}

.date-container {
    display: flex;
    width: 500px;
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
    margin-left: 100px;
    margin-right: 30px;
}

.info-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-content: flex-start;
    margin-top: 15px;
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
    height: 60%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.card-info {
    display: flex;
    height: 40%;
    flex-direction: column;
}

.team-name {
    text-align: center;
    height: 20%;
    font-size: 20px;
    font-weight: bold;
}

.team-details {
    display: flex;
    height: 20%;
    margin-top: 10px;
    justify-content: center;
    align-items: center;
}

.detail-item {
    margin-right: 10px;
    margin-left: 10px;
}

.pagination-container {
    margin-top: 50px;
    margin-bottom: 50px;
}
</style>