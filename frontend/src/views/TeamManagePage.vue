<template>
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
        <img src="../assets/images/hand_shaking.png" id="avatar">
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
      <el-input type="textarea" v-model="teamIntroduction" placeholder="输入团队介绍(不超过500字)" :rows="5" :maxlength="500" show-word-limit clearable></el-input>
    </div>
    <el-divider style="width: 90%; margin-left: 100px;"/>
    <div class="footer">
      <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <v-btn size="large" @click="showCreateProjectDialog">创建项目</v-btn>
      </div>
      <el-table :data="displayedProjects" style="width: 80%; margin: 0 auto;" border max-height="550">
        <template #empty>
          <p>无匹配数据</p>
        </template>
        <el-table-column prop="name" label="项目名称" align="center">
          <template #header>项目名称
            <el-input v-model="projectNameKey" placeholder="输入项目名称" style="width: 260px;" clearable></el-input>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="所属类别" align="center" size="large">
          <template #header>
            <div>所属类别</div>
            <el-select v-model="projectTypeKey" placeholder="选择所属项目" clearable>
              <el-option label="社区服务" key="社区服务" value="社区服务"></el-option>
              <el-option label="科技科普" key="科技科普" value="科技科普"></el-option>
              <el-option label="支教助学" key="支教助学" value="支教助学"></el-option>
              <el-option label="体育赛事" key="体育赛事" value="体育赛事"></el-option>
              <el-option label="大型演出" key="大型演出" value="大型演出"></el-option>
              <el-option label="其它" key="其它" value="其它"></el-option>
            </el-select>
          </template>
          <template #default="scope">
            <span v-if="scope.row.category === '1'">社区服务</span>
            <span v-else-if="scope.row.category === '2'">科技科普</span>
            <span v-else-if="scope.row.category === '3'">支教助学</span>
            <span v-else-if="scope.row.category === '4'">体育赛事</span>
            <span v-else-if="scope.row.category === '5'">大型演出</span>
            <span v-else>其它</span>
          </template>
        </el-table-column>
        <el-table-column prop="createdDate" label="创建日期" align="center" sortable></el-table-column>
        <el-table-column label="查看详情" align="center">
            <template #default="scope">
                <el-button type="link" size="small" @click="viewProjectDetails(scope.row)">
                  <el-badge is-dot :hidden="scope.row.hasComments === false">
                    <span>点击查看</span>
                  </el-badge>
                </el-button>
            </template>
        </el-table-column>
      </el-table>
    </div>
    <div> 
      <v-dialog v-model="createApplicationDialogVisible" width="auto">
        <el-table :data="applicationList" border style="width: 99%; border: 2px solid gray" :default-sort="[{ prop: 'date', order: 'descending' }]">
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
      <v-dialog v-model="createProjectDialogVisible" width="auto" max-height="1000">
        <div class="create-dialog-container">
          <div class="create-item">
            <h3 style="margin-bottom: 15px;">项目名称</h3>
            <el-input v-model="projectName" clearable style="width: 150px;">
              <template #prefix>
                <el-icon><Postcard /></el-icon>
              </template>
            </el-input>
          </div>
          <div class="create-item">
            <h3 style="margin-bottom: 15px;">项目简介</h3>
            <el-input type="textarea" v-model="projectIntro" clearable :maxlength="500" :autosize="{minRows: 2}" show-word-limit style="width: 400px;"></el-input>
          </div>
          <div class="create-item">
            <h3 style="margin-bottom: 15px;">项目类别</h3>
            <el-radio-group v-model="projectType">
              <el-radio label="1" border size="small">社区服务</el-radio>
              <el-radio label="2" border size="small">科技科普</el-radio>
              <el-radio label="3" border size="small" style="margin-top: 8px;">支教助学</el-radio>
              <el-radio label="4" border size="small" style="margin-top: 8px;">体育赛事</el-radio>
              <el-radio label="5" border size="small" style="margin-top: 8px;">大型演出</el-radio>
              <el-radio label="6" border size="small" style="margin-top: 8px;">其它类别</el-radio>
            </el-radio-group>
          </div>
          <div class="create-item">
            <h3 style="margin-bottom: 15px;">上传项目图片</h3>
            <el-upload
                class="avatar-uploader"
                action="#"
                :show-file-list="false"
                :auto-upload="false"
                :on-change="uploadFile"
            >
              <el-image v-if="imageUrl" :src="imageUrl" style="width: 190px; height: 190px" fit="contain" />
              <el-icon v-if="!imageUrl"><Plus /></el-icon>
            </el-upload>

          </div>
          <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
            <el-button size="large" @click="handleCreateProjectSubmit">提交</el-button>
          </div>
        </div>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus';
import store from '../store'

