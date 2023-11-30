<template>
    <div class="project-management">
        <v-btn class="back-button" @click="handleBack">
            <template v-slot:prepend>
                <el-icon><Back /></el-icon>
            </template>
            返回
        </v-btn>
        <h2 class="title">项目详情</h2>
        <div class="header">
            <div class="project-avatar">
                <img src="../assets/images/project.png" id="avatar">
            </div>
            <el-divider direction="vertical" style="height: 200px;"></el-divider>
            <div class="project-info-container">
                <div class="project-info">
                    <h3 style="display: flex; justify-content: center; margin-bottom: 10px; font-weight: bold;">项目信息</h3>
                    <el-descriptions column="2" border>
                        <el-descriptions-item label="项目名称" width="150px">
                            <el-input placeholder="输入项目名称" v-model="projectName" clearable></el-input>
                        </el-descriptions-item>
                        <el-descriptions-item label="项目类别" width="150px">
                            <el-tag>{{ projectType }}</el-tag>
                        </el-descriptions-item>
                        <el-descriptions-item label="创建时间">
                            {{ createdDate }}
                        </el-descriptions-item>
                    </el-descriptions>
                </div>
                <div class="project-info-buttons">
                    <div class="project-info-button">
                        <el-badge :value="this.comments.length" :max="99">
                            <v-btn size="x-large" @click="viewComments" rounded="lg">查看评论</v-btn>
                        </el-badge>
                    </div>
                    <div class="project-info-button">
                        <v-btn size="x-large" @click="viewTutorial" rounded="sm">查看教程</v-btn>
                    </div>
                    <div class="project-info-button">
                        <v-btn size="x-large" @click="handleSave" rounded="xl">保存修改</v-btn>
                    </div>
                </div>
            </div>
        </div>
        <el-divider style="width: 90%; margin-left: 100px;" />
        <div class="content">
            <el-input type="textarea" v-model="projectIntro" placeholder="输入项目简介（不超过500字）" :autosize="{minRows: 5}" clearable :maxlength="500" show-word-limit></el-input>
        </div>
        <el-divider style="width: 90%; margin-left: 100px;" />
        <div class="footer">
            <div style="display: flex; justify-content: center; margin-bottom: 10px">
                <v-btn size="large" @click="viewCreateRecruitment">发布招募</v-btn>
            </div>
            <el-table :data="displayedRecruitments" style="width: 99%; margin: 0 auto;" border max-height="550" :cell-style="setCellStyle">
                <template #empty>
                    <p>无匹配数据</p>
                </template>
                <el-table-column prop="state" label="招募状态" align="center">
                    <template #header>
                        <div>招募状态</div>
                        <el-select v-model="statusKey" clearable placeholder="选择招募状态">
                            <el-option label="即将招募" key="即将招募" value="即将招募"></el-option>
                            <el-option label="招募中" key="招募中" value="招募中"></el-option>
                            <el-option label="招募结束" key="招募结束" value="招募结束"></el-option>
                        </el-select>
                    </template>
                </el-table-column>
                <el-table-column prop="location" label="活动地点" align="center">
                    <template #header>
                        <div>活动地点</div>
                        <el-input v-model="locationKey" clearable placeholder="输入活动地点"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="type" label="面向群体" align="center">
                    <template #header>
                        <div>面向群体</div>
                        <el-select v-model="typeKey" clearable placeholder="选择面向人群">
                            <el-option label="面向公共招募" key="面向公共招募" value="面向公共招募"></el-option>
                            <el-option label="仅限团队内部" key="仅限团队内部" value="仅限团队内部"></el-option>
                        </el-select>
                    </template>
                </el-table-column>
                <el-table-column prop="launchTime" label="发布时间" align="center" sortable></el-table-column>
                <el-table-column prop="deadline" label="招募结束时间" align="center" sortable></el-table-column>
                <el-table-column prop="startTime" label="活动开始时间" align="center" sortable></el-table-column>
                <el-table-column prop="endTime" label="活动结束时间" align="center" sortable></el-table-column>
                <el-table-column prop="hours" label="志愿时长" align="center" sortable></el-table-column>
                <el-table-column prop="number" label="招募人数上限" align="center" sortable></el-table-column>
            </el-table>
        </div>
        <div>
            <el-dialog v-model="createRecruitmentVisible" width="500px">
                <div class="create-recruitment-dialog-container">
                    <div class="create-item">
                        <h3 style="margin-bottom: 10px;">活动地点</h3>
                        <el-input v-model="location" clearable>
                            <template #prefix>
                                <el-icon><Location /></el-icon>
                            </template>
                        </el-input>
                    </div>
                    <div class="create-item">
                        <h3 style="margin-bottom: 10px;">活动开始时间</h3>
                        <el-date-picker
                            v-model="startTime"
                            type="datetime"
                            format="YYYY-MM-DD HH:mm"
                            value-format="YYYY-MM-DD HH:mm"
                            :disabled-date="disabledDates"
                            @focus="focus"
                        ></el-date-picker>
                    </div>
                    <div class="create-item">
                        <h3 style="margin-bottom: 10px;">活动结束时间</h3>
                        <el-date-picker
                            v-model="endTime"
                            type="datetime"
                            format="YYYY-MM-DD HH:mm"
                            value-format="YYYY-MM-DD HH:mm"
                            :disabled-date="disabledDates"
                            @focus="focus"
                    ></el-date-picker>
                    </div>
                    <div class="create-item">
                        <h3 style="margin-bottom: 10px;">招募结束时间</h3>
                        <el-date-picker
                            v-model="deadline"
                            type="datetime"
                            format="YYYY-MM-DD HH:mm"
                            value-format="YYYY-MM-DD HH:mm"
                            :disabled-date="disabledDates"
                            @focus="focus"
                    ></el-date-picker>
                    </div>
                    <div class="create-item">
                        <h3 style="margin-bottom: 10px;">面向群体</h3>
                        <el-radio-group v-model="type">
                            <el-radio label="1" border size="middle">面向公共招募</el-radio>
                            <el-radio label="2" border size="middle">仅限团队内部</el-radio>
                        </el-radio-group>
                    </div>
                    <div class="create-item">
                        <h3 style="margin-bottom: 10px;">招募人数上限</h3>
                        <el-input-number v-model="maxNumber" size="small" :min="1"></el-input-number>
                    </div>
                    <div class="create-item">
                        <h3 style="margin-bottom: 10px;">志愿时长</h3>
                        <el-input-number v-model="hours" size="small" :min="1"></el-input-number>
                    </div>
                    <div style="margin-left: 200px; margin-top: 30px; margin-bottom: 20px;">
                        <el-button size="large" @click="handleCreateRecruitmentSubmit">提交</el-button>
                    </div>
                </div>
            </el-dialog>
        </div>
        <div>
            <v-dialog v-model="createTutorialVisible" width="600px" style="z-index: 10000000;">
                <div class="create-tutorial-dialog-container">
                    <div class="create-item">
                        <h3 style="margin-bottom: 15px;">教程标题</h3>
                        <el-input v-model="tutorialTitle" clearable style="width: 70%;">
                            <template #prefix>
                                <el-icon><Postcard /></el-icon>
                            </template>
                        </el-input>
                    </div>
                    <div class="create-item">
                        <h3 style="margin-bottom: 15px;">教程标签</h3>
                        <el-input v-model="tutorialTag" clearable style="width: 70%;">
                            <template #prefix>
                                <el-icon><CollectionTag /></el-icon>
                            </template>
                        </el-input>
                    </div>
                    <div class="create-item">
                        <h3 style="margin-bottom: 15px;">教程内容</h3>
                        <el-input v-model="tutorialContent" type="textarea" clearable :autosize="{minRows: 12}" style="width: 70%;" show-word-limit :maxlength="500"></el-input>
                    </div> 
                    <div style="display: flex; justify-content: center; margin-bottom: 30px; margin-top: 40px">
                        <el-button @click="handleCreateTutorial">提交</el-button>
                    </div>
                </div>
            </v-dialog>
        </div>
        <div>
            <el-dialog v-model="viewTutorialsVisible" style="height: 550px; width: 750px; border: 2px solid black;" :modal="false">
                <div class="tutorial-topbar">
                    <v-btn size="large" @click="viewCreateTutorial">发布教程</v-btn>
                </div>
                <div class="tutorials-container">
                    <el-table :data="displayedTutorials" border>
                        <template #empty>
                            <p>无匹配数据</p>
                        </template>
                        <el-table-column prop="title" label="教程标题" align="center">
                            <template #header>
                                <div>教程标题</div>
                                <el-input v-model="tutorialNameKey" clearable placeholder="输入教程标题"></el-input>
                            </template>
                        </el-table-column>
                        <el-table-column prop="tag" label="标签" align="center">
                            <template #header>
                                <div>标签</div>
                                <el-input v-model="tutorialTagKey" clearable placeholder="输入标签"></el-input>
                            </template>
                            <template #default="scope">
                                <el-tag>{{ scope.row.tag }}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column prop="date" label="发布日期" align="center" sortable></el-table-column>
                        <el-table-column label="操作" align="center">
                            <template #default="scope">
                                <el-button @click="viewTutorialDetail(scope.row)" type="primary"><span style="color: white;">编辑</span></el-button>
                                <el-button @click="handleDeleteTutorial(scope.$index, scope.row)" type="warning"><span style="color: white;">删除</span></el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </el-dialog>
        </div>
        <div>
            <el-dialog v-model="viewTutorialDetailVisible" style="height: 550px; width: 750px; background-color: white;" @close="closeEditTutorialDialog">
                <div class="edit-tutorial-dialog-container">
                    <el-form>
                        <el-form-item label="教程标题： " style="margin-left: 50px;">
                            <el-input v-model="selectedTutorial.title" clearable style="width: 250px;"></el-input>
                        </el-form-item>
                        <el-form-item label="教程标签：" style="margin-left: 50px;">
                            <el-input v-model="selectedTutorial.tag" clearable style="width: 150px;"></el-input>
                        </el-form-item>
                        <div style="margin-left: 50px; margin-bottom: 10px; margin-top: 25px">教程内容：</div>
                        <el-input v-model="selectedTutorial.content" clearable type="textarea" :autosize="{minRows: 12}" style="width: 75%; margin-left: 100px" :maxlength="500" show-word-limit></el-input>
                    </el-form>
                </div>
            </el-dialog>
        </div>
        <div>
            <el-dialog v-model="viewCommentsVisible" :modal="false" style="border: 2px solid black; width: 600px;">
                <h2 style="text-align: center; margin-bottom: 10px;">提问清单</h2>
                <v-list>
                    <v-list-item
                        v-for="(item, i) in this.comments"
                        :key="i"
                        :value="item"
                        rounded="xl"
                        @click="handleReplyComment(item, i)"
                    >
                    <template v-slot:prepend>
                        <el-icon><QuestionFilled /></el-icon>
                        &nbsp; &nbsp;
                    </template>
                    <div style="display: flex; justify-content: space-between">
                        <div>{{ item.content }}</div>
                        <div>{{ item.posterName }} &nbsp; 提问于 &nbsp; {{ item.date }}</div>
                    </div>
                    </v-list-item>
                </v-list>
            </el-dialog>
        </div>
        <div>
            <el-dialog v-model="replyCommentVisible" style="width: 600px; height: 300px; margin-top: 470px;">
                <h3 style="display: flex; justify-content: center; margin-bottom: 10px">回复留言</h3>
                <div>问题：{{ this.selectedComment.content }}</div>
                <div style="margin-top: 15px">回复：
                    <el-input style="width: 550px; margin-top: 10px" type="textarea" v-model="replyContent" :maxlength="500" show-word-limit></el-input>
                </div>
                <el-button style="margin-left: 230px; margin-top: 25px;" @click="replyCommentSubmit">提交回复</el-button>
            </el-dialog>
        </div>
    </div>
    
