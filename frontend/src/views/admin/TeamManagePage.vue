<template>
  <div class="main-container">
    <div class="sidebar-container">
      <el-menu mode="vertical" default-active="info" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
          <el-menu-item index="info" @click="changeToTeamManagePage">
              <span class="item-font" style="font-weight: bold;">团队详情</span>
          </el-menu-item>
          <el-menu-item index="list" @click="changeToProjectListPage">
              <span class="item-font" style="font-weight: bold;">项目管理</span>
          </el-menu-item>
      </el-menu>
    </div>
  <div class="team-management">
    <v-btn class="back-button" @click="handleBack">
      <template v-slot:prepend>
        <el-icon><Back /></el-icon>
      </template>
      返回
    </v-btn>
    <h2 class="title">团队详情</h2>
    <div class="header">
      <div class="team-avatar">
        <el-tooltip placement="right" content="更换头像" effect="light">
          <img src="../../assets/images/hand_shaking.png" id="avatar" @click="setAvatarVisible = true">
        </el-tooltip>
      </div>
      <el-divider direction="vertical" style="height: 200px;" />
      <div class="team-info-container">
        <div class="team-info">
          <h3 style="display: flex; justify-content: center; margin-bottom: 10px; font-weight: bold;">团队信息</h3>
          <el-descriptions column="2" border>
            <el-descriptions-item label="团队名称" width="150px">
              <el-input placeholder="输入团队名称" v-model="teamName" clearable></el-input>
            </el-descriptions-item>
            <el-descriptions-item label="团队人数" width="150px">
              {{ teamSize }} 人
            </el-descriptions-item>
            <el-descriptions-item label="成立日期" width="150px">
              {{ establishmentDate }}
            </el-descriptions-item>
            <el-descriptions-item label="总志愿时长" width="150px">
              {{ totalHours }} h
            </el-descriptions-item>
          </el-descriptions>
        </div>
        <div class="team-info-buttons">
          <div class="team-info-button">
            <el-badge :value="this.applicationList.length" :max="99">
              <v-btn size="x-large" @click="viewApplications" rounded="lg">查看申请</v-btn>
            </el-badge>
          </div>
          <div class="team-info-button">
            <v-btn size="x-large" @click="viewMembers" rounded="sm">查看成员</v-btn>
          </div>
          <div class="team-info-button">
            <v-btn size="x-large" @click="handleSave" rounded="xl">保存修改</v-btn>
          </div>
        </div>
      </div>
    </div>
    <el-divider style="width: 90%; margin-left: 100px;"/>
    <div class="content">
      <el-input type="textarea" v-model="teamIntroduction" placeholder="输入团队介绍(不超过500字)" :rows="15" :maxlength="500" show-word-limit clearable></el-input>
    </div>
    <div> 
      <v-dialog v-model="createApplicationDialogVisible" width="900px" max-height="600">
        <div class="applications-container">
          <h2 style="margin: 20px 0; display: flex; justify-content: center;">申请列表</h2>
          <el-table :data="applicationList" border style="width: 99%; display: flex; justify-content: center; align-items: center;">
            <el-table-column prop="collegeId" label="学工号" width="200px" align="center"></el-table-column>
            <el-table-column prop="name" label="姓名" width="200px" align="center"></el-table-column>
            <el-table-column prop="date" label="申请日期" width="250px" align="center" sortable></el-table-column>
            <el-table-column label="操作" width="200px" align="center">
              <template #default="scope">
                <el-button @click="handleAccept(scope.$index, scope.row, 'true')" type="primary"><span style="color: white;">通过</span></el-button>
                <el-button @click="handleAccept(scope.$index, scope.row, 'false')" type="warning"><span style="color: white;">拒绝</span></el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </v-dialog>
    </div>
    <div>
      <v-dialog v-model="viewMembersDialogVisible" width="800px" max-height="600">
        <div class="members-container">
          <h2 style="margin: 20px 0; display: flex; justify-content: center;">成员列表</h2>
          <el-table :data="displayedMembers" style=" display: flex; justify-content: center; align-items: center;">
            <template #empty>
                <p>暂无成员</p>
            </template>
            <el-table-column prop="collegeId" label="学工号" align="center">
              <template #header>
                <div>学工号</div>
                <el-input v-model="collegeIdKey" clearable placeholder="输入学工号"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="姓名" align="center">
              <template #header>
                <div>姓名</div>
                <el-input v-model="memberNameKey" clearable placeholder="输入姓名"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="telephone" label="联系电话" align="center">
              <template #header>
                <div>联系电话</div>
                <el-input v-model="telephoneKey" clearable placeholder="输入联系电话"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="joinDate" label="加入日期" align="center" sortable></el-table-column>
            <el-table-column label="操作" align="center">
              <template #default="scope">
                <el-button type="warning" @click="handleDelete(scope.$index, scope.row)"><span style="color: white;">删除</span></el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </v-dialog>
    </div>
    <div>
      <v-dialog v-model="setAvatarVisible">
        <div class="setAvatar-container">
          <el-button @click="setAvatarVisible = false" style="margin-top: 10px; margin-left: 200px">退出</el-button>
          <h3 style="margin-bottom: 20px; margin-top: 20px;">上传新头像</h3>
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
          <el-button @click="handleSetTeamAvatarSubmit" size="large" style="margin-top: 30px;">点击上传</el-button>
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
    displayedMembers() {
      let displayedMembers = this.members;
      if (this.memberNameKey != null && this.collegeIdKey != null && this.telephoneKey != null) {
        displayedMembers = displayedMembers.filter(item => {
          return item.name.includes(this.memberNameKey) && item.telephone.includes(this.telephoneKey) && item.collegeId.includes(this.collegeIdKey);
        })
      }
      return displayedMembers;
    }
  },
  created() {
    this.fetch();
    this.fetchPicture();
  },
  data() {
    return {
      teamId: this.$route.query.teamId,
      teamName: "",
      teamSize: "",
      establishmentDate: "",
      totalHours: "",
      teamIntroduction: "",
      createApplicationDialogVisible: false,
      viewMembersDialogVisible: false,
      createProjectDialogVisible: false,
      projectName: "",
      projectIntro: "",
      projectType: "",
      // 搜索功能
      projectNameKey: "",
      projectTypeKey: "",
      collegeIdKey: "",
      memberNameKey: "",
      telephoneKey: "",
      // 图片
      imageUrl: null,
      fileToUpload: null,
      setAvatarVisible: false,
      fileToUpload: null,
      applicationList: [
        {
          collegeId: "21370000",
          name: "aaa",
          date: "2023-11-17",
        },
        {
          collegeId: "21370001",
          name: "bbb",
          date: "2023-11-18",
        },
        {
          collegeId: "21370002",
          name: "ccc",
          date: "2023-11-19",
        },
        {
          collegeId: "21370003",
          name: "ddd",
          date: "2023-11-20",
        },
      ],
      members: [
        {
          collegeId: "21371372",
          name: "严皓钧",
          telephone: "13710000001",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21371401",
          name: "王乐",
          telephone: "13710000002",
          joinDate: "2023-11-19",
          hours: 1,
        },
        {
          collegeId: "21371295",
          name: "张昊翔",
          telephone: "13710000003",
          joinDate: "2023-11-20",
          hours: 1,
        },

      ],
    };
  },
  methods: {
    fetchPicture() {
      const submitParams = {
        teamId: this.teamId,

      };

      this.axios({
        method: 'post',
        url: 'http://localhost:8000/get_team_avatar',
        data: submitParams,
      })
        .then((res) => {
          console.log(res);
          if (res.data) {
            var avatar = document.getElementById('avatar');
            avatar.src = "data:image/jpeg;base64," + res.data;
          }
          else {
            console.log("获取团队头像失败");
          }
        })

    },
    fetch() {
      const submitParams = {
        teamId: this.teamId,

      }

      const vm = this;
      (async () => {
          await vm.axios({
              method: 'post',
              url: 'http://localhost:8000/admin_get_specific_team_details',
              data: submitParams,

            })
              .then(async (res) => {
                  console.log('获取团队详情');
                  console.log(res);
                  if (res.data.code === 0) {
                      console.log('请求成功');
                      vm.teamName = res.data.teamName;
                      vm.teamSize = res.data.teamSize;
                      vm.totalHours = res.data.totalHours;
                      vm.establishmentDate = res.data.establishmentDate;
                      vm.teamIntroduction = res.data.teamIntro;
                      vm.applicationList = res.data.applicationList;
                      vm.members = res.data.memberList;
                  }
                  else {
                      console.log('请求失败, 错误码code不是0');
                  }
              });
          })();
    },
    changeToProjectListPage() {
      this.$router.push({
        path: '/admin/projectlist',
        query: {
          teamId: this.teamId,
        }
      })
    },
    changeToTeamManagePage() {
      this.$router.push({
        path: '/admin/teaminfo',
        query: {
          teamId: this.teamId,
        }
      })
    },
    viewMembers() {
      this.viewMembersDialogVisible = true;
    },
    handleSave() {
      const submitParams = {
        teamId: this.teamId,
        newTeamName: this.teamName,
        newTeamIntro: this.teamIntroduction,
        
      }

      if (this.teamName === '') {
        ElMessageBox.alert("新的团队名不能为空", "注意", {
          confirmButtonText: 'OK',
          type: 'warning'
        }).then(() => {
          return;
        })
        return;
      }
      
      const vm = this;
      (async () => {
          await vm.axios({
              method: 'post',
              url: 'http://localhost:8000/admin_update_team_info',
              data: submitParams,
            })
              .then(async (res) => {
                  console.log('尝试修改团队信息');
                  console.log(res);
                  if (res.data.code === 0) {
                      console.log('修改成功');
                      ElMessage.success("保存成功");
                  }
                  else if (res.data.code === 1) {
                    console.log("团队名已被注册");
                    ElMessage.error("团队名已被注册");
                  }
                  else {
                      console.log('请求失败, 错误码code不是0或1');
                  }
              });
          })();
    },
    handleBack() {
      this.$router.push({
        path: '/admin/manage'
      })
    },
    viewApplications() {
      if (this.applicationList.length === 0) {
        ElMessage.error("暂无申请");
      }
      else {
        this.createApplicationDialogVisible = true;
      }
    },
    handleAccept(index, row, approved) {
      const submitParams = {
        userId: row.userId,
        teamId: this.teamId,
        approved: approved,
        message: {
          title: "您的团队审核结果已出",
          content: "您申请加入 " + this.teamName + " 团队的请求" + (approved === "true" ? "已通过" : "被拒绝"),
        }
      };

      const vm = this;
      (async () => {
          await vm.axios({
              method: 'post',
              url: 'http://localhost:8000/admin_review_team_application',
              data: submitParams,
            })
              .then(async (res) => {
                  console.log(res);
                  if (res.data.code === 0) {
                      console.log('操作成功');
                      vm.applicationList.splice(index, 1);
                      // 刷新团队页
                      vm.fetch();
                      if (approved === "true") {
                        ElMessage.success("通过申请");
                      }
                      else {
                        ElMessage.success("拒绝申请");
                      }
                  }
                  else {
                      console.log('请求失败, 错误码code不是0');
                  }
              });
          })();

      if (this.applicationList.length === 0) {
        this.createApplicationDialogVisible = false;
      }
    },
    handleDelete(index, row) {
      this.viewMembersDialogVisible = false;
      if (row.userId === this.$store.state.userId) {
          ElMessage.error("无法删除管理员!");
          this.viewMembersDialogVisible = true;
          return;
      }
      
      ElMessageBox.confirm('确定删除该成员?', '注意', {
        confirmButtonText: '是',
        cancelButtonText: '否',
        type: 'warning'
      }).then(() => {

        const submitParams = {
          userId: row.userId,
          teamId: this.teamId,

        }

        const vm = this;
        (async () => {
            await vm.axios({
                method: 'post',
                url: 'http://localhost:8000/admin_remove_team_member',
                data: submitParams,
              })
                .then(async (res) => {
                    console.log(res);
                    if (res.data.code === 0) {
                        console.log('删除成员');
                        vm.members.splice(index, 1);
                        // 刷新团队页
                        vm.fetch();
                        ElMessage.success("已删除");
                        vm.viewMembersDialogVisible = true;
                    }
                    else {
                        console.log('请求失败, 错误码code不是0');
                    }
                });
            })();

      }).catch(() => {
        ElMessage.success("取消删除");
        this.viewMembersDialogVisible = true;
      });
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
      handleSetTeamAvatarSubmit() {
        const formData = new FormData();
        formData.append("teamAvatar", this.fileToUpload);
        formData.append("teamId", this.teamId);

        this.axios({
          method: 'post',
          url: 'http://localhost:8000/',
          data: formData
        })
            .then((res) => {
              console.log(res);
              // 刷新头像
              this.fetchPicture();
              this.setAvatarVisible = false;
            })
      }
  }
};
</script>

