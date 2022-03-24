<template>
  <div class="home">
    <MenuBar />
    <ImageViewer msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
// @ is an alias to /src
import MenuBar from "@/components/widgets/MenuBar"
import ImageViewer from "@/components/ImageViewer.vue";

export default {
  name: "Home",
  components: {
    MenuBar,
    ImageViewer
  }
};
</script>
