<template>
<div>
 <!-- 对应data_v1 -->
 <el-menu class="el-menu-demo" background-color="#545c64" text-color="#fff" mode="horizontal" @select="handleSelect">
    <el-submenu v-for='m1 in value2' :index="m1[0]" :key='m1[0]'>
      <template slot="title">{{m1[0]}}</template>
      <div v-for='m2 in m1[1]' :key='m2[0]'>
        <el-menu-item v-if='!(m2[1] instanceof Array)' :index="m2[0]" :key='m2[0]'>
          {{m2[0]}}
        </el-menu-item>
        <el-submenu v-else :index="m2[0]">
          <template slot="title">{{m2[0]}}</template>
            <div v-for='m3 in m2[1]' :key='m3[0]'>
              <el-menu-item v-if='!(m3[1] instanceof Array || m3[1]==="-")' :index="m3[0]" :key='m3[0]'>
                {{m3[0]}}
              </el-menu-item>
              <template v-else>
                <h2> Cannot parse the fourth level menu!</h2>
              </template>    
            </div>
        </el-submenu>      
      </div>
    </el-submenu>
  </el-menu>

  <!-- for data_dict -->
<!--  <el-menu class="el-menu-demo" mode="horizontal" @select="handleSelect">
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
  </el-menu> -->

</div>
</template>



<script>
import axios from 'axios';

export default {
  name: "MenuBar",
  data() {
    return {
      value: 123,
      value2: 'change after clicked',
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