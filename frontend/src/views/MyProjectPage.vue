<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="my">
                <el-menu-item index="join" @click="changeToJoinProjectPage">
                    <span class="item-font" style="font-weight: bold">加入项目</span>
                </el-menu-item>
                <el-menu-item index="my" @click="changeToMyProjectPage">
                    <span class="item-font" style="font-weight: bold">我的项目</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="content-container">
            
        </div>
    </div>
</template>


<script>

export default {
    data() {
        return {
            typeRadio: null,
            authRadio: null,
            statusRadio: null,
            date: null,
            keyword: null,
            currentPage: 1,
            totalList: [
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
                {hours: 0, number: 0, remaining: 0, intro: null},
            ]
        };
    },
    computed: {
        displayedList() {
            let startIndex = (this.currentPage - 1) * 9;
            return this.totalList.slice(startIndex, startIndex + 9);
        }
    },
    methods: {
        handlePageChange(currentPage) {
            this.currentPage = currentPage;
        },
        changeToMyProjectPage() {
            this.$router.push({
            path: '/project/my'
        })
        },
        changeToJoinProjectPage() {
            this.$router.push({
            path: '/project/join'
        })
        },
        checkRecruitmentTable() {
            /* 招募逻辑 */
            alert("这是招募表单！");
        }
    }
}

</script>


<style scoped>
.main-container {
    display: flex;
}

.sidebar-container {
    display: flex;
    width: 180px;
    flex-direction: column;
    padding-top: 20px;
    margin-left: 20px;
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.icon-container {
    font-size: 25px;
}

.content-container {
    display: flex;   
    flex-direction: column;
}

.selector-container {
    height: 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
}

.menu-container {
    width: 590px;
}

.search-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 160px;
    margin-right: 100px;
}

.search-item-container {
    margin-left: 10px;
    margin-right: 15px;
}

.radio-container {
    display: flex;
    flex-direction: column;
    width: 130px;
}

.recruitments-container {
    display: flex;
    align-items: center;
    flex-direction: column;
}

.info-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-content: flex-start;
    margin-top: 40px;
    height: 1000px;
    width: 1350px;
}

.card {
    width: calc(33.33% - 10px);
    height: 300px;
    margin-top: 20px;
    margin-right: 8px;
}

.inner-card {
    width: 100%;
    height: 100%;
}

.img-container {
    width: 100%;
    height: 66.6%;
    object-fit: cover;
    display: flex;
    justify-content: center;
}

.info-item {
    margin-top: 10px;
}

.card-info {
    display: flex;
    flex-direction: column;
}

.pagination-container {
    margin-top: 50px;
    margin-bottom: 50px;
}

</style>