import os
import numpy as np
import cv2, json, shutil
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


class AppBuffer(BrowserBuffer):
    def __init__(self, buffer_id, url, arguments):
        BrowserBuffer.__init__(self, buffer_id, url, arguments, False)

        # self.asuka = os.path.abspath("/home/scheng/asuka.png")
        self.asuka = '/home/scheng/asuka.png'
        
        self.img = cv2.imread(self.asuka)
        self.current_handle_img = self.img
        
        self.temp_image_dir = os.path.join(self.config_dir, "photo-editor", "temp")
        self.temp_image = ''
        self.num = 0

        self.current_temp = 1
        
        self.clean_temp_image()
        self.load_index_html(__file__)
        
        

    def init_app(self):
        self.buffer_widget.eval_js_function('''addFiles''', self.asuka)

        
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

        
