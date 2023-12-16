<template>
    <div class="main-container">
        <div class="top-container">
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
                        <el-image style="width: 320px; height: 180px" :src="avatar" fit="contain" />
                    </div>
                    <div class="content-container">
                        <div class="row1-container">
                            <h1 style="margin-right: 20px;">{{ projectName }}</h1>

                            <el-button size="large" type="primary" style="margin-top: 5px; margin-left: 40px;"
                                @click="collectProject">
                                <span v-if="isCollect"
                                    style="font-weight: bold; font-size: 15px; color:whitesmoke">取消收藏</span>
                                <span v-else style="font-weight: bold; font-size: 15px; color:whitesmoke">收藏</span>
                            </el-button>
                            <br>
                        </div>
                        <div class="row2-container">
                            <p>所属团队:<el-button text><strong style="color: #110f0f; font-size: 20px; padding-bottom: 4px"
                                        @click="changeToTeamInfoPage(teamId)">
                                        {{ teamName }}</strong>
                                </el-button></p>
                            <el-divider border-style="solid" direction="vertical" />
                            <p> &nbsp; 项目类别：<el-tag style="font-size: 16px; font-weight: bold; padding-bottom: 4px;">
                                    {{ showProjectType(projectType) }}</el-tag></p>
                        </div>
                        <p style="font-size: 18px; color: rgb(65, 64, 64);">{{ showRecruitmentStatus(latestTime) }}</p>
                    </div>
                </div>
                <div class="intro-container">
                    <p style="font-size: 22px; font-weight: bold; margin-bottom: 8px;"><el-icon>
                            <Document />
                        </el-icon>项目简介</p>
                    <p style="line-height: 30px;" v-html="contentWithBreaks(projectIntro)"></p>
                </div>
            </div>
            <div class="right-container">
                <div class="title-container">教程</div>

                <div v-for="(item, index) in tutorialList" :key="index" class="tutorial-container"
                    @click="showTutorialContent(item.id)">
                    <p>{{ item.title }}<el-tag
                            style="font-size: 16px; font-weight: bold; margin-left: 10px; padding-bottom: 3px;">
                            {{ item.tag }}</el-tag></p>
                    <span style="font-size: 16px; color: grey;">{{ item.time }}</span>
                </div>
            </div>
        </div>
        <div class="bottom-container">
            <div class="title-container">Q & A</div>

            <div v-for="(item, index) in discussionList" :key="index" class="discussion-container">
                <div class="discussion-item">
                    <el-avatar :size="50" :src="getUserAvatar(item.posterId)" fit="cover"></el-avatar>
                    <p style="margin-left: 20px;"><el-icon>
                            <ChatDotRound />
                        </el-icon> {{ item.posterName }}
                    <p v-html="contentWithBreaks(item.question)"></p>
                    <span style="font-size: 16px; color: grey;">{{ item.questionTime }}</span>
                    </p>
                </div>

                <div class="discussion-item">
                    <el-avatar :size="50" :src="getUserAvatar(leaderId)" fit="cover"></el-avatar>
                    <p style="margin-left: 20px;"><el-icon>
                            <Checked />
                        </el-icon> {{ leaderName }} <el-tag
                            style="font-size: 16px; font-weight: bold; margin-left: 15px; padding-bottom: 3px;">负责人</el-tag>
                    <p v-html="contentWithBreaks(item.reply)"></p>
                    <span style="font-size: 16px; color: grey;">{{ item.replyTime }}</span>
                    </p>
                </div>
            </div>

            <el-button v-if="!questionInput" type="primary" @click="showQuestionInput"
                style="font-weight: bold; font-size: 16px; color:whitesmoke">我要提问</el-button>
            <el-input v-if="questionInput" v-model="newQuestion" type="textarea" placeholder="输入你的问题"
                style="margin-bottom: 30px; font-size: 16px;"></el-input>
            <el-button v-if="questionInput" type="primary" @click="askQuestion"
                style="font-weight: bold; font-size: 16px; color:whitesmoke">完成</el-button>
        </div>
        <el-dialog v-model="tutorialContent" :title="getTutorialTitle()" width="50%" align-center center draggable>
            <p>{{ getTutorialTime() }} <el-tag
                    style="font-size: 14px; font-weight: bold; padding-bottom: 4px; margin-left: 10px;">
                    {{ getTutorialTag() }}</el-tag></p>
            <br>
            <p v-html="contentWithBreaks(getTutorialContent())" class="tutorial-content"></p>
            <template #footer>
                <span class="dialog-footer">
                    <el-button type="primary" @click="tutorialContent = false">
                        <span style="color:whitesmoke; font-weight: bold;">关闭</span>
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus';