<style scoped>
.main-container {
  display: flex;
}

#avatar:hover {
  cursor: pointer;
}

.team-management {
  height: 500px;
  width: 100%;
  margin-top: 20px;
}

.sidebar-container {
    display: flex;
    width: 205px;
    flex-direction: column;
    padding-top: 20px;
    margin-left: 20px;
    height: 900px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.back-button {
  margin-left: 25px;
  margin-top: 5px;
}

.title {
  display: flex;
  margin-bottom: 10px;
  justify-content: center;
}

.team-avatar {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
}

.team-avatar img {
  max-width: 350px;
  max-height: 200px;
  width: auto;
  height: auto;
}

.setAvatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: white;
  height: 450px;
  width: 300px;
  margin-left: 700px;
}

.team-info-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-right: 50px;
}

.team-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-right: 50px;
}

.team-info-buttons {
  display: flex;
  flex-direction: row;
  margin-left: 60px;
  margin-top: 10px;
}

.team-info-button {
  margin-bottom: 5px;
  margin-right: 30px;
  margin-left: 30px;
}

.content {
  margin-top: 20px;
  width: 80%;
  margin: 0 auto;
}

.members-container {
  height: 600px;
  width: 1000px;
  margin: auto;
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  background: white;
}

.applications-container {
  height: 400px;
  width: 900px;
  margin: auto;
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  background-color: white;
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