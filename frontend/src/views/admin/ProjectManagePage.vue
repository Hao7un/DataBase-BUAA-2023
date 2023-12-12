<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="info" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="info" @click="changeToProjectManagePage">
                    <span class="item-font" style="font-weight: bold;">项目详情</span>
                </el-menu-item>
                <el-menu-item index="list" @click="changeToRecruitmentManangePage">
                    <span class="item-font" style="font-weight: bold;">招募管理</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="project-management">
            <v-btn class="back-button" @click="handleBack">
                <template v-slot:prepend>
                    <el-icon>
                        <Back />
                    </el-icon>
                </template>
                返回
            </v-btn>
            <h2 class="title">项目详情</h2>
            <div class="header">
                <div class="project-avatar">
                    <el-tooltip placement="right" content="更换头像" effect="light">
                        <img src="../../assets/images/project.png" id="avatar" @click="setAvatarVisible = true" style="box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); padding: 10px;">
                    </el-tooltip>
                </div>
                <el-divider direction="vertical" style="height: 200px;"></el-divider>
                <div class="project-info-container">
                    <div class="project-info">
                        <h3 style="display: flex; justify-content: center; margin-bottom: 10px; font-weight: bold;">项目信息
                        </h3>
                        <el-descriptions column="2" border>
                            <el-descriptions-item label="项目名称" width="200px" align="center">
                                <el-input placeholder="输入项目名称" v-model="projectName" clearable></el-input>
                            </el-descriptions-item>
                            <el-descriptions-item label="项目类别" width="100px" align="center">
                                <el-tag v-if="projectType === '1'">社区服务</el-tag>
                                <el-tag v-else-if="projectType === '2'">科技科普</el-tag>
                                <el-tag v-else-if="projectType === '3'">支教助学</el-tag>
                                <el-tag v-else-if="projectType === '4'">体育赛事</el-tag>
                                <el-tag v-else-if="projectType === '5'">大型演出</el-tag>
                                <el-tag v-else>其它类别</el-tag>
                            </el-descriptions-item>
                            <el-descriptions-item label="创建时间" align="center">
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
                <el-input type="textarea" v-model="projectIntro" placeholder="输入项目简介(不超过500字)" :rows="15" clearable
                    :maxlength="500" show-word-limit style="font-size: 20px;"></el-input>
            </div>
            <div style="font-size: 12px; display: flex; justify-content: center; margin-top: 30px;">
                Copyright BUAA Volunteer Service © 2023. All rights reserved.
              </div>
            <div>
                <v-dialog v-model="createTutorialVisible" width="550px">
                    <div class="create-tutorial-dialog-container">
                        <div class="create-item">
                            <h3 style="margin-bottom: 15px;">教程标题</h3>
                            <el-input v-model="tutorialTitle" clearable style="width: 70%;">
                                <template #prefix>
                                    <el-icon>
                                        <Postcard />
                                    </el-icon>
                                </template>
                            </el-input>
                        </div>
                        <div class="create-item">
                            <h3 style="margin-bottom: 15px;">教程标签</h3>
                            <el-input v-model="tutorialTag" clearable style="width: 70%;">
                                <template #prefix>
                                    <el-icon>
                                        <CollectionTag />
                                    </el-icon>
                                </template>
                            </el-input>
                        </div>
                        <div class="create-item">
                            <h3 style="margin-bottom: 15px;">教程内容</h3>
                            <el-input v-model="tutorialContent" type="textarea" clearable :autosize="{ minRows: 12 }"
                                style="width: 70%;" show-word-limit :maxlength="500"></el-input>
                        </div>
                        <div style="display: flex; margin-bottom: 30px; margin-top: 40px;">
                            <el-button @click="handleCreateTutorial">提交</el-button>
                        </div>
                    </div>
                </v-dialog>
            </div>
        </div>
        <div>
            <v-dialog v-model="viewTutorialsVisible">
                <div style="height: 600px; width: 800px; border: 2px solid black; background: white; margin-left: 450px;">
                    <div style="margin-left: 715px; margin-top: 10px;">
                        <v-btn @click="viewTutorialsVisible = !viewTutorialsVisible">退出</v-btn>
                    </div>
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
                                    <el-button @click="viewTutorialDetail(scope.row)" type="primary"><span
                                            style="color: white;">编辑</span></el-button>
                                    <el-button @click="handleDeleteTutorial(scope.$index, scope.row)" type="warning"><span
                                            style="color: white;">删除</span></el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
            </v-dialog>
        </div>
        <div>
            <v-dialog v-model="viewTutorialDetailVisible">
                <div style="height: 600px; width: 800px; background-color: white; padding-top: 50px; margin-left: 450px;">
                    <div class="edit-tutorial-dialog-container">
                        <el-form>
                            <el-form-item label="教程标题： " style="margin-left: 50px;">
                                <el-input v-model="selectedTutorial.title" clearable style="width: 250px;"></el-input>
                            </el-form-item>
                            <el-form-item label="教程标签：" style="margin-left: 50px;">
                                <el-input v-model="selectedTutorial.tag" clearable style="width: 150px;"></el-input>
                            </el-form-item>
                            <div style="margin-left: 50px; margin-bottom: 10px; margin-top: 25px">教程内容：</div>
                            <el-input v-model="selectedTutorial.content" clearable type="textarea" :autosize="{ minRows: 12 }"
                                style="width: 600px; margin-left: 100px" :maxlength="500" show-word-limit></el-input>
                        </el-form>
                    </div>
                    <div style="display: flex; justify-content: center; margin-top: 40px;"><v-btn
                            @click="closeEditTutorialDialog">编辑完成</v-btn></div>
                </div>
            </v-dialog>
        </div>
        <div>
            <v-dialog v-model="viewCommentsVisible">
                <div style="background-color: white; width: 800px; border: 2px solid black; margin-left: 400px;">
                    <h2 style="text-align: center; margin-bottom: 20px; margin-top: 20px;">提问清单</h2>
                    <v-list>
                        <v-list-item v-for="(item, i) in this.comments" :key="i" :value="item" rounded="xl"
                            @click="handleReplyComment(item, i)">
                            <template v-slot:prepend>
                                <el-icon>
                                    <QuestionFilled />
                                </el-icon>
                                &nbsp; &nbsp;
                            </template>
                            <div style="display: flex; justify-content: space-between">
                                <div>{{ item.content }}</div>
                                <div>{{ item.posterName }} &nbsp; 提问于 &nbsp; {{ item.date }}</div>
                            </div>
                        </v-list-item>
                    </v-list>
                </div>
            </v-dialog>
        </div>
    </div>
    <div>
        <v-dialog v-model="replyCommentVisible" style="margin-left: 500px; margin-bottom: 200px;">
            <div style="width: 600px; height: 300px; margin-top: 470px; background: white;">
                <div style="margin-left: 520px; margin-top: 10px">
                    <v-btn
                        @click="replyCommentVisible = !replyCommentVisible; viewCommentsVisible = !viewCommentsVisible">取消</v-btn>
                </div>
                <h3 style="display: flex; justify-content: center; margin-bottom: 10px;">回复留言</h3>
                <div style="margin-left: 15px;">问题：{{ this.selectedComment.content }}</div>
                <div style="margin-top: 15px; margin-left: 15px;">回复：
                    <el-input style="width: 550px; margin-top: 10px" type="textarea" v-model="replyContent" :maxlength="500"
                        show-word-limit></el-input>
                </div>
                <el-button style="margin-left: 250px; margin-top: 25px; margin-bottom: 10px;"
                    @click="replyCommentSubmit">提交回复</el-button>
            </div>
        </v-dialog>
    </div>
    <div>
        <v-dialog v-model="setAvatarVisible">
            <div class="setAvatar-container">
                <el-button @click="setAvatarVisible = false" style="margin-top: 10px; margin-left: 200px">退出</el-button>
                <h3 style="margin-bottom: 20px; margin-top: 20px;">上传新头像</h3>
                <el-upload class="avatar-uploader" action="#" :show-file-list="false" :auto-upload="false"
                    :on-change="uploadFile">
                    <el-image v-if="imageUrl" :src="imageUrl" style="width: 218px; height: 218px" fit="contain" />
                    <el-icon v-if="!imageUrl">
                        <Plus />
                    </el-icon>
                </el-upload>
                <el-button @click="handleSetProjectAvatarSubmit" size="large" style="margin-top: 30px;">点击上传</el-button>
            </div>
        </v-dialog>
    </div>
