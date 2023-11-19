<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="password">
                <el-menu-item index="info" @click="changeToUserInfoPage">
                    <span class="item-font" style="font-weight: bold;">个人信息</span>
                </el-menu-item>
                <el-menu-item index="password" @click="changeToPasswordPage">
                    <span class="item-font" style="font-weight: bold;">修改密码</span>
                </el-menu-item>
                <el-menu-item index="volunteerHours" @click="changeToVolunteerHoursPage">
                    <span class="item-font" style="font-weight: bold;">志愿统计</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content-container">
            <label class="font">旧密码：</label>
            <el-input v-model="oldPassword" type="password" placeholder="请输入旧密码" maxlength="64" clearable show-password
                class="mb-3" />

            <label class="font">新密码：</label>
            <el-input v-model="newPassword" type="password" placeholder="请输入新密码" maxlength="64" clearable show-password
                class="mb-3" />

            <label class="font">验证新密码：</label>
            <el-input v-model="confirmPassword" type="password" placeholder="请再次输入新密码" maxlength="64" clearable
                show-password />

            <div style="margin-top: 30px;">

                <el-button type="primary" round size="large" @click="checkPassword">
                    <span style="font-weight: bold; font-size: 15px; color:whitesmoke">完成</span></el-button>
            </div>

            <el-dialog v-model="dialogVisible" title="注意" width="30%" align-center center draggable>
                <span class="text-font">你的密码将被修改。</span>
                <template #footer>
                    <span class="dialog-footer">
                        <el-button @click="dialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="editPassword">
                            <span style="color:whitesmoke">确认</span>
                        </el-button>
                    </span>
                </template>
            </el-dialog>
        </div>



    </div>
</template>

<script>
import { ElMessage } from 'element-plus'


export default {
    data() {
        return {
            oldPassword: '',
            newPassword: '',
            confirmPassword: '',
            dialogVisible: false
        }
    },
    methods: {
        changeToUserInfoPage() {
            this.$router.push({
                path: '/user/info'
            })
        },
        changeToPasswordPage() {
            this.$router.push({
                path: '/user/password'
            })
        },
        changeToVolunteerHoursPage() {
            this.$router.push({
                path: '/user/volunteer-hours'
            })
        },
        checkPassword() {
            if (this.oldPassword != this.$store.state.password) {
                ElMessage.error('旧密码错误');
                this.oldPassword = '';
                this.newPassword = '';
                this.confirmPassword = '';
            } else if (this.newPassword == '') {
                ElMessage.error('新密码不能为空');
            } else if (this.newPassword.length < 6) {
                ElMessage.error('新密码长度不能小于6位');
                this.newPassword = '';
                this.confirmPassword = '';
            } else if (this.newPassword == this.oldPassword) {
                ElMessage.error('新密码不能与旧密码相同');
                this.newPassword = '';
                this.confirmPassword = '';
            } else if (this.newPassword != this.confirmPassword) {
                ElMessage.error('两次输入的新密码不一致');
                this.confirmPassword = '';
            } else {
                this.dialogVisible = true;
            }
        },
        editPassword() {
            this.axios.post('http://localhost:5173/user/password', {
                userId: this.$store.state.userId,
                newPassword: this.newPassword
            })
                .then(res => {
                    console.log(res);
                    if (res.data.code === 0) {
                        console.log("修改成功");
                        ElMessage.success('修改成功');
                        this.$store.commit('setPassword', this.newPassword);
                        this.oldPassword = '';
                    } else if (res.data.code === 1) {
                        console.log("修改失败");
                        ElMessage.error('密码格式错误');
                    }
                    this.newPassword = '';
                    this.confirmPassword = '';
                });
            this.dialogVisible = false;
        }
    }
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
}

.content-container {
    display: block;
    flex-direction: column;
    margin-top: 50px;
    margin-left: 300px;
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.font {
    font-size: 20px;
    font-weight: bold;
}

.text-font {
    font-size: 16px;
    color: #000;
}

.mb-3 {
    margin-bottom: 1rem;
}

.dialog-footer button:first-child {
    margin-right: 10px;
}
</style>