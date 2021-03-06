import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue"
import ImageViewer from "../components/ImageViewer.vue";

Vue.use(VueRouter);

const routes = [
  { 
    path: "/", 
    name: "Home",
    component: Home
    // redirect: { name: "App" } 
  },
  {
    path: "/app",
    name: "App",
    component: ImageViewer
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  },
  {
    path: "/test",
    name: "Test",
    component: () =>
      import("../views/Test.vue")
  }
];

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
});

export default router;