export default {
    created() {
        this.fetchProjectInfo();
    },
    data() {
        return {
            projectId: '',
            avatar: null,
            isCollect: false,
            projectName: '',
            projectType: '',
            projectIntro: '',
            latestTime: '',
            leaderId: '',
            leaderName: '',
            teamId: '',
            teamName: '',
            discussionList: [
                // { posterId: '1', posterName: '张三', questionTime: '2023-01-01 19:00', question: '这个项目需要什么技能？', replyTime: '2023-01-02 19:00', reply: '不需要什么技能，只要你有热情就可以了。' },
                // { posterId: '2', posterName: '李四', questionTime: '2023-01-03 19:00', question: '这个项目需要什么技能？', replyTime: '2023-01-04 19:00', reply: '不需要什么技能。\n只要你有热情就可以了。' },
                // { posterId: '3', posterName: '王五', questionTime: '2023-01-05 19:00', question: '这个项目需要什么技能？', replyTime: '2023-01-06 19:00', reply: '不需要什么技能，只要你有热情就可以了。' }
            ],
            avatarList: [],
            tutorialList: [
                // { id: '1', time: '2023-01-01 19:00', title: '宣讲内容', tag: '培训', content: '自愿。即主观自觉选择，没有强制性。\n不图物质报酬。即动机上不追求物质报酬，但不否定开展志愿服务需要一定的物质条件。\n服务于社会公益事业。即服务的内容应是社会公众的公共利益和困难群体的利益，不是社会非困难群体的小团体利益;同时属于政府职责范围内的事情、能够通过正常的市场交换获得的服务(困难群体除外)，一般不能作为志愿者服务的内容。\n奉献自己的力所能及。奉献自己的时间、精力、智力、经验的人是志愿者外，出于自愿的献血、捐献骨髓、捐款捐物的人，也是志愿者。\n非本职职责范围内。比如自来水公司修理水管的职工，如果他正在值班、正在岗位上，为用户提供了优质的修理水管服务，那是本职工作，不是志愿服务;如果他不在值班、不在岗位上，是利用业余时间自愿且不取报酬地为他人提供了修理水管的服务，那他就是志愿者了。' },
                // { id: '2', time: '2023-05-02 19:00', title: '注意事项', tag: '注意', content: '请大家注意安全。' },
                // { id: '3', time: '2023-05-02 19:00', title: '注意事项', tag: '注意', content: '请大家注意安全。' },
                // { id: '4', time: '2023-05-02 19:00', title: '注意事项', tag: '注意', content: '请大家注意安全。' },
                // { id: '5', time: '2023-05-02 19:00', title: '注意事项', tag: '注意', content: '请大家注意安全。' }
            ],
            tutorialId: '',
            tutorialContent: false,
            questionInput: false,
            newQuestion: ''
        }
    },
    methods: {
        fetchProjectInfo() {
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
                        this.leaderId = res.data.leaderId;
                        this.leaderName = res.data.leaderName;
                        this.teamId = res.data.teamId;
                        this.teamName = res.data.teamName;
                        this.discussionList = res.data.discussionList;
                        this.tutorialList = res.data.tutorialList;
                        this.fetchProjectAvatar();
                        this.fetchUsersAvatar();
                    }
                });
        },
        fetchProjectAvatar() {
            this.axios.post('http://localhost:8000/get_project_avatar', {
                projectId: this.projectId
            })
                .then(res => {
                    console.log(res);
                    if (res.data) {
                        this.avatar = "data:image/jpeg;base64," + res.data;
                    }
                });
        },
        handleBack() {
            this.$store.commit("setActiveMenu", this.lastMenu);
            this.$router.go(-1);
        },
        changeToTeamInfoPage(id) {
            this.$store.commit("setActiveMenu", "team");
            this.$store.commit("setLastMenu", "project");
            console.log('teamId:', id);
            this.$router.push({
                name: 'teamInfo',
                params: { teamId: id }
            });
        },
        showRecruitmentStatus(latestTime) {
            if (latestTime === 'N/A') {
                return '暂未招募';
            } else {
                if (new Date() < new Date(latestTime))
                    return '招募中';
                else
                    return '最近招募：' + latestTime;
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
                        if (this.isCollect)
                            ElMessage.success('已收藏');
                        else
                            ElMessage.success('已取消收藏');
                    }
                });
        },
        showTutorialContent(id) {
            this.tutorialId = id;
            this.tutorialContent = true;
        },
        getTutorialTime() {
            let tutorial = this.tutorialList.find(item => item.id === this.tutorialId);
            if (!tutorial)
                return '';
            else
                return tutorial.time;
        },
        getTutorialTitle() {
            let tutorial = this.tutorialList.find(item => item.id === this.tutorialId);
            if (!tutorial)
                return '';
            else
                return tutorial.title;
        },
        getTutorialTag() {
            let tutorial = this.tutorialList.find(item => item.id === this.tutorialId);
            if (!tutorial)
                return '';
            else
                return tutorial.tag;
        },
        getTutorialContent() {
            let tutorial = this.tutorialList.find(item => item.id === this.tutorialId);
            if (!tutorial)
                return '';
            else
                return tutorial.content;
        },
        fetchUsersAvatar() {
            this.fetchUserAvatar(this.leaderId);
            for (let i = 0; i < this.discussionList.length; i++) {
                this.fetchUserAvatar(this.discussionList[i].posterId);
            }
        },
        fetchUserAvatar(id) {
            this.axios.post('http://localhost:8000/get_user_avatar', {
                userId: id
            })
                .then(res => {
                    console.log(res);
                    if (res.data) {
                        var avatar = "data:image/jpeg;base64," + res.data;
                        this.avatarList.push([id, avatar]);
                    }
                });
        },
        getUserAvatar(id) {
            for (let i = 0; i < this.avatarList.length; i++) {
                if (this.avatarList[i][0] === id) {
                    return this.avatarList[i][1];
                }
            }
        },
        showQuestionInput() {
            this.questionInput = true;
        },
        askQuestion() {
            if (this.newQuestion === '') {
                ElMessage.error('问题为空');
                this.questionInput = false;
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
                        this.questionInput = false;
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
        },
        lastMenu() {
            return this.$store.state.lastMenu;
        }
    },
}
</script>

