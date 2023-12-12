<template>
  <div class="main-container">
    <div class="sidebar-container">
      <el-menu mode="vertical" default-active="info" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
        <el-menu-item index="info" @click="changeToUserInfoPage">
          <span class="item-font" style="font-weight: bold;">个人信息</span>
        </el-menu-item>
        <el-menu-item index="volunteerTime" @click="changeToVolunteerTimePage">
          <span class="item-font" style="font-weight: bold;">志愿统计</span>
        </el-menu-item>
      </el-menu>
    </div>

    <div class="user-container">
      <div class="info-container">
        <el-descriptions :column="1" size="large">
          <el-descriptions-item label="姓名" width="400px">
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <Paperclip />
                </el-icon>
                &nbsp;学工号
              </div>
            </template>
            &nbsp;
            <span style="font-size: 16px; color: #000;">{{ collegeId }}</span>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <User />
                </el-icon>
                &nbsp;姓名
              </div>
            </template>
            &nbsp;
            <span style="font-size: 16px; color: #000;">{{ userName }}</span>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <School />
                </el-icon>
                &nbsp;用户类型
              </div>
            </template>
            &nbsp;
            <el-tag style="font-size: 16px;">{{ userType }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <Iphone />
                </el-icon>
                &nbsp;电话
              </div>
            </template>
            <el-input type="text" v-model="telephone" class="input-container"></el-input>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <MessageBox />
                </el-icon>
                &nbsp;邮箱
              </div>
            </template>
            <el-input type="text" v-model="email" class="input-container"></el-input>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon>
                  <Postcard />
                </el-icon>
                &nbsp;个人简介
              </div>
            </template>
            <el-input type="textarea" v-model="userIntro" class="input-container"></el-input>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <div class="button-container">
        <el-button type="primary" round size="large" @click="editUserInfo">
          <span style="font-weight: bold; font-size: 16px; color:whitesmoke">保存信息</span></el-button>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <el-button type="primary" round size="large" @click="showAvatarDialog">
          <span style="font-weight: bold; font-size: 16px; color:whitesmoke">上传头像</span></el-button>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <el-button type="primary" round size="large" @click="showPasswordDialog">
          <span style="font-weight: bold; font-size: 16px; color:whitesmoke">修改密码</span></el-button>
      </div>
    </div>


    <el-dialog v-model="avatarDialogVisible" title="上传头像" width="30%" align-center center draggable>
      <el-upload class="avatar-uploader" action="#" :show-file-list="false" :auto-upload="false" :on-change="uploadImage">
        <el-image v-if="imageUrl" :src="imageUrl" style="width: 200px; height: 200px" fit="cover" />
        <el-icon v-if="!imageUrl">
          <Plus />
        </el-icon>
      </el-upload>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeAvatarDialog">取消</el-button>
          <el-button type="primary" @click="editAvatar">
            <span style="color:whitesmoke; font-weight: bold;">上传</span>
          </el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog v-model="passwordDialogVisible" title="修改密码" width="30%" align-center center draggable>
      <div class="password-container">
        <label class="text-font">旧密码：</label>
        <el-input v-model="oldPassword" type="password" placeholder="请输入旧密码" maxlength="64" clearable show-password
          class="mb-3" />

        <label class="text-font">新密码：</label>
        <el-input v-model="newPassword" type="password" placeholder="请输入新密码" maxlength="64" clearable show-password
          class="mb-3" />

        <label class="text-font">验证新密码：</label>
        <el-input v-model="confirmPassword" type="password" placeholder="请再次输入新密码" maxlength="64" clearable
          show-password />
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closePasswordDialog">取消</el-button>
          <el-button type="primary" @click="editPassword">
            <span style="color:whitesmoke; font-weight: bold;">完成</span>
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
    this.axios.post('http://localhost:8000/get_user_info', {
      userId: this.userId
    })
      .then(res => {
        console.log(res);
        if (res.data.code === 0) {
          this.telephone = res.data.telephone;
          this.email = res.data.email;
          this.userIntro = res.data.userIntro;
        }
      });
  },
  data() {
    return {
      telephone: '18101000000',
      email: '123@xyz.com',
      userIntro: '我是张昊翔。\n我来自北京航空航天大学。',
      avatarDialogVisible: false,
      imageUrl: null,
      fileToUpload: null,
      passwordDialogVisible: false,
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
    };
  },
  computed: {
    userId() {
      return this.$store.state.userId;
    },
    collegeId() {
      return this.$store.state.collegeId;
    },
    userName() {
      return this.$store.state.userName;
    },
    userType() {
      if (this.$store.state.userType === "0") {
        return "普通用户";
      } else if (this.$store.state.userType === "1") {
        return "管理员";
      }
    },
    password() {
      return this.$store.state.password;
    }
  },
  methods: {
    changeToUserInfoPage() {
      this.$router.push({
        path: '/user/info'
      })
    },
    changeToVolunteerTimePage() {
      this.$router.push({
        path: '/user/volunteer-time'
      })
    },
    showAvatarDialog() {
      this.avatarDialogVisible = true;
    },
    uploadImage(file) {
      const isJPG = file.raw.type === 'image/jpeg';
      const isPNG = file.raw.type === 'image/png';
      if (!isJPG && !isPNG) {
        ElMessage.error("只能上传JPG或PNG格式的文件");
        return false;
      } else if (file.size / 1024 / 1024 > 2) {
        ElMessage.error("图片大小不能超过2MB");
        return false;
      } else {
        this.imageUrl = URL.createObjectURL(file.raw);
        this.fileToUpload = file.raw;
        return true;
      }
    },
    closeAvatarDialog() {
      this.avatarDialogVisible = false;
      this.imageUrl = null;
      this.fileToUpload = null;
    },
    editAvatar() {
      const formData = new FormData();
      formData.append("userId", this.userId);
      formData.append("userAvatar", this.fileToUpload);

      this.axios({
        method: 'post',
        url: 'http://localhost:8000/upload_user_avatar',
        data: formData,
      })
        .then(res => {
          console.log(res);
          if (res.data) {
            this.$store.commit("setAvatar", "data:image/jpeg;base64," + res.data);
            console.log("上传成功");
            ElMessage.success('上传成功');
            this.avatarDialogVisible = false;
          }
        });
    },
    showPasswordDialog() {
      this.passwordDialogVisible = true;
    },
    closePasswordDialog() {
      this.passwordDialogVisible = false;
      this.oldPassword = '';
      this.newPassword = '';
      this.confirmPassword = '';
    },
    editPassword() {
      if (this.oldPassword != this.password) {
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
        this.axios.post('http://localhost:8000/change_password', {
          userId: this.userId,
          newPassword: this.newPassword
        })
          .then(res => {
            console.log(res);
            if (res.data.code === 0) {
              console.log("修改成功");
              ElMessage.success('修改成功');
              this.$store.commit('setPassword', this.newPassword);
              this.oldPassword = '';
              this.newPassword = '';
              this.confirmPassword = '';
              this.passwordDialogVisible = false;
            }
          });
      }
    },
    editUserInfo() {
      if (this.telephone == '') {
        ElMessage.error('电话不能为空');
        return;
      } else if (this.email == '') {
        ElMessage.error('邮箱不能为空');
        return;
      } else if (this.telephone.length != 11) {
        ElMessage.error('电话格式错误');
        return;
      } else if (this.email.indexOf('@') == -1) {
        ElMessage.error('邮箱格式错误');
        return;
      }

      this.axios.post('http://localhost:8000/update_user_info', {
        userId: this.userId,
        telephone: this.telephone,
        email: this.email,
        userIntro: this.userIntro
      })
        .then(res => {
          console.log(res);
          if (res.data.code === 0) {
            console.log("修改成功");
            ElMessage.success('修改成功');
          }
        });
    }
  }
}
</script>
  
<style scoped>
.cell-item {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

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

.user-container {
  display: flex;
  flex-direction: column;
  margin-left: 400px;
  margin-top: 50px;
  width: 500px;
}

.info-container {
  display: flex;
  flex-direction: column;
}

.button-container {
  display: flex;
  flex-direction: row;
  margin-top: 40px;
}

.item-font {
  font-size: 18px;
  margin-left: 10px;
}

.input-container {
  margin-top: 10px;
  font-size: 16px;
}

.avatar-uploader {
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px dashed black;
  width: 200px;
  height: 200px;
  margin-left: 125px;
}

.password-container {
  display: flex;
  flex-direction: column;
  margin-left: 50px;
  margin-right: 50px;
}

.text-font {
  font-size: 16px;
  color: #000;
}

.mb-3 {
  margin-bottom: 1rem;
}

.dialog-footer button:first-child {
  margin-right: 50px;
}
</style>
  