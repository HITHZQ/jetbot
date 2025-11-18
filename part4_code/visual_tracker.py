#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import rospy
import message_filters
import numpy as np
import cv2
from matplotlib import pyplot as plt
#from cv_bridge import CvBridge 
from ultralytics import YOLOv10

from sensor_msgs.msg import Image
from simple_follower.msg import position as PositionMsg
from std_msgs.msg import String as StringMsg
from std_msgs.msg import Int8

import sys
def imgmsg_to_cv2(img_msg, desired_encoding="bgr8"):
    # Determine the correct dtype based on the encoding
    if '8' in img_msg.encoding:
        dtype = np.dtype("uint8")
    elif '16' in img_msg.encoding:
        dtype = np.dtype("uint16")
    elif '32FC' in img_msg.encoding:
        dtype = np.dtype("float32")
    else:
        raise ValueError(f"Unsupported encoding type: {img_msg.encoding}")
    
    # Set byte order
    dtype = dtype.newbyteorder('>' if img_msg.is_bigendian else '<')
    
    # Determine image shape
    if 'rgb' in img_msg.encoding or 'bgr' in img_msg.encoding:
        shape = (img_msg.height, img_msg.width, 3)
    else:
        shape = (img_msg.height, img_msg.width)
    
    image_opencv = np.ndarray(shape=shape, dtype=dtype, buffer=img_msg.data)
    
    # Adjust byte order if necessary
    if img_msg.is_bigendian == (sys.byteorder == 'little'):
        image_opencv = image_opencv.byteswap().newbyteorder()
    
    # Handle the desired encoding conversion
    if desired_encoding != "passthrough" and img_msg.encoding != desired_encoding:
        if desired_encoding == "rgb8" and img_msg.encoding == "bgr8":
            image_opencv = cv2.cvtColor(image_opencv, cv2.COLOR_BGR2RGB)
        elif desired_encoding == "bgr8" and img_msg.encoding == "rgb8":
            image_opencv = cv2.cvtColor(image_opencv, cv2.COLOR_RGB2BGR)
        else:
            raise ValueError(f"Unsupported conversion from {img_msg.encoding} to {desired_encoding}")

    return image_opencv

def cv2_to_imgmsg(cv_image, encoding="bgr8"):
    img_msg = Image()
    img_msg.height = cv_image.shape[0]
    img_msg.width = cv_image.shape[1]
    img_msg.encoding = encoding
    img_msg.is_bigendian = 0
    img_msg.data = cv_image.tobytes()
    img_msg.step = len(img_msg.data) // img_msg.height

    return img_msg
np.seterr(all='raise')  
displayImage = False

plt.close('all')
class visual_tracker:
    def __init__(self):
        #self.bridge = CvBridge()
        self.i=0        #语音识别标志

        self.pictureHeight= rospy.get_param('~pictureDimensions/pictureHeight')
        self.pictureWidth = rospy.get_param('~pictureDimensions/pictureWidth')
        vertAngle =rospy.get_param('~pictureDimensions/verticalAngle')
        horizontalAngle =  rospy.get_param('~pictureDimensions/horizontalAngle')
        # precompute tangens since thats all we need anyways: 预计算切线
        self.tanVertical = np.tan(vertAngle)
        self.tanHorizontal = np.tan(horizontalAngle)    
        self.lastPoCsition =None

        self.targetDist = rospy.get_param('~targetDist')

        # 加载YOLOv10模型
        try:
            self.model = YOLOv10("/home/wheeltec/wheeltec_robot/src/ros-yolov10/scripts/yolov10n.pt")
            print('init success')
        except Exception as e:
            print(f"init error:{e}")

        # one callback that deals with depth and rgb at the same time 一个同时处理深度和RGB的回调
        im_sub = message_filters.Subscriber('/camera/rgb/image_raw', Image)
        dep_sub = message_filters.Subscriber('/camera/depth/image_raw', Image)
        self.timeSynchronizer = message_filters.ApproximateTimeSynchronizer([im_sub, dep_sub], 10, 0.5)
        
        self.timeSynchronizer.registerCallback(self.trackObject)

        self.positionPublisher = rospy.Publisher('/object_tracker/current_position', PositionMsg, queue_size=3)
        #self.infoPublisher = rospy.Publisher('/object_size=3)
        self._pub = rospy.Publisher("/yolo_detect_result", Image, queue_size=1)



    def trackObject(self, image_data, depth_data):
        if(image_data.encoding != 'rgb8'):
            raise ValueError('image is not rgb8 as expected')
        #convert both images to numpy arrays # 将两张图片都转换为Numpy数组
        frame = imgmsg_to_cv2(image_data, desired_encoding='rgb8')
        depthFrame = imgmsg_to_cv2(depth_data, desired_encoding='passthrough')#"32FC1")    
        # 使用YOLOv10进行目标检测 并发布目标位置信息（请在此填空）
        


        
    def publishPosition(self, pos):
        # calculate the angles from the raw position
        #从原始位置计算角度
        angleX = self.calculateAngleX(pos)
        angleY = self.calculateAngleY(pos)
        # publish the position (angleX, angleY, distance)
        posMsg = PositionMsg(angleX, angleY, pos[2])
        self.positionPublisher.publish(posMsg)
        
        
    def calculateAngleX(self, pos):
        '''calculates the X angle of displacement from straight ahead'''
        '''“检查某个位置是否合理，即是否足够接近上一个位置。”'''
        centerX = pos[0]
        displacement = 2*centerX/self.pictureWidth-1
        angle = -1*np.arctan(displacement*self.tanHorizontal)
        return angle

    def calculateAngleY(self, pos):
        '''calculates the X angle of displacement from straight ahead从正前方计算位移的X角度'''
        centerY = pos[1]
        displacement = 2*centerY/self.pictureHeight-1
        angle = -1*np.arctan(displacement*self.tanVertical)
        return angle
    
    
if __name__ == '__main__':
    visualfwflagPublisher = rospy.Publisher('/visual_follow_flag', Int8, queue_size =1)
    rospy.init_node('visual_tracker',anonymous = False)
    tracker=visual_tracker()
    rospy.logwarn('visualTracker init done')



    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.logwarn('failed')
