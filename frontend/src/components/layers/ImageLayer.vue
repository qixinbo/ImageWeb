<template>
  <div class="image-layer">
    <!-- 通过组件的layer属性切换是否显示 -->
    <section v-if="layer">
      <b-field label="opacity">
        <!-- 该组件在模板中只有一个滑动条 -->
        <b-slider
          v-model="config.opacity"
          @input="updateOpacity"
          :min="0"
          :max="1.0"
          :step="0.1"
        ></b-slider>
      </b-field>
      <!-- <b-field v-if="config.climit" label="contrast limit">
        <b-slider v-model="config.climit" :min="1" :max="255" :step="0.5" ticks>
        </b-slider>
      </b-field> -->
    </section>
  </div>
</template>

<script>
// 从openlayers中导入必要的包
import { Map } from "ol";
import Static from "ol/source/ImageStatic";
import ImageLayer from "ol/layer/Image";
import Projection from "ol/proj/Projection";

//将File对象转为base64编码的对象
function file2base64(file) {
  return new Promise((resolve, reject) => {
    var reader = new FileReader();
    reader.onload = event => {
      resolve(url2base64(event.target.result));
    };
    reader.onerror = err => {
      reject(err);
    };
    reader.readAsDataURL(file);
  });
}

// 将图片url转为base64编码的对象
async function url2base64(url) {
  return new Promise((resolve, reject) => {
    var img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = function() {
      var canvas = document.createElement("canvas");
      var ctx = canvas.getContext("2d");
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
      resolve({
        url: canvas.toDataURL("image/png"),
        w: img.width,
        h: img.height
      });
    };
    img.onerror = function(e) {
      reject("image load error:" + String(e));
    };
    img.src = url;
  });
}

// 将无符号的整型数组转化为base64编码的对象
function array2rgba(imageArr, ch, w, h) {
  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext("2d");
  const canvas_img = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const canvas_img_data = canvas_img.data;
  const count = w * h;

  const raw = new Uint8Array(imageArr.buffer);
  if (imageArr instanceof Uint8Array) {
    if (ch === 1) {
      for (let i = 0; i < count; i++) {
        canvas_img_data[i * 4] = raw[i];
        canvas_img_data[i * 4 + 1] = raw[i];
        canvas_img_data[i * 4 + 2] = raw[i];
        canvas_img_data[i * 4 + 3] = 255;
      }
    } else if (ch === 2) {
      for (let i = 0; i < count; i++) {
        canvas_img_data[i * 4] = raw[i * 2];
        canvas_img_data[i * 4 + 1] = raw[i * 2 + 1];
        canvas_img_data[i * 4 + 2] = 0;
        canvas_img_data[i * 4 + 3] = 255;
      }
    } else if (ch === 3) {
      for (let i = 0; i < count; i++) {
        canvas_img_data[i * 4] = raw[i * 3];
        canvas_img_data[i * 4 + 1] = raw[i * 3 + 1];
        canvas_img_data[i * 4 + 2] = raw[i * 3 + 2];
        canvas_img_data[i * 4 + 3] = 255;
      }
    } else if (ch === 4) {
      for (let i = 0; i < count; i++) {
        canvas_img_data[i * 4] = raw[i * 3];
        canvas_img_data[i * 4 + 1] = raw[i * 3 + 1];
        canvas_img_data[i * 4 + 2] = raw[i * 3 + 2];
        canvas_img_data[i * 4 + 3] = raw[i * 4 + 3];
      }
    }
  } else {
    throw "unsupported array type";
  }
  ctx.putImageData(canvas_img, 0, 0);
  return {
    url: canvas.toDataURL("image/png"),
    w: w,
    h: h
  };
}

export default {
  name: "image-layer",
  type: "2d-image",
  show: false,
  // 从父组件中接收参数
  props: {
    // map也是从父组件中传过来的存放于vuex中的map属性
    map: {
      type: Map,
      default: null
    },
    selected: {
      type: Boolean,
      default: false
    },
    visible: {
      type: Boolean,
      default: false
    },
    // 这里的config会修改父组件中的config
    config: {
      type: Object,
      default: function() {
        return {};
      }
    }
  },
  data() {
    return {
      layer: null
    };
  },
  watch: {
    visible: function(newVal) {
      this.layer.setVisible(newVal);
    }
  },
  mounted() {
    this.config.climit = [4, 50];
    this.config.opacity = 1.0;
    this.config.init = this.init;
  },
  beforeDestroy() {
    if (this.layer) {
      this.map.removeLayer(this.layer);
    }
  },
  created() {},
  methods: {
    // init初始化函数非常重要，它在vuex状态管理中被调用
    async init() {
      this.layer = await this.setupLayer();
      this.map.addLayer(this.layer);
      this.$forceUpdate();
      return this.layer;
    },
    updateOpacity() {
      if (this.layer) this.layer.setOpacity(this.config.opacity);
    },
    selectLayer() {},

    // 这里就是对this.layer进行加工的详细过程了
    async setupLayer() {
      let imgObj;
      const data = this.config.data;
      // 根据data的类型，进行不同的转换
      // 如果data是个字符串，比如是个图片路径
      if (typeof data === "string") {
        // 调用url2base64函数将其转化成base64编码格式
        imgObj = await url2base64(this.config.data);
      } else if (data instanceof File) { // 如果是File对象实例，则调用file2base64
        imgObj = await file2base64(this.config.data);
      } else if ( // 如果不是上面两种格式，就应该是无符号的整型数组及一些尺寸属性
        data &&
        data.imageType &&
        data.size &&
        data.imageType.componentType &&
        data.data
      ) {
        if (data.imageType.componentType !== "uint8_t") {
          throw `Unsupported data type: ${data.imageType.componentType}`;
        }

        if (data.imageType.components < 1 && data.imageType.components > 4) {
          throw `Unsupported components number: ${data.imageType.components}`;
        }

        if (data.imageType.dimension !== 2) {
          throw `Dimension must be 2`;
        }

        if (data.imageType.pixelType !== 1) {
          throw `Pixel type must be 1`;
        }
        imgObj = array2rgba(
          data.data,
          data.imageType.components,
          data.size[0],
          data.size[1]
        );
      } else {
        imgObj = {
          url: "https://images.proteinatlas.org/19661/221_G2_1_red_green.jpg",
          w: 2048,
          h: 2048
        };
      }
      const extent = [0, 0, imgObj.w, imgObj.h];
      // Map总是需要一个projection，这里只是想把图像坐标系映射到地图坐标系中，所以直接使用以像素为单位的图像内容来创建projection
      const projection = new Projection({
        code: "image",
        units: "pixels",
        extent: extent
      });
      // 创建一个static对象来作为下面ImageLayer的source
      const image_source = new Static({
        url: imgObj.url,
        projection: projection,
        imageExtent: extent
      });
      // 新建一个ImageLayer图层
      const image_layer = new ImageLayer({
        source: image_source
      });
      // 向父组件发射消息，使其能够监听到自定义事件，目前看主要是影响了显示中心位置
      this.$emit("update-extent", { id: this.config.id, extent: extent });
      return image_layer;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style></style>
