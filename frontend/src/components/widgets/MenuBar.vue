<template>
<div>
 <!-- 对应data_v1 -->
<!--  <div>
   <h1>{{value2}}</h1>
 </div>
 <div>
   <h1>{{value}}</h1>
   <h1>{{value3}}</h1>
 </div>
 --> 
<!--  <img class="fit-picture" id='myImage'
     src="/static/img/kaibu-banner.png"
     alt="Grapefruit slice atop a pile of other slices"/> -->
 <el-menu class="el-menu-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" 
    mode="horizontal" @select="handleSelect">
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
import Static from "ol/source/ImageStatic";
import Projection from "ol/proj/Projection";
// https://gist.github.com/ibreathebsb/a104a9297d5df4c8ae944a4ed149bcf1
// helper function: generate a new file from base64 String
const dataURLtoFile = (dataurl, filename) => {
  const arr = dataurl.split(',')
  const mime = arr[0].match(/:(.*?);/)[1]
  const bstr = atob(arr[1])
  let n = bstr.length
  const u8arr = new Uint8Array(n)
  while (n) {
    u8arr[n - 1] = bstr.charCodeAt(n - 1)
    n -= 1 // to make eslint happy
  }
  return new File([u8arr], filename, { type: mime })
}

export default {
  name: "MenuBar",
  data() {
    return {
      value: 123,
      value2: 'change after clicked',
      value3: 456,
    }
  },
  mounted(){
    axios
      .get('http://localhost:5000/menu/')
      .then(response => {
        this.value2 = response.data
      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);

      // // generate file from base64 string
      // const file = dataURLtoFile('data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA    AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==', 'myfile')

      const layer = this.$store.state.layers[this.$store.state.currentLayer.id]
      const dataURL = layer.getSource().getUrl()
      const file = dataURLtoFile(dataURL)
      // put file into form data
      const data = new FormData()
      data.append('file', file, file.name)

      // now upload
      const config = {
        headers: { 'Content-Type': 'multipart/form-data' }
      }

      axios({
              method: 'POST',
              url: 'http://localhost:5000/img/',
              data: data,
              headers: {
                  'Content-Type': 'multipart/form-data'
              }
          })
        .then(response => {
          // console.log("----", response.data)
          const dimensions = response.data.dimensions
          // console.log(response.data.dimensions.split(',').map(Number))
          // console.log("url", dataURL)


          const extent = [0, 0, dimensions.width, dimensions.height];
          // const extent = [0, 0, 2048, 2048];
          // Map总是需要一个projection，这里只是想把图像坐标系映射到地图坐标系中，所以直接使用以像素为单位的图像内容来创建projection
          const projection = new Projection({
            code: "image",
            units: "pixels",
            extent: extent
          });
          // 创建一个static对象来作为下面ImageLayer的source
          const image_source = new Static({
            url: response.data.encoded_img,
            projection: projection,
            imageExtent: extent
          });

          layer.setSource(image_source)

          // console.log("new url", layer.getSource().getUrl())

        })
        .catch(error => {
            console.error(error);
        });


      axios
        .get('http://localhost:5000/plugins/', {
          params:{id: key}
        })
        .then(response => (this.value = response.data))
        .catch(function (error) { // 请求失败处理
          console.log(error);
        })      
    }
  }
};
</script>