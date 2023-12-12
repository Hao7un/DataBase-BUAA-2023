# API

## 个人系统
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



### 上传用户头像

* 发送请求：

  ```javascript
  {
    userId: "1",
    userAvatar: file.raw
  }
  ```

* 上传成功

  ```javascript
  {
    data: image // Base64编码
  }
  ```



### 获取志愿时长信息

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
    total: 100,   // 总志愿时长
    totalTarget: 120,
    semester: 8, // 本学期志愿时长
    semesterTarget: 16,
    type1: 20,    // 社区服务
    type2: 100,   // 科技科普
    type3: 50,    // 支教助学
    type4: 0,     // 体育赛事
    type5: 13,    // 大型演出
    type6: 20,    // 其它
    month1: 0,
    month2: 30,
    month3: 0,
    month4: 20,
    month5: 10,
    month6: 10,
    month7: 5,
    month8: 2,
    month9: 20,
    month10: 18,
    month11: 10,
    month12: 5
  }
  ```



### 设置志愿时长目标

* 发送请求：

  ```javascript
  {
    userId: "1",
    totalTarget: 120,
    semesterTarget: 16
  }
  ```

* 设置成功

  ```javascript
  {
    code: 0,
    message: ""
  }
  ```



## 团队系统

### 获取所有团队概况

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



### 获取我加入的团队概况

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



### 获取团队头像

* 发送请求
  ```javascript
  {
    teamId: "1"
  }
  ```

* 获取成功

  ```javascript
  {
    data: image // Base64编码
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



## 项目系统

### 获取所有项目概况

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
          latestTime: "YYYY-MM-DD" // 上一次招募结束时间 
        }
    ] 
  }
  ```



### 获取我收藏的项目概况

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
          latestTime: "YYYY-MM-DD" // 上一次招募结束时间，N/A: 未发布招募
        }
    ] 
  }
  ```



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
    leaderId: "1",  // 团队负责人
    leaderName: "张昊翔",
    teamId: "1",
    teamName: "志愿团队1",
    discussionList: [
        {
          posterId: "1",
          posterName: "张三", 
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



### 获取项目头像

* 发送请求
  ```javascript
  {
    teamId: "1"
  }
  ```

* 获取成功

  ```javascript
  {
    data: image // Base64编码
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



## 招募系统

### 获取可见招募信息
可见招募有**我加入的团队的招募**和其它团队的**公开招募**

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
    futureRecruitmentList: [  // 即将进行的活动
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
    pastRecruitmentList: [    // 已经结束的活动
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