<template>
    <div class="main-container">
        <div class="team-container">
            <div class="left-container">
                <div class="info-container">
                    <div class="img-container">
                        <img src="../../assets/images/inf.png">
                    </div>
                    <div class="content-container">
                        <div class="high-container">
                            <h1 style="margin-right: 20px;">{{ projectName }}</h1>

                            <el-button size="large" type="primary" style="margin-top: 5px; margin-left: 40px;"
                                @click="collectProject">
                                <span v-if="isCollect"
                                    style="font-weight: bold; font-size: 15px; color:whitesmoke">取消收藏</span>
                                <span v-else style="font-weight: bold; font-size: 15px; color:whitesmoke">收藏</span>
                            </el-button>
                            <br>
                        </div>
                        <div class="low-container">
                            <p>所属团队:<el-button text><strong style="color: #110f0f; font-size: 20px; padding-bottom: 4px"
                                        @click="changeToTeamInfoPage(teamId)">
                                        {{ teamName }}</strong>
                                </el-button></p>
                            <el-divider border-style="solid" direction="vertical" />
                            <p> &nbsp; 项目类别：<el-tag style="font-size: 16px; font-weight: bold; padding-bottom: 4px;">
                                    {{ showProjectType(projectType) }}</el-tag></p>
                        </div>
                        <p style="font-size: 18px; color: rgb(65, 64, 64);">{{ recruitmentStatus(latestTime) }}</p>
                    </div>
                </div>
                <div class="intro-container">
                    <p style="font-size: 22px; font-weight: bold; margin-bottom: 8px;"><el-icon>
                            <Document />
                        </el-icon>项目简介</p>
                    <p style="line-height: 30px;" v-html="contentWithBreaks(projectIntro)"></p>
                </div>
            </div>
            <div class="tutorial-container">
                <div class="title-container">
                    <p>教程</p>
                </div>
                <div v-for="(item, index) in tutorialList" :key="index">
                    <p>{{ item.title }} {{ item.time }}<el-tag>{{ item.tag }}</el-tag></p>
                    <p>{{ item.content }}</p>
                    <br>
                </div>
            </div>
        </div>
        <div class="qa-container">
            <div class="title-container">
                <p>Q & A</p>
            </div>

            <div v-for="(item, index) in discussionList" :key="index" class="discussion-container">
                <p><el-icon>
                        <ChatDotRound />
                    </el-icon> {{ item.questionPoster }}
                <p v-html="contentWithBreaks(item.question)"></p>
                <span style="font-size: 16px; color: grey;">{{ item.questionTime }}</span></p>
                <br>
                <p><el-icon>
                        <Checked />
                    </el-icon> {{ projectLeader }} <el-tag
                        style="font-size: 16px; font-weight: bold; margin-left: 15px; padding-bottom: 2px;">负责人</el-tag>
                <p v-html="contentWithBreaks(item.reply)"></p>
                <span style="font-size: 16px; color: grey;">{{ item.replyTime }}</span></p>
            </div>
            <br>
            <el-button v-if="!questionInput" type="primary" @click="showQuestionInput"
                style="font-weight: bold; font-size: 16px; color:whitesmoke">我要提问</el-button>
            <el-input v-if="questionInput" v-model="newQuestion" type="textarea" placeholder="输入你的问题"
                style="margin-bottom: 20px;"></el-input>
            <el-button v-if="questionInput" type="primary" @click="askQuestion"
                style="font-weight: bold; font-size: 16px; color:whitesmoke">完成</el-button>
        </div>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus';

