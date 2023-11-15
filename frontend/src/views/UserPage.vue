<template>
  <div>
    <h1 class="title">个人信息</h1>
  </div>

  <el-radio-group v-model="size">
    <el-radio label="large">大字体</el-radio>
    <el-radio>默认</el-radio>
    <el-radio label="small">小字体</el-radio>
  </el-radio-group>

  <el-descriptions class="margin-top" :column="3" :size="size" border>
    <template #extra>
    </template>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <User />
          </el-icon>
          学工号
        </div>
      </template>
      21371295
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <User />
          </el-icon>
          姓名
        </div>
      </template>
      张昊翔
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <Iphone />
          </el-icon>
          电话号码
        </div>
      </template>
      18100000000
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <VideoCamera />
          </el-icon>
          邮箱
        </div>
      </template>
      212345131@gmail.com
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <Tickets />
          </el-icon>
          用户类型
        </div>
      </template>
      <el-tag size="small">普通用户</el-tag>
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <DataBoard />
          </el-icon>
          志愿时长
        </div>
      </template>
      100h
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <Postcard />
          </el-icon>
          个人简介
        </div>
      </template>
      <el-input type="textarea" class="full-width"></el-input>
    </el-descriptions-item>
  </el-descriptions>
  <br>
  <el-button type="primary">编辑</el-button>
</template>
  
<script setup lang="ts">
import { computed, ref } from 'vue'
import {
  Iphone,
  VideoCamera,
  Tickets,
  User,
  DataBoard,
  Postcard,
} from '@element-plus/icons-vue'

const size = ref('')
const iconStyle = computed(() => {
  const marginMap = {
    large: '8px',
    default: '6px',
    small: '4px',
  }
  return {
    marginRight: marginMap[size.value] || marginMap.default,
  }
})
</script>
  
<style scoped>
.title {
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
}

.cell-item {
  display: flex;
  align-items: center;
}

.margin-top {
  margin-top: 20px;
}

.full-width {
  width: 100%;
}
</style>
  