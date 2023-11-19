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
        <img src="../assets/images/hand_shaking.png">
      </div>
      <el-divider direction="vertical" style="height: 200px;" />
      <div class="team-info">
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
            <el-badge :value="this.applicationList.length" :hidden="applicationNum === 0" :max="99">
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
      <el-input type="textarea" v-model="teamIntroduction" placeholder="输入团队介绍（不超过500字）" :rows="5"></el-input>
    </div>
    <el-divider style="width: 90%; margin-left: 100px;"/>
    <div class="footer">
      <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <v-btn size="large" @click="showCreateDialog">创建项目</v-btn>
      </div>
      <el-table :data="projects" style="width: 80%; margin: 0 auto;" border max-height="550">
        <el-table-column prop="name" label="项目名称" align="center"></el-table-column>
        <el-table-column prop="category" label="所属类别" align="center"></el-table-column>
        <el-table-column prop="createdDate" label="创建日期" align="center"></el-table-column>
        <el-table-column label="查看详情" align="center">
            <el-button type="link">点击查看</el-button>
        </el-table-column>
      </el-table>
    </div>
    <div> 
      <v-dialog v-model="createApplicationDialogVisible" width="auto">
        <el-table :data="applicationList" border style="width: 100%; border: 2px solid gray">
          <el-table-column prop="collegeId" label="学工号" width="200px" align="center"></el-table-column>
          <el-table-column prop="name" label="姓名" width="200px" align="center"></el-table-column>
          <el-table-column prop="date" label="申请日期" width="250px" align="center"></el-table-column>
          <el-table-column label="操作" width="200px" align="center">
            <template #default="scope">
              <el-button @click="handleAccept(scope.$index, scope.row, 'accept')" type="primary"><span style="color: white;">通过</span></el-button>
              <el-button @click="handleAccept(scope.$index, scope.row, 'reject')" type="warning"><span style="color: white;">拒绝</span></el-button>
            </template>
          </el-table-column>
        </el-table>
      </v-dialog>
    </div>
    <div>
      <v-dialog v-model="viewMembersDialogVisible" width="auto" max-height="600">
        <div class="members-container">
          <h2 style="margin: 20px 0; display: flex; justify-content: center;">成员列表</h2>
          <el-table :data="members" style=" display: flex; justify-content: center; align-items: center;">
            <el-table-column prop="collegeId" label="学工号" align="center"></el-table-column>
            <el-table-column prop="name" label="姓名" align="center"></el-table-column>
            <el-table-column prop="telephone" label="联系电话" align="center"></el-table-column>
            <el-table-column prop="joinDate" label="加入日期" align="center"></el-table-column>
            <!-- <el-table-column prop="hours" label="在本团队贡献的小时数" align="center"></el-table-column> -->
            <el-table-column label="操作" align="center">
              <template #default="scope">
                <el-button type="warning" @click="handleDelete(scope.$index, scope.row)"><span style="color: white;">删除</span></el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus';
import store from '../store'

export default {
  created() {
    // 根据teamId获取各详细信息：申请表、成员表、团队介绍、（项目列表）
    this.fetch();
  },
  data() {
    return {
      teamId: this.$route.query.id,
      teamName: this.$route.query.name,
      establishmentDate: this.$route.query.date,
      teamSize: this.$route.query.number,
      totalHours: this.$route.query.hours,
      teamIntroduction: "我们是阳光志愿者团队，已经成立了五年。作为一支热心的志愿者团队，我们致力于为社区提供志愿服务。在过去的五年里，我们团队获得了多项荣誉和认可，其中包括社区服务卓越奖和当地政府的优秀志愿者团队表彰。如果您对我们的团队感兴趣或想了解更多信息，请随时与我们联系。期待与您一起创造美好的志愿服务经历！",
      createApplicationDialogVisible: false,
      viewMembersDialogVisible: false,
      projects: [
        {
          name: "志愿项目1",
          category: "社区服务",
          createdDate: "2023-11-17"
        },
        {
          name: "志愿项目2",
          category: "科技科普",
          createdDate: "2023-11-17"
        },
        {
          name: "志愿项目3",
          category: "支教助学",
          createdDate: "2023-11-17"
        },
        {
          name: "志愿项目4",
          category: "大型演出",
          createdDate: "2023-11-17"
        },
        {
          name: "志愿项目5",
          category: "体育赛事",
          createdDate: "2023-11-17"
        },
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
          date: "2023-11-17",
        },
        {
          collegeId: "21370002",
          name: "ccc",
          date: "2023-11-17",
        },
        {
          collegeId: "21370003",
          name: "ddd",
          date: "2023-11-17",
        },
      ],
      members: [
        {
          collegeId: "21379999",
          name: "aa",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21379998",
          name: "bb",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21379997",
          name: "cc",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21379996",
          name: "dd",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21379995",
          name: "ee",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21379996",
          name: "dd",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21379995",
          name: "ee",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21379996",
          name: "dd",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21379995",
          name: "ee",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21379996",
          name: "dd",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        },
        {
          collegeId: "21379995",
          name: "ee",
          telephone: "13710000000",
          joinDate: "2023-11-18",
          hours: 1,
        }
      ],
    };
  },
  methods: {
    fetch() {
      const submitParams = {
        teamId: this.teamId,

      }

      const vm = this;
      (async () => {
          await vm.axios({
              method: 'post',
              url: '',
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
                      // 暂时没有项目列表，所以项目列表目前是写死的
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
    viewProjectDetails(project) {
      
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
              url: '',
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
      };

      const vm = this;
      (async () => {
          await vm.axios({
              method: 'post',
              url: '',
              data: submitParams,
            })
              .then(async (res) => {
                  console.log(res);
                  if (res.data.code === 0) {
                      console.log('操作成功');
                      vm.applicationList.splice(index, 1);
                      // 刷新团队页
                      vm.fetch();
                      if (approved === "accept") {
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
                url: '',
                data: submitParams,
              })
                .then(async (res) => {
                    console.log(res);
                    if (res.data.code === 0) {
                        console.log('删除成员');
                        vm.memberList.splice(index, 1);
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
  }
};
</script>

<style scoped>
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

.team-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-right: 50px;
}

.team-info-buttons {
  display: flex;
  flex-direction: row;
  margin-top: 5px;
  margin-left: 60px;
}

.team-info-button {
  margin-bottom: 5px;
  margin-right: 30px;
  margin-left: 30px;
}

.team-info-item {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.team-info-item label {
  margin-right: 10px;
}

.team-info-buttons {
  margin-top: 10px;
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
</style>