export default {
    created() {
        this.projectId = this.$route.params.projectId;
        this.axios.post('http://localhost:8000/user_get_specific_project', {
            userId: this.userId,
            projectId: this.projectId
        })
            .then(res => {
                console.log(res);
                if (res.data.code === 0) {
                    this.isCollect = res.data.isCollect;
                    this.projectName = res.data.projectName;
                    this.projectType = res.data.projectType;
                    this.projectIntro = res.data.projectIntro;
                    this.latestTime = res.data.latestTime;
                    this.projectLeader = res.data.projectLeader;
                    this.teamId = res.data.teamId;
                    this.teamName = res.data.teamName;
                    this.discussionList = res.data.discussionList;
                    this.tutorialList = res.data.tutorialList;
                }
            });
    },
    data() {
        return {
            projectId: '00001',
            isCollect: false,
            projectName: '气象防灾减灾宣讲',
            projectType: '1',
            projectIntro: '团队致力于发挥气象行业特色，常态化开展气象防灾减灾科普进社区、进校园公益项目，创办了独具特色的“气象科普”品牌。\n2022年，结合文明实践“一圈一带一群”建设，与徐汇区多个社区形成合作机制，定期为徐家汇商圈和社区居民开展科普讲座，惠及学生和市民千余人次，申报的“气象防灾减灾宣讲”入选为上海市文明实践百项重点项目。',
            latestTime: '2023-11-01',
            projectLeader: '张昊翔',
            teamId: '1',
            teamName: '计算机学院志愿服务队',
            discussionList: [
                { questionPoster: '张三', questionTime: '2021-01-01', question: '这个项目需要什么技能？', replyTime: '2021-01-02', reply: '不需要什么技能，只要你有热情就可以了。' },
                { questionPoster: '李四', questionTime: '2021-01-03', question: '这个项目需要什么技能？', replyTime: '2021-01-04', reply: '不需要什么技能。\n只要你有热情就可以了。' },
                { questionPoster: '王五', questionTime: '2021-01-05', question: '这个项目需要什么技能？', replyTime: '2021-01-06', reply: '不需要什么技能，只要你有热情就可以了。' },
            ],
            tutorialList: [
                { time: '2023-01-01', title: '宣讲内容', tag: '培训', content: '请大家注意安全。' },
                { time: '2023-05-02', title: '注意事项', tag: '注意', content: '请大家注意安全。' },
            ],
            newQuestion: '',
            questionInput: false,
        }
    },
    methods: {
        changeToTeamInfoPage(id) {
            console.log('teamId:', id);
            this.$router.push({
                name: 'teamInfo',
                params: { teamId: id }
            });
        },
        recruitmentStatus(latestTime) {
            if (latestTime === 'N/A') {
                return '暂未招募';
            } else {
                if (new Date() < new Date(latestTime)) return '招募中';
                else return '最近招募：' + latestTime;
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
        collectProject() {
            this.axios.post('http://localhost:8000/user_toggle_favorite_project', {
                userId: this.userId,
                projectId: this.projectId,
                type: this.isCollect
            })
                .then(res => {
                    console.log(res);
                    if (res.data.code === 0) {
                        this.isCollect = !this.isCollect;
                        if (this.isCollect) ElMessage.success('已收藏');
                        else ElMessage.success('已取消收藏');
                    }
                });
        },
        showQuestionInput() {
            this.questionInput = true;
        },
        askQuestion() {
            if (this.newQuestion === '') {
                ElMessage.error('问题不能为空');
                return;
            }
            this.axios.post('http://localhost:8000/user_post_question', {
                userId: this.userId,
                projectId: this.projectId,
                question: this.newQuestion
            })
                .then(res => {
                    console.log(res);
                    if (res.data.code === 0) {
                        ElMessage.success('提问成功，请等待负责人回复');
                        this.newQuestion = '';
                        this.showQuestionInput = false;
                    }
                });
        },
        contentWithBreaks(content) {
            return content.replace(/\n/g, '<br>');
        }
    },
    computed: {
        userId() {
            return this.$store.state.userId;
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
    margin-bottom: 20px;
    font-size: 20px;
}

.intro-container {
    padding-top: 10px;
    font-size: 18px;
    border-top: 2px solid rgb(114, 110, 104, 0.2);
}

.tutorial-container {
    display: flex;
    flex-direction: column;
    margin-left: 30px;
    padding-top: 50px;
    padding-left: 80px;
    font-size: 18px;
    border-left: 2px solid rgb(114, 110, 104, 0.2);
}

.qa-container {
    margin-top: 30px;
    margin-bottom: 100px;
    margin-left: 150px;
    margin-right: 150px;
    display: block;
}

.discussion-container {
    font-size: 18px;
    margin-top: 50px;
    padding-top: 30px;
    padding-bottom: 30px;
    padding-left: 200px;
    display: flex;
    flex-direction: column;
    border: 2px solid rgb(114, 110, 104, 0.2);
    border-radius: 50px;
}

.title-container {
    text-align: center;
    color: rgb(47, 67, 67);
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
}
</style>