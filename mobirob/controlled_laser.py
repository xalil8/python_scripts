import numpy as np
import cv2


class ControlledLaser(object):
    __instance = None

    def __init__(self, image_size, initial_pt=None):
        """

        :param image_size: size of the image the laser will be superimposed on
        :param initial_pt: (optional) the initial position of the laser point on the image
        """

        if ControlledLaser.__instance != None:
            raise Exception("Only one ControlledLaser can be generated (Singleton)!")
        else:
            ControlledLaser.__instance = self

        if initial_pt is None:
            self.__x_center = image_size[0] // 2
            self.__y_center = image_size[1] // 2
        else:
            self.__x_center = initial_pt[0]
            self.__y_center = initial_pt[1]

        self.__x_spd = 0
        self.__y_spd = 0
        self.xmax = image_size[0]
        self.ymax = image_size[1]
        self.max_speed = (image_size[0] // 5, image_size[1] // 5)
        self.noise_sigma = (.1, .1)
        self.dot = cv2.resize(cv2.imread("reddot.png", cv2.IMREAD_UNCHANGED), None, fx=0.5, fy=0.5)

    def step(self, image, speed):
        """

        :param image: input image
        :param speed: speed of the laser pointer when the image is taken
        :return: input image with dot on it
        """
        image = cv2.copyMakeBorder(image, self.dot.shape[0], self.dot.shape[0], self.dot.shape[1], self.dot.shape[1],
                                   cv2.BORDER_CONSTANT, None, (0, 0, 0))

        xspd = np.clip(np.rint(np.random.normal(speed[0], self.noise_sigma[0], 1)), -self.max_speed[0],
                       self.max_speed[0])

        yspd = np.clip(np.rint(np.random.normal(speed[1], self.noise_sigma[1], 1)), -self.max_speed[1],
                       self.max_speed[1])

        self.__x_center = int(
            np.clip(self.__x_center + (np.sign(xspd) * np.sign(self.__x_spd) >= 0) * xspd, 0, self.xmax))
        self.__y_center = int(
            np.clip(self.__y_center + (np.sign(yspd) * np.sign(self.__y_spd) >= 0) * yspd, 0, self.ymax))

        self.__x_spd = xspd
        self.__y_spd = yspd

        x_offset = self.__x_center + self.dot.shape[1] // 2
        y_offset = self.__y_center + self.dot.shape[0] // 2

        y1, y2 = y_offset, y_offset + self.dot.shape[0]
        x1, x2 = x_offset, x_offset + self.dot.shape[1]

        alpha_s = self.dot[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            image[y1:y2, x1:x2, c] = (alpha_s * self.dot[:, :, c] + alpha_l * image[y1:y2, x1:x2, c])

        return image[self.dot.shape[0]: -self.dot.shape[0], self.dot.shape[1]: -self.dot.shape[1]]

