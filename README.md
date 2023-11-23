# API
## UserInfoPage

### 获取用户信息
* 发送请求：

  ```javascript
  {
    userId: "00001",
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    telephone: "18100000000",
    email: "abcd@xyz.com",
    volunteerTime: "20",
    userIntro: "我是一个好人。"
  }
  ```


### 修改用户信息

* 发送请求：

  ```javascript
  {
    userId: "00001",
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
    userId: "00001",
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

## JoinTeamPage
### 获取所有团队

* 发送请求：

  ```javascript
  {

  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    totalList: [
        {
          id: "00001",
          name: "志愿团队1",
          date: "YYYY-MM-DD",
          number: "50",
          hours: "150"
        }
    ] 
  }
  ```

## MyTeamPage
### 获取我所在的团队

* 发送请求：

  ```javascript
  {
    userId: "00001"
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    teamList: [
        {
          id: "00001",
          name: "志愿团队1",
          number: "50",
          hours: "150"
        }
    ] 
  }
  ```
  
## TeamInfoPage
### 获取团队信息

* 发送请求：

  ```javascript
  {
    userId: "00001",
    teamId: "00001"
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    isTeamMember: true, // true: 是团队成员，false: 不是团队成员
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
  ```

### 申请加入团队

* 发送请求：

  ```javascript
  {
    userId: "00001",
    teamId: "00001"
  }
  ```

* 申请成功

  ```javascript
  {
    code: 0,
    message: ""
  }
  ```

## AllProjectPage
### 获取所有项目

* 发送请求：

  ```javascript
  {
    userId: "00001"
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    projectList: [
        {
          id: "00001",
          name: "志愿项目1",
          type: "社区服务",
          team: "志愿团队1",
          isMyTeam: true, // true: 是我所在的团队，false: 不是我所在的团队
          status: "招募中" // 招募中、本月、本学期、上学期、本学年未招募
        }
    ] 
  }
  ```

## MyProjectPage
### 获取我收藏的项目

* 发送请求：

  ```javascript
  {
    userId: "00001"
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    projectList: [
        {
          id: "00001",
          name: "志愿项目1",
          type: "社区服务",
          team: "志愿团队1",
          latestTime: "YYYY-MM-DD" // 上一次招募时间 
          status: "招募中" // 招募中、本月、本学期、上学期、本学年未招募
        }
    ] 
  }
  ```
