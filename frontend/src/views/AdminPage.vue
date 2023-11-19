<template>
    <div class="main-container">

        <div class="content-container">
            <div class="create-button-container">
                <v-btn size="x-large" @click="showCreateDialog">创建团队</v-btn>
            </div>
            <div class="table-container">
                <el-table :data="totalTeamList" border style="width: 100%; border: 2px solid grey;" max-height="600">
                    <el-table-column prop="name" label="团队名称" width="250px" align="center"></el-table-column>
                    <el-table-column prop="number" label="成员数量" width="250px" align="center"></el-table-column>
                    <el-table-column prop="date" label="成立日期" width="250px" align="center"></el-table-column>
                    <el-table-column prop="hours" label="总志愿时长" width="250px" align="center"></el-table-column>
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
                            <h3 style="margin-bottom: 20px;">团队名称</h3>
                            <el-input v-model="teamName" clearable></el-input>
                        </div>
                        <div class="create-item">
                            <h3 style="margin-bottom: 20px;">团队简介</h3>
                            <el-input type="textarea" v-model="teamIntro" clearable :maxlength="500" show-word-limit></el-input>
                        </div>
                        <div class="create-item">
                            <h3 style="margin-bottom: 20px;">上传团队头像</h3>
                                <el-upload
                                    class="upload-container"
                                    list-type="picture-card"
                                    action="#"
                                    :auto-upload="false"
                                    :show-file-list="true"
                                    :on-success="handlePictureSuccess"
                                    :before-upload="beforePictureUpload"
                                    limit=1
                                >
                                </el-upload>
                        </div>
                        <div style="text-align: center; margin-top: 50px;">
                            <el-button size="large" @click="handleCreateTeamSubmit">提交</el-button>
                        </div>
                    </div>
                </v-dialog>
            </div>
        </div>
    </div>
</template>

<script>
import store from '../store'
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
    created() {
        // 根据试验，应该可以在created中调用methods中定义的方法
        this.fetch();
    },
    data() {
        return {
            createDialogVisible: false,
            teamName: "",
            teamIntro: "",
            imageURL: null,
            totalTeamList: [
            ],
        }

    },
    methods: {
        // 这里尝试过，应该可以在created中调用methods中定义的方法
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
        handlePictureSuccess(response, uploadFile) {
            this.imageURL = URL.createObjectURL(uploadFile.raw);
            console.log(this.imageURL);
        },
        beforePictureUpload(rawFile) {
            if (rawFile.type !== 'image/jpeg') {
                ElMessage.error("请上传JPG格式的图片");
                return false;
            }
            else if (rawFile.size / 1024 / 1024 > 2) {
                ElMessage.error("图片大小不得超过2MB");
                return false;
            }
            console.log(this.imageURL);
            return true;
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
        handleCreateTeamSubmit() {
            const submitParams = {
                userId: this.$store.state.userId,
                teamName: this.teamName,
                teamIntro: this.teamIntro,
                // 暂时不能上传图片
            }
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
                    data: submitParams,
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
    margin-left: 350px;
}

.create-dialog-container {
    height: 650px;
    width: 500px;
    background: white;
    display: flex;
    flex-direction: column;
}

.create-item {
    margin-top: 50px;
    margin-left: 50px;
    width: 70%;
}


</style>