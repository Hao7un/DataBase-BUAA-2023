<template>
  <div class="header-container">
    <div class="logo-container">
      <img src="../assets/images/logo.png" alt="Logo!">
    </div>
    <div class="nav-container">
      <el-menu mode="horizontal" :default-active="activeMenu" class="menu-container">
        <el-menu-item index="recruit" class="item-font" @click="changeToRecruit()">志愿招募</el-menu-item>
        <el-menu-item index="project" class="item-font" @click="changeToProject()">志愿项目</el-menu-item>
        <el-menu-item index="team" class="item-font" @click="changeToTeam()">志愿团队</el-menu-item>
      </el-menu>
    </div>
    <div class="avatar-container">
      <el-dropdown trigger="click">
        <el-avatar :size="45" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"></el-avatar>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="changeToUserInfo()">个人主页</el-dropdown-item>
            <el-dropdown-item @click="logout()">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
    <!-- <div class="username-container">{{ username }}</div> -->
  </div>
</template>

<script>
import { ElMessage } from 'element-plus';


export default {
  data() {
    return {
      activeMenu: "project"
    }
  },
  methods: {
    changeToRecruit() {
      console.log("change to recruit");
      this.$router.push({
        path: '/recruitment/join'
      });
    },
    changeToProject() {
      console.log("change to project");
      this.$router.push({
        path: '/project/join'
      });
    },
    changeToTeam() {
      console.log("change to team");
      this.$router.push({
        path: '/team/join'
      });
    },
    changeToUserInfo() {
      console.log("change to user");
      this.activeMenu = "temp"; // 设置为一个临时的值
      this.$nextTick(() => { // 在下一个 DOM 更新周期后执行
        this.activeMenu = "none"; // 再将 activeMenu 设置为 "none"
      });
      this.$router.push({
        path: '/user/info'
      });
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
  /* padding: 0 10px; */
  border-bottom: 2px solid rgb(114, 110, 104, 0.2);
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
