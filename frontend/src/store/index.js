import { createStore } from 'vuex'

// 使用全局变量的例子：
// 设置全局变量（调用对应函数）：this.$store.commit("setUserName", "yourUserName");
// 获取全局变量（直接修改引用）：let tempUserName = this.$store.state.userName;

const store = createStore({
    state() {
        return {
            userName: null,
            account: null, // collegeId
            email: null,
            userType: null,
            isAdmin: null,
            
        }
    },
    mutations: {
        setUserName(state, userName) {
            state.userName = userName;
        },
        setAccount(state, account) {
            state.account = account;
        },
        setEmail(state, email) {
            state.email = email;
        },
        setIsAdmin(state, isAdmin) {
            state.isAdmin = isAdmin;
        },

    },

})

export default store;