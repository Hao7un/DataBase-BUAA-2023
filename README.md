# API
## UserInfoPage

### 获取用户信息
* 发送请求：

  ```javascript
  {
      collegeId: ""
  }
  ```

* 获取成功

  ```javascript
  {
      code: 0,
      message: "",
      data: {
          telephone: "",
          email: "",
          volunteerTime: "",
          userIntro: ""
      }
  }
  ```


### 修改用户信息

* 发送请求：

  ```javascript
  {
      collegeId: "",
      telephone: "",
      email: "",
      userIntro: ""
  }
  ```

* 修改成功

  ```javascript
  {
      code: 0,
      message: ""
  }
  ```

## PasswordPage
### 修改密码

* 发送请求：

  ```javascript
  {
      collegeId: "",
      newPassword: ""
  }
  ```

* 修改成功

  ```javascript
  {
      code: 0,
      message: ""
  }
  ```

* 修改失败

  ```javascript
  {
      code: 1,
      message: ""
  }
  ```

## MyTeamPage
### 获取我的团队

* 发送请求：

  ```javascript
  {
      collegeId: ""
  }
  ```

* 获取成功

  ```javascript
  {
      code: 0,
      message: "",
      data: {
          teamList: [
              {
                  id: "",
                  name: "",
                  number: "",
                  hours: "",
              }
          ]
      }
  }
  ```
  
