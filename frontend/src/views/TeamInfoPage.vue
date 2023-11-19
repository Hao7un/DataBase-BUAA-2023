<template>
    <h1>{{ teamName }}</h1>
    <p>{{ teamIntro }}</p>
    <p>成立日期：{{ foundationDate }}</p>
    <p>团队人数：{{ number }}</p>
    <p>团队领导：{{ teamLeader }}</p>
    <p>联系电话：{{ telephone }}</p>
    <p>电子邮件：{{ email }}</p>
    <el-button v-if="!isTeamMember" type="primary" @click="applyForTeam">申请加入</el-button>
    <h2>项目列表</h2>
    <ul>
      <li v-for="project in projectList" :key="project.id">
        {{ project.name }} - {{ project.type }} - {{ project.hours }} 小时
      </li>
    </ul>
</template>

<script>
import { ElMessage } from 'element-plus';

export default {
    created() {
        this.teamId = this.$route.params.teamId;
        this.axios.post('http://localhost:5173/team/info', {
            collegeId: this.collegeId,
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
            email: '1234@12.com',
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
            console.log(id);
            this.$router.push({
                name: 'projectInfo',
                params: { projectId: id }
            });
        },
        applyForTeam() {
            this.axios.post('http://localhost:5173/team/info', {
                collegeId: this.collegeId,
                teamId: this.teamId,
                applyTime: "2021-01-01 00:00:00"
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
        collegeId() {
            return this.$store.state.collegeId;
        }
    }
}
</script>

<style scoped></style>