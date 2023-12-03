<template>
    <div class="main-container">
        <div class="top-container">
            <div class="left-container">
                <div class="info-container">
                    <div class="img-container">
                        <img src="../../assets/images/inf.png">
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
                <p><el-icon>
                        <ChatDotRound />
                    </el-icon> {{ item.questionPoster }}
                <p v-html="contentWithBreaks(item.question)"></p>
                <span style="font-size: 16px; color: grey;">{{ item.questionTime }}</span></p>
                <br>
                <p><el-icon>
                        <Checked />
                    </el-icon> {{ projectLeader }} <el-tag
                        style="font-size: 16px; font-weight: bold; margin-left: 15px; padding-bottom: 3px;">负责人</el-tag>
                <p v-html="contentWithBreaks(item.reply)"></p>
                <span style="font-size: 16px; color: grey;">{{ item.replyTime }}</span></p>
            </div>
            <br>
            <el-button v-if="!questionInput" type="primary" @click="showQuestionInput"
                style="font-weight: bold; font-size: 16px; color:whitesmoke">我要提问</el-button>
            <el-input v-if="questionInput" v-model="newQuestion" type="textarea" placeholder="输入你的问题"
                style="margin-bottom: 20px; font-size: 16px;"></el-input>
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
            projectId: '1',
            isCollect: false,
            projectName: '气象防灾减灾宣讲',
            projectType: '1',
            projectIntro: '团队致力于发挥气象行业特色，常态化开展气象防灾减灾科普进社区、进校园公益项目，创办了独具特色的“气象科普”品牌。\n2022年，结合文明实践“一圈一带一群”建设，与徐汇区多个社区形成合作机制，定期为徐家汇商圈和社区居民开展科普讲座，惠及学生和市民千余人次，申报的“气象防灾减灾宣讲”入选为上海市文明实践百项重点项目。',
            latestTime: '2023-11-01',
            projectLeader: '张昊翔',
            teamId: '1',
            teamName: '计算机学院志愿服务队',
            discussionList: [
                { questionPoster: '张三', questionTime: '2023-01-01 19:00', question: '这个项目需要什么技能？', replyTime: '2023-01-02 19:00', reply: '不需要什么技能，只要你有热情就可以了。' },
                { questionPoster: '李四', questionTime: '2023-01-03 19:00', question: '这个项目需要什么技能？', replyTime: '2023-01-04 19:00', reply: '不需要什么技能。\n只要你有热情就可以了。' },
                { questionPoster: '王五', questionTime: '2023-01-05 19:00', question: '这个项目需要什么技能？', replyTime: '2023-01-06 19:00', reply: '不需要什么技能，只要你有热情就可以了。' },
            ],
            tutorialList: [
                { id: '1', time: '2023-01-01 19:00', title: '宣讲内容', tag: '培训', content: '最近小米14、华为mate60的销量让我彻底认清了市场高端的本质是营销，是爱国加持过去的华为冲高端，随便堆料高端直接就成了，我们这帮混数码圈的，经常把原因归结为：自研soc、核心技术但我们仔细反思，不对劲，国内真自研的东西不少，没有一个能吃上华为的待遇。\n以雷军旗下的东西为例子，wps消费者会嫌弃它广告多，澎湃s1正宗国产自研+中芯国际代工，性能不错，小米5c机器也便宜，但就是卖不出去但凡你们真的支持自研，多买点小米5c，小米也不会评估澎湃s2竞争力不足卖不掉给砍了你要说产品吧，至少小米12su是真独一档，从去年七月四号到十一月下旬四个多月时间是真正意义的独一档，是最近两年安卓最好的芯片，它流畅续航好温度低，还有碾压级的拍照水平拍照体验，以及改变了数码圈打法的徕卡影调（今年是人是鬼都在玩人文影调，去年这会还在比夜景亮度）它不仅仅配置高，而且生涯没有翻一点点车，再怎么米黑都没有从它身上挑出一点刺，堪称那个时代完美神机。\n如果高端真的看产品，小米这一次高端直接成了你说的很好，但小米12su卖的不行全生涯周期，12su小米商城评论只有18w，你要说高端成了，在坐各位都笑出了声既然自研和高端无关，产品做的好也和高端无关那到底什么和高端有关？到底要怎么做才能成为高端？无论怎么做无论产品多好，就是赢不了，这已经是事实摆在眼前了每一次做出好产品，销量都那么回事，每次都是“保持这个水准几代之后高端就成了”你扪心自问，你真的相信小米做出好产品，靠着粉丝自来水传播就能在未来某一天小米数字销量一千万两千万吗？\n可以说，按照数码圈的论调，小米的高端之路、高端形象已经彻底到头了，根本就赢不了碾压行业的产品不可能年年有，稍微犯点错就被踩到谷底这个世界上哪有从不翻车的手机厂？苹果没烧过主板吗？三星没爆炸过吗？华为p50、mate50、p60、mate60是靠产品力取胜的吗？买小米旗舰的，无非是死忠米粉和部分围观路人，这部分人是很有限的更多的人，连看都懒得看小米产品一眼，都懒得看就更不会花钱买了小米冲高四年多了，居然还有人问“小米是不是美国企业”你就这样怎么冲高？冲高真的是看产品吗？' },
                { id: '2', time: '2023-05-02 19:00', title: '注意事项', tag: '注意', content: '请大家注意安全。' },
                { id: '3', time: '2023-05-02 19:00', title: '注意事项', tag: '注意', content: '请大家注意安全。' },
                { id: '4', time: '2023-05-02 19:00', title: '注意事项', tag: '注意', content: '请大家注意安全。' },
                { id: '5', time: '2023-05-02 19:00', title: '注意事项', tag: '注意', content: '请大家注意安全。' },
            ],
            tutorialId: '',
            tutorialContent: false,
            questionInput: false,
            newQuestion: '',
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
        showRecruitmentStatus(latestTime) {
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
        showTutorialContent(id) {
            this.tutorialId = id;
            this.tutorialContent = true;
        },
        getTutorialTime() {
            let tutorial = this.tutorialList.find(item => item.id === this.tutorialId);
            if (!tutorial) return '';
            else return tutorial.time;
        },
        getTutorialTitle() {
            let tutorial = this.tutorialList.find(item => item.id === this.tutorialId);
            if (!tutorial) return '';
            else return tutorial.title;
        },
        getTutorialTag() {
            let tutorial = this.tutorialList.find(item => item.id === this.tutorialId);
            if (!tutorial) return '';
            else return tutorial.tag;
        },
        getTutorialContent() {
            let tutorial = this.tutorialList.find(item => item.id === this.tutorialId);
            if (!tutorial) return '';
            else return tutorial.content;
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
    margin-top: 20px;
}

.img-container {
    display: flex;
    width: 300px;
    height: 200px;
    margin-bottom: 30px;
    margin-left: 50px;
}

.content-container {
    display: flex;
    flex-direction: column;
    margin-top: 20px;
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
    margin-left: 30px;
    padding-top: 50px;
    padding-left: 30px;
    padding-right: 30px;
    font-size: 18px;
    border-left: 2px solid rgb(114, 110, 104, 0.2);
    overflow-x: hidden;
    overflow-y: auto;
    max-height: 400px;
}

.tutorial-container {
    width: 400px;
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
    margin-bottom: 20px;
}

.tutorial-content {
    font-size: 16px;
    color: #000;
}

.dialog-footer button:first-child {
    margin-right: 10px;
}
</style>