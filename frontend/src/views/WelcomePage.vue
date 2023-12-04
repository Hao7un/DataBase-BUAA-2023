<template>
  <div class="main">
    <div class="top-container">志 愿 北 航</div>
    <div class="button-container" v-if="buttonVisible">
      <el-button class="button" round @click="showLoginWindow()">登 录</el-button>
      <div class="spacer"></div>
      <el-button class="button" round @click="showRegisterWindow()">注 册</el-button>
    </div>
  </div>
  <div class="login-container" v-if="loginWindowVisible">
    <div class="quit-container">
        <el-button round @click="quitLoginWindow()">
          <el-icon><CloseBold /></el-icon>
        </el-button>
    </div>
    <div class="form-container">
      <el-form :rules="rules" :model="loginForm" ref="loginForm" label-width="80px">
        <div>
          <el-form-item label="学工号" prop="loginAccount">
            <el-input v-model="loginForm.account" clearable placeholder="请输入学工号" :style="{width: '300px', height: '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item label="密码" prop="loginPassword">
            <el-input v-model="loginForm.password" show-password clearable placeholder="请输入密码" :style="{width: '300px', height: '40px'}"></el-input>
          </el-form-item>
        </div>
      </el-form>
      <div class="submit-container">
          <el-button class="login-button" @click="loginSubmit()">登 录</el-button>
      </div>
      <el-link class="hint" @click="showRegisterWindow()">还未注册？点击注册</el-link>
    </div>
  </div>
  <div class="register-container" v-if="registerWindowVisible">
    <div class="quit-container">
      <el-button round @click="quitRegisterWindow()">
          <el-icon><CloseBold /></el-icon>
      </el-button>
    </div>
    <div class="form-container">
      <el-form :rules="rules" :model="registerForm" ref="registerForm" label-width="80px">
        <div>
          <el-form-item prop="username" label="姓名">
            <el-input v-model="registerForm.username" clearable placeholder="请输入姓名" :style="{width: '300px', height: '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="registerAccount" label="学工号">
            <el-input v-model="registerForm.account" clearable placeholder="请输入学工号" :style="{width: '300px', height: '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="telephone" label="电话">
            <el-input v-model="registerForm.telephone" clearable placeholder="请输入电话" :style="{width: '300px', height: '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="email" label="邮箱">
            <el-input v-model="registerForm.email" clearable placeholder="请输入邮箱" :style="{width : '300px', height : '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="registerPassword" label="密码">
            <el-input v-model="registerForm.password" show-password clearable placeholder="请输入密码" :style="{width : '300px', height : '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="confirmPassword" label="确认密码">
            <el-input v-model="registerForm.rePassword" show-password clearable placeholder="请再次输入密码" :style="{width : '300px', height : '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item label="注册类型" prop="userType">
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <el-radio-group v-model="registerForm.userType">
              <el-radio label="普通用户">普通用户</el-radio>
              <el-radio label="团队负责人">团队负责人</el-radio>
            </el-radio-group>
          </el-form-item>
        </div>
      </el-form>
      <div class="submit-container">
          <el-button class="register-button" @click="registerSubmit()">注 册</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus';

