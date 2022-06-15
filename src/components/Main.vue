<template>
  <div class="page">
    
    <v-stage :config="configKonva">
      
      <v-layer>
        <v-image :config="{
                 image: image,
                 draggable: true,
                 x: offsetX,
                 y: offsetY
                 }" alt=""/>
      </v-layer>
      
      <v-layer>
        <v-circle :config="configCircle"></v-circle>
      </v-layer>
      
    </v-stage>
    
  </div>
</template>

<script>
 import { QWebChannel } from "qwebchannel";
 
 export default {
   name: 'Main',
   data() {
     return {
       photo: '',
       image: null,
       stage: null,
       windowWidth: window.innerWidth,
       windowHeight: window.innerHeight,
       offsetX: 0,
       offsetY: 0,
       configKonva: {
         width: window.innerWidth,
         height: window.innerHeight,
       },
       configCircle: {
         x: 100,
         y: 100,
         radius: 70,
         fill: "red",
         stroke: "black",
         strokeWidth: 4
       }
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
   },
   
   methods: {
     addFiles(path) {
       this.photo = path;
       const nImage = new window.Image();
       nImage.src = this.photo;
       
       nImage.onload = () => {
         // set image only when it is loaded
         this.offsetX = (this.windowWidth - nImage.width) / 2;
         this.offsetY = (this.windowHeight - nImage.height) / 2;
         this.image = nImage;
       };
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
   background: #FFFF00;
 }
 
 .img {
   display: flex;
   z-index: -1;
 }

 v-image {
   display: block;
   max-height: 800px;
 }

 
</style>