export default {
  computed: {
    displayedProjects() {
      let displayedProjects = this.projects;
      let newProjectTypeKey = this.projectTypeKey === "社区服务" ? "1" : this.projectTypeKey === "科技科普" ? "2" : this.projectTypeKey === "支教助学" ? "3" : this.projectTypeKey === "体育赛事" ? "4" : this.projectTypeKey === "大型演出" ? "5" : this.projectTypeKey === "其它" ? "6" : ""; 
      if (this.projectNameKey != null && newProjectTypeKey != null) {
          displayedProjects = displayedProjects.filter(item => {
            return item.name.includes(this.projectNameKey) && item.category.includes(newProjectTypeKey);
          })
      }
      return displayedProjects;
    },
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
      teamId: this.$route.query.id,
      teamName: this.$route.query.name,
      teamSize: this.$route.query.number,
      establishmentDate: this.$route.query.date,
      totalHours: this.$route.query.hours,
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
      projects: [
        {
          hasComments: false,
          name: "志愿项目1",
          category: "1",
          createdDate: "2023-11-17"
        },
        {
          hasComments: false,
          name: "志愿项目2",
          category: "2",
          createdDate: "2023-11-18"
        },
        {
          hasComments: false,
          name: "志愿项目3",
          category: "3",
          createdDate: "2023-11-19"
        },
        {
          hasComments: false,
          name: "志愿项目4",
          category: "4",
          createdDate: "2023-11-20"
        },
        {
          hasComments: false,
          name: "志愿项目5",
          category: "5",
          createdDate: "2023-11-21"
        },
        {
          hasComments: false,
          name: "志愿项目6",
          category: "6",
          createdDate: "2023-11-27"
        }
      ],
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
          if (res.data.code === 0) {
            var avatar = document.getElementById('avatar');
            var img = res.data.avatar;
            avatar.src = "data:image/jpeg;base64," + btoa(
                new Uint8Array(img).reduce(function(img, byte) {
                    return img + String.fromCharCode(byte);
              }, '')
            );
          }
          else {
            console.log("获取团队头像失败, 错误码不是0");
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
                      vm.teamIntroduction = res.data.teamIntro;
                      vm.applicationList = res.data.applicationList;
                      vm.members = res.data.memberList;
                      vm.projects = res.data.projects;
                  }
                  else {
                      console.log('请求失败, 错误码code不是0');
                  }
              });
          })();
    },
    viewMembers() {
      this.viewMembersDialogVisible = true;
    },
    showCreateProjectDialog() {
      this.createProjectDialogVisible = true;
    },
    viewProjectDetails(row) {
      let fatherTeam = {
          id: this.teamId,
          name: this.teamName,
          establishmentDate: this.establishmentDate,
          size: this.teamSize,
          totalHours: this.totalHours,
      };
      this.$router.push({
        path: '/admin/projectinfo',
        query: {
          id: row.id,
          name: row.name,
          type: row.category,
          createdDate: row.createdDate,
          // 还要传递所属团队
          fatherTeam: JSON.stringify(fatherTeam),
        }
      })
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
    handleCreateProjectSubmit() {
      this.createProjectDialogVisible = false;
      if (this.projectName === "" || this.projectType === "" || this.projectIntro === "") {
        ElMessageBox.alert("请填写完整的项目信息", "注意", {
          confirmButtonText: "OK",
          type: "warning",
        }).then(() => {
          this.createProjectDialogVisible = true;
        })
      }
      else {
        const formData = new FormData();
        formData.append("projectAvatar", this.fileToUpload);
        // console.log(formData.get("projectAvatar"));
        formData.append("teamId", this.teamId);
        formData.append("projectName", this.projectName);
        formData.append("projectIntro", this.projectIntro);
        formData.append("projectType", this.projectType);
        // const submitParams = {
        //   teamId: this.teamId,
        //   projectName: this.projectName,
        //   projectIntro: this.projectIntro,
        //   projectType: this.projectType,
        //   avatar: formData,

        // };

        this.axios({
          method: 'post',
          url: 'http://localhost:8000/admin_create_project',
          data: formData,
        })
        .then((res) => {
          console.log(res);
          if (res.data.code === 0) {
            console.log("创建项目成功");
            // 刷新项目列表
            this.fetch();
            ElMessage.success("成功创建项目");
          }
          else if (res.data.code === 1) {
            ElMessage.error("项目名已被注册");
            console.log("项目名称重复");
          }
          else {
            console.log("创建失败, 错误码不是 0 或 1");
          }
        })

      }
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
  }
};
</script>

<style scoped>
.team-management {
  height: 1000px;
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
  max-width: 100%;
  max-height: 100%;
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

footer {
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

.create-dialog-container {
  display: flex;
  height: 800px;
  width: 500px;
  background: white;
  flex-direction: column;
}

.create-item {
  margin-top: 50px;
  margin-left: 50px;
  width: 90%;
}

.avatar-uploader {
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px dashed black;
    width: 185px;
    height: 185px;
    
}

</style>