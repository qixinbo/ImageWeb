<template>
<div>
 <!-- 对应data_v1 -->
<!--  <div>
   <h1>{{menu}}</h1>
 </div> -->
<!--  <div>
   <h1>{{view}}</h1>
   <h1>{{para}}</h1>
 </div> -->
 
 <el-menu class="el-menu-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" 
    mode="horizontal" @select="handleSelect">
    <el-submenu v-for='m1 in menu' :index="m1[0]" :key='m1[0]'>
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

    <el-dialog
      title="参数对话框"
      :visible.sync="dialogVisible"
      width="40%">
      <el-form ref="form" :model="para" label-width="80px">
        <el-form-item v-for="p, index in view" :label="p[1]" :key="index">
          <el-input v-model="para[p[1]]" v-if="p[0]==='str'"></el-input>
          <el-input v-model.number="para[p[1]]" 
          v-if="p[0]==='int'" 
          oninput="value=value.replace(/[^0-9]/g,'')">
          </el-input>

          <el-input v-model.number="para[p[1]]" v-if="p[0]==='float'"></el-input>
          <el-slider v-model.number="para[p[1]]" v-if="p[0]==='slide'" :min="p[2][0]" :max="p[2][1]" show-input></el-slider>
          
          <el-switch v-model="para[p[1]]" v-if="p[0]==='bool'"
            active-color="#13ce66"
            inactive-color="#ff4949">
          </el-switch>

          <el-select v-model="para[p[1]]" v-if="p[0]==='list'" placeholder="Please choose">
            <el-option
              v-for="item in p[2]"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>

          <el-checkbox-group v-model="para[p[1]]" v-if="p[0]==='chos'">
            <el-checkbox 
              v-for="item in p[2]"
              :key="item"
              :label="item">
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">Submit</el-button>
          <el-button @click="onCancel">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </el-menu>
</div>
</template>



<script>
import axios from 'axios';
import Static from "ol/source/ImageStatic";
import Projection from "ol/proj/Projection";

import ITKHelper from '@kitware/vtk.js/Common/DataModel/ITKHelper';
import {encode} from 'uint8-to-base64';

import Base64 from '@kitware/vtk.js/Common/Core/Base64';


// import * as imjoyCore from 'imjoy-core'
// const imjoy = new imjoyCore.ImJoy({
//     imjoy_api: {},
//     //imjoy config
// });

// imjoy.start({workspace: 'default'}).then(async ()=>{
//     await imjoy.api.alert("hello world");
//   }
// )

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
      view: [],
      para: null,
      menu: 'change after clicked',
      dialogVisible: false,
      currentKey: null
    }
  },
  mounted(){

    axios
      .get('http://localhost:5000/menu/')
      .then(response => {
        this.menu = response.data
      })
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });

  },
  methods: {

    axios_img(key, para){
      // // generate file from base64 string
      // const file = dataURLtoFile('data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA    AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==', 'myfile')

      const layer = this.$store.state.layers[this.$store.state.currentLayer.id]
      // console.log("layer = ", layer)

      // ////////////////////   codes for itk-vtk-viewer //////////////
      // const itkImage = ITKHelper.convertVtkToItkImage(layer.getLayerAPI().get_image())
      // console.log("itkImage = ", itkImage)

      // const vtkImage = layer.getLayerAPI().get_image()
      // console.log('vtkImage = ', vtkImage)

      // console.log("Base64 = ", Base64)
      // console.log("b641 = ", Base64.fromArrayBuffer(itkImage.data))
      // const utf8Binary = new Uint8Array(anyArrayBuffer);
       
      // // encode converts Uint8Array instances to utf-16 strings
      // const encoded_b64 = 'data:image/png;base64,' + encode(itkImage.data);

      // console.log("b64 = ", encoded_b64)
      // const file = dataURLtoFile(encoded_b64)
      // ////////////////////   end for itk-vtk-viewer //////////////

      const dataURL = layer.getSource().getUrl()
      const file = dataURLtoFile(dataURL)

      // put file into form data
      const data = new FormData()
      data.append('file', file, 'itk-vtk')
      data.append('plugin', key)
      data.append('para', para)

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
          // console.log("url", dataURL)


          const extent = [0, 0, dimensions.width, dimensions.height];
          // const extent = [0, 0, 2048, 2048];
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
            // console.error('---------', error.response.data);
            alert(error.response.data.detail)
        });
    },

    handleSelect(key, keyPath) {
      console.log(key, keyPath);
      this.currentKey = key

      axios
        .get('http://localhost:5000/plugins/', {
          params:{id: key}
        })
        .then(response => 
          {
            console.log('response = ', response)
            if (response.data)
            {
              this.view = response.data[0];
              this.para = response.data[1];
              this.dialogVisible = true;
            }
            else
            {
              this.para = null
              this.axios_img(key, JSON.stringify(this.para))
            }
            console.log("para222 ---- = ", JSON.stringify(this.para))
          }
          )
        .catch(function (error) { // 请求失败处理
          console.log(error.response.data);
        })      
    },
    onSubmit() {
      console.log('submit!');
      console.log('999999 = ', this.para)
      this.axios_img(this.currentKey, JSON.stringify(this.para))
      this.dialogVisible = false
    },
    onCancel() {
      this.dialogVisible = false
    }
  }
};
</script>