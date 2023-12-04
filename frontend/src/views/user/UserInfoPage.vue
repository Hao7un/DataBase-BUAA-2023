<template>
  <div class="main-container">
    <div class="sidebar-container">
      <el-menu mode="vertical" default-active="info" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
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
      <el-descriptions class="margin-top" :column="1" size="large">
        <el-descriptions-item label="姓名" width="400px">
          <template #label>
            <div class="cell-item">
              <el-icon>
                <Paperclip />
              </el-icon>
              学工号
            </div>
          </template>
          <span style="font-size: 16px; color: #000;">{{ collegeId }}</span>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon>
                <User />
              </el-icon>
              姓名
            </div>
          </template>
          <span style="font-size: 16px; color: #000;">{{ userName }}</span>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon>
                <School />
              </el-icon>
              用户类型
            </div>
          </template>
          <el-tag style="font-size: 16px;">{{ userType }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon>
                <Iphone />
              </el-icon>
              电话
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
              邮箱
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
              个人简介
            </div>
          </template>
          <el-input type="textarea" v-model="userIntro" class="input-container"></el-input>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon>
                <DataLine />
              </el-icon>
              志愿时长
            </div>
          </template>
          <span style="font-size: 16px; color: #000;">{{ volunteerTime }} 小时</span>
        </el-descriptions-item>
      </el-descriptions>

      <br>
      <el-button type="primary" round size="large" @click="editUserInfo">
        <span style="font-weight: bold; font-size: 15px; color:whitesmoke">保存</span></el-button>
    </div>
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
          this.volunteerTime = res.data.volunteerTime;
          this.userIntro = res.data.userIntro;
        }
      });
  },
  data() {
    return {
      telephone: '18101000000',
      email: '123@xyz.com',
      volunteerTime: '100',
      userIntro: '我是张昊翔。\n我来自北京航空航天大学。'
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

.margin-top {
  margin-top: 50px;
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

.content-container {
  display: block;
  flex-direction: column;
  margin-left: 400px;
  width: 500px;
}

.item-font {
  font-size: 18px;
  margin-left: 10px;
}

.input-container {
  margin-top: 10px;
  font-size: 16px;
}
</style>
  