<template>
    <div class="main-container">
        <div class="content-container">
            <div class="create-button-container">
                <v-btn size="x-large" @click="showCreateDialog">创建团队</v-btn>
            </div>
            <div class="table-container">
                <el-table :data="displayedTeamList" border style="width: 100%; height: 100%; border: 2px solid grey;" max-height="600">
                    <template #empty>
                        <p>无匹配数据</p>
                    </template>
                    <el-table-column prop="name" label="团队名称" width="250px" align="center">
                        <template #header>
                            <div>团队名称</div>
                            <el-input v-model="teamNameKey" clearable placeholder="输入团队名称"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="number" label="成员数量" width="250px" align="center" sortable></el-table-column>
                    <el-table-column prop="date" label="成立日期" width="250px" align="center" sortable></el-table-column>
                    <el-table-column prop="hours" label="总志愿时长" width="250px" align="center" sortable></el-table-column>
                    <el-table-column label="查看详情" width="250px" align="center">
                        <template #default="scope">
                            <el-button type="link" size="small" @click="viewTeamDetails(scope.row)">
                                <el-badge is-dot :hidden="scope.row.hasApplication === false">
                                    <span>点击查看</span>
                                </el-badge>
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div>
                <v-dialog v-model="createDialogVisible" width="auto">
                    <div class="create-dialog-container">
                        <div class="create-item">
                            <h3 style="margin-bottom: 15px;">团队名称</h3>
                            <el-input v-model="teamName" clearable></el-input>
                        </div>
                        <div class="create-item">
                            <h3 style="margin-bottom: 15px;">团队简介</h3>
                            <el-input type="textarea" v-model="teamIntro" clearable :maxlength="500" show-word-limit></el-input>
                        </div>
                        <div class="create-item">
                            <h3 style="margin-bottom: 15px;">上传团队头像</h3>
                            <el-upload
                                    class="avatar-uploader"
                                    action="#"
                                    :show-file-list="false"
                                    :auto-upload="false"
                                    :on-change="uploadFile"
                                >
                                <el-image v-if="imageUrl" :src="imageUrl" style="width: 218px; height: 218px" fit="contain" />
                                <el-icon v-if="!imageUrl"><Plus /></el-icon>
                            </el-upload>
                        </div>
                        <div style="text-align: center; margin-top: 30px;">
                            <el-button size="large" @click="handleCreateTeamSubmit">提交</el-button>
                        </div>
                    </div>
                </v-dialog>
            </div>
        </div>
    </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
    computed: {
        displayedTeamList() {
            let displayedTeamList = this.totalTeamList;
            if (this.teamNameKey != null) {
                displayedTeamList = displayedTeamList.filter(item => {
                    return item.name.includes(this.teamNameKey);
                })
            }
            return displayedTeamList;
        }
    },
    created() {
        this.fetch();
    },
    data() {
        return {
            fileToUpload: null,
            createDialogVisible: false,
            teamName: "",
            teamIntro: "",
            imageUrl: null,
            teamNameKey: "",
            totalTeamList: [
                {
                    teamId: "666",
                    name: "计算机学院团队",
                    number: 5,
                    date: "2023-11-21",
                    hours: 10,
                    hasApplication: false,
                },
                {
                    teamId: "888",
                    name: "软件学院团队",
                    number: 10,
                    date: "2023-11-20",
                    hours: 12,
                    hasApplication: true,
                }
            ],
        }

    },
    methods: {
        fetch() {
            const submitParams = {
                userId: this.$store.state.userId,
                
            };

            (async () => {
                await this.axios({
                    method: 'post',
                    url: 'http://localhost:8000/admin_get_all_teams',
                    data: submitParams,
                })
                .then(async (res) => {
                    console.log('获取管理团队列表');
                    console.log(res);
                    if (res.data.code === 0) {
                        console.log('请求成功');
                        this.totalTeamList = res.data.teamList;
                    } 
                    else {
                        console.log('请求失败, 错误码code不是0');
                    }
                });
            })();
        },
        changeToJoinTeamPage() {
            this.$router.push({
                path: '/team/join'
            })
        },
        changeToMyTeamPage() {
            this.$router.push({
                path: '/team/myteam'
            })
        },
        showCreateDialog() {
            this.createDialogVisible = true;
            console.log("显示创建团队对话");
        },
        handleRemovePicture() {
            this.imageUrl = "";
        },
        viewTeamDetails(row) {
            this.$router.push({
                path: '/admin/teaminfo',
                query: {
                    id: row.teamId,
                    name: row.name,
                    number: row.number,
                    hours: row.hours,
                    date: row.date,
                }
            })
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
        handleCreateTeamSubmit() {
            const formData = new FormData();
            formData.append("teamAvatar", this.fileToUpload);
            formData.append("userId", this.$store.state.userId);
            formData.append("teamName", this.teamName);
            formData.append("teamIntro", this.teamIntro);

            if (this.teamName === '') {
                this.createDialogVisible = false;
                ElMessageBox.alert("团队名不能为空", "注意", {
                    confirmButtonText: 'OK',
                    type: 'warning'
                }).then(() => {
                    this.createDialogVisible = true;
                })
                return;
            }
            
            const vm = this;
            (async () => {
                await vm.axios({
                    method: 'post',
                    url: 'http://localhost:8000/admin_create_team',
                    data: formData,
                })
                    .then(async(res) => {
                        console.log(res);
                        if (res.data.code === 0) {
                            console.log("创建团队成功");
                            ElMessage.success("创建团队成功");
                            // 刷新团队列表
                            vm.fetch();
                            vm.createDialogVisible = false;
                        }
                        else if (res.data.code === 1) {
                            console.log("团队名已被注册");
                            ElMessage.error("团队名已被注册");
                        }
                        else {
                            console.log("错误码code既不是0也不是1");
                        }
                    })
            })();

        }
    },
}
</script>

<style scoped>
.main-container {
    display: flex;
}

.create-button-container {
    display: flex;
    justify-content: center;
    margin-top: 30px;
}

.table-container {
    margin-top: 35px;
    height: 600px;
    width: 99%;
}

.sidebar-container {
    display: flex;
    width: 180px;
    height: 890px;
    flex-direction: column;
    padding-top: 20px;
    margin-left: 20px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.content-container {
    display: flex;
    flex-direction: column;
    margin-left: 250px;
}

.create-dialog-container {
    height: 650px;
    width: 500px;
    background: white;
    display: flex;
    flex-direction: column;
}

.create-item {
    margin-top: 40px;
    margin-left: 50px;
    width: 70%;
}

.avatar-uploader {
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px dashed black;
    width: 220px;
    height: 220px;
    
}

</style>