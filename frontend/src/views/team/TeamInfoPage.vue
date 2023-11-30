<template>
    <div class="main-container">
        <div class="team-container">
            <div class="left-container">
                <div class="info-container">
                    <div class="img-container">
                        <img src="../assets/images/hand_shaking.png">
                    </div>
                    <div class="content-container">
                        <div class="high-container">
                            <h1 style="margin-right: 20px;">{{ teamName }}</h1>

                            <el-button size="large" type="primary" style="margin-top: 5px; margin-left: 40px;"
                                :disabled="isTeamMember" @click="applyForTeam">
                                <span v-if="isTeamMember"
                                    style="font-weight: bold; font-size: 15px; color:whitesmoke">加入于{{ joinDate }}</span>
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
                    <p>{{ teamIntro }}</p>
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
                <el-carousel height="400px" :interval="5000" type="card">
                    <el-carousel-item v-for="project in projectList" :key="project.id"
                        @click="changeToProjectInfoPage(project.id)">
                        <h2 style="margin-top: 30px;">{{ project.name }}</h2>
                        <div style="margin-top: 20px; margin-bottom: 20px;">
                            <img src="../assets/images/project.png">
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
                }
            });
    },
    data() {
        return {
            teamId: '00001',
            isTeamMember: true,
            teamName: '计算机学院志愿服务队',
            teamNumber: '10',
            teamIntro: '团队致力于发挥气象行业特色，常态化开展气象防灾减灾科普进社区、进校园公益项目，创办了独具特色的“气象科普”品牌。2022年，结合文明实践“一圈一带一群”建设，与徐汇区多个社区形成合作机制，定期为徐家汇商圈和社区居民开展科普讲座，惠及学生和市民千余人次，申报的“气象防灾减灾宣讲”入选为上海市文明实践百项重点项目。',
            foundationDate: '2020-01-01',
            joinDate: '2023-01-01',
            teamLeader: '张昊翔',
            telephone: '18100000000',
            email: '1234@xyz.com',
            projectList: [
                { id: 1, name: '项目1', type: '1', times: 10 },
                { id: 2, name: '项目2', type: '2', times: 5 },
                { id: 3, name: '项目3', type: '3', times: 3 },
                { id: 4, name: '项目4', type: '4', times: 20 },
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
    margin-top: 20px;
}

.img-container {
    display: flex;
    width: 300px;
    height: 200px;
    margin-bottom: 30px;
    margin-left: 100px;
}

.content-container {
    display: flex;
    flex-direction: column;
    margin-top: 20px;
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
    font-style: italic;
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
    margin-left: 10px;
    margin-right: 10px;
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

.el-carousel__item:nth-child(2n) {
    background-color: #a4b6c2;
}

.el-carousel__item:nth-child(2n + 1) {
    background-color: #d3dce6;
}
</style>