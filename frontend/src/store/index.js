import { createStore } from 'vuex'

// 使用全局变量的例子：
// 设置全局变量（调用对应函数）：this.$store.commit("setUserName", "yourUserName");

const store = createStore({
    state() {
        return {
            userId: null,
            userName: null,
            collegeId: null,
            email: null,
            telephone: null,
            userType: null,
            isAdmin: true,
            password: null,
            userIntro: null,
            totalHours: null,
        }
    },
    mutations: {
        setUserId(state, userId) {
            state.userId = userId;
        },
        setUserName(state, userName) {
            state.userName = userName;
        },
        setPassword(state, password) {
            state.password = password;
        },
        setCollegeId(state, collegeId) {
            state.collegeId = collegeId;
        },
        setEmail(state, email) {
            state.email = email;
        },
        setUserType(state, userType) {
            state.userType = userType;
        },
        setIsAdmin(state, isAdmin) {
            state.isAdmin = isAdmin;
        },
        setTelephone(state, telephone) {
            state.telephone = telephone;
        },
        setPassword(state, password) {
            state.password = password;
        },
        setUserIntro(state, userIntro) {
            state.userIntro = userIntro;
        },
        setTotalHours(state, totalHours) {
            state.totalHours = totalHours;
        },
    },

})

export default store;