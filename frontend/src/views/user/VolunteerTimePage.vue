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
                <div v-if="statisticType === 'type'">
                    <div ref="pieChart" class="chart-item"></div>
                    <p class="text-item">
                        您最喜欢的志愿项目类别是<strong>{{ maxTimeType }}</strong>，总共获得了<strong>{{ maxTime }}</strong>小时的志愿时长。
                    </p>
                </div>
                <div v-else>
                    <div ref="lineChart" class="chart-item"></div>
                    <p class="text-item">
                        您本月的志愿时长相比{{ currentMonth - 1 }}月增加了<strong>{{ diffValue }}</strong>小时，继续加油！
                    </p>
                </div>
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
        },
        maxTime() {
            return Math.max(this.type1, this.type2, this.type3, this.type4, this.type5, this.type6);
        },
        maxTimeType() {
            let max = 0;
            let maxType = '';
            if (this.type1 > max) {
                max = this.type1;
                maxType = '社区服务';
            }
            if (this.type2 > max) {
                max = this.type2;
                maxType = '科技科普';
            }
            if (this.type3 > max) {
                max = this.type3;
                maxType = '支教助学';
            }
            if (this.type4 > max) {
                max = this.type4;
                maxType = '体育赛事';
            }
            if (this.type5 > max) {
                max = this.type5;
                maxType = '大型演出';
            }
            if (this.type6 > max) {
                max = this.type6;
                maxType = '其它';
            }
            return maxType;
        },
        currentMonth() {
            const date = new Date();
            return date.getMonth() + 1;
        },
        diffValue() {
            const lastMonth = this.currentMonth - 2 < 0 ? 12 : this.currentMonth - 1;
            const lastMonthVolunteerTime = this[`month${lastMonth}`];
            const currentMonthVolunteerTime = this[`month${this.currentMonth}`];
            return currentMonthVolunteerTime - lastMonthVolunteerTime;
        }
    },
    data() {
        return {
            statisticType: 'type',
            total: 0,
            totalTarget: 120,
            semester: 0,
            semesterTarget: 16,
            type1: 0,
            type2: 0,
            type3: 0,
            type4: 0,
            type5: 0,
            type6: 0,
            month1: 0,
            month2: 0,
            month3: 0,
            month4: 0,
            month5: 0,
            month6: 0,
            month7: 0,
            month8: 0,
            month9: 0,
            month10: 0,
            month11: 0,
            month12: 0,
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
                this.month1 = res.data.month1;
                this.month2 = res.data.month2;
                this.month3 = res.data.month3;
                this.month4 = res.data.month4;
                this.month5 = res.data.month5;
                this.month6 = res.data.month6;
                this.month7 = res.data.month7;
                this.month8 = res.data.month8;
                this.month9 = res.data.month9;
                this.month10 = res.data.month10;
                this.month11 = res.data.month11;
                this.month12 = res.data.month12;
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
                        data: [this.month1, this.month2, this.month3, this.month4, this.month5, this.month6, this.month7, this.month8, this.month9, this.month10, this.month11, this.month12],
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
    font-size: 15px;
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
    margin-bottom: 20px;
    margin-left: 200px;
}

.text-item {
    font-size: 17px;
    margin-left: 240px;
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