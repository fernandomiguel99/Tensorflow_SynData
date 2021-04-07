import tensorflow as tf
import numpy as np
from scipy import misc
import cv2

class bgs:

    def __init__(self):
        self.g_mean = np.array(([126.88,120.24,112.19])).reshape([1,1,3])
        self.gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction = 1.0)
        self.checkpoint = './salience_model'
        self.meta_graph = './meta_graph/my-model.meta'

        self.sess = tf.Session(config=tf.ConfigProto(gpu_options = self.gpu_options))
        self.saver = tf.train.import_meta_graph(self.meta_graph)
        self.saver.restore(self.sess,tf.train.latest_checkpoint(self.checkpoint))
        self.image_batch = tf.get_collection('image_batch')[0]
        self.pred_mattes = tf.get_collection('mask')[0]

    def rgba2rgb(self, img):
        return img[:,:,:3]*np.expand_dims(img[:,:,3],2)

    def rgb2rgba(self, rgb, alpha):
        r_channel, g_channel, b_channel = cv2.split(rgb)
        return cv2.merge((r_channel, g_channel, b_channel, alpha))

    def find_alpha(self, rgb_img):

        if rgb_img.shape[2] == 4:
            rgb_img = rgba2rgb(rgb_img)
        origin_shape = rgb_img.shape[:2]
        rgb_img = np.expand_dims(misc.imresize(rgb_img.astype(np.uint8),[320,320,3],interp="nearest").astype(np.float32)-self.g_mean,0)

        pred_alpha = self.sess.run(self.pred_mattes,feed_dict = {self.image_batch:rgb_img})
        alpha = misc.imresize(np.squeeze(pred_alpha),origin_shape)

        ret, final_alpha = cv2.threshold(alpha,127,255,cv2.THRESH_TOZERO)

        return final_alpha

    def crop_object(self, img, alpha, edge = 5):
        contours, hierarchy = cv2.findContours(alpha, 1, 2)
        cnt = contours[0]
        x,y,w,h = cv2.boundingRect(cnt)
        new_img = img[y-edge:y+h+edge, x-edge:x+w+edge]
        new_alpha = alpha[y-edge:y+h+edge, x-edge:x+w+edge]

        return new_img, new_alpha

    def __exit__(self):
        print "Closing TensorFlow session!"
        self.sess.close()
