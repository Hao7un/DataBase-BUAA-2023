<template>
    <div class="main-container">
        <div class="team-container">
            <div class="left-container">
                <div class="info-container">
                    <v-btn class="back-button" @click="handleBack">
                        <template v-slot:prepend>
                            <el-icon>
                                <Back />
                            </el-icon>
                        </template>
                        返回
                    </v-btn>
                    <div class="img-container">
                        <el-image style="width: 400px; height: 225px" :src="avatar" fit="contain" />
                    </div>
                    <div class="content-container">
                        <div class="high-container">
                            <h1 style="margin-right: 20px;">{{ teamName }}</h1>
                            <el-button size="large" type="primary" style="margin-top: 5px; margin-left: 40px;"
                                :disabled="isTeamMember" @click="applyForTeam">
                                <span v-if="isTeamMember" style="font-weight: bold; font-size: 15px; color:whitesmoke">加入于{{
                                    joinDate }}</span>
                                <span v-else style="font-weight: bold; font-size: 15px; color:whitesmoke">申请加入</span>
                            </el-button>
                            <br>
                        </div>
                        <div class="low-container">
                            <p>成立日期：{{ foundationDate }}</p>
                            <el-divider border-style="solid" direction="vertical" />
                            <p>团队人数：{{ teamNumber }}</p>
                        </div>
                    </div>
                </div>
                <div class="intro-container">
                    <p style="font-size: 22px; font-weight: bold; margin-bottom: 8px;"><el-icon>
                            <Document />
                        </el-icon>团队简介</p>
                    <p style="line-height: 30px;" v-html="teamIntroWithBreaks"></p>
                </div>
            </div>
            <div class="leader-container">
                <p><el-icon>
                        <User />
                    </el-icon><strong> 团队负责人：</strong> {{ teamLeader }}</p>
                <br>
                <p><el-icon>
                        <Iphone />
                    </el-icon><strong> 负责人电话：</strong> {{ telephone }}</p>
                <br>
                <p><el-icon>
                        <MessageBox />
                    </el-icon><strong> 负责人邮箱：</strong> {{ email }}</p>
            </div>
        </div>
        <div class="project-container">
            <div class="title-container">
                <h2>志 愿 风 采</h2>
            </div>
            <div class="text-center">
                <el-carousel height="450px" :interval="3000" type="card">
                    <el-carousel-item v-for="project in projectList" :key="project.id"
                        @click="changeToProjectInfoPage(project.id)">
                        <h2 style="margin-top: 30px;">{{ project.name }}</h2>
                        <div style="margin-top: 20px; margin-bottom: 20px;">
                            <el-image style="width: 400px; height: 225px" :src="getProjectAvatar(project.id)" fit="contain" />
                        </div>
                        <p><el-icon>
                                <Guide />
                            </el-icon> 项目类别：{{ projectType(project.type) }}</p>
                        <br>
                        <p><el-icon>
                                <Calendar />
                            </el-icon> 招募次数：{{ project.times }} </p>
                    </el-carousel-item>
                </el-carousel>
            </div>

        </div>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus';