</template>


<script>
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
    computed: {
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
            teamId: this.$route.query.teamId,
            projectId: this.$route.query.projectId,
            projectName: "",
            createdDate: "",
            projectIntro: "",
            projectType: "",
            // 新建教程
            tutorialTitle: "",
            tutorialTag: "",
            tutorialContent: "",
            // 查看教程
            selectedTutorial: null,
            // 查看教程
            // 各种visible
            viewTutorialsVisible: false,
            createTutorialVisible: false,
            viewTutorialDetailVisible: false,
            viewCommentsVisible: false,
            replyCommentVisible: false,
            selectedComment: null,
            setAvatarVisible: false,
            // 各种visible
            // 搜索功能
            replyContent: "",
            tutorialNameKey: "",
            tutorialTagKey: "",
            // 头像
            imageUrl: null,
            fileToUpload: null,
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
                        console.log("获取项目图片失败");
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
                        this.projectName = res.data.projectName;
                        this.projectType = res.data.projectType;
                        this.projectIntro = res.data.projectIntro;
                        this.createdDate = res.data.createdDate;
                        this.comments = res.data.comments;
                        this.tutorials = res.data.tutorials;
                    }
                    else {
                        console.log("获取失败, 错误码不是0");
                    }
                })

        },
        changeToProjectManagePage() {
            this.$router.push({
                path: '/admin/projectinfo',
                query: {
                    projectId: this.projectId,
                    teamId: this.teamId,
                }
            })
        },
        changeToRecruitmentManangePage() {
            this.$router.push({
                path: '/admin/recruitment',
                query: {
                    projectId: this.projectId,
                    projectName: this.projectName,
                    teamId: this.teamId,
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
                    else if (res.data.code === 1) {
                        console.log("保存失败, 项目名重复");
                        ElMessage.error("修改失败, 项目名称已被使用");
                        this.fetch();
                    }
                    else {
                        console.log("保存失败, 错误码不是0");
                    }
                })
        },
        handleBack() {
            this.$router.push({
                path: '/admin/projectlist',
                query: {
                    teamId: this.teamId,
                },
            })
        },
        viewComments() {
            this.viewCommentsVisible = true;
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
        viewCreateTutorial() {
            this.createTutorialVisible = true;
        },
        handleCreateTutorial() {
            if (this.tutorialTitle === "" || this.tutorialTag === "" || this.tutorialContent === "") {
                this.createTutorialVisible = false;
                this.viewTutorialsVisible = false;
                ElMessageBox.alert("请填写完整的教程信息", "注意", {
                    confirmButtonText: "OK",
                    type: "warning",
                }).then(() => {
                    this.createTutorialVisible = true;
                })
            }
            else {
                this.viewTutorialsVisible = true;
                this.createTutorialVisible = false;
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
                this.viewTutorialsVisible = false;
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
                this.viewTutorialDetailVisible = false;
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
            this.viewCommentsVisible = false;
            this.selectedComment = item;
        },
        replyCommentSubmit() {
            if (this.replyContent === "") {
                this.replyCommentVisible = false;
                ElMessageBox.alert("回复内容不能为空", "注意", {
                    confirmButtonText: "OK",
                    type: 'warning',
                }).then(() => {
                    this.viewCommentsVisible = true;
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
        },
        uploadFile(file) {
            const isJPG = file.raw.type === 'image/jpeg';
            const isPNG = file.raw.type === 'image/png';
            if (!isJPG && !isPNG) {
                ElMessage.error("只能上传JPG或PNG格式的文件");
                return false;
            }
            else if (file.size / 1024 / 1024 > 2) {
                ElMessage.error("图片大小不能超过2MB");
                return false;
            }
            else {
                this.imageUrl = URL.createObjectURL(file.raw);
                this.fileToUpload = file.raw;
                return true;
            }
        },
        handleSetProjectAvatarSubmit() {
            const formData = new FormData();
            formData.append("projectAvatar", this.fileToUpload);
            formData.append("projectId", this.projectId);

            this.axios({
                method: 'post',
                url: 'http://localhost:8000/upload_project_avatar',
                data: formData
            })
                .then((res) => {
                    console.log(res);
                    // 刷新头像
                    this.fetchPicture();
                    this.setAvatarVisible = false;
                })
        }

    }
}

</script>


<style scoped>
.main-container {
    display: flex;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 40px;
}

#avatar:hover {
    cursor: pointer;
}

.sidebar-container {
    display: flex;
    width: 205px;
    flex-direction: column;
    padding-top: 20px;
    margin-left: 20px;
    min-height: 900px;
    height: auto;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.project-management {
    height: 1000px;
    width: 100%;
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.back-button {
    margin-left: 25px;
    margin-top: 25px;
    font-weight: bold;
    font-size: 15px;
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

.tutorial-topbar {
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    background: white;
}

.tutorial-container {
    height: 500px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    background: white;
}

.create-item {
    margin-top: 28px;
    margin-left: 50px;
    width: 99%;
}

.create-tutorial-dialog-container {
    display: flex;
    height: 99%;
    width: 80%;
    background-color: white;
    flex-direction: column;
}

.edit-tutorial-dialog-container {
    display: flex;
}

.avatar-uploader {
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px dashed black;
    width: 220px;
    height: 220px;

}

.setAvatar-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: white;
    height: 450px;
    width: 300px;
    margin-left: 700px;
}
</style>