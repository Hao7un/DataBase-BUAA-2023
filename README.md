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

  