export default {
    created() {
        this.fetchTeamInfo();
    },
    data() {
        return {
            teamId: '',
            avatar: null,
            isTeamMember: false,
            teamName: '',
            teamNumber: '',
            teamIntro: '',
            foundationDate: '',
            joinDate: '',
            teamLeader: '',
            telephone: '',
            email: '',
            projectList: [
                // { id: 1, name: '项目1', type: '1', times: 10 },
                // { id: 2, name: '项目2', type: '2', times: 5 },
                // { id: 3, name: '项目3', type: '3', times: 3 },
                // { id: 4, name: '项目4', type: '4', times: 20 }
            ],
            projectAvatarList: [],
        }
    },
    methods: {
        fetchTeamInfo() {
            this.teamId = this.$route.params.teamId;
            this.axios.post('http://localhost:8000/user_get_specific_team_details', {
                userId: this.userId,
                teamId: this.teamId
            })
                .then(res => {
                    console.log(res);
                    if (res.data.code === 0) {
                        this.isTeamMember = res.data.isTeamMember;
                        this.teamName = res.data.teamName;
                        this.teamNumber = res.data.teamNumber;
                        this.teamIntro = res.data.teamIntro;
                        this.foundationDate = res.data.foundationDate;
                        this.joinDate = res.data.joinDate;
                        this.teamLeader = res.data.teamLeader;
                        this.telephone = res.data.telephone;
                        this.email = res.data.email;
                        this.projectList = res.data.projectList;
                        this.fetchTeamAvatar();
                        this.fetchProjectsAvatar();
                    }
                });
        },
        fetchTeamAvatar() {
            this.axios.post('http://localhost:8000/get_team_avatar', {
                teamId: this.teamId
            })
                .then(res => {
                    console.log(res);
                    if (res.data) {
                        this.avatar = "data:image/jpeg;base64," + res.data;
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
                        var avatar = "data:image/jpeg;base64," + res.data;
                        this.projectAvatarList.push([id, avatar])
                    }
                });
        },
        getProjectAvatar(id) {
            for (let i = 0; i < this.projectAvatarList.length; i++) {
                if (this.projectAvatarList[i][0] === id) {
                    return this.projectAvatarList[i][1];
                }
            }
        },
        handleBack() {
            this.$store.commit("setActiveMenu", this.lastMenu);
            this.$router.go(-1);
        },
        changeToProjectInfoPage(id) {
            this.$store.commit("setActiveMenu", "project");
            this.$store.commit("setLastMenu", "team");
            console.log('projectId:', id);
            this.$router.push({
                name: 'projectInfo',
                params: { projectId: id }
            });
        },
        applyForTeam() {
            this.axios.post('http://localhost:8000/user_apply_to_join_team', {
                userId: this.userId,
                teamId: this.teamId,
            })
                .then(res => {
                    console.log(res);
                    if (res.data.code === 0) {
                        ElMessage.success('申请成功，请等待负责人通过');
                    } else {
                        ElMessage.error('请勿重复申请');
                    }
                });
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
    },
    computed: {
        userId() {
            return this.$store.state.userId;
        },
        lastMenu() {
            return this.$store.state.lastMenu;
        },
        teamIntroWithBreaks() {
            return this.teamIntro.replace(/\n/g, '<br>');
        }
    },
}
</script>

<style scoped>
.main-container {
    margin-left: 60px;
    margin-right: 60px;
    display: flex;
    flex-direction: column;
}

.team-container {
    display: flex;
    flex-direction: row;
    margin-bottom: 80px;
}

.left-container {
    display: flex;
    flex-direction: column;
    margin-top: 30px;
    width: 1200px;
}

.info-container {
    display: flex;
    flex-direction: row;
}

.back-button {
    font-weight: bold;
    font-size: 15px;
}

.img-container {
    margin-top: 30px;
    margin-bottom: 50px;
    margin-left: 50px;
    margin-right: 50px;
}

.content-container {
    display: flex;
    flex-direction: column;
    margin-top: 30px;
    margin-left: 10px;
}

.high-container {
    display: flex;
    flex-direction: row;
    align-items: center;
}

.low-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-top: 30px;
    font-size: 18px;
}

.intro-container {
    padding-top: 10px;
    font-size: 18px;
    border-top: 2px solid rgb(114, 110, 104, 0.2);
}

.leader-container {
    display: flex;
    flex-direction: column;
    margin-left: 50px;
    padding-left: 30px;
    padding-top: 50px;
    font-size: 18px;
    border-left: 2px solid rgb(114, 110, 104, 0.2);
}

.project-container {
    margin-top: 30px;
    margin-bottom: 100px;
    margin-left: 100px;
    margin-right: 100px;
    display: block;
    flex-direction: column;
}

.title-container {
    text-align: center;
    color: rgb(47, 67, 67);
    font-size: 18px;
    margin-bottom: 10px;
}


.demonstration {
    color: var(--el-text-color-secondary);
}

.el-carousel__item:nth-child(3n) {
    background-color: #99ccff;
}

.el-carousel__item:nth-child(3n + 1) {
    background-color: #3399cc;
}

.el-carousel__item:nth-child(3n + 2) {
    background-color: #ccffff;
}
</style>