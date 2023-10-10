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
      <el-form :rules="rules" :model="loginForm" ref="loginForm">
        <div>
          <el-form-item prop="username">
            <span class="form-font">用户名</span>
            <el-input v-model="loginForm.username" clearable placeholder="请输入用户名" :style="{width : '275px', height : '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="loginPassword">
            <span class="form-font">密码</span>
            <el-input v-model="loginForm.password" show-password clearable placeholder="请输入密码" :style="{width : '300px', height : '40px'}"></el-input>
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
      <el-form :rules="rules" :model="registerForm" ref="registerForm">
        <div>
          <el-form-item prop="username">
            <span class="form-font">用户名</span>
            <el-input v-model="registerForm.username" clearable placeholder="请输入用户名" :style="{width : '275px', height : '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="account">
            <span class="form-font">学工号</span>
            <el-input v-model="registerForm.account" clearable placeholder="请输入学工号" :style="{width : '275px', height : '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="telephone">
            <span class="form-font">电话</span>
            <el-input v-model="registerForm.telephone" clearable placeholder="请输入电话" :style="{width : '300px', height : '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="email">
            <span class="form-font">邮箱</span>
            <el-input v-model="registerForm.email" clearable placeholder="请输入邮箱" :style="{width : '300px', height : '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="registerPassword">
            <span class="form-font">密码</span>
            <el-input v-model="registerForm.password" show-password clearable placeholder="请输入密码" :style="{width : '300px', height : '40px'}"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item prop="confirmPassword">
            <span class="form-font">确认密码</span>
            <el-input v-model="registerForm.rePassword" show-password clearable placeholder="请再次输入密码" :style="{width : '250px', height : '40px'}"></el-input>
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
      // else if (密码错误) {
        // callback(new Error("密码错误！"));
      // }
      else {
        callback();
      }
    };
    const validateRegisterPassword = (rule, value, callback) => {
      if (this.registerForm.password === '') {
        callback(new Error("密码不能为空！"));
      }
      else if (this.registerForm.password.length < 6) {
        callback(new Error("密码长度不能小于6位！"));
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
        username: [
          {required: true, message: "用户名不能为空！", trigger: 'blur'},
        ],
        telephone: [
          {required: true, message: "电话不能为空！", trigger: 'blur'},
        ],
        email: [
          {required: true, message: "邮箱不能为空！", trigger: 'blur'},
          {type: "email", message: "请输入有效的邮箱地址！", trigger: 'blur'}
        ],
        account: [
          {required: true, message:"学工号不能为空！", trigger: 'blur'},
        ],
        loginPassword: [
          {validator: validateLoginPassword, trigger: 'blur'},
        ],
        registerPassword: [
          {validator: validateRegisterPassword, trigger: 'blur'},
        ],
        confirmPassword: [
          {validator: validateConfirmPassword, trigger: 'blur'}
        ]
      },
      loginForm: {
        username: "",
        password: "",
      },
      registerForm: {
        username: "",
        telephone: "",
        email: "",
        account: "",
        password: "",
        rePassword: "",
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
      this.loginForm.username = "";
      this.loginForm.password = "";
    },
    clearRegisterForm() {
      this.registerForm.account = "";
      this.registerForm.email = "";
      this.registerForm.telephone = "";
      this.registerForm.username = "";
      this.registerForm.password = "";
      this.registerForm.rePassword = "";
    },

    loginSubmit() {
      this.$refs.loginForm.validate(valid => {
        /* 登录判断逻辑 */
        if (valid) {
          console.log("登录成功");
          ElMessage.success('登陆成功')
          this.$router.push({path: '/project/join'});
        }
        else {
          ElMessage.error("请填写正确的登录信息");
        }
      });
    },
    registerSubmit() {
      this.$refs.registerForm.validate(valid => {
          if (valid) {
            console.log("注册成功");
            /* 注册成功逻辑 */
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