<template>
  <div class="page">
    <img class="img" :src="photo">
  </div>
</template>

<script>
 export default {
   name: 'Main',
   data() {
     return {
       photo: '',
     }
   },
   props: {

   },
   mounted() {
     window.addFiles = this.addFiles;
   },
   methods: {
     addFiles(path) {
       this.photo = path;
     }
   }
 }
</script>

<style scoped>
 .page {
   display: flex;
   width: 100%;
   height: 100%;
 }
 .img {
   width: 100%;
   height: 100%;
   display: flex;
   flex-direction: column;
   justify-content: center;
 }
</style>
