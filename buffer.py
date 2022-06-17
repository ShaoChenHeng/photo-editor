import os
import numpy as np
import cv2, json, shutil, base64
from scipy.interpolate import UnivariateSpline
import time
from json import dumps
from PIL import Image
from PyQt6 import QtCore
from PyQt6.QtCore import QUrl, QThread
from PyQt6.QtGui import QColor
from core.webengine import BrowserBuffer
from core.utils import (eval_in_emacs, PostGui, get_emacs_vars, 
                        interactive, message_to_emacs, 
                        get_emacs_func_result, get_emacs_config_dir, 
                        touch, get_emacs_var)

def LookupTable(x, y):
    spline = UnivariateSpline(x, y)
    return spline(range(256))

class AppBuffer(BrowserBuffer):
    def __init__(self, buffer_id, url, arguments):
        BrowserBuffer.__init__(self, buffer_id, url, arguments, False)

        # self.asuka = os.path.abspath("/home/scheng/asuka.png")
        self.asuka = '/home/scheng/asuka.png'
        self.ayanami = '/home/scheng/ayanami.jpg'
        self.ayanami1 = '/home/scheng/ayanami1.jpg'
        self.zafu = '/home/scheng/zafu.jpeg'
        
        self.img = cv2.imread(self.zafu)
        self.current_handle_img = self.img
        
        self.temp_image_dir = os.path.join(self.config_dir, "photo-editor", "temp")
        self.temp_image = ''
        self.num = 0

        self.current_temp = 1
        
        self.clean_temp_image()
        self.load_index_html(__file__)
        
        

    def init_app(self):
        self.buffer_widget.eval_js_function('''addFiles''', self.zafu)

        
    def clean_temp_image(self):
        if os.path.exists(os.path.join(self.config_dir, "photo-editor")):
            shutil.rmtree(os.path.join(self.config_dir, "photo-editor"))
            os.mkdir(os.path.join(self.config_dir, "photo-editor"))

    def fetch_temp_photo_dir(self):
        pass
            
    def save_temp_image(self, image):
        self.current_temp = self.temp_image_dir + str(self.num) + '.png'
        self.num += 1
        print(self.current_temp)
        cv2.imwrite(self.current_temp, image)
        
    @QtCore.pyqtSlot(int, int)
    def resize(self, A, B):
        img_resized = cv2.resize(self.current_handle_img, None, fx = 0.5, fy = 0.5, interpolation=cv2.INTER_LINEAR)

        self.current_handle_img = img_resized
        self.save_temp_image(img_resized)
        print(self.current_temp)
        self.buffer_widget.eval_js_function('''updateFiles''', self.current_temp)

    
    @QtCore.pyqtSlot(str)
    def get_image_from_js(self, image_string):
        image_string = image_string.replace('data:image/png;base64,', '')
        image_data = base64.b64decode(image_string)
        nparr = np.fromstring(image_data, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        self.current_handle_image = img_np
        self.save_temp_image(img_np)

    @QtCore.pyqtSlot()
    def pencil(self):
        def pencile_sketch_col(img):
            sk_gray, sk_color, = cv2.pencilSketch(img, sigma_s = 60, sigma_r = 0.07, shade_factor = 0.1)
            return sk_color
        
        pencil_image = pencile_sketch_col(self.current_handle_img)
        self.current_handle_img = pencil_image
        self.save_temp_image(pencil_image)
        self.buffer_widget.eval_js_function('''addFiles''', self.current_temp)

    @QtCore.pyqtSlot()
    def winter(self):
        def winter_filter(img):
            increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
            decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 100, 256])
            blue_channel, green_channel, red_channel = cv2.split(img)
            red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
            blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
            win = cv2.merge((blue_channel, green_channel, red_channel))
            return win
        winter_image = winter_filter(self.current_handle_img)
        self.current_handle_img = winter_image
        self.save_temp_image(winter_image)
        self.buffer_widget.eval_js_function('''addFiles''', self.current_temp)
    @QtCore.pyqtSlot()
    def summer(self):
        def summer_filter(img):
            increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
            decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
            blue_channel, green_channel, red_channel = cv2.split(img)
            red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
            blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
            summ = cv2.merge((blue_channel, green_channel, red_channel))
            return summ
        
        summer_image = summer_filter(self.current_handle_img)
        self.current_handle_img = summer_image
        self.save_temp_image(summer_image)
        self.buffer_widget.eval_js_function('''addFiles''', self.current_temp)
        
    #<--- rotate begin 
    def rotate_image_clockwise_90(self):
        self.rotate(-90)

    def rotate_image_counterclockwise_90(self):
        self.rotate(90)

    def rotate(self, angel):
        h, w = self.current_handle_img.shape[:2]
        
        center_x, center_y = (w // 2, h // 2)
        
        M = cv2.getRotationMatrix2D((center_x, center_y), angel, 1)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        M[0, 2] += (nW / 2) - center_x
        M[1, 2] += (nH / 2) - center_y
        
        img_rotated = cv2.warpAffine(self.current_handle_img, M, (nW, nH))

        self.current_handle_img = img_rotated
        self.save_temp_image(img_rotated)
        self.buffer_widget.eval_js_function('''addFiles''', self.current_temp)
    # rotate end --->

    # <--- flip begin
    def flip_x(self):
        self.flip(0)

    def flip_y(self):
        self.flip(1)

    def flip_xy(self):
        self.flip(-1)

    def flip(self, direction):
        img_fliped = cv2.flip(self.current_handle_img, direction)
        
        self.current_handle_img = img_fliped
        self.save_temp_image(img_fliped)
        print(self.current_temp)
        self.buffer_widget.eval_js_function('''addFiles''', self.current_temp) 
    # flip end--->
    
    def handle_input_response(self, callback_tag, result_content):
        BrowserBuffer.handle_input_response(self, callback_tag, result_content)

        
