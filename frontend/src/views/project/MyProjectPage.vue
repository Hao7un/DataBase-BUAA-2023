<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="my" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="all" @click="changeToAllProjectPage">
                    <span class="item-font" style="font-weight: bold">查看项目</span>
                </el-menu-item>
                <el-menu-item index="my" @click="changeToMyProjectPage">
                    <span class="item-font" style="font-weight: bold">我的收藏</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content-container">
            <div class="selector-container">
                <div class="left-container">
                    <el-select v-model="statusRadio" placeholder="最近招募" clearable size="large" class="select-container">
                        <template #prefix>
                            <el-icon class="icon-container">
                                <Open />
                            </el-icon>
                        </template>
                        <el-option v-for="item in option2" :key="item.key" :value="item.value"></el-option>
                    </el-select>
                </div>
                <div class="right-container">
                    <div class="right-item-container">
                        <el-select v-model="typeRadio" placeholder="项目类别" clearable size="large">
                            <template #prefix>
                                <el-icon class="icon-container">
                                    <FolderOpened />
                                </el-icon>
                            </template>
                            <el-option v-for="item in option1" :key="item.key" :value="item.value" size="large"></el-option>
                        </el-select>
                    </div>
                    <div class="right-item-container">
                        <el-input v-model="teamName" placeholder="输入团队名称" clearable size="large"
                            style="width: 200px"></el-input>
                    </div>
                    <div class="right-item-container">
                        <el-input v-model="projectName" placeholder="输入项目名称" clearable size="large"
                            style="width: 200px"></el-input>
                    </div>
                </div>
            </div>
            <div class="project-container">
                <div class="info-container">
                    <div class="card" v-for="item in displayedList">
                        <el-card shadow="hover" class="inner-card" @click="changeToProjectInfoPage(item.id)">
                            <div class="img-container">
                                <img :src="getProjectAvatar(item.id)" alt="project_avatar">
                            </div>
                            <div class="card-info">
                                <div class="title-container">{{ item.name }}</div>
                                <div class="info-item">项目类别：{{ projectType(item.type) }}
                                    <el-divider border-style="solid" direction="vertical" />所属团队：<strong>{{ item.team
                                    }}</strong>
                                </div>
                                <div class="info-item">{{ recruitmentStatus(item.latestTime) }}</div>
                            </div>
                        </el-card>
                    </div>
                </div>
                <div class="pagination-container">
                    <el-pagination @current-change="handlePageChange" :page-size="12" :total="filteredList.length"
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
        this.fetchProjectsInfo();
    },
    data() {
        return {
            typeRadio: "",
            projectName: "",
            teamName: "",
            statusRadio: "",
            currentPage: 1,
            projectList: [
                { id: 1, name: "志愿项目1", type: "1", team: "志愿团队1", latestTime: "2023-12-21" },
                { id: 2, name: "志愿项目2", type: "2", team: "志愿团队2", latestTime: "2023-09-01" },
                { id: 3, name: "志愿项目3", type: "3", team: "志愿团队3", latestTime: "2023-11-01" },
                { id: 4, name: "志愿项目4", type: "4", team: "志愿团队4", latestTime: "2023-09-01" },
                { id: 5, name: "志愿项目5", type: "5", team: "志愿团队5", latestTime: "2023-04-01" },
                { id: 6, name: "志愿项目6", type: "6", team: "志愿团队6", latestTime: "2022-01-01" },
                { id: 7, name: "志愿项目7", type: "3", team: "志愿团队7", latestTime: "2023-11-21" },
                { id: 8, name: "志愿项目8", type: "5", team: "志愿团队8", latestTime: "2021-01-01" },
                { id: 9, name: "志愿项目9", type: "1", team: "志愿团队9", latestTime: "2023-11-01" },
                { id: 10, name: "志愿项目10", type: "4", team: "志愿团队10", latestTime: "2023-10-01" },
                { id: 11, name: "志愿项目11", type: "2", team: "志愿团队6", latestTime: "2023-05-01" },
                { id: 12, name: "志愿项目12", type: "3", team: "志愿团队7", latestTime: "2021-01-01" },
                { id: 13, name: "志愿项目13", type: "5", team: "志愿团队8", latestTime: "2023-11-22" },
                { id: 14, name: "志愿项目14", type: "1", team: "志愿团队9", latestTime: "2023-11-23" },
                { id: 15, name: "志愿项目15", type: "2", team: "志愿团队10", latestTime: "N/A" }
            ],
            avatarList: [],
            option1: [
                { key: 1, value: "社区服务" },
                { key: 2, value: "科技科普" },
                { key: 3, value: "支教助学" },
                { key: 4, value: "体育赛事" },
                { key: 5, value: "大型演出" },
                { key: 6, value: "其它" },

            ],
            option2: [
                { key: 1, value: "招募中" },
                { key: 2, value: "本月" },
                { key: 3, value: "本学期" },
                { key: 4, value: "上学期及以前" },
                { key: 5, value: "暂未招募" },
            ]
        };
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 12;
            let endIndex = startIndex + 12;
            let filteredList = this.projectList;
            if (this.typeRadio != null && this.projectName != null && this.teamName != null && this.statusRadio != null) {
                filteredList = filteredList.filter(item => {
                    let itemStatus = this.projectStatus(item.latestTime);
                    let itemType = this.projectType(item.type);
                    return itemType.includes(this.typeRadio) && item.name.includes(this.projectName)
                        && item.team.includes(this.teamName) && itemStatus.includes(this.statusRadio);
                }
                )
            }
            return filteredList.slice(startIndex, endIndex);
        },
        filteredList() {
            let list = this.projectList;
            if (this.typeRadio != null && this.projectName != null && this.teamName != null && this.statusRadio != null) {
                list = list.filter(item => {
                    let itemStatus = this.projectStatus(item.latestTime);
                    let itemType = this.projectType(item.type);
                    return itemType.includes(this.typeRadio) && item.name.includes(this.projectName)
                        && item.team.includes(this.teamName) && itemStatus.includes(this.statusRadio);
                }
                )
            }
            return list;
        },
    },
    methods: {
        fetchProjectsInfo() {
            this.axios.post('http://localhost:8000/user_get_favorite_projects', {
            userId: this.$store.state.userId
        })
            .then(res => {
                console.log(res);
                if (res.data.code === 0) {
                    this.projectList = res.data.projectList;
                    this.fetchProjectsAvatar();
                }
            });
        },
        fetchProjectsAvatar() {
            for (let i = 0; i < this.projectList.length; i++) {
                this.fetchProjectAvatar(this.projectList[i].id);
            }
        },
        fetchProjectAvatar(id) {
            this.axios.post('http://localhost:8000/get_project_avatar', {
                projectId: id
            })
                .then(res => {
                    console.log(res);
                    if (res.data) {
                        // var avatar = document.getElementById('avatar');
                        var avatar = "data:image/jpeg;base64," + res.data;
                        this.avatarList.push([id, avatar]);
                    }
                });
        },
        getProjectAvatar(id) {
            for (let i = 0; i < this.avatarList.length; i++) {
                if (this.avatarList[i][0] === id) {
                    return this.avatarList[i][1];
                }
            }
        },
        handlePageChange(currentPage) {
            this.currentPage = currentPage;
            window.scrollTo(0, 0);
        },
        changeToMyProjectPage() {
            this.$router.push({
                path: '/project/my'
            })
        },
        changeToAllProjectPage() {
            this.$router.push({
                path: '/project/all'
            })
        },
        changeToProjectInfoPage(id) {
            this.$store.commit("setLastMenu", "project");
            console.log('projectId:', id);
            this.$router.push({
                name: 'projectInfo',
                params: { projectId: id }
            });
        },
        projectStatus(time) {
            const currentTime = new Date();
            if (time == "N/A") {
                return "暂未招募";
            } else {
                const latestTime = new Date(time);
                if (currentTime < latestTime) {
                    return "招募中";
                } else if (currentTime.getFullYear() == latestTime.getFullYear() && currentTime.getMonth() == latestTime.getMonth()) {
                    return "本月";
                } else if (currentTime.getFullYear() == latestTime.getFullYear() && Math.floor(currentTime.getMonth() / 6) == Math.floor(latestTime.getMonth() / 6)) {
                    return "本学期";
                } else {
                    return "上学期及以前";
                }
            }
        },
        recruitmentStatus(latestTime) {
            if (latestTime === 'N/A') {
                return '暂未招募';
            } else {
                if (new Date() < new Date(latestTime)) return '招募中';
                else return '上一次招募：' + latestTime;
            }
        },
        projectType(type) {
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
    height: auto;
    min-height: 750px;
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
    margin-left: 30px;
}

.selector-container {
    height: 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 25px;
}

.left-container {
    display: flex;
    margin-left: 35px;
}

.right-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 10px;
    margin-right: 50px;
}

.right-item-container {
    margin-left: 10px;
    margin-right: 30px;
}

.project-container {
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
    margin-right: 50px;
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
    height: 60%;
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
    align-items: center;
}

.pagination-container {
    margin-top: 50px;
    margin-bottom: 50px;
}

.select-container {
    margin-left: 20px;
    margin-right: 30px;
}

.title-container {
    text-align: center;
    height: 20%;
    font-size: 22px;
    font-weight: bold;
}
</style>