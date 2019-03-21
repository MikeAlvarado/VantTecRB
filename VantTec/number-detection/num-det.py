import cv2
import numpy as np
import deepnn as net
import sys
#import pytesseract as pt

def crop_aspect_center(img, aspect):
    '''Crops the image to the selected aspect ratio minimizing the lost area'''
    ow, oh = img.shape

    w = int(oh / aspect)
    h = int(ow * aspect)

    dw = ow - w
    dh = oh - h

    if dw > dh:
        off = int(dw // 2)
        return img[off:w,:]
    
    off = int(dh // 2)

    return img[:,off:h]

def search_number(img):
    minVal=50
    maxVal=100
    contourAreaThresh = 150
    white = [255,255,255]
    width, height, _ = img.shape
    size = (width, height, 1)
    target_size = (25, 35)
    target_aspect = float(target_size[0]) / float(target_size[1])

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny=cv2.Canny(img,minVal,maxVal,True)
    
    _, contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
    
    contour_img = np.zeros(size, dtype=np.uint8)

    for contour in contours:
        if cv2.contourArea(contour) > contourAreaThresh:
            cv2.drawContours(contour_img, [contour], 0, white, cv2.FILLED)

    inverted = cv2.bitwise_not(contour_img)
    inverted = cv2.resize(crop_aspect_center(inverted, target_aspect), target_size)

    cv2.namedWindow('contours', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('contours', 600, 600)
    cv2.imshow('contours', inverted)
    cv2.waitKey()

    return inverted

def search_display(img, template):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    min_matches = 10

    FLANN_INDEX_LSH = 6
    index_params= dict(
            algorithm = FLANN_INDEX_LSH,
            table_number = 12, # 6
            key_size = 20,     # 12
            multi_probe_level = 2 # 1
    )

    orb = cv2.ORB_create()
    matcher = cv2.FlannBasedMatcher(index_params, dict())

    # matcher.write("flann_params.yaml")
    
    tkp, tdes = orb.detectAndCompute(template, None)
    qkp, qdes = orb.detectAndCompute(img, None)

    kp_img = cv2.drawKeypoints(template, tkp, None)

    cv2.imshow('kp_img', kp_img)
    cv2.waitKey(0)

    matches = matcher.knnMatch(qdes,tdes,2)

    good = []

    # ratio test as per Lowe's paper
    for match in matches:
        if len(match) == 2:
            m, n = match
            if m.distance < 0.7 * n.distance:
                good.append(m)

    if len(good) > min_matches:
        src_pts = np.float32([ qkp[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ tkp[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
	
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        
        h, w = template.shape

        trans = cv2.warpPerspective(img, M, (w,h))

        cv2.imshow('trans', trans)
        return trans
    #    matchesMask = mask.ravel().tolist()


	
    #    h,w = template.shape
    #    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    #    dst = cv2.perspectiveTransform(pts,M)
    #    
    #    img = cv2.polylines(img,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    #else:
    #    print( "Not enough matches are found - {}/{}".format(len(good), min_matches) )
    #    matchesMask = None

    #match_img = cv2.drawMatches(img,qkp,template,tkp,good,None, flags=2, matchesMask=matchesMask)

    #cv2.namedWindow('matches', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('matches', 600, 600)
    #cv2.imshow('matches', match_img)
    #cv2.waitKey()

    return None

def main(argv):
    # img = cv2.imread(argv[1])
    display = cv2.imread(argv[1])
    # template = cv2.imread(argv[2])
    
    # display = search_display(img, template)
    
    if display is not None:
        number = search_number(display)
        print(net.predict(number, 'last_one'))

if __name__ == '__main__':
    main(sys.argv)
