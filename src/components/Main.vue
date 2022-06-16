<template>
  <div class="page">
    <p class="{color: 'white'}"> {{ number }} </p>
    <v-stage :config="configKonva">
      
      <v-layer>
        <v-image
          ref="image"
          :config="{
            image: image,
            x: offsetX,
            y: offsetY,}" alt=""/>
      </v-layer>
      
      <v-layer>
        <v-wedge :config="cursor"></v-wedge>
      </v-layer>
      
    </v-stage>
    
  </div>
</template>

<script>
 import { QWebChannel } from "qwebchannel";
 import Konva from 'konva';
 
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

       number: 0,
       
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
       },

       filters: [Konva.Filters.Noise]
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
     window.add = this.add;
     window.minus = this.minus;
     
     const imageNode = this.$refs.image.getNode();
     imageNode.cache();
   },

   updated() {
     this.rgba(this.number);
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

     // basic
     threshold(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Threshold]);
       imageNode.threshold(depth * 0.005);
     },

     // basic
     brighten(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Brighten]);
       imageNode.brightness(depth * 0.01);
     },

     // filter
     solarize() {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Solarize]);
     },

     // filter
     sepia(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Sepia]);
       imageNode.sepia(depth);
       imageNode.threshold(depth * 0.1);
     },

     // basic
     blur(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Blur]);
       imageNode.blurRadius(depth);
     },

     // basic
     pixelate(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Pixelate]);
       imageNode.pixelSize(depth);
     },

     // basic
     contrast(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Contrast]);
       imageNode.contrast(depth);
     },

     // filter
     grayscale() {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Grayscale]);
     },

     // filter or basic?
     emboss(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Emboss]);
       imageNode.embossStrength(0.7 + depth * 0.01);
       imageNode.embossWhiteLevel(0.95 + depth * 0.01);
       imageNode.embossDirection("left");
     },

     // basic
     hsl(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.HSL]);
       imageNode.luminance(depth * 0.01);
     },

     // basic
     hsv(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.HSV]);
       imageNode.value(depth * 0.01);
     },

     // basic
     enhance(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Enhance]);
       imageNode.enhance(depth * 0.1);
     },

     // filter
     invert() {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Invert]);
     },

     // basic
     noise(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Noise]);
       imageNode.noise(depth * 0.01);
     },

     // basic
     rgba(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       console.log(imageNode);
       imageNode.filters([Konva.Filters.RGBA]);
       imageNode.alpha(depth * 0.01);
     },

     
     
     add() {
       this.number = this.number + 2;
     },

     minus() {
       this.number = this.number - 2;
     }
     
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

