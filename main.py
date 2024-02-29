# IMPORT NUMPY AND OPENCV
import numpy as np # importing numpy, a library that allows for complex data structures
import cv2 # importing opencv, a image processing library for python
from imgprocessing import processed # importing processing function

# VIDEO = VIDEO CAPTURE
vid = cv2.VideoCapture(0) # setting vid equal to index 0 capture (default webcam)

# WHILE TRUE
while (True): # indefinite loop

    # IMAGE PROCESSING
    ret, img = vid.read() # img or (frame) is equal to the frame being read
    maskx = 500 # mask variables
    masky = 180
    maskw = 920
    maskh = 720
    maskimg = processed(img=img, maskx=maskx, masky=masky, maskw=maskw, maskh=maskh) # image processing function

    contours, hierarchy = cv2.findContours(maskimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # detecting contour lines

    # IF THERE ARE CONTOURS
    if contours is not None and len(contours) >= 2: # if there are atleast two contour lines detected
        line1 = []
        line2 = []

        contours = sorted(contours, key=cv2.contourArea, reverse=False) # sorting the contours by area so bigger will be the outer curve and smaller will be the inner curve
        contour1 = contours[0] # smallest (inner) contour
        contour2 = contours[-1] # biggest (outer) contour
        cv2.polylines(img, [np.array(contour1)], False, (255, 0, 0), 3) # collects all the points stored in the contour1 array and connects lines in between them
        cv2.polylines(img, [np.array(contour2)], False, (0, 0, 255), 3) # collects all the points stored in the contour2 array and connects lines in between them

        for pt in range(min(len(contour1), len(contour2))):  # finding which contour has less points, then iterating through the loop for however many points the smallest contour has
            x1 = int(contour1[pt][0][0])
            x2 = int(contour2[pt][0][0])
            y1 = int(contour1[pt][0][1])
            y2 = int(contour2[pt][0][1])
            line1.append([x1, y1])
            line2.append([x2, y2])

        def interpolate(a1, a2, poly_deg=3, n_points=100, plot=True):

            a1 = np.array(a1)
            a2 = np.array(a2)

            min_a1_x, max_a1_x = min(a1[0:-1, 0]), max(a1[0:-1, 0])
            new_a1_x = np.linspace(min_a1_x, max_a1_x, n_points)
            a1_coefs = np.polyfit(a1[:, 0], a1[:, 1], poly_deg)
            new_a1_y = np.polyval(a1_coefs, new_a1_x)
            min_a2_x, max_a2_x = min(a2[:, 0]), max(a2[:, 0])
            new_a2_x = np.linspace(min_a2_x, max_a2_x, n_points)
            a2_coefs = np.polyfit(a2[:, 0], a2[:, 1], poly_deg)
            new_a2_y = np.polyval(a2_coefs, new_a2_x)
            midx = [np.mean([new_a1_x[i], new_a2_x[i]]) for i in range(n_points)]
            midy = [np.mean([new_a1_y[i], new_a2_y[i]]) for i in range(n_points)]

            # if plot:
            #     plt.plot(a1[:, 0], a1[:, 1], c='black')
            #     plt.plot(a2[:, 0], a2[:, 1], c='black')
            #     plt.plot(midx, midy, '--', c='black')
            #     plt.show()

            return np.array([[x, y] for x, y in zip(midx, midy)])

        midline = interpolate(line1, line2)

        # POLYLINES CONNECT ARRAY
        #cv2.polylines(img, [np.array(midline)], False, (0, 255, 0), 3) # collects all the points stored in the midline array and connects lines in between them

        # HIGHLIGHT MASK WITH RECTANGLE
        cv2.rectangle(img, (maskx, masky), (maskx + maskw, masky + maskh), (255, 255, 255), 3) # uses the variables from the rectangle mask to draw a rectangle for end user purposes

        # SHOW IMAGE
        cv2.imshow('frame', img) # uses cv2 show image function to display final image

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        cv2.imshow('frame', img) # uses cv2 show image function to display final image
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# PROGRAMMING WORKS CITED

# Video capture and video display (Lines 1-13, 55-63) https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
# OpenCV rectangle (Line 44) https://www.geeksforgeeks.org/python-opencv-cv2-rectangle-method/
# OpenCV contours (Lines 20) https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html
# Contour area (Line 26) https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
# Polylines (Line 29, 30, 41) https://www.geeksforgeeks.org/python-opencv-cv2-polylines-method/
# Sorting (Line 26) https://docs.python.org/3/howto/sorting.html
# Sorting (Line 26) https://docs.python.org/3/howto/sorting.html