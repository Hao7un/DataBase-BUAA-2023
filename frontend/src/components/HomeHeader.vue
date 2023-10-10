<template>
<div class="header-container">
    <div class="logo-container">
      <img src="../assets/images/logo.png" alt="Logo!">
    </div>
    <div class="nav-container">
      <el-menu mode="horizontal" :default-active="activeMemu" class="menu-container">
        <el-menu-item index="project" class="item-font" @click="changeToProject()">志愿项目</el-menu-item>
        <el-menu-item index="team" class="item-font" @click="changeToTeam()">志愿团队</el-menu-item>
      </el-menu>
    </div>
    <div class="avatar-container">
      <el-dropdown trigger="click">
        <el-avatar :size="50" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"></el-avatar>
        <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="changeToUserInfo()">个人信息</el-dropdown-item>
          <el-dropdown-item @click="logout()">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </template>
      </el-dropdown>
    </div>
</div>
</template>

<script>
import { ElMessage } from 'element-plus';


export default {
  data() {
    return {
      activeMemu: "project"
    }
  },
  methods: {
    changeToProject() {
      console.log("change to project");
      this.$router.push({
        path: 'project'
      });
    },
    changeToTeam() {
      console.log("change to team");
      this.$router.push({
        path: 'team'
      });
    },
    changeToUserInfo() {
      console.log("change to user info");
      /* 切换到profile页 */
    },
    logout() {
      console.log("quit to welcome");
      ElMessage.success('已登出');
      this.$router.push({
        path: '/welcome'
      })
    }
  }
}

</script>

<style scoped>
.header-container {
    height: 60px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 10px;
}

.logo-container img {
  margin-left: 20px;
  margin-right: 10px;
  height: 50px;
}

.nav-container {
  display: flex;
  width: 100%;
  justify-content: center;
}

.menu-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

.avatar-container {
  margin-top: 10px;
  margin-right: 50px;
  margin-left: 30px;
}

.item-font {
  font-size: 20px;
  font-weight: bold;
}
</style>
