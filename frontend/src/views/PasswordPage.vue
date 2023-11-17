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
                path: '/user/volunteerHours'
            })
        },
        checkPassword() {
            if (this.oldPassword != this.$store.state.password) {
                ElMessage.error('旧密码错误');
                this.oldPassword = '';
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
    height: 1200px;
    flex-direction: column;
    padding-top: 20px;
    margin-left: 20px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
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