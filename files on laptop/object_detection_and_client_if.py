#################################################################################################
# Derived from code written by: Vivan Bhalla
# Description: This program is used to detect the object using its color as a parameter
#################################################################################################

### Import the libraries ####
import numpy as np
import cv2
import random
import argparse
import socket
#from matplotlib import pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description='vikingbot client.')

    parser.add_argument(
            '--host',
            default='192.168.0.102',
            help='host ip of the vikingbot')

    parser.add_argument(
            '--port',
            default=5000,
            type=int,
            help='port used to communicate to the vikingbot')

    return parser.parse_args()


def Main(host, port):
    mySocket = socket.socket()
    mySocket.connect((host,port))

#    message = raw_input(" -> ")
    message = 'go_forward'

#    while message != 'q':
#        if message:
#            mySocket.send(message.encode())
#            data = mySocket.recv(1024).decode()

#            print ('Received from server: ' + data)

#        message = raw_input(" -> ")

#    mySocket.close()


    ## HSV constants for object and spotlight
    H_object=179
    S_object=255
    #V_object=243 #light object
    V_object=42 #dark object
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

    X = 1 # hack to prevent seg fault when dark area is initially too small
    Y = 1
    directive = 'nonsensical-string'


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
        lower_boundary = np.array([H_low,S_low,V_low])

        ############################ TODO ######################################
        # Convert the captured frame from BGR to HSV format
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only our object
        threshold_object = cv2.inRange(hsv,lower_boundary,higher_boundary_object)

        # Get the targeted image by doing bitwise and
        target_object = cv2.bitwise_and(frame,frame,mask=threshold_object)

        ## Perform morphological transformations #####
        ## Morphological opening
        # We first remove the white noise from the boundaries of the detected object - Erode operation
        # We create an elliptical kernel for the erosion
        target_object = cv2.erode(target_object,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))

        # Perform the dilation to get the more enchanced image of the object
        target_object = cv2.dilate(target_object,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))

        ## Morphological Closing - This is done to fill holes insie the detected object.
        ## This is done by first dilation then eroding the image
        target_object = cv2.dilate(target_object,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
        target_object = cv2.erode(target_object,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))



        ######################## Object Tracking #########################################################
        # We use the moments method to track the object

        # Convert the images to black and white

        cap_array = np.asarray(cap)

#        ret,thresh = cv2.threshold(target_object,127,255,0)

#        contours,hierarchy = cv2.findContours(thresh, 1, 2)

#        cnt = contours[0]
#        M = cv2.moments(cnt)

#        print M


        # Get the moments of the two images
        moments_object = cv2.moments(threshold_object)

        # Calculate the area of the object object
        area_object=moments_object["m00"]

        # To remove the effect of noise, consider tracking above only a threshold of area
        if(area_object > 10000):
            # Calculate the x and y coordinates of center
            X_r = moments_object["m10"] / area_object;
            Y_r = moments_object["m01"] / area_object
            X = int(X_r)
            Y = int(Y_r)

            # Decide to go forward or turn left or right
            if X <= (width * 1/5): #left third of FOV (field of view)
                directive = 'go_forward 0.5'
            elif (width * 1/5) < X <= (width * 4/5): #middle third of FOV
                blarg = random.randint(0,20)
                if blarg > 1:
                    directive = 'turn_left 0.5'
                else:
                    directive = 'turn_left 0.5'
            else: #right third of FOV
                directive = 'go_forward 0.5'

        # print center of mass of object and decision
        print "X: ", str(X).rjust(4), "Y: ", str(Y).rjust(4), "  ", directive

        # Next two outer if statements designed to prevent laptop from filling
        # vikingbot's buffer.

        # send the directive in a message
        if message:
            print '\nmessage exists. Sending. '
            mySocket.send(message.encode())
            message = None

#        # psuedo-code:
#        if not child_pid:
#            child_pid = fork()
#            if child_pid: #I'm the parent
#                keep going
#            else: #I'm the child.
#                Wait for the socket
#                return the value from the socket
#                tell parent to set child_pid to None (null)
#                kill myself
#        else: #child alrady exists
#            keep going

        # check if data back from vikingbot
        data = mySocket.recv(1024).decode()
        print 'got here at least' #debug
        if data:
            print '\ndata exists ' #debug
            print ('Received from server: ' + data)
#            if 'ready' in data: #vikingbot ready for next command
            if 'seconds' in data: #vikingbot ready for next command
                print 'ready for next message'
                message = directive



        ## Display the images
        cv2.imshow("Result_object",target_object)
        cv2.imshow("Mask_object",threshold_object)
        cv2.circle(frame,(X,Y),3,255,-1)

        cv2.imshow("Original Image",frame)
    #    plt.imshow(frame),plt.show()

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

    # Releast the socket
    mySocket.close()


if __name__ == '__main__':
    args = get_args()

    print('Host: {}'.format(args.host))
    print('Port: {}'.format(args.port))

    Main(args.host, args.port)
