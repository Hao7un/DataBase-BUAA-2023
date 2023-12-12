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
        <div class="statistic-container">
            <div class="title-container">
                <p>志愿者<strong>{{ userName }}</strong>，您本学期的志愿时长为 <strong>{{ semester
                }}</strong> 小时，累计志愿时长 <strong>{{ total }}</strong> 小时。</p>
                <el-button type="primary" round size="large" style="margin-left: 100px;" @click="showDialog">
                    <span style="font-weight: bold; font-size: 15px; color:whitesmoke">设置目标</span></el-button>
            </div>
            <div class="progress-container">
                <div class="progress">
                    <span style="font-weight: bold; font-size: 18px;">累计</span>
                    <el-progress :text-inside="true" :stroke-width="30" :percentage="totalPercent"
                        :status="totalPercent == 100 ? 'success' : ''" />
                </div>
                <div class="progress">
                    <span style="font-weight: bold; font-size: 18px;">本学期</span>
                    <el-progress :text-inside="true" :stroke-width="30" :percentage="semesterPercent" />
                </div>
            </div>
            <div class="chart-container">
                <el-radio-group v-model="statisticType">
                    <el-radio label="type" size="large" style="font-weight: bold;" border>按类别</el-radio>
                    <el-radio label="month" size="large" style="font-weight: bold;" border>按月份</el-radio>
                </el-radio-group>
                <div v-if="statisticType === 'type'" ref="pieChart" class="chart-item"></div>
                <div v-else ref="lineChart" class="chart-item"></div>
            </div>
        </div>

        <el-dialog v-model="dialogVisible" title="设置目标" width="30%" align-center center draggable>
            <div class="input-container">
                <label class="text-font">累计目标：</label>
                <el-input v-model="newTotalTarget" type="text" class="mb-3" />
                <label class="text-font">本学期目标：</label>
                <el-input v-model="newSemesterTarget" type="text" class="mb-3" />
            </div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="closeDialog">取消</el-button>
                    <el-button type="primary" @click="editTarget">
                        <span style="color:whitesmoke; font-weight: bold;">完成</span>
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus';
import * as echarts from 'echarts';

