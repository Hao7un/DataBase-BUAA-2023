# API
## UserInfoPage

### 获取用户信息
* 发送请求：

  ```javascript
  {
    userId: "1",
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
    userIntro: "我是张昊翔。"
  }
  ```


### 修改用户信息

* 发送请求：

  ```javascript
  {
    userId: "1",
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
    userId: "1",
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
          id: "1",
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
    userId: "1"
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    teamList: [
        {
          id: "1",
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
    userId: "1",
    teamId: "1"
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
    joinDate: "YYYY-MM-DD", // N/A: 未加入团队
    teamLeader: "张昊翔",
    telephone: "18100000000",
    email: "abcd@xyz.com",
    projectList: [
        { 
          id: "1", 
          name: "志愿项目1", 
          type: "1", // 1: 社区服务，2: 科技科普，3: 支教助学，4: 体育赛事，5: 大型演出，6: 其它
          times: "10" 
        }  
    ]
  }
  ```

### 申请加入团队

* 发送请求：

  ```javascript
  {
    userId: "1",
    teamId: "1"
  }
  ```

* 申请成功

  ```javascript
  {
    code: 0,
    message: ""
  }
  ```

* 重复申请

  ```javascript
  {
    code: 1,
    message: ""
  }
  ```

## AllProjectPage
### 获取所有项目

* 发送请求：

  ```javascript
  {
    userId: "1"
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    projectList: [
        {
          id: "1",
          name: "志愿项目1",
          type: "1", // 1: 社区服务，2: 科技科普，3: 支教助学，4: 体育赛事，5: 大型演出，6: 其它
          team: "志愿团队1",
          isMyTeam: true, // true: 是我所在的团队，false: 不是我所在的团队
          latestTime: "YYYY-MM-DD", // 上一次招募结束时间 
        }
    ] 
  }
  ```

## MyProjectPage
### 获取我收藏的项目

* 发送请求：

  ```javascript
  {
    userId: "1"
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    projectList: [
        {
          id: "1",
          name: "志愿项目1",
          type: "1", // 1: 社区服务，2: 科技科普，3: 支教助学，4: 体育赛事，5: 大型演出，6: 其它
          team: "志愿团队1",
          latestTime: "YYYY-MM-DD", // 上一次招募结束时间，N/A: 未发布招募
        }
    ] 
  }
  ```

## ProjectInfoPage
### 获取项目信息

* 发送请求：

  ```javascript
  {
    userId: "1",
    projectId: "1"
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    isCollect: true, // true: 已收藏，false: 未收藏
    projectName: "志愿项目1",
    projectType: "1" // 1: 社区服务，2: 科技科普，3: 支教助学，4: 体育赛事，5: 大型演出，6: 其它
    projectIntro: "优秀项目。",
    latestTime: "YYYY-MM-DD", // 上一次招募结束时间，N/A: 未发布招募
    projectLeader: '张昊翔', // 团队负责人
    teamId: "1",
    teamName: "志愿团队1",
    discussionList: [
        {
          questionPoster: "张三", 
          questionTime: "YYYY-MM-DD HH:MM", 
          question: "需要什么技能？", 
          replyTime: "YYYY-MM-DD HH:MM", 
          reply: "需要一定的技术基础。"
        }
    ],
    tutorialList: [
        {
          id: "1",
          time: "YYYY-MM-DD HH:MM",
          title: "注意事项",
          tag: "培训",
          content: "注意安全。"
        }
    ]
  }
  ```

### 收藏/取消收藏项目

* 发送请求：

  ```javascript
  {
    userId: "1",
    projectId: "1",
    type: false  // true: 取消收藏，false: 收藏
  }
  ```

* 收藏/取消收藏成功

  ```javascript
  {
    code: 0,
    message: ""
  }
  ```

### 发布提问

* 发送请求：

  ```javascript
  {
    userId: "1",
    projectId: "1",
    question: "需要什么技能？"
  }
  ```

* 提问成功

  ```javascript
  {
    code: 0,
    message: ""
  }
  ```

## JoinRecruitmentPage
### 获取可见招募信息
**仅包含我所在的团队的招募和其它团队的公开招募**

* 发送请求：

  ```javascript
  {
    userId: "1"
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    recruitmentList: [
        {
          id: "1",
          launchTime: "YYYY-MM-DD HH:MM", // 招募发布时间
          dueTime: "YYYY-MM-DD HH:MM", // 招募结束时间
          startTime: "YYYY-MM-DD HH:MM", // 活动开始时间
          endTime: "YYYY-MM-DD HH:MM", // 活动结束时间
          location: "操场",
          volunteerHour: "5",
          isAttend: true, // true: 已报名，false: 未报名
          type: "1", // 1: 面向公共招募，2: 仅限团队内部
          maxNumber: "50",
          currentNumber: "30",
          projectId: "1",
          projectName: "志愿项目1",
          projectType: "1" // 1: 社区服务，2: 科技科普，3: 支教助学，4: 体育赛事，5: 大型演出，6: 其它
        }
    ] 
  }
  ```

### 报名招募

* 发送请求：

  ```javascript
  {
    userId: "1",
    recruitmentId: "1"
  }
  ```

* 报名成功

  ```javascript
  {
    code: 0,
    message: ""
  }
  ```

* 人数已满

  ```javascript
  {
    code: 1,
    message: ""
  }
  ```

* 时间冲突

  ```javascript
  {
    code: 2,
    message: ""
  }
  ```

## MyRecruitmentPage
### 获取我参加的招募信息

* 发送请求：

  ```javascript
  {
    userId: "1"
  }
  ```

* 获取成功

  ```javascript
  {
    code: 0,
    message: "",
    futureRecruitmentList: [
        {
          id: "1",
          startTime: "YYYY-MM-DD HH:MM", // 活动开始时间
          endTime: "YYYY-MM-DD HH:MM", // 活动结束时间
          location: "操场",
          volunteerHour: "5",
          type: "1", // 1: 面向公共招募，2: 仅限团队内部
          maxNumber: "50",
          participantNumber: "30",
          projectId: "1",
          projectName: "志愿项目1",
          projectType: "1" // 1: 社区服务，2: 科技科普，3: 支教助学，4: 体育赛事，5: 大型演出，6: 其它
        }
    ],
    pastRecruitmentList: [
        {
          id: "1",
          startTime: "YYYY-MM-DD HH:MM", // 活动开始时间
          endTime: "YYYY-MM-DD HH:MM", // 活动结束时间
          location: "操场",
          volunteerHour: "5",
          type: "1", // 1: 面向公共招募，2: 仅限团队内部
          maxNumber: "50",
          participantNumber: "30",
          projectId: "1",
          projectName: "志愿项目1",
          projectType: "1" // 1: 社区服务，2: 科技科普，3: 支教助学，4: 体育赛事，5: 大型演出，6: 其它
        }
    ] 
  }
  ```