</template>


<script>
import { ElMessage, ElMessageBox } from 'element-plus';
import store from '../store'

export default {
    computed: {
        recruitmentList() {
            let recruitmentList = [];
            for (let i = 0; i < this.recruitements.length; i++) {
                let item = this.recruitements[i];
                let element = {
                    state: "",
                    launchTime: item.launchTime,
                    deadline: item.deadline,
                    startTime: item.startTime,
                    endTime: item.endTime,
                    location: item.location,
                    type: item.type,
                    hours: item.hours,
                    number: item.number,
                }
                if (Date.now() < new Date(item.launchTime)) {
                    element.state = "即将招募";
                }
                else if (Date.now() < new Date(item.deadline)) {
                    element.state = "招募中";
                }
                else {
                    element.state = "招募结束";
                }
                recruitmentList.push(element);
            }
            return recruitmentList;
        },
        displayedRecruitments() {
            let displayedRecruitments = this.recruitmentList;
            if (this.typeKey != null && this.locationKey != null && this.statusKey != null) {
                displayedRecruitments = displayedRecruitments.filter(item => {
                    return item.state.includes(this.statusKey) && item.type.includes(this.typeKey) && item.location.includes(this.locationKey);
                })
            }
            return displayedRecruitments;
        },
        displayedTutorials() {
            let displayedTutorials = this.tutorials;
            if (this.tutorialNameKey != null && this.tutorialTagKey != null) {
                displayedTutorials = displayedTutorials.filter(item => {
                    return item.title.includes(this.tutorialNameKey) && item.tag.includes(this.tutorialTagKey);
                })
            }
            return displayedTutorials;
        },
    },
    created() {
        this.fetch();
        this.fetchPicture();
    },
    data() {
        return {
            fatherTeam: null,
            projectId: this.$route.query.id,
            projectName: this.$route.query.name,
            createdDate: this.$route.query.createdDate,
            projectType: this.$route.query.type,
            // 发布招募
            projectIntro: "",
            startTime: "",
            deadline: "",
            endTime: "",
            location: "",
            type: "",
            hours: "",
            maxNumber: 0,
            // 新建教程
            tutorialTitle: "",
            tutorialTag: "",
            tutorialContent: "",
            // 查看教程
            selectedTutorial: null,
            // 查看教程
            // 各种visible
            createRecruitmentVisible: false,
            viewTutorialsVisible: false,
            createTutorialVisible: false,
            viewTutorialDetailVisible: false,
            viewCommentsVisible: false,
            replyCommentVisible: false,
            selectedComment: null,
            // 各种visible
            // 搜索功能
            statusKey: "",
            replyContent: "",
            locationKey: "",
            typeKey: "",
            tutorialNameKey: "",
            tutorialTagKey: "",
            recruitements: [
                {
                    state: "",
                    launchTime: "2023-11-24 12:22",
                    deadline: "2023-11-24 13:00",
                    startTime: "2023-11-25 16:08",
                    endTime: "2023-11-25 17:00",
                    location: "校医院",
                    type: "面向公共招募",
                    hours: 16,
                    number: 10,
                },
                {
                    state: "",
                    launchTime: "2023-11-23 12:23",
                    deadline: "2023-11-28 14:00",
                    startTime: "2023-11-24 16:09",
                    endTime: "2023-11-24 18:00",
                    location: "田径场",
                    type: "面向公共招募",
                    hours: 4,
                    number: 20,
                },
                {
                    state: "",
                    launchTime: "2023-11-29 12:24",
                    deadline: "2023-11-23 15:00",
                    startTime: "2023-11-24 16:10",
                    endTime: "2023-11-24 17:30",
                    location: "晨兴音乐厅",
                    type: "仅限团队内部",
                    hours: 8,
                    number: 100,
                },
            ],
            comments: [
                {
                    questionId: "1",
                    date: "2023-11-24 10:45",
                    content: "这个项目大概每隔多久发一次招募？",
                    posterId: "1",
                    posterName: "王乐",
                },
                {
                    questionId: "2",
                    date: "2023-11-24 10:46",
                    content: "参加这个项目需要我学习些什么？",
                    posterId: "1",
                    posterName: "王乐",
                },
                {
                    questionId: "2",
                    date: "2023-11-24 10:47",
                    content: "什么时候结算上一次招募的志愿时长？",
                    posterId: "1",
                    posterName: "王乐",
                },
            ],
            tutorials: [
                {
                    id: "1",
                    title: "项目教程1",
                    content: "lorem",
                    date: "2023-11-24",
                    tag: "急救知识",
                },
                {
                    id: "2",
                    title: "项目教程2",
                    content: "lorem",
                    date: "2023-11-25",
                    tag: "礼仪规范",
                },
                {
                    id: "3",
                    title: "项目教程3",
                    content: "lorem",
                    date: "2023-11-24",
                    tag: "环境保护",
                },
                {
                    id: "4",
                    title: "项目教程4",
                    content: "lorem",
                    date: "2023-11-25",
                    tag: "文化尊重",
                },
                {
                    id: "5",
                    title: "项目教程5",
                    content: "lorem",
                    date: "2023-11-24",
                    tag: "心理健康",
                },
            ]

        }
    },
    methods: {
        fetchPicture() {
            const submitParams = {
                projectId: this.projectId,

            };
            this.axios({
                method: 'post',
                url: 'http://localhost:8000/get_project_avatar',
                data: submitParams,
            })
                .then((res) => {
                    console.log(res);
                    if (res.data) {
                        var avatar = document.getElementById('avatar');
                        avatar.src = "data:image/jpeg;base64," + res.data;
                    }
                    else {
                        console.log("获取项目图片失败, 错误码不是0");
                    }
                })
        },
        fetch() {
            const submitParams = {
                projectId: this.projectId,
            };

            this.axios({
                method: 'post',
                url: 'http://localhost:8000/admin_get_project_details',
                data: submitParams,
            })
                .then((res) => {
                    console.log(res);
                    if (res.data.code === 0) {
                        console.log("获取项目信息成功");
                        this.projectIntro = res.data.projectIntro;
                        this.comments = res.data.comments;
                        this.tutorials = res.data.tutorials;
                        this.recruitements = res.data.recruitments;
                    }
                    else {
                        console.log("获取失败, 错误码不是0");
                    }
                })

        },
        handleSave() {
            const submitParams = {
                projectId: this.projectId,
                newProjectName: this.projectName,
                newProjectIntro: this.projectIntro,

            };

            if (this.projectName === "") {
                ElMessageBox.alert("新的项目名不能为空", "注意", {
                    confirmButtonText: "OK",
                    type: "warning",
                }).then(() => {
                    return;
                })
                return;
            }

            this.axios({
                method: 'post',
                url: 'http://localhost:8000/admin_update_project_info',
                data: submitParams,
            })
                .then((res) => {
                    console.log(res);
                    if (res.data.code === 0) {
                        console.log("保存成功");
                        ElMessage.success("修改成功");
                    }
                    else {
                        console.log("保存失败, 错误码不是0");
                    }
                })
        },
        handleBack() {
            this.fatherTeam = JSON.parse(this.$route.query.fatherTeam);
            this.$router.push({
                path: '/admin/teaminfo',
                query: {
                    id: this.fatherTeam.id,
                    name: this.fatherTeam.name,
                    number: this.fatherTeam.size,
                    date: this.fatherTeam.establishmentDate,
                    hours: this.fatherTeam.totalHours,
                },
            })
        },
        setCellStyle({ row, column, rowIndex, columnIndex }) {
            if (row.state === "招募中" && columnIndex == 0) {
                return { 'color': 'green' }
            }
            else if (row.state === '即将招募' && columnIndex == 0) {
                return { 'color' : 'orange' }
            }
            else if (row.state === "招募结束" && columnIndex == 0) {
                return { 'color': 'red' }
            }
        },
        viewComments() {
            this.viewCommentsVisible = true;
        },
        viewCreateRecruitment() {
            this.createRecruitmentVisible = true;
        },
        viewTutorial() {
            this.viewTutorialsVisible = true;
        },
        disabledDates(date) {
            return date.getTime() < Date.now()
        },
        focus() {
            this.$nextTick(() => {
                document.getElementsByClassName('el-picker-panel__link-btn')[0].setAttribute('style', 'display:none');
            })
        },
        handleCreateRecruitmentSubmit() {
            console.log(typeof(this.type));
            if (this.startTime === "" || this.location === "" || this.type === "" || this.deadline === "" || this.endTime === "") {
                this.createRecruitmentVisible = false;
                ElMessageBox.alert("请填写完整的招募信息", "注意", {
                    confirmButtonText: 'OK',
                    type: 'warning'
                }).then(() => {
                    this.createRecruitmentVisible = true;
                })
            }
            else if (this.maxNumber === null) {
                this.createRecruitmentVisible = false;
                ElMessageBox.alert("招募人数上限不能为空", "注意", {
                    confirmButtonText: 'OK',
                    type: 'warning'
                }).then(() => {
                    this.createRecruitmentVisible = true;
                })
            }
            else if (this.hours === null) {
                this.createRecruitmentVisible = false;
                ElMessageBox.alert("志愿时长不能为空", "注意", {
                    confirmButtonText: 'OK',
                    type: 'warning'
                }).then(() => {
                    this.createRecruitmentVisible = true;
                })
            }
            else {
                const submitParams = {
                    projectId: this.projectId,
                    startTime: this.startTime,
                    deadline: this.deadline,
                    endTime: this.endTime,
                    location: this.location,
                    type: this.type,
                    hours: this.hours,
                    maxNumber: this.maxNumber,
                    message: {
                        title: "您收藏的项目发布了新的招募",
                        content: "您关注的 " + this.projectName + " 项目发布了新的招募, 招募开始时间为 " + startTime,
                    }
                };

                this.axios({
                    method: 'post',
                    url: 'http://localhost:8000/admin_create_recruitment',
                    data: submitParams,
                })
                    .then((res) => {
                        console.log(res);
                        if (res.data.code === 0) {
                            console.log("发布招募成功");
                            // 刷新招募列表
                            this.fetch();
                            this.createRecruitmentVisible = false;
                            ElMessage.success("创建成功")
                        }
                        else {
                            console.log("发布招募失败, 错误码不是0");
                        }
                    })
            }

        },
        viewCreateTutorial() {
            this.createTutorialVisible = true;
        },
        handleCreateTutorial() {
            if (this.tutorialTitle === "" || this.tutorialTag === "" || this.tutorialContent === "") {
                this.createTutorialVisible = false;
                ElMessageBox.alert("请填写完整的教程信息", "注意", {
                    confirmButtonText: "OK",
                    type: "warning",
                }).then(() => {
                    this.createTutorialVisible = true;
                })
            }
            else {
                const submitParams = {
                    projectId: this.projectId,
                    tutorialTitle: this.tutorialTitle,
                    tutorialTag: this.tutorialTag,
                    tutorialContent: this.tutorialContent,

                };
                this.axios({
                    method: 'post',
                    url: 'http://localhost:8000/admin_create_tutorial',
                    data: submitParams,
                })
                    .then((res) => {
                        console.log(res);
                        if (res.data.code === 0) {
                            console.log("创建教程成功");
                            // 刷新教程列表
                            this.fetch();
                            this.createTutorialVisible = false;
                        }
                        else {
                            console.log("创建教程失败, 错误码不是0");
                        }
                    })
            }
        },
        handleDeleteTutorial(index, row) {
            this.selectedTutorial = row;
            this.viewTutorialsVisible = false;
            ElMessageBox.confirm("确定删除该教程?", "注意", {
                confirmButtonText: '是',
                cancelButtonText: '否',
                type: "warning",
            }).then(() => {
                const submitParams = {
                    tutorialId: this.selectedTutorial.id,

                };

                this.axios({
                    method: 'post',
                    url: 'http://localhost:8000/admin_delete_tutorial',
                    data: submitParams,
                })
                    .then((res) => {
                        console.log(res);
                        if (res.data.code === 0) {
                            console.log("删除教程成功");
                            ElMessage.success("已删除");
                            this.tutorials.splice(index, 1);
                            this.fetch();
                            this.viewTutorialsVisible = true;
                        }
                        else {
                            console.log("删除教程失败, 错误码不是0");
                        }
                    })
            }).catch((error) => {
                console.log(error);
                ElMessage.success("取消删除");
                this.viewTutorialsVisible = true;
            })
        },
        viewTutorialDetail(row) {
            this.selectedTutorial = row;
            this.viewTutorialDetailVisible = true;
        },
        closeEditTutorialDialog() {
            if (this.selectedTutorial.title === "" || this.selectedTutorial.tag === "" || this.selectedTutorial.content === "") {
                this.viewTutorialDetailVisible = false;
                ElMessageBox.alert("请填写完整的教程信息", "注意", {
                    confirmButtonText: "OK",
                    type: "warning",
                }).then(() => {
                    // 还原教程列表
                    this.fetch();
                    this.viewTutorialDetailVisible = true;
                })
            }
            else {
                    const submitParams = {
                        tutorialId: this.selectedTutorial.id,
                        newTutorialTitle: this.selectedTutorial.title,
                        newTutorialTag: this.selectedTutorial.tag,
                        newTutorialContent: this.selectedTutorial.content,

                    }
                    
                    this.axios({
                        method: 'post',
                        url: 'http://localhost:8000/admin_update_tutorial',
                        data: submitParams,
                    })
                        .then((res) => {
                            console.log(res);
                            if (res.data.code === 0) {
                                console.log("修改教程成功");
                                this.viewTutorialDetailVisible = false;
                                // 刷新教程列表中的详细信息
                                this.fetch();
                                ElMessage.success("修改教程成功");
                            }
                            else {
                                console.log("修改教程失败, 错误码不是0");
                            }
                        })
            }
        },
        handleReplyComment(item, index) {
            this.replyCommentVisible = true;
            this.selectedComment = item;
        },
        replyCommentSubmit() {
            if (this.replyContent === "") {
                ElMessageBox.alert("回复内容不能为空", "注意", {
                    confirmButtonText: "OK",
                    type: 'warning',
                }).then(() => {
                    return;
                })
            }
            else {
                const submitParams = {
                    questionId: this.selectedComment.questionId,
                    userId: this.$store.state.userId,
                    replyContent: this.replyContent,
                    message: {
                        title: "您的问题得到了回复",
                        content: "您的问题' " + this.selectedComment.content + " '得到了回复: " + this.replyContent,
                    }
                };

                this.axios({
                    method: 'post',
                    url: 'http://localhost:8000/admin_reply_question',
                    data: submitParams,
                })
                    .then((res) => {
                        console.log(res);
                        if (res.data.code === 0) {
                            console.log("回复成功");
                            ElMessage.success("回复成功");
                            // 刷新评论列表
                            this.fetch();
                            this.replyCommentVisible = false;
                        }
                        else {
                            console.log("回复评论失败, 错误码不是0");
                        }
                    })
            }
        }
        
    }
}

