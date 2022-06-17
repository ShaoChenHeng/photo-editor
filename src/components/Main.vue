<template>
  <div class="page">
    <div class="container" ref="container">
    <v-stage ref="stage" :config="configKonva">
      <v-layer ref="layer">
        <v-image ref="image" :config="{image}" alt=""/>
      </v-layer>
    </v-stage>
    
    </div>
    <div class="cont">
    <div v-if="isBasic" class="bar3">
      <button class="block"> 对比度 </button>
      <button class="block"> 增强 </button>
      <button class="block"> 噪点 </button>
      <button class="block"> HSL </button>
      <button class="block"> HSV </button>
      <button class="block1 light"> 遮盖 </button>
      <button class="block"> Invert </button>
      <button class="block"> 素描 </button>
      <button class="block"> 阈值 </button>
      <button class="block"> 模糊 </button>
      <button class="block"> 像素化 </button>
      
    </div>
    <div v-if="isFilters" class="bar3">
      <button class="block"> Grayscale </button>
      <button class="block"> Sepia </button>
      <button class="block"> Solarize </button>
      <button class="block"> Invert </button>
      <button class="block"> Sharp </button>
      <button class="block"> Pencil </button>
      <button class="block1 light"> Summer </button>
      <button class="block"> Cold </button>
    </div>
     <div v-if="isTrim" class="bar3">
      <button class="block"> 旋转 </button>
      <button class="block"> 翻转 </button>
      <button class="block"> 裁剪 </button>
      <button class="block1 light"> 缩放 </button>
     </div>
    </div>
    
    <div class="bar2">
      <div class="under-bar-left"> </div>
      <div class="under-bar-right"> </div>
    </div>
    
    <div class="global-bar">
      <button class="basic global-button"> 调整 </button>
      <button class="filters global-button1 light"> 滤镜 </button>
      <button class="trim global-button" > 修整 </button>
    </div>
    
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
       isFilters: true,
       isBasic: false,
       isTrim: false,
       
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
     window.rotate = this.rotate;
     window.save = this.save;
     window.noise = this.noise;
     
     const imageNode = this.$refs.image.getNode();
     imageNode.cache();
   },

   updated() {
     
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
         if (width  > this.configKonva.width ||
             height > this.configKonva.height) {
           ratio = Math.min(this.configKonva.width * 1.0/ width,
                            this.configKonva.height * 1.0/ height);
         }
         
         imageNode.x(Math.abs(this.configKonva.width - width * ratio) / 2);
         imageNode.y(Math.abs(this.configKonva.height - height * ratio) / 2);
         imageNode.scaleX(ratio);
         imageNode.scaleY(ratio);
         console.log(height);
         console.log(width)
       };
       
     },

     "number": function() {
       this.summer();
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
       console.log('here');
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
       // imageNode.cache();
       //var endRadius = imageNode.fillRadialGradientEndRadius();

       // set radial gradient end radius

       // imageNode.fillPatternRotation(20);
       
       // imageNode.width(imageNode.height());
       // imageNode.height(imageNode.width());
       // let height = imageNode.height();
       // let width = imageNode.width();
       
       
       
       imageNode.offsetX(imageNode.width() / 2);
       imageNode.offsetY(imageNode.height() / 2);
       imageNode.rotate(90);
       console.log(imageNode.offsetX());
       console.log(imageNode.offsetY());
       let width = imageNode.width();
       let height = imageNode.height();
       let ratio = 1;
       if (width  > this.configKonva.width ||
           height > this.configKonva.height) {
         ratio = Math.min(this.configKonva.width * 1.0/ width,
                          this.configKonva.height * 1.0/ height);
       }
       console.log('here');
       imageNode.x(700);
       imageNode.y(500);
       imageNode.scaleX(ratio);
       imageNode.scaleY(ratio);
       // imageNode.offsetX((this.windowWidth - imageNode.width()) / 2);
       // imageNode.offsetY((this.windowHeight - imageNode.height()) / 2);
     },

     scale(depth) {
       const imageNode = this.$refs.image.getNode();
       imageNode.cache();
       imageNode.scaleX(1 + depth * 0.01);
       imageNode.scaleY(1 + depth * 0.01);
     },

     pencil() {
       this.pyobject.pencil();
     },

     winter() {
       this.pyobject.winter();
     },

     summer() {
       this.pyobject.summer();
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
 }

 .light {
   background: #AAA2FF;
 }

 .block1 {
   margin-left: 15px;
   height: 60px;
   width: 120px;
   border-radius: 10px;
   color: white;
   font-size: 22px;
   font-weight: bold;
 }
 
 .block {
   margin-left: 15px;
   height: 60px;
   width: 120px;
   border-radius: 10px;
   background: #5d5d5d;
   color: white;
   font-size: 22px;
   font-weight: bold;
 }
 
 .cont {
   overflow: scroll;
   text-overflow: ellipsis;
   width: 1500px;
   margin: 0 auto;
 }

 .bar3 {   
   align-items: center;
   flex-direction: row;
   display: inline-flex;
 }

 .under-bar-right {
   background: #5d5d5d;
   width: 200px;
   height: 5px;
 }

 .under-bar-left {
   
   background: #5d5d5d;
   width: 200px;
   height: 5px;
 }
 
 .bar2 {
   margin-top: 10px;
   margin-bottom: 10px;
   margin-left: 50px;
   margin-right: 50px;
   background: #5d5d5d;
   display: inline-flex;
   flex-direction: row;
   justify-content: center;
 }

 .global-bar {
   height: 40px;
   width: 360px;
   display: flex;
   text-align: center;
   align-items: center;
   justify-content: center;
   
   margin: 0 auto;
 }

 .global-button {
   display: flex;
   color: white;
   background: #5d5d5d;
   
   flex: 1;
   font-size: 20px;
   font-weight: bold;
   
   justify-content: center;
   align-items: center;
   margin-left: 8px;
   margin-right: 8px;

   border-radius: 10px;
 }

 .global-button1 {
   display: flex;
   color: white;
   background: #AAA2FF;
   
   flex: 1;
   font-size: 20px;
   font-weight: bold;
   
   justify-content: center;
   align-items: center;
   margin-left: 8px;
   margin-right: 8px;

   border-radius: 10px;
 }
</style>

