<template>
  <div>
    <h1 class="title">个人信息</h1>
  </div>

  <el-descriptions class="margin-top" :column="1" border>
    <template #extra>
    </template>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <User />
          </el-icon>
          学工号
        </div>
      </template>
      {{ collegeId }}
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
      {{ userName }}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <Tickets />
          </el-icon>
          用户类型
        </div>
      </template>
      <el-tag>{{ userType }}</el-tag>
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
      <el-input type="textarea" v-model="telephone"></el-input>
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <VideoCamera />
          </el-icon>
          邮箱
        </div>
      </template>
      <el-input type="textarea" v-model="email"></el-input>
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
      <el-input type="textarea" v-model="userIntro"></el-input>
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <DataBoard />
          </el-icon>
          志愿时长
        </div>
      </template>
      {{ volunteerTime }}
    </el-descriptions-item>
  </el-descriptions>
  
  <br>
  <el-button type="primary" @click="editUserInfo">保存</el-button>
</template>
  
<script>
import {
  Iphone,
  VideoCamera,
  Tickets,
  User,
  DataBoard,
  Postcard,
} from '@element-plus/icons-vue'

export default {
  data() {
    return {
      collegeId : '21371295',
      userName : '张昊翔',
      password : '123456',
      telephone : '18100000000',
      email : '21371295@buaa.edu.cn',
      userType : '普通用户',
      volunteerTime : '100h',
      userIntro : '我是张昊翔，我来自北京航空航天大学'
    }
  },
  methods: {
    editUserInfo(){
      this.axios.post('http://localhost:5173/user', {
      collegeId: this.collegeId,
      password: this.password,
      telephone: this.telephone,
      email: this.email,
      userIntro: this.userIntro,
    })
      .then(res => {
        console.log(res)
        if (res.data.code === 0) {
          console.log("修改成功");
          this.telephone = res.data.telephone;
          this.email = res.data.email;
          this.userIntro = res.data.userIntro;
        }
      })
    }
  }
}
</script>
  
<style scoped>
.title {
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
}

.cell-item {
  display: flex;
  align-items: center;
}

.margin-top {
  margin-top: 20px;
}
</style>
  