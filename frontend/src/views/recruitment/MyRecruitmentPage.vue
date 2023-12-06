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
            <div class="switch-container">
                <el-radio-group v-model="selectedActivity">
                    <el-radio label="upcoming" size="large" style="font-weight: bold;" border>即将进行的活动</el-radio>
                    <el-radio label="past" size="large" style="font-weight: bold;" border>已经结束的活动</el-radio>
                </el-radio-group>
                <div v-if="selectedActivity === 'past'" style="margin-left: 100px;">
                    只看本学期<el-switch v-model="onlySemester" style="padding-left: 10px;" />
                </div>
            </div>
            <div v-if="selectedActivity === 'upcoming'" v-for="item in futureRecruitmentList" :key="item.id">
                <div class="recruitment-container">
                    <div>
                        <el-button text><span class="project-name" @click="changeToProjectInfoPage(item.projectId)">
                                {{ item.projectName }}
                            </span></el-button>
                        <p>项目类型：{{ showProjectType(item.projectType) }}</p>
                        <p>活动时间：{{ item.startTime }} ~ {{ item.endTime }}</p>
                        <p>活动地点：{{ item.location }}</p>
                        <p>招募人数：{{ item.participantNumber }} / {{ item.maxNumber }}</p>
                        <p>志愿时长：{{ item.volunteerHour }}</p>
                        <p>招募类型：{{ showRecruitmentType(item.type) }}</p>
                    </div>
                </div>
            </div>

            <div v-else v-for="item in pastRecruitmentList" :key="item.id">
                <div class="recruitment-container">
                    <div>
                        <el-button text><span class="project-name" @click="changeToProjectInfoPage(item.projectId)">
                                {{ item.projectName }}
                            </span></el-button>
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
        this.axios.post('http://localhost:8000/user_get_my_recruitments', {
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
            selectedActivity: 'upcoming',
            onlySemester: false,
            futureRecruitmentList: [
                { id: "10", startTime: "2023-12-26 19:00", endTime: "2023-12-26 21:00", location: "操场", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "10", projectName: "志愿项目10", projectType: "1" },
                { id: "9", startTime: "2023-12-11 19:00", endTime: "2023-12-11 21:00", location: "新主楼G1000", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "9", projectName: "志愿项目9", projectType: "2" },
                { id: "8", startTime: "2023-12-25 19:00", endTime: "2023-12-25 21:00", location: "操场", volunteerHour: "5", type: "2", maxNumber: "50", participantNumber: "30", projectId: "3", projectName: "志愿项目3", projectType: "3" },
                { id: "7", startTime: "2023-12-02 19:00", endTime: "2023-12-02 21:00", location: "操场", volunteerHour: "5", type: "2", maxNumber: "50", participantNumber: "50", projectId: "2", projectName: "志愿项目2", projectType: "4" },
                { id: "6", startTime: "2023-12-01 19:00", endTime: "2023-12-01 21:00", location: "操场", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "1", projectName: "志愿项目1", projectType: "5" },
            ],
            pastRecruitmentList: [
                { id: "5", startTime: "2023-12-26 19:00", endTime: "2023-12-26 21:00", location: "操场", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "5", projectName: "志愿项目5", projectType: "1" },
                { id: "4", startTime: "2023-12-11 19:00", endTime: "2023-12-11 21:00", location: "新主楼G1000", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "4", projectName: "志愿项目4", projectType: "2" },
                { id: "3", startTime: "2023-12-25 19:00", endTime: "2023-12-25 21:00", location: "操场", volunteerHour: "5", type: "2", maxNumber: "50", participantNumber: "30", projectId: "3", projectName: "志愿项目3", projectType: "3" },
                { id: "2", startTime: "2023-12-02 19:00", endTime: "2023-12-02 21:00", location: "操场", volunteerHour: "5", type: "2", maxNumber: "50", participantNumber: "50", projectId: "2", projectName: "志愿项目2", projectType: "4" },
                { id: "1", startTime: "2023-12-01 19:00", endTime: "2023-12-01 21:00", location: "操场", volunteerHour: "5", type: "1", maxNumber: "50", participantNumber: "30", projectId: "1", projectName: "志愿项目1", projectType: "5" },
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
        changeToProjectInfoPage(id) {
            this.$store.commit("setActiveMenu", "project");
            this.$store.commit("setLastMenu", "recruit");
            console.log('projectId:', id);
            this.$router.push({
                name: 'projectInfo',
                params: { projectId: id }
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
    height: auto;
    min-height: 750px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.content-container {
    display: flex;
    flex-direction: column;
    margin-left: 80px;
    margin-top: 50px;
}

.switch-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 20px;
}

.recruitment-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-top: 20px;
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 2px solid rgb(114, 110, 104, 0.2);
}

.project-name {
    font-weight: bold;
    font-size: 20px;
    color: #110f0f;
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}
</style>