<style scoped>
.main-container {
    display: flex;
    flex-direction: column;
    margin-left: 40px;
    margin-right: 40px;
}

.top-container {
    display: flex;
    flex-direction: row;
    margin-bottom: 30px;
}

.left-container {
    display: flex;
    flex-direction: column;
    margin-top: 30px;
    width: 1100px;
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
    margin-bottom: 30px;
    margin-left: 50px;
    margin-right: 50px;
}

.content-container {
    display: flex;
    flex-direction: column;
    margin-top: 30px;
    margin-left: 10px;
}

.row1-container {
    display: flex;
    flex-direction: row;
    align-items: center;
}

.row2-container {
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

.right-container {
    display: flex;
    flex-direction: column;
    width: 470px;
    margin-left: 30px;
    padding-top: 50px;
    font-size: 18px;
    border-left: 2px solid rgb(114, 110, 104, 0.2);
    overflow-x: hidden;
    overflow-y: auto;
    max-height: 400px;
}

.tutorial-container {
    width: 400px;
    margin-left: 30px;
    margin-bottom: 30px;
    padding-top: 30px;
    padding-bottom: 30px;
    padding-left: 90px;
    border: 2px solid rgb(114, 110, 104, 0.2);
    border-radius: 10px;
    cursor: pointer;
}

.bottom-container {
    margin-top: 30px;
    margin-bottom: 100px;
    margin-left: 150px;
    margin-right: 150px;
    display: block;
}

.discussion-container {
    font-size: 18px;
    margin-top: 30px;
    margin-bottom: 50px;
    padding-top: 30px;
    padding-bottom: 30px;
    padding-left: 300px;
    display: flex;
    flex-direction: column;
    border: 2px solid rgb(114, 110, 104, 0.2);
    border-radius: 50px;
}

.discussion-item {
    display: flex;
    flex-direction: row;
    margin-top: 30px;
    margin-bottom: 30px;
}

.title-container {
    text-align: center;
    color: rgb(47, 67, 67);
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}

.tutorial-content {
    font-size: 16px;
    color: #000;
}

.dialog-footer button:first-child {
    margin-right: 18px;
}
</style>