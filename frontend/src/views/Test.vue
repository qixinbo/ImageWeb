<template>
  <div class="test">
    <b-navbar>
        <template #brand>
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
                <img
                    src="/static/img/kaibu-banner.png"
                    alt="Lightweight UI components for Vue.js based on Bulma"
                >
            </b-navbar-item>
        </template>
        <template #start>
            <b-navbar-item href="#">
                Home
            </b-navbar-item>
            <b-navbar-item href="#">
                Documentation
            </b-navbar-item>
            <b-navbar-dropdown label="Info">
                <b-navbar-item href="#">
                    About
                </b-navbar-item>
                <b-navbar-item href="#">
                    Contact
                </b-navbar-item>
            </b-navbar-dropdown>
        </template>

        <template #end>
            <b-navbar-item tag="div">
                <div class="buttons">
                    <a class="button is-primary">
                        <strong>Sign up</strong>
                    </a>
                    <a class="button is-light">
                        Log in
                    </a>
                </div>
            </b-navbar-item>
        </template>
    </b-navbar>
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
  name: "Test",
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