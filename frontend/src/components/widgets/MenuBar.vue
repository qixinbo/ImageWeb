<template>
<div>
  <div class="MenuBar">
    <h1>{{value}}</h1>
    <section>
        <b-button @click="clickMe">Click Me</b-button>
    </section>
    <h1>{{value2}}</h1>
  </div>
<!--   <el-menu class="el-menu-demo" mode="horizontal" @select="handleSelect">
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
 -->  

<!--  对应data_v1
 <el-menu class="el-menu-demo" mode="horizontal" @select="handleSelect">
    <el-submenu v-for='m1 in value2[1]' :index="m1[0]" :key='m1[0]'>
      <template slot="title">{{m1[0]}}</template>
      <div v-for='m2 in m1[1]' :key='m2[0]'>
        <el-menu-item v-if='!(m2[1] instanceof Array)' :index="m2[0]" :key='m2[0]'>
          {{m2[0]}}
        </el-menu-item>
        <el-submenu v-else :index="m2[0]">
          <template slot="title">{{m2[0]}}</template>
            <div v-for='m3 in m2[1]' :key='m3[0]'>
              <el-menu-item v-if='!(m3[1] instanceof Array)' :index="m3[0]" :key='m3[0]'>
                {{m3[0]}}
              </el-menu-item>
              <template v-else>
                <h2> Cannot parse the fourth level menu!</h2>
              </template>    
            </div>
        </el-submenu>      
      </div>
    </el-submenu>
  </el-menu> -->

  <h1> {{value2["menu"]}}</h1>

 <el-menu class="el-menu-demo" mode="horizontal" @select="handleSelect">
    <el-submenu v-for='(m1, n1) in value2["menu"]' :index="n1" :key='n1'>
      <template slot="title">{{n1}}</template>
      <div v-for='(m2, n2) in m1' :key='n2'>
        <el-menu-item v-if='m2.hasOwnProperty("name")' :index="n2" :key='n2'>
          {{n2}}
        </el-menu-item>
        <el-submenu v-else :index="n2">
          <template slot="title">{{n2}}</template>
            <div v-for='(m3, n3) in m2' :key='n3'>
              <el-menu-item v-if='m3.hasOwnProperty("name")' :index="n3" :key='n3'>
                {{n3}}
              </el-menu-item>
              <template v-else>
                <h2> Cannot parse the fourth level menu!</h2>
              </template>    
            </div>
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
    axios
      .get('http://localhost:5000/t')
      .then(response => (this.value2 = response.data))
      .catch(function (error) { // 请求失败处理
        console.log(error);
      })
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
      axios
        .post('http://localhost:5000/plugins/', JSON.stringify(keyPath), 
          {headers: {'Content-Type': 'application/json'}})
        .then(response => (this.value = response.data))
        .catch(function (error) { // 请求失败处理
          console.log(error);
        })      
    }
  }
};
</script>