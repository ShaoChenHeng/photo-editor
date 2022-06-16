<template>
  <div class="page">
    <div class="container" ref="container">
    <p class="{color: 'white'}"> {{ number }} </p>
    
    <v-stage ref="stage" :config="configKonva">
      <v-layer ref="layer">
        <v-image
          ref="image"
          :config="{
            x: offsetX,
            y: offsetY}" alt=""/>
      </v-layer>
    </v-stage>
    
    </div>
    <div class="bar3"> 具体 </div>
    <div class="bar2"> 刻度 </div>
    <div class="bar1"> 选择 </div>
    
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
         height: window.innerHeight - 150,
       },
       
       configCircle: {
         x: 100,
         y: 100,
         radius: 70,
         fill: "red",
         stroke: "black",
         strokeWidth: 4
       },

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
     window.test = this.test;
     window.save = this.save;
     
     console.log(this.$refs.container.width);
     
     
     const imageNode = this.$refs.image.getNode();
     imageNode.cache();
   },

   updated() {
     this.mask(this.number)
   },

   watch: {
     "photo": function() {
       const imageNode = this.$refs.image.getNode();
       const nImage = new window.Image();
       nImage.src = this.photo;
       nImage.onload = () => {
         // set image only when it is loaded
         imageNode.image(nImage);
         let height = nImage.height;
         let width = nImage.width;
         let ratio = 1;
         if (width > this.configKonva.width ||
             height * 1.0 > this.configKonva.height) {
           ratio = Math.min(this.configKonva.width * 1.0/ width,
                            this.configKonva.height * 1.0/ height);
         }
         
         imageNode.x(Math.abs(this.configKonva.width - width * ratio) / 2);
         imageNode.y(Math.abs(this.configKonva.height - height * ratio) / 2);
         
         imageNode.scaleX(ratio);
         imageNode.scaleY(ratio);
       };
       // imageNode.image(nImage);
       // console.log(nImage.height);
       // console.log(nImage.width);

     }
   },
   
   methods: {
     addFiles(path) {
       this.photo = path;
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
     mask(depth) {
       const imageNode = this.$refs.image.getNode();
       // may need to redraw layer manually
       imageNode.cache();
       imageNode.filters([Konva.Filters.Mask]);
       imageNode.threshold(depth * 10);
     },

     // basic
     rotate() {
       const imageNode = this.$refs.image.getNode();
       imageNode.cache();
       //var endRadius = imageNode.fillRadialGradientEndRadius();

       // set radial gradient end radius

       // imageNode.fillPatternRotation(20);
       imageNode.offset(100);
       imageNode.rotate(90);
       // imageNode.width(imageNode.height());
       // imageNode.height(imageNode.width());
       let height = imageNode.height();
       let width = imageNode.width();
       console.log(height);
       console.log(width);
       
       console.log(imageNode.x());
       console.log(imageNode.y());
       console.log('here');
       // imageNode.offsetX((this.windowWidth - imageNode.width()) / 2);
       // imageNode.offsetY((this.windowHeight - imageNode.height()) / 2);
     },

     add() {
       this.number = this.number + 2;
     },

     minus() {
       this.number = this.number - 2;
     },

     save() {
       let stage = this.$refs.image.getNode();
       const dataURL = stage.toDataURL({
         mimeType: "image/png",
       });
       this.pyobject.get_image_from_js(dataURL);
     }
     
   }
 }
</script>

<style scoped>
 .page {
   display: flex;
   flex-direction: column;
   position: relative;
 }

 .container{
   display: flex;
   background: #5d5d5d;
 }
 
 .bar3{
   background: #eF7342;
   height: 60px;
   width: 360px;
   align-items: center;
   justify-content: center;
 }

 .bar2{
   background: #5d5d5d;
   height: 60px;
   width:360px;
   align-items: center;
   justify-content: center;
 }

 .bar1{
   background: #eFdd32;
   height: 30px;
   width: 360px;
   align-items: center;
   justify-content: center;
   
 }
</style>

