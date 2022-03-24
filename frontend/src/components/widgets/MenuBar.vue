<template>
  <div class="MenuBar">
    <h1>{{value}}</h1>
    <section>
        <b-button @click="clickMe">Click Me</b-button>
    </section>
    <h1>{{value2}}</h1>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "MenuBar",
  data() {
    return {
      value: 123,
      value2: 'change after clicked'
    };
  },
  mounted(){
    axios
      .get('http://localhost:5000/')
      .then(response => (this.value = response.data))
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
    }
  }
};
</script>