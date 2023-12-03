<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="list" style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="info" @click="changeToTeamManagePage">
                    <span class="item-font" style="font-weight: bold;">团队详情</span>
                </el-menu-item>
                <el-menu-item index="list" @click="changeToProjectListPage">
                    <span class="item-font" style="font-weight: bold;">项目管理</span>
                </el-menu-item>
            </el-menu>
          </div>
        <div class="content-container">
            <div class="selector-container">
                <div class="left">
                    <el-input v-model="nameKey" placeholder="搜索项目名称" clearable size="large" style="width: 200px">
                        <template #prefix>
                            <el-icon><Open /></el-icon>
                        </template>                    
                    </el-input>
                </div>
                <div class="right">
                    <el-select v-model="typeKey" placeholder="选择项目类别" clearable size="large">
                        <el-option>
                            <template #prefix>
                                <el-icon><FolderOpened /></el-icon>
                            </template>
                            <el-option>

                            </el-option>                          
                        </el-option>
                    </el-select>
                </div>
            </div>
            <div class="projects-container">

            </div>
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            nameKey: "",
            typeKey: "",
        }
    },
    methods: {
        fetch() {

        },
        changeToProjectListPage() {
            this.$router.push({
                path: '/admin/projectlist'
                // params
            })
        },
        changeToTeamManagePage() {
            this.$router.push({
                path: '/admin/teaminfo'
                // params
            })
        },
    },
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
    height: 1000px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.selector-container {
    width: 1200px;
    margin-top: 50px;
    margin-left: 400px;
    display: flex;
    align-items: center;
}



</style>