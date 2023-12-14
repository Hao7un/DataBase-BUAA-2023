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
        <el-menu-item index="manage" class="item-font" @click="changeToManagement()"
          v-if="this.$store.state.isAdmin">管理端</el-menu-item>
      </el-menu>
    </div>
    <div class="message-button-container">
      <el-badge :value="this.notReadMessageNum">
        <v-btn @click="messagesVisible = !messagesVisible"><el-icon>
            <ChatDotSquare />
          </el-icon></v-btn>
      </el-badge>
    </div>
    <div class="avatar-container">
      <el-dropdown trigger="click">
        <el-avatar :size="45" :src="avatar" fit="cover"></el-avatar>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="changeToUserInfoPage">个人信息</el-dropdown-item>
            <el-dropdown-item @click="changeToVolunteerTimePage">志愿统计</el-dropdown-item>
            <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <v-app>
      <v-navigation-drawer v-model="messagesVisible" location="top" temporary rounded
        style=" width: 500px; height: 300px; margin-left: 600px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);">
        <div class="message-container">
          <h2 style="text-align: center; margin: 10px 0"><el-icon>
              <MessageBox />
            </el-icon>&nbsp;&nbsp;收件箱</h2>
          <v-list>
            <v-list-item v-for="(message, index) in displayedMessages" :key="index" :value="message"
              @click="viewMessageDetail(message)">
              <div style="display: flex; align-items: center;">
                <div style="flex: 1; display: flex; justify-content: center; flex-direction: column;">
                  <div style="font-weight: bold; margin-left: 10px;">
                    {{ message.title }}
                  </div>
                  <div style="margin-left: 10px">
                    {{ message.time }}
                  </div>
                </div>
                <div
                  style="flex: 1; display: flex; justify-content: flex-end; align-items: center; padding-right: 10px; ">
                  {{ message.isRead === true ? "" : "未读" }}
                </div>
              </div>
            </v-list-item>
          </v-list>
          <div class="message-bottom-container">
            <div style="margin-left: 15px;">
              <span>仅展示未读</span> &nbsp; &nbsp;
              <el-switch v-model="showNotRead"></el-switch>
            </div>
            <div>
              <el-pagination :page-size="3"
                :total="this.showNotRead === false ? this.rawMessages.length : this.notReadMessages.length"
                layout="prev, pager, next" @current-change="handlePageChange" style="margin-left: 180px;">
              </el-pagination>
            </div>
          </div>
        </div>
      </v-navigation-drawer>
      <v-dialog v-model="viewMessageVisible" style="margin-left: 500px;">
        <div style="width: 600px; height: 200px; background: white; display: flex; flex-direction: column;">
          <div style="height: 50px; display: flex; align-items: center; justify-content: center; padding-left: 10px">
            <div style="font-weight: bold;">
              {{ this.selectedMessage.title }}
            </div>
          </div>
          <div style="height: 100px; display: flex; align-items: center; justify-content: center;">
            <p>{{ this.selectedMessage.content }}</p>
          </div>
          <div style="display: flex; justify-content: flex-end; align-items: flex-end; margin-right: 10px;">
            接收时间：&nbsp; {{ this.selectedMessage.time }}
          </div>
        </div>
      </v-dialog>
    </v-app>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus';

