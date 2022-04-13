<template>
<div>
  <el-menu class="el-menu-demo" mode="horizontal" @select="handleSelect">
    <el-submenu v-for='(v1, n1) in menu' :index="n1" :key='n1'>
      <template slot="title">{{n1}}</template>
      <div v-for='(v2, n2) in v1' :key='n2'>
        <el-menu-item v-if='!(v2 instanceof Object)' :index="n2" :key='n2'>
          {{v2}}
        </el-menu-item>
        <el-submenu v-else :index="n2">
          <template slot="title">{{n2}}</template>
          <el-menu-item v-for='(v3, n3) in v2' :key='n3' :index="n3">
            {{v3}}
          </el-menu-item>
        </el-submenu>      
      </div>
    </el-submenu>
  </el-menu>
</div>
</template>



<!-- <template>
  <div class="MenuBar">
    <h1>{{value}}</h1>
    <section>
        <b-button @click="clickMe">Click Me</b-button>
    </section>
    <h1>{{value2}}</h1>
  </div>
</template>
 -->
<script>
import axios from 'axios';

export default {
  name: "MenuBar",
  data() {
    return {
      value: 123,
      value2: 'change after clicked',
      menu:{
        File: {
          Open:{
            jpg:'jpg',
            png:'png'
          },
          Close:'Close'
        },
        Edit: {
          Crop:'Crop',
          Invert: 'Invert'  
        }
      }
    }
  },
  mounted(){
    // axios
    //   .get('http://localhost:5000/')
    //   .then(response => (this.value = response.data))
    //   .catch(function (error) { // 请求失败处理
    //     console.log(error);
    //   })
  },
  methods: {
    clickMe() {
      axios
        .get('http://localhost:5000/')
        .then(response => (this.value2 = response.data))
        .catch(function (error) { // 请求失败处理
          console.log(error);
        })
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    }
  }
};
</script>