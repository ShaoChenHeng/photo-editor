<template>
  <div class="page">
    <div class="container">
      <img class="img" ref="image" :src="photo" alt="">
    </div>
  </div>
</template>

<script>
 import { QWebChannel } from "qwebchannel";
 
 export default {
   name: 'Main',
   data() {
     return {
       photo: '',
       afterPhoto:'',
       myCropper: null,
     }
   },
   props: {
     
   },
   created() {
     // eslint-disable-next-line no-undef
     new QWebChannel(qt.webChannelTransport, channel => {
       window.pyobject = channel.objects.pyobject;
       this.pyobject = window.pyobject;
     });
   },
   mounted() {
     window.addFiles = this.addFiles;
     window.updateFiles = this.updateFiles;
     window.rotate = this.rotate;
     window.cleanFiles = this.cleanFiles;
     window.rotateClockwise = this.rotateClockwise
     window.rotateCounterclockwise = this.rotateCounterclockwise
   },
   methods: {
     addFiles(path) {
       this.photo = path;
       this.$forceUpdate()
       
     },

     updateFiles(photo) {
       this.photo = photo;
     },
     
     pyResize() {
       this.pyobject.resize(2, 2);
     },

     cleanFiles() {
       this.photo = '';
     },
     
     
   }
 }
</script>

<style scoped>
 .page {
   display: flex;
 }

 .container {
   width: 100%;
   height: 100%;
   display: flex;
   flex-direction: column;
   justify-content: center;
 }
 
 .img {
   display: flex;
   z-index: -1;
 }

 img {
   display: block;
   max-height: 800px;
 }

 
</style>

