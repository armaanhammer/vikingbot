#################################################################################################
# Derived from code written by: Vivan Bhalla
# Description: This program is used to detect the object using its color as a parameter
#################################################################################################

### Import the libraries ####
import numpy as np
import cv2
import random
from matplotlib import pyplot as plt


## HSV constants for object and spotlight
H_object=179
S_object=255
#V_object=243 #light object
V_object=42 #dark object
#H_spotlight=179
#S_spotlight=255
#V_spotlight=243
H_low=0
S_low=0
V_low=0




## Create a video capture object
cap = cv2.VideoCapture(0) # Send 0 since we have only one camera. Send 1 to use second camera


## Check whether capture object is opened or not
if(cap.isOpened() == False):
    ## If object is not initialized then open it
    cap.open()

width = cap.get(3)  # float
height = cap.get(4) # float

#height, width, channels = cap.shape
print "Height: ", height, "Width: ", width #, "Channels: ", channels.rjust(4)


# Create a window
cv2.namedWindow('image')

## Start capturing frame by frame in an infinite loop
while(True):

    # Start capturing the frames
    ret, frame = cap.read() # Get the returned value(T/F) and the frame.

    if(ret != True): # Check if reading was successful or not
        print "Cannot read from the frame\n"

    # Create numpy arrays of these boundaries
    # TODO: hardcode the values below from what is found through experiment
    higher_boundary_object = np.array([H_object,S_object,V_object])
#    higher_boundary_spotlight = np.array([H_spotlight,S_spotlight,V_spotlight])
    lower_boundary = np.array([H_low,S_low,V_low])

    ############################ TODO ######################################

    # Convert the captured frame from BGR to HSV format
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only our object
    threshold_object = cv2.inRange(hsv,lower_boundary,higher_boundary_object)
#    threshold_spotlight = cv2.inRange(hsv,lower_boundary,higher_boundary_spotlight)

    # Get the targeted image by doing bitwise and
    target_object = cv2.bitwise_and(frame,frame,mask=threshold_object)
#    target_spotlight = cv2.bitwise_and(frame,frame,mask=threshold_spotlight)

    ## Perform morphological transformations #####
    ## Morphological opening
    # We first remove the white noise from the boundaries of the detected object - Erode operation
    # We create an elliptical kernel for the erosion
    target_object = cv2.erode(target_object,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
#    target_spotlight = cv2.erode(target_spotlight,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))

    # Perform the dilation to get the more enchanced image of the object
    target_object = cv2.dilate(target_object,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
#    target_spotlight = cv2.dilate(target_spotlight,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))

    ## Morphological Closing - This is done to fill holes insie the detected object.
    ## This is done by first dilation then eroding the image

    target_object = cv2.dilate(target_object,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
    target_object = cv2.erode(target_object,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
#    target_spotlight = cv2.dilate(target_spotlight,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
#    target_spotlight = cv2.erode(target_spotlight,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))



    ######################## Object Tracking #########################################################
    # We use the moments method to track the object

    # Convert the images to black and white

    # Get the moments of the two images
    moments_object = cv2.moments(threshold_object)
#    moments_spotlight = cv2.moments(threshold_spotlight)

    # Calculate the area of the object object
    area_object=moments_object["m00"]
#    area_spotlight=moments_spotlight["m00"]

    # To remove the effect of noise, consider tracking above only a threshold of area
    if(area_object > 10000):
        # Calculate the x and y coordinates of center
        X_r = moments_object["m10"] / area_object;
        Y_r = moments_object["m01"] / area_object
        X = int(X_r)
        Y = int(Y_r)

        if X <= (width * 1/3): #left third of FOV (field of view)
            directive = 'go_forward'
        elif (width * 1/3) < X <= (width * 2/3): #middle third of FOV
            if random.randint(0,1):
                directive = 'turn_left'
            else:
                directive = 'turn_right'
        else: #right third of FOV
            directive = 'go_forward'



#    if(area_spotlight>8000):
        # Calculate the centre for spotlight
#        X_s=moments_spotlight["m10"] / area_spotlight
#        Y_s=moments_spotlight["m01"] / area_spotlight

#    print "X for S is"+str(X_s)
#    print "Y for S is"+str(Y_s)
#    print "X for R is"+str(X_r)
#    print "Y for R is"+str(Y_r)
    print "X: ", str(X).rjust(4), "Y: ", str(Y).rjust(4), directive

    ## Display the images
    cv2.imshow("Result_object",target_object)
    cv2.imshow("Mask_object",threshold_object)
#    cv2.imshow("Result_spotlight",target_spotlight)
#    cv2.imshow("Mask_spotlight",threshold_spotlight)
    cv2.circle(frame,(X,Y),3,255,-1)
    cv2.imshow("Original Image",frame)

#    plt.imshow(frame),plt.show()


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break





# Release the capture
cap.release()
cv2.destroyAllWindows()