export default {
  async created() {
    await this.fetchUserAvatar();
  },
  async mounted() {
    await this.fetchUserAvatar();
    this.fetch();
    // setInterval(this.fetch, 5000);
  },
  data() {
    return {
      messagesVisible: false,
      viewMessageVisible: false,
      showNotRead: false,
      selectedMessage: null,
      messages: [
        // {
        //   id: "1",
        //   title: "您关注的项目发布了新的招募",
        //   time: "2023-11-28 15:36",
        //   content: "1111111111111",
        //   isRead: true,
        // },
        // {
        //   id: "2",
        //   title: "您的问题得到了回复",
        //   time: "2023-11-28 15:43",
        //   content: "11111111111",
        //   isRead: true,
        // },
        // {
        //   id: "3",
        //   title: "您的团队审核结果已出",
        //   time: "2023-11-28 15:43",
        //   content: "11111111111111",
        //   isRead: true
        // },
        // {
        //   id: "4",
        //   title: "您关注的项目发布了新的招募",
        //   time: "2023-11-28 15:43",
        //   content: "111111111111",
        //   isRead: true,
        // },
        // {
        //   id: "5",
        //   title: "您的团队审核结果已出",
        //   time: "2023-11-28 15:43",
        //   content: "11111111111111",
        //   isRead: false,
        // },
        // {
        //   id: "6",
        //   title: "您的问题得到了回复",
        //   time: "2023-11-28 15:43",
        //   content: "11111111111111",
        //   isRead: false,
        // }
      ],
      currentPage: 1,
    }
  },
  computed: {
    userId() {
      return this.$store.state.userId;
    },
    avatar() {
      return this.$store.state.avatar;
    },
    activeMenu() {
      return this.$store.state.activeMenu;
    },
    notReadMessageNum() {
      let cnt = 0;
      for (let i = 0; i < this.messages.length; i++) {
        if (this.messages[i].isRead === false) {
          cnt++;
        }
      }
      return cnt;
    },
    rawMessages() {
      return this.messages;
    },
    notReadMessages() {
      return this.messages.filter(item => {
        return item.isRead === false;
      });
    },
    displayedMessages() {
      if (this.showNotRead === true) {
        const startIndex = (this.currentPage - 1) * 3;
        const endIndex = startIndex + 3;
        return this.notReadMessages.sort((a, b) => {
          const dateA = new Date(a.time);
          const dateB = new Date(b.time);
          return dateB - dateA;
        }).slice(startIndex, endIndex);
      }
      else {
        const startIndex = (this.currentPage - 1) * 3;
        const endIndex = startIndex + 3;
        return this.messages.sort((a, b) => {
          const dateA = new Date(a.time);
          const dateB = new Date(b.time);
          return dateB - dateA;
        }).slice(startIndex, endIndex);
      }
    },
  },
  methods: {
    fetch() {
      const submitParams = {
        userId: this.userId,
      }

      this.axios({
        method: 'post',
        url: 'http://localhost:8000/user_get_message',
        data: submitParams,
      })
        .then((res) => {
          console.log(res);
          if (res.data.code === 0) {
            console.log("获取通知列表成功");
            this.messages = res.data.messages;
          }
          else {
            console.log("获取通知列表失败, 错误码不是0");
          }
        });
    },
    async fetchUserAvatar() {
      const res = await this.axios.post('http://localhost:8000/get_user_avatar', {
        userId: this.userId
      });
      console.log(res);
      if (res.data) {
        this.$store.commit("setAvatar", "data:image/jpeg;base64," + res.data);
      }
    },
    viewMessageDetail(message) {
      this.selectedMessage = message;
      this.viewMessageVisible = true;

      // axios
      const submitParams = {
        messageId: message.id,
      };

      this.axios({
        method: 'post',
        url: 'http://localhost:8000/user_read_message',
        data: submitParams,
      })
        .then((res) => {
          console.log(res);
          if (res.data.code === 0) {
            console.log("消息已读");
            this.fetch();
          }
          else {
            console.log("消息阅读失败, 错误码不是0");
          }
        })
    },
    handlePageChange(currentPage) {
      this.currentPage = currentPage;
    },
    changeToRecruit() {
      this.$store.commit("setActiveMenu", "recruit");
      console.log("change to recruit");
      this.$router.push({
        path: '/recruitment/join'
      });
    },
    changeToProject() {
      this.$store.commit("setActiveMenu", "project");
      console.log("change to project");
      this.$router.push({
        path: '/project/all'
      });
    },
    changeToTeam() {
      this.$store.commit("setActiveMenu", "team");
      console.log("change to team");
      this.$router.push({
        path: '/team/join'
      });
    },
    changeToUserInfoPage() {
      this.$store.commit("setActiveMenu", "none");
      console.log("change to user info");
      this.$router.push({
        path: '/user/info'
      });
    },
    changeToVolunteerTimePage() {
      this.$store.commit("setLastMenu", this.activeMenu);
      this.$store.commit("setActiveMenu", "none");
      console.log("change to volunteer time");
      this.$router.push({
        path: '/user/volunteer-time'
      });
    },
    changeToManagement() {
      this.$store.commit("setActiveMenu", "manage");
      console.log("change to admin");
      this.$router.push({
        path: '/admin/manage',
      })
    },
    logout() {
      this.$store.commit("setUserId", "");
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
  margin-left: 10px;
  display: flex;
  justify-content: center;
  width: 100%;
}

.message-button-container {
  margin-right: 40px;
}

.avatar-container {
  margin-right: 40px;
}

.item-font {
  font-size: 20px;
  font-weight: bold;
}

.message-container {
  position: relative;
}

.message-bottom-container {
  display: flex;
  justify-content: space-around;
  top: 250px;
  position: absolute;
}
</style>
