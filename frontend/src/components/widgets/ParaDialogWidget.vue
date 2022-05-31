<template>
<div>
<el-form ref="form" :model="para" label-width="80px">
  <el-form-item v-for="p, index in view" :label="p[1][0]" :key="index">
    <el-input v-model="para[p[1][0]]" v-if="p[0]==='str'"></el-input>
    <el-input v-model="para[p[1][0]]" v-if="p[0]==='int'"></el-input>
    <el-input v-model="para[p[1][0]]" v-if="p[0]==='float'"></el-input>
    <el-slider v-model="para[p[1][0]]" v-if="p[0]==='slide'" :min="p[1][1][0]" :max="p[1][1][1]" show-input></el-slider>
    
    <el-switch v-model="para[p[1][0]]" v-if="p[0]==='bool'"
      active-color="#13ce66"
      inactive-color="#ff4949">
    </el-switch>

    <el-checkbox-group v-model="para[p[1][0]]" v-if="p[0]==='chos'">
      <el-checkbox 
        v-for="item in p[1][1]"
        :key="item"
        :label="item">
      </el-checkbox>
    </el-checkbox-group>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="onSubmit">立即创建</el-button>
    <el-button>取消</el-button>
  </el-form-item>
</el-form>
</div>
</template>
<script>
  export default {
    props: ['view', 'para'],
    mounted(){
      console.log("8888", this.view)
      console.log("9999", this.para)
    },
    methods: {
      onSubmit() {
        console.log('submit!');
        console.log('999999 = ', this.para)
      }
    }
  }
</script>