</script>


<style scoped>
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
}

.back-button {
    margin-left: 25px;
    margin-top: 5px;
}

.title {
    display: flex;
    margin-bottom: 10px;
    justify-content: center;
}

.project-avatar {
    display: flex;
    justify-content: center;
    align-items: center;
    flex: 1;
}

.project-avatar img {
    max-width: 350px;
    max-height: 200px;
    width: auto;
    height: auto;
}


.project-info-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-right: 50px;
}

.project-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-right: 50px;
}

.project-info-buttons {
  display: flex;
  flex-direction: row;
  margin-top: 5px;
  margin-left: 60px;
  margin-top: 10px;
}

.project-info-button {
  margin-bottom: 5px;
  margin-right: 30px;
  margin-left: 30px;  
}

.content {
    margin-top: 20px;
    width: 80%;
    margin: 0 auto;
}

.footer {
  width: 80%;
  margin: 0 auto; 
}

.green-status {
  background: green;
  color: white;
  border-radius: 5px;
}

.grey-status {
  background: grey;
  color: white;
  border-radius: 5px;
}

.tutorial-topbar {
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
}

.tutorial-container {
    height: 500px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
}

.create-recruitment-dialog-container {
    display: flex;
    height: 750px;
    width: 300px;
    background-color: white;
    flex-direction: column;
}

.create-item {
    margin-top: 28px;
    margin-left: 50px;
    width: 99%;
}

.create-tutorial-dialog-container {
    display: flex;
    /* height: 99%;
    width: 99%; */
    background-color: white;
    flex-direction: column;
}

</style>