export default {
    async created() {
        await this.fetchStatistic();
    },
    async mounted() {
        await this.fetchStatistic();
        this.initPieChart();
        this.initLineChart();
    },
    computed: {
        userId() {
            return this.$store.state.userId;
        },
        userName() {
            return this.$store.state.userName;
        },
        lastMenu() {
            return this.$store.state.lastMenu;
        },
        totalPercent() {
            let percent = this.total / this.totalTarget * 100;
            if (percent > 100) {
                percent = 100;
            }
            return percent.toFixed(1);
        },
        semesterPercent() {
            let percent = this.semester / this.semesterTarget * 100;
            if (percent > 100) {
                percent = 100;
            }
            return percent.toFixed(1);
        }
    },
    data() {
        return {
            statisticType: 'type',
            total: 100,
            totalTarget: 120,
            semester: 5,
            semesterTarget: 16,
            type1: 20,
            type2: 100,
            type3: 50,
            type4: 0,
            type5: 13,
            type6: 20,
            january: 0,
            february: 30,
            march: 0,
            april: 20,
            may: 10,
            june: 10,
            july: 5,
            august: 2,
            september: 20,
            october: 18,
            november: 10,
            december: 5,
            dialogVisible: false,
            newTotalTarget: '',
            newSemesterTarget: ''
        }
    },
    watch: {
        statisticType(newType) {
            this.$nextTick(() => {
                if (newType === 'type') {
                    this.initPieChart();
                } else {
                    this.initLineChart();
                }
            });
        }
    },
    methods: {
        async fetchStatistic() {
            const res = await this.axios.post('http://localhost:8000/user_get_volunteer_statistics', {
                userId: this.userId
            });
            console.log(res);
            if (res.data.code === 0) {
                this.total = res.data.total;
                this.totalTarget = res.data.totalTarget;
                this.semester = res.data.semester;
                this.semesterTarget = res.data.semesterTarget;
                this.type1 = res.data.type1;
                this.type2 = res.data.type2;
                this.type3 = res.data.type3;
                this.type4 = res.data.type4;
                this.type5 = res.data.type5;
                this.type6 = res.data.type6;
                this.january = res.data.january;
                this.february = res.data.february;
                this.march = res.data.march;
                this.april = res.data.april;
                this.may = res.data.may;
                this.june = res.data.june;
                this.july = res.data.july;
                this.august = res.data.august;
                this.september = res.data.september;
                this.october = res.data.october;
                this.november = res.data.november;
                this.december = res.data.december;
            }
        },
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
        showDialog() {
            this.newTotalTarget = this.totalTarget;
            this.newSemesterTarget = this.semesterTarget;
            this.dialogVisible = true;
        },
        closeDialog() {
            this.dialogVisible = false;
        },
        editTarget() {
            if (this.newTotalTarget == '' || this.newSemesterTarget == '') {
                ElMessage.error('请设置目标');
            } else {
                this.axios.post('http://localhost:8000/update_hour_target', {
                    userId: this.userId,
                    totalTarget: Number(this.newTotalTarget),
                    semesterTarget: Number(this.newSemesterTarget)
                })
                    .then(res => {
                        console.log(res);
                        if (res.data.code === 0) {
                            console.log("设置成功");
                            ElMessage.success('设置成功');
                            this.totalTarget = Number(this.newTotalTarget);
                            this.semesterTarget = Number(this.newSemesterTarget);
                            this.dialogVisible = false;
                        }
                    });
            }
        },
        initPieChart() {
            const chartDom = this.$refs.pieChart;
            const myChart = echarts.init(chartDom);

            const option = {
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '5%',
                    left: 'center'
                },
                series: [
                    {
                        name: '项目类别',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        avoidLabelOverlap: false,
                        itemStyle: {
                            borderRadius: 10,
                            borderColor: '#fff',
                            borderWidth: 2
                        },
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: 20,
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: [
                            { value: this.type1, name: '社区服务' },
                            { value: this.type2, name: '科技科普' },
                            { value: this.type3, name: '支教助学' },
                            { value: this.type4, name: '体育赛事' },
                            { value: this.type5, name: '大型演出' },
                            { value: this.type6, name: '其它' }
                        ]
                    }]
            };
            myChart.setOption(option);
        },
        initLineChart() {
            const chartDom = this.$refs.lineChart;
            const myChart = echarts.init(chartDom);

            const option = {
                tooltip: {
                    trigger: 'axis'
                },
                xAxis: {
                    type: 'category',
                    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: [this.january, this.february, this.march, this.april, this.may, this.june, this.july, this.august, this.september, this.october, this.november, this.december],
                        type: 'line',
                        smooth: true
                    }
                ]
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
    margin-top: 30px;
    margin-left: 50px;
}

.statistic-container {
    display: flex;
    flex-direction: column;
    margin-left: 50px;
    margin-top: 80px;
}

.title-container {
    display: flex;
    flex-direction: row;
    font-size: 19px;
}

.progress-container {
    display: flex;
    flex-direction: row;
    margin-top: 30px;
    margin-bottom: 50px;
}

.progress {
    width: 450px;
    margin-right: 100px;
}

.chart-container {
    display: flex;
    flex-direction: column;
}

.chart-item {
    width: 600px;
    height: 350px;
    margin-top: 20px;
    margin-left: 200px;
}

.input-container {
    display: flex;
    flex-direction: column;
    margin-left: 50px;
    margin-right: 50px;
}

.text-font {
    font-size: 16px;
    color: #000;
}

.mb-3 {
    margin-bottom: 1rem;
}

.dialog-footer button:first-child {
    margin-right: 50px;
}
</style>