export default {
  data() {
    const validateLoginPassword = (rule, value, callback) => {
      if (this.loginForm.password === '') {
        callback(new Error("密码不能为空！"));
      }
      else {
        callback();
      }
    };
    const validateLoginAccount = (rule, value, callback) => {
      if (this.loginForm.account === "") {
        callback(new Error("学工号不能为空！"));
      }
      else {
        callback();
      }
    };
    const validateRegisterUserName = (rule, value, callback) => {
      if (this.registerForm.username === '') {
        callback(new Error("姓名不能为空！"));
      }
      else {
        callback();
      }
    };
    const validateRegisterAccount = (rule, value, callback) => {
      if (this.registerForm.account === '') {
        callback(new Error("学工号不能为空！"));
      }
      else {
        callback();
      }
    };
    const validateTelephone = (rule, value, callback) => {
      if (this.registerForm.telephone === '') {
        callback(new Error("电话不能为空！"));
      }
      else {
        callback();
      }
    };
    const validateEmail = (rule, value, callback) => {
      if (this.registerForm.email === '') {
        callback(new Error('邮箱不能为空！'))
      }
      let reg = /^[a-zA-Z0-9]+([-_.][A-Za-zd]+)*@([a-zA-Z0-9]+[-.])+[A-Za-zd]{2,5}$/
      var result = reg.test(this.registerForm.email)
      if (!result) {
          callback(new Error('邮箱格式不正确！'));
      }
      else {
        callback();
      }
    };
    const validateRegisterPassword = (rule, value, callback) => {
      if (this.registerForm.password === '') {
        callback(new Error("密码不能为空！"));
      }
      else if (this.registerForm.password.length < 6) {
        callback(new Error("密码长度不能小于6位! "));
      }
      else {
        callback();
      }
    };
    const validateConfirmPassword = (rule, value, callback) => {
      if (this.registerForm.rePassword === '') {
        callback(new Error("请重新确认密码！"));
      }
      else if (this.registerForm.rePassword !== this.registerForm.password) {
        callback(new Error("两次密码不一致！"));
      }
      else {
        callback();
      }
    };
    return {
      rules: {
        loginAccount: [
          {validator: validateLoginAccount, trigger: 'blur'},
        ],
        username: [
          {validator: validateRegisterUserName, trigger: 'blur'},
        ],
        telephone: [
          {validator: validateTelephone, trigger: 'blur'},
        ],
        email: [
          {validator: validateEmail, trigger: 'blur'},
        ],
        registerAccount: [
          {validator: validateRegisterAccount, trigger: 'blur'},
        ],
        loginPassword: [
          {validator: validateLoginPassword, trigger: 'blur'},
        ],
        registerPassword: [
          {validator: validateRegisterPassword, trigger: 'blur'},
        ],
        confirmPassword: [
          {validator: validateConfirmPassword, trigger: 'blur'}
        ],
      },
      loginForm: {
        account: "",
        password: "",
        userType: "普通用户",
      },
      registerForm: {
        username: "",
        telephone: "",
        email: "",
        account: "",
        password: "",
        rePassword: "",
        userType: "普通用户",
      },
      loginWindowVisible: false,
      registerWindowVisible: false,
      buttonVisible: true,
    }
  },
  methods : {
    showLoginWindow() {
      this.loginWindowVisible = true;
      this.registerWindowVisible = false;
      this.buttonVisible = false;
      this.clearRegisterForm();
      console.log("showLoginWindow");
    },
    showRegisterWindow() {
      this.registerWindowVisible = true;
      this.loginWindowVisible = false;
      this.buttonVisible = false;
      this.clearLoginForm();
      console.log("showRegisterWindow");
    },
    quitLoginWindow() {
      this.loginWindowVisible = false;
      this.registerWindowVisible = false;
      this.buttonVisible = true;
      this.clearLoginForm();
      this.clearRegisterForm();
    },
    quitRegisterWindow() {
      this.registerWindowVisible = false;
      this.loginWindowVisible = false;
      this.buttonVisible = true;
      this.clearLoginForm();
      this.clearRegisterForm();
    },
    clearLoginForm() {
      this.loginForm.account = "";
      this.loginForm.password = "";
      this.loginForm.userType = "普通用户";
    },
    clearRegisterForm() {
      this.registerForm.account = "";
      this.registerForm.email = "";
      this.registerForm.telephone = "";
      this.registerForm.username = "";
      this.registerForm.password = "";
      this.registerForm.rePassword = "";
      this.registerForm.userType = "普通用户";
    },

    loginSubmit() {
      this.$refs.loginForm.validate(async (valid) => {
        /* 登录判断逻辑 */
        if (valid) {
          // this.$store.commit("setCollegeId", "21371295");
          // this.$store.commit("setPassword", "123456");
          // this.$store.commit("setUserName", "张昊翔");
          // this.$store.commit("setUserType", "0");
          this.$router.push({path: '/project/all'});

          const submitParams = {
            collegeId: this.loginForm.account,
            password: this.loginForm.password,
          }

          // await this.axios({
          //   method: 'post',
          //   url: 'http://localhost:8000/login_info',
          //   data: submitParams,
          // })
          //   .then(async(res) => {
          //     console.log(res);
          //     /* 登陆成功 */
          //     if (res.data.code === 0) {
          //       console.log("登录成功");
          //       ElMessage.success('登录成功');
          //       this.$store.commit("setUserId", res.data.userId);
          //       this.$store.commit("setUserName", res.data.userName);
          //       this.$store.commit("setCollegeId", this.loginForm.account);
          //       this.$store.commit("setIsAdmin", res.data.userType === "0" ? false : true);
          //       this.$store.commit("setPassword", this.loginForm.password);
          //       this.$store.commit("setUserType", res.data.userType);
          //       this.$router.push({path: '/project/all'});
          //     }
          //     /* 用户不存在 */
          //     else if (res.data.code === 1) {
          //       console.log("用户不存在");
          //       ElMessage.error('该用户不存在！');
          //     }
          //     /* 密码错误 */
          //     else if (res.data.code === 2) {
          //       console.log("密码错误");
          //       ElMessage.error('密码错误！');
          //     }
          //   })
        }
        else {
          ElMessage.error("请填写正确的登录信息");
        }
      });
    },
    registerSubmit() {
      this.$refs.registerForm.validate(async(valid) => {
          if (valid) {
            console.log("注册信息有效");
            /* 注册有效逻辑 */
            const submitParams = {
              userName: this.registerForm.username,
              collegeId: this.registerForm.account,
              password: this.registerForm.password,
              email: this.registerForm.email,
              telephone: this.registerForm.telephone,
              userType: this.registerForm.userType === "普通用户" ? "0" : "1",
            }

            await this.axios({
              method: 'post',
              url: 'http://localhost:8000/register_info',
              data: submitParams,
            })
              .then(async (res) => {
                  /* 注册成功 */
                  console.log(res);
                  if (res.data.code === 0) {
                    ElMessage.success('注册成功');
                    this.$store.commit("setUserId", res.data.userId);
                    this.$store.commit("setUserName", this.registerForm.username);
                    this.$store.commit("setCollegeId", this.registerForm.account);
                    this.$store.commit("setIsAdmin", this.registerForm.userType === "普通用户" ? false : true);
                    this.$store.commit("setPassword", this.registerForm.password);
                    this.$router.push({path: '/project/all'});
                  }
                  /* 重复注册 */
                  else if (res.data.code === 1) {
                    ElMessage.error('该用户已被注册！');
                  }
                }
            )

          }
          else {
            ElMessage.error('请正确填写注册信息！');
          }
        });
    }

  }
}
</script>

