<template>
  <div class="home">
    <MenuBar/>
    <ImageViewer msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
// @ is an alias to /src
import ImageViewer from "@/components/ImageViewer.vue";
import MenuBar from "@/components/widgets/MenuBar"

export default {
  name: "Home",
  components: {
    MenuBar,
    ImageViewer
  }
};
</script>
