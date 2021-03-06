import numpy as np 
import cv2
import dlib
import random

    
def add_hat(img):
    
    img = cv2.imread(img)

    hats = ['christmas_hat.png','cowboy_hat.png','flower_crown.png',
        'witch_hat.png','straw.png','love.png']

    hat_img = cv2.imread(hats[random.randint(0, 5)],-1)
    
    r,g,b,a = cv2.split(hat_img) 
    rgb_hat = cv2.merge((r,g,b))


    predictor_path = "shape_predictor_5_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)  

    detector = dlib.get_frontal_face_detector()

    dets = detector(img, 1)

    if len(dets)>0:  
        for d in dets:
            x,y,w,h = d.left(),d.top(), d.right()-d.left(), d.bottom()-d.top()

            shape = predictor(img, d)

            point1 = shape.part(0)
            point2 = shape.part(2)

            eyes_center = ((point1.x+point2.x)//2,(point1.y+point2.y)//2)

            factor = 1.5
            resized_hat_h = int(round(rgb_hat.shape[0]*w/rgb_hat.shape[1]*factor))
            resized_hat_w = int(round(rgb_hat.shape[1]*w/rgb_hat.shape[1]*factor))

            if resized_hat_h > y:
                resized_hat_h = y-1

            resized_hat = cv2.resize(rgb_hat,(resized_hat_w,resized_hat_h))

            mask = cv2.resize(a,(resized_hat_w,resized_hat_h))
            mask_inv =  cv2.bitwise_not(mask)

            dh = 0
            dw = 0

            bg_roi = img[y+dh-resized_hat_h:y+dh,(eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)]
            bg_roi = bg_roi.astype(float)
            mask_inv = cv2.merge((mask_inv,mask_inv,mask_inv))
            alpha = mask_inv.astype(float)/255

            alpha = cv2.resize(alpha,(bg_roi.shape[1],bg_roi.shape[0]))
 
            bg = cv2.multiply(alpha, bg_roi)
            bg = bg.astype('uint8')


            hat = cv2.bitwise_and(resized_hat,resized_hat,mask = mask)
            hat = cv2.resize(hat,(bg_roi.shape[1],bg_roi.shape[0]))

            add_hat = cv2.add(bg,hat)

            img[y+dh-resized_hat_h:y+dh,(eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)] = add_hat

            return img

