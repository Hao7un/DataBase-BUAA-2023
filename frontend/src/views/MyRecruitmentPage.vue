<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="my" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="join" @click="changeToJoinRecruitmentPage">
                    <span class="item-font" style="font-weight: bold;">参与招募</span>
                </el-menu-item>
                <el-menu-item index="my" @click="changeToMyRecruitmentPage">
                    <span class="item-font" style="font-weight: bold;">我的活动</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content-container">
            <h2>即将进行的活动</h2>
            <div v-for="item in futureRecruitmentList" :key="item.id">
                <div class="recruitment-container">
                    <div>
                        <h3>{{ item.projectName }}</h3>
                        <p>项目类型：{{ showProjectType(item.projectType) }}</p>
                        <p>活动时间：{{ item.startTime }} ~ {{ item.endTime }}</p>
                        <p>活动地点：{{ item.location }}</p>
                        <p>招募人数：{{ item.participantNumber }} / {{ item.maxNumber }}</p>
                        <p>志愿时长：{{ item.volunteerHour }}</p>
                        <p>招募类型：{{ showRecruitmentType(item.type) }}</p>
                    </div>
                </div>
            </div>

            <br>
            <h2>已经结束的活动</h2>
            <div v-for="item in pastRecruitmentList" :key="item.id">
                <div class="recruitment-container">
                    <div>
                        <h3>{{ item.projectName }}</h3>
                        <p>项目类型：{{ showProjectType(item.projectType) }}</p>
                        <p>活动时间：{{ item.startTime }} ~ {{ item.endTime }}</p>
                        <p>活动地点：{{ item.location }}</p>
                        <p>招募人数：{{ item.participantNumber }} / {{ item.maxNumber }}</p>
                        <p>志愿时长：{{ item.volunteerHour }}</p>
                        <p>招募类型：{{ showRecruitmentType(item.type) }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
export default {
    created() {
        this.axios.post('http://localhost:8000/', {
            userId: this.userId
        })
            .then(res => {
                console.log(res);
                if (res.data.code === 0) {
                    this.futureRecruitmentList = res.data.futureRecruitmentList;
                    this.pastRecruitmentList = res.data.pastRecruitmentList;
                }
            });
    },
    data() {
        return {
            futureRecruitmentList: [
                { id: "00008", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "00001", projectName: "志愿项目8", projectType: "1" },
                { id: "00009", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "2", maxNumber: "50", participantNumber: "30", projectId: "00002", projectName: "志愿项目9", projectType: "2" },
                { id: "00010", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "00003", projectName: "志愿项目10", projectType: "3" },
                { id: "00011", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "00004", projectName: "志愿项目11", projectType: "4" },
            ],
            pastRecruitmentList: [
                { id: "00001", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "2", maxNumber: "50", participantNumber: "30", projectId: "00001", projectName: "志愿项目1", projectType: "5" },
                { id: "00002", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "00002", projectName: "志愿项目2", projectType: "6" },
                { id: "00003", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "2", maxNumber: "50", participantNumber: "30", projectId: "00003", projectName: "志愿项目3", projectType: "1" },
                { id: "00004", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "00004", projectName: "志愿项目4", projectType: "2" },
                { id: "00005", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "2", maxNumber: "50", participantNumber: "30", projectId: "00005", projectName: "志愿项目5", projectType: "3" },
                { id: "00006", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "2", maxNumber: "50", participantNumber: "30", projectId: "00006", projectName: "志愿项目6", projectType: "5" },
                { id: "00007", startTime: "YYYY-MM-DD HH:MM", endTime: "YYYY-MM-DD HH:MM", location: "操场", volunteerHour: "5", type: "2", maxNumber: "50", participantNumber: "30", projectId: "00007", projectName: "志愿项目7", projectType: "4" },
            ],
        };
    },
    methods: {
        changeToJoinRecruitmentPage() {
            this.$router.push({
                path: '/recruitment/join'
            });
        },
        changeToMyRecruitmentPage() {
            this.$router.push({
                path: '/recruitment/my'
            });
        },
        showRecruitmentType(type) {
            switch (type) {
                case '1':
                    return '面向公共招募';
                case '2':
                    return '仅限团队内部';
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
    display: flex;
}

.sidebar-container {
    display: flex;
    width: 180px;
    flex-direction: column;
    padding-top: 20px;
    margin-left: 20px;
    height: 3000px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.content-container {
    display: flex;
    flex-direction: column;
    margin-left: 20px;
    margin-top: 20px;
}

.recruitment-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-top: 20px;
    margin-bottom: 20px;
    border-bottom: 2px solid rgb(114, 110, 104, 0.2);
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}
</style>
