<template>
    <div class="main-container">
        <div class="team-container">
            <div class="left-container">
                <div class="info-container">
                    <div class="img-container">
                        <img src="../assets/images/hand_shaking.png">
                    </div>
                    <div class="content-container">
                        <h1>{{ teamName }}</h1>
                        <el-button type="primary" :disabled="isTeamMember" @click="applyForTeam">
                            <span v-if="isTeamMember"
                                style="font-weight: bold; font-size: 15px; color:whitesmoke">已加入</span>
                            <span v-else style="font-weight: bold; font-size: 15px; color:whitesmoke">申请加入</span>
                        </el-button>
                        <p>成立日期：{{ foundationDate }}</p>
                        <p>团队人数：{{ number }}</p>
                    </div>
                    <div class="intro-container">
                        {{ teamIntro }}
                    </div>
                </div>
            </div>
            <div class="leader-container">
                <p>团队领导：{{ teamLeader }}</p>
                <p>联系电话：{{ telephone }}</p>
                <p>电子邮件：{{ email }}</p>
            </div>
        </div>
        <div class="project-container">
            <div class="title-container">
                <h2>志 愿 项 目</h2>
            </div>
            <div class="block text-center">
                <el-carousel height="400px" :interval="5000" type="card">
                    <el-carousel-item v-for="project in projectList" :key="project.id"
                        @click="changeToProjectInfoPage(project.id)">
                        <h3>{{ project.name }}</h3>
                        <p>项目类别：{{ project.type }}</p>
                        <p>总服务时长：{{ project.hours }} 小时</p>
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
                    this.teamLeader = res.data.teamLeader;
                    this.telephone = res.data.telephone;
                    this.email = res.data.email;
                    this.projectList = res.data.projectList;
                }
            });
    },
    data() {
        return {
            isTeamMember: false,
            teamId: '123',
            teamName: '志愿团队1',
            teamIntro: '这是一个志愿团队',
            foundationDate: '2020-01-01',
            number: '10',
            teamLeader: '张昊翔',
            telephone: '18100000000',
            email: '1234@xyz.com',
            projectList: [
                { id: 1, name: '项目1', type: '社区服务', hours: 100 },
                { id: 2, name: '项目2', type: '体育比赛', hours: 50 },
                { id: 3, name: '项目3', type: '科普讲解', hours: 50 },
                { id: 4, name: '项目4', type: '支教助学', hours: 2000 },
            ],
        }
    },
    methods: {
        changeToProjectInfoPage(id) {
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
                        ElMessage.success('申请成功');
                    }
                });
        }

    },
    computed: {
        userId() {
            return this.$store.state.userId;
        }
    }
}
</script>

<style scoped>
.main-container {
    margin-top: 30px;
    margin-left: 60px;
    margin-right: 60px;
    display: flex;
    flex-direction: column;
}

.team-container {
    display: flex;
    flex-direction: row;
}

.left-container {
    display: flex;
    flex-direction: column;
}

.info-container {
    display: flex;
    flex-direction: row;
}

.img-container {
    display: flex;
    width: 300px;
    height: 200px;
    margin-top: 50px;
    margin-bottom: 50px;
    margin-left: 100px;
}

.content-container {
    display: flex;
    flex-direction: row;
    margin-top: 50px;
    margin-left: 10px;
}

.intro-container {
    display: flex;
    margin-top: 50px;
    margin-right: 100px;
}

.leader-container {
    display: flex;
    flex-direction: column;
    margin-top: 50px;
    margin-left: 100px;

}

.project-container {
    margin-top: 30px;
    margin-bottom: 100px;
    margin-left: 10px;
    margin-right: 10px;
    display: block;
    flex-direction: column;
}

.title-container {
    text-align: center;
    color: darkslategrey;
    margin-bottom: 10px;
}

.demonstration {
    color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
    color: #475669;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
    text-align: center;
}

.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
    background-color: #d3dce6;
}
</style>