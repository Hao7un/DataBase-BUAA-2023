<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="list" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="info" @click="changeToTeamManagePage">
                    <span class="item-font" style="font-weight: bold;">团队详情</span>
                </el-menu-item>
                <el-menu-item index="list" @click="changeToProjectListPage">
                    <span class="item-font" style="font-weight: bold;">项目管理</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content-container">
            <v-btn class="back-button" @click="handleBack">
                <template v-slot:prepend>
                    <el-icon>
                        <Back />
                    </el-icon>
                </template>
                返回
            </v-btn>
            <div class="selector-container">
                <div class="left">
                    <el-input v-model="projectNameKey" placeholder="搜索项目名称" clearable size="large" style="width: 200px">
                        <template #prefix>
                            <el-icon>
                                <Open />
                            </el-icon>
                        </template>
                    </el-input>
                </div>
                <div class="middle">
                    <el-select v-model="projectTypeKey" placeholder="选择项目类别" clearable size="large">
                        <template #prefix>
                            <el-icon>
                                <FolderOpened />
                            </el-icon>
                        </template>
                        <el-option label="社区服务" key="社区服务" value="社区服务"></el-option>
                        <el-option label="科技科普" key="科技科普" value="科技科普"></el-option>
                        <el-option label="支教助学" key="支教助学" value="支教助学"></el-option>
                        <el-option label="体育赛事" key="体育赛事" value="体育赛事"></el-option>
                        <el-option label="大型演出" key="大型演出" value="大型演出"></el-option>
                        <el-option label="其它" key="其它" value="其它"></el-option>
                    </el-select>
                </div>
                <div class="right">
                    <el-switch v-model="projectSortKey" active-text="按日期升序排序" inactive-text="按日期降序排序">
                    </el-switch>
                </div>
            </div>
            <el-divider style="margin-left: 50px;"></el-divider>
            <div class="projects-container">
                <div style="display: flex; justify-content: center; margin-left: 50px;">
                    <v-btn size="large" @click="createProjectDialogVisible = true">创建项目</v-btn>
                </div>
                <div class="projects-list-container">
                    <el-card shadow="hover" v-for="project in displayedList" class="card">
                        <template #header>
                            <div style="display: flex; justify-content: center">
                                <span style="font-weight: bold; font-size: x-large; position: absolute;">{{
                                    project.name }}</span>
                                <span style="margin-left: 700px;">项目ID: {{ project.id }}</span>
                            </div>
                        </template>
                        <div style="display: flex; justify-content: space-between;">
                            <div style="width: 400px;">
                                <span><el-icon>
                                        <Clock />
                                    </el-icon>&nbsp; 创建时间: {{ project.createdDate }}</span>
                                &nbsp; &nbsp; &nbsp;
                                <span v-if="project.category === '1'" style="color: red;"><el-icon>
                                        <FolderOpened />
                                    </el-icon>&nbsp; 项目类别: 社区服务</span>
                                <span v-else-if="project.category === '2'" style="color: green;"><el-icon>
                                        <FolderOpened />
                                    </el-icon>&nbsp; 项目类别: 科技科普</span>
                                <span v-else-if="project.category === '3'" style="color: paleturquoise;"><el-icon>
                                        <FolderOpened />
                                    </el-icon>&nbsp; 项目类别: 支教助学</span>
                                <span v-else-if="project.category === '4'" style="color: orange;"><el-icon>
                                        <FolderOpened />
                                    </el-icon>&nbsp; 项目类别: 体育赛事</span>
                                <span v-else-if="project.category === '5'" style="color: pink;"><el-icon>
                                        <FolderOpened />
                                    </el-icon>&nbsp; 项目类别: 大型演出</span>
                                <span v-else style="color: blue;"><el-icon>
                                        <FolderOpened />
                                    </el-icon>&nbsp; 项目类别: 其它</span>
                            </div>
                            <el-button style="margin-right: 40px;" @click="viewProjectDetails(project.id)"><el-badge
                                    :hidden="project.hasComments === false" is-dot>查看详情</el-badge></el-button>
                        </div>
                    </el-card>
                </div>
            </div>
        </div>
    </div>
    <v-dialog v-model="createProjectDialogVisible" width="auto" max-height="1000">
        <div class="create-dialog-container">
            <div class="create-item">
                <h3 style="margin-bottom: 15px;">项目名称</h3>
                <el-input v-model="projectName" clearable style="width: 400px;">
                    <template #prefix>
                        <el-icon>
                            <Postcard />
                        </el-icon>
                    </template>
                </el-input>
            </div>
            <div class="create-item">
                <h3 style="margin-bottom: 15px;">项目简介</h3>
                <el-input type="textarea" v-model="projectIntro" clearable :maxlength="500" :autosize="{ minRows: 2 }"
                    show-word-limit style="width: 400px;"></el-input>
            </div>
            <div class="create-item">
                <h3 style="margin-bottom: 15px;">项目类别</h3>
                <el-radio-group v-model="projectType">
                    <el-radio label="1" border size="small">社区服务</el-radio>
                    <el-radio label="2" border size="small">科技科普</el-radio>
                    <el-radio label="3" border size="small">支教助学</el-radio>
                    <el-radio label="4" border size="small" style="margin-top: 8px;">体育赛事</el-radio>
                    <el-radio label="5" border size="small" style="margin-top: 8px;">大型演出</el-radio>
                    <el-radio label="6" border size="small" style="margin-top: 8px;">其它类别</el-radio>
                </el-radio-group>
            </div>
            <div class="create-item">
                <h3 style="margin-bottom: 15px;">上传项目图片</h3>
                <el-upload class="avatar-uploader" action="#" :show-file-list="false" :auto-upload="false"
                    :on-change="uploadFile">
                    <el-image v-if="imageUrl" :src="imageUrl" style="width: 190px; height: 190px" fit="contain" />
                    <el-icon v-if="!imageUrl">
                        <Plus />
                    </el-icon>
                </el-upload>

            </div>
            <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                <el-button size="large" @click="handleCreateProjectSubmit">提交</el-button>
            </div>
        </div>
    </v-dialog>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
    created() {
        this.fetch();
    },
    computed: {
        displayedList() {
            let displayedList = this.projects;
            let newProjectTypeKey = this.projectTypeKey === "社区服务" ? "1" : this.projectTypeKey === "科技科普" ? "2" : this.projectTypeKey === "支教助学" ? "3" : this.projectTypeKey === "体育赛事" ? "4" : this.projectTypeKey === "大型演出" ? "5" : this.projectTypeKey === "其它" ? "6" : "";
            if (this.projectNameKey != null && newProjectTypeKey != null) {
                displayedList = displayedList.filter(item => {
                    return item.name.includes(this.projectNameKey) && item.category.includes(newProjectTypeKey);
                })
            }

            if (this.projectSortKey === true) {
                displayedList = displayedList.sort((a, b) => {
                    const dateA = new Date(a.createdDate)
                    const dateB = new Date(b.createdDate)
                    return dateA - dateB;
                })
            }
            else {
                displayedList = displayedList.sort((a, b) => {
                    const dateA = new Date(a.createdDate)
                    const dateB = new Date(b.createdDate)
                    return dateB - dateA;
                })
            }
            return displayedList;
        }
    },
    data() {
        return {
            teamId: this.$route.query.teamId,
            projectNameKey: "",
            projectTypeKey: "",
            projectSortKey: "",
            createProjectDialogVisible: false,
            projectName: "",
            projectIntro: "",
            projectType: "",
            // 图片
            imageUrl: null,
            fileToUpload: null,
            projects: [
                // {
                //     id: "1",
                //     hasComments: true,
                //     name: "志愿项目1",
                //     category: "1",
                //     createdDate: "2023-11-17"
                // },
                // {
                //     id: "2",
                //     hasComments: false,
                //     name: "志愿项目2",
                //     category: "2",
                //     createdDate: "2023-11-18"
                // },
                // {
                //     id: "3",
                //     hasComments: false,
                //     name: "志愿项目3",
                //     category: "3",
                //     createdDate: "2023-11-19"
                // },
                // {
                //     id: "4",
                //     hasComments: false,
                //     name: "志愿项目4",
                //     category: "4",
                //     createdDate: "2023-11-20"
                // },
                // {
                //     id: "5",
                //     hasComments: false,
                //     name: "志愿项目5",
                //     category: "5",
                //     createdDate: "2023-11-21"
                // },
                // {
                //     id: "6",
                //     hasComments: false,
                //     name: "志愿项目6",
                //     category: "6",
                //     createdDate: "2023-11-27"
                // }
            ]
        }
    },
    methods: {
        fetch() {
            const submitParams = {
                teamId: this.teamId,
            };

            this.axios({
                method: 'post',
                url: 'http://localhost:8000/admin_get_team_projects',
                data: submitParams,
            })
                .then((res) => {
                    console.log("获取团队下的项目列表");
                    console.log(res);
                    if (res.data.code === 0) {
                        console.log("获取成功");
                        this.projects = res.data.projects;
                    }
                    else {
                        console.log("请求失败, 错误码不是0");
                    }
                })
        },
        viewProjectDetails(projectId) {
            this.$router.push({
                path: '/admin/project-info',
                query: {
                    teamId: this.teamId,
                    projectId: projectId
                }
            })
        },
        changeToProjectListPage() {
            this.$router.push({
                path: '/admin/project-list',
                query: {
                    teamId: this.teamId
                }
            })
        },
        changeToTeamManagePage() {
            this.$router.push({
                path: '/admin/team-info',
                query: {
                    teamId: this.teamId,
                }
            })
        },
        handleCreateProjectSubmit() {
            this.createProjectDialogVisible = false;
            if (this.projectName === "" || this.projectType === "" || this.projectIntro === "") {
                ElMessageBox.alert("请填写完整的项目信息", "注意", {
                    confirmButtonText: "OK",
                    type: "warning",
                })
                    .then(() => {
                        this.createProjectDialogVisible = true;
                    })
            }
            else {
                const formData = new FormData();
                formData.append("projectAvatar", this.fileToUpload);
                // console.log(formData.get("projectAvatar"));
                formData.append("teamId", this.teamId);
                formData.append("projectName", this.projectName);
                formData.append("projectIntro", this.projectIntro);
                formData.append("projectType", this.projectType);

                this.axios({
                    method: 'post',
                    url: 'http://localhost:8000/admin_create_project',
                    data: formData,
                })
                    .then((res) => {
                        console.log(res);
                        if (res.data.code === 0) {
                            console.log("创建项目成功");
                            // 刷新项目列表
                            this.fetch();
                            ElMessage.success("成功创建项目");
                        }
                        else if (res.data.code === 1) {
                            ElMessage.error("项目名已被注册");
                            console.log("项目名称重复");
                        }
                        else {
                            console.log("创建失败, 错误码不是 0 或 1");
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
        handleBack() {
            this.$router.push({
                path: '/admin/manage'
            })
        },
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

.back-button {
    margin-left: 25px;
    margin-top: 25px;
    font-weight: bold;
    font-size: 15px;
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.selector-container {
    width: 1200px;
    margin-left: 100px;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.projects-list-container {
    margin-left: 230px;
    margin-bottom: 50px;
    width: 70%;
}

.card {
    margin-top: 15px;
}

.create-dialog-container {
    display: flex;
    height: 800px;
    width: 500px;
    background: white;
    flex-direction: column;
}

.create-item {
    margin-top: 50px;
    margin-left: 50px;
    width: 90%;
}

.avatar-uploader {
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px dashed black;
    width: 188px;
    height: 188px;
}
</style>