<style scoped>
.main {
  background-image: url(../assets/images/mountain.png);
  background-size: cover;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.test {
  border-radius: 1em
}

.top-container {
  position: absolute;
  height: 100px;
  width: 1000px;
  font-size: 80px;
  font-weight: bold;
  color: white;
  top: 150px;
  text-align: center;
}

.button-container {
  margin-top: 200px;
  display: flex;
  justify-content: center;
}

.form-container {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  margin-top: 50px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  height: 400px;
  width: 600px;
  background: rgba(235, 233, 233, 0.8);
  border-radius: 10px;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  margin-top: 50px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  height: 600px;
  width: 600px;
  background: rgba(235, 233, 233, 0.8);
  border-radius: 10px;
}

.quit-container {
  position: absolute;
  top: 10px;
  right: 10px;
}

.spacer {
  width: 200px;
}

.hint {
  margin-top: 22px;
  font-size: 15px;
}

.button {
  font-size: 40px;
  font-weight: bold;
  width: 170px;
  height: 80px;
}

.login-button {
  margin-top: 15px;
  font-size: 25px;
  height: 50px;
  width: 120px;
}

.register-button {
  margin-top: 20px;
  font-size: 25px;
  height: 50px;
  width: 120px;
}

.form-font {
  font-size: 25px;
  margin-right: 20px;
}

</style>