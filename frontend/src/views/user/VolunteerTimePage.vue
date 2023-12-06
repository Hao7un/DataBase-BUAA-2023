<template>
    <div class="main-container">
        <div class="sidebar-container">
            <el-menu mode="vertical" default-active="volunteerTime"
                style="border-right: 0px solid rgb(114, 110, 104, 0.2);">
                <el-menu-item index="info" @click="changeToUserInfoPage">
                    <span class="item-font" style="font-weight: bold;">个人信息</span>
                </el-menu-item>
                <el-menu-item index="volunteerTime" @click="changeToVolunteerTimePage">
                    <span class="item-font" style="font-weight: bold;">志愿统计</span>
                </el-menu-item>
            </el-menu>
        </div>
        <v-btn class="back-button" @click="handleBack">
            <template v-slot:prepend>
                <el-icon>
                    <Back />
                </el-icon>
            </template>
            返回
        </v-btn>
        <div>
            <div ref="barChart" style="width: 600px; height: 400px;"></div>
            <div ref="pieChart" style="width: 600px; height: 400px;"></div>
            <div ref="lineChart" style="width: 600px; height: 400px;"></div>
        </div>
    </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    mounted() {
        this.initBarChart();
        this.initPieChart();
        this.initLineChart();
    },
    computed: {
        userId() {
            return this.$store.state.userId;
        },
        lastMenu() {
            return this.$store.state.lastMenu;
        }
    },
    methods: {
        changeToUserInfoPage() {
            this.$router.push({
                path: '/user/info'
            })
        },
        changeToVolunteerTimePage() {
            this.$router.push({
                path: '/user/volunteer-time'
            })
        },
        handleBack() {
            this.$store.commit("setActiveMenu", this.lastMenu);
            this.$router.go(-1);
        },
        initBarChart() {
            const chartDom = this.$refs.barChart;
            const myChart = echarts.init(chartDom);

            const option = {
                title: {
                    text: '柱图示例'
                },
                xAxis: {
                    type: 'category',
                    data: ['A', 'B', 'C', 'D', 'E']
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    name: '柱图数据',
                    type: 'bar',
                    data: [10, 20, 15, 25, 30]
                }]
            };

            myChart.setOption(option);
        },
        initPieChart() {
            const chartDom = this.$refs.pieChart;
            const myChart = echarts.init(chartDom);

            const option = {
                title: {
                    text: '饼图示例',
                    left: 'center'
                },
                series: [{
                    name: '饼图数据',
                    type: 'pie',
                    radius: '50%',
                    data: [
                        { value: 10, name: 'A' },
                        { value: 20, name: 'B' },
                        { value: 15, name: 'C' },
                        { value: 25, name: 'D' },
                        { value: 30, name: 'E' }
                    ]
                }]
            };
            myChart.setOption(option);
        },
        initLineChart() {
            const chartDom = this.$refs.lineChart;
            const myChart = echarts.init(chartDom);

            const option = {
                title: {
                    text: '折线图示例'
                },
                xAxis: {
                    type: 'category',
                    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    name: '示例数据',
                    type: 'line',
                    data: [150, 230, 224, 218, 135, 147, 260]
                }]
            };

            myChart.setOption(option);
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
    height: auto;
    min-height: 750px;
    border-right: 2px solid rgb(114, 110, 104, 0.2);
}

.item-font {
    font-size: 18px;
    margin-left: 10px;
}

.back-button {
    font-weight: bold;
    font-size: 16px;
}
</style>