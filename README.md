# API
## UserInfoPage

### 获取用户信息
* 发送请求：

  ```javascript
  {
      collegeId: "21371295"
  }
  ```

* 获取成功

  ```javascript
  {
      code: 0,
      message: "",
      data: {
          telephone: "18100000000",
          email: "abcd@xyz.com",
          volunteerTime: "20",
          userIntro: "我是一个好人。"
      }
  }
  ```


### 修改用户信息

* 发送请求：

  ```javascript
  {
      collegeId: "21371295",
      telephone: "18100000000",
      email: "abcd@xyz.com",
      userIntro: "我是一个好人。"
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
      collegeId: "21371295",
      newPassword: "123456"
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
### 获取我所在的团队

* 发送请求：

  ```javascript
  {
      collegeId: "21371295"
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
                  id: "00001",
                  name: "志愿团队1",
                  number: "50",
                  hours: "150"
              }
          ]
      }
  }
  ```
  
## TeamInfoPage
### 获取团队信息

* 发送请求：

  ```javascript
  {
      collegeId: "21371295",
      teamId: "00001"
  }
  ```

* 获取成功

  ```javascript
  {
      code: 0,
      message: "",
      data: {
          isTeamMember: "0", // 0: 不是团队成员，1: 是团队成员
          teamName: "志愿团队1",
          teamNumber: "50",
          teamIntro: "优秀团队。",
          foundationDate: "YYYY-MM-DD",
          teamLeader: "张昊翔",
          telephone: "18100000000",
          email: "abcd@xyz.com",
          projectList: [
              { 
                  id: "00001", 
                  name: "志愿项目1", 
                  type: "社区服务", 
                  hours: "100" 
              }  
          ]
      }
  }
  ```

### 申请加入团队

* 发送请求：

  ```javascript
  {
      collegeId: "21371295",
      teamId: "00001",
      applyTime: "YYYY-MM-DD HH:MM:SS"
  }
  ```

* 申请成功

  ```javascript
  {
      code: 0,
      message: ""
  }
  ```

