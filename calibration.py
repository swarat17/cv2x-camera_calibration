import cv2
import numpy as np

# Define checkerboard dimensions
CHECKERBOARD = (6, 9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Real-world square size in inches
square_size = 7.0 / 16.0  # inches

# Prepare object points (0,0,0), (1,0,0), ..., (5,8,0)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp[:, :2] *= square_size  # Scale to real-world units

objpoints = []  # 3d points in real world space
imgpoints = []  # 2d points in image plane

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Press 'c' to capture a calibration image, 'q' to finish calibration.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    display = frame.copy()
    if found:
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        cv2.drawChessboardCorners(display, CHECKERBOARD, corners2, found)

    cv2.imshow('Calibration', display)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c') and found:
        objpoints.append(objp.copy())
        imgpoints.append(corners2)
        print(f"Captured calibration image #{len(objpoints)}")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if len(objpoints) < 5:
    print("Not enough images for calibration. Need at least 5.")
    exit()

# Calibrate camera using all collected images
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)
print("Final Camera matrix:\n", mtx)
print("Distortion coefficients:\n", dist)

# Now, capture a new image for extrinsic calculation
cap = cv2.VideoCapture(0)
print("Press 'e' to capture an image for extrinsic calculation.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
    display = frame.copy()
    if found:
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        cv2.drawChessboardCorners(display, CHECKERBOARD, corners2, found)

    cv2.imshow('Extrinsic', display)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('e') and found:
        # Use solvePnP to get extrinsic parameters for this image
        retval, rvec, tvec = cv2.solvePnP(objp, corners2, mtx, dist)
        print("Rotation vector:\n", rvec)
        print("Translation vector:\n", tvec)
        R, _ = cv2.Rodrigues(rvec)
        extrinsic = np.hstack((R, tvec))
        print("Extrinsic matrix [R|t]:\n", extrinsic)
        # Save the image used for extrinsic calculation
        cv2.imwrite("extrinsic_image.jpg", frame)
        print("Saved extrinsic image as extrinsic_image.jpg")
        break
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()