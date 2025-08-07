# Camera Calibration and Extrinsic Matrix Estimation using OpenCV

This Python script performs **camera calibration** using a checkerboard pattern and computes **extrinsic parameters** (rotation and translation vectors) relative to a specific scene using OpenCV.

## 📹 Overview

The code:
1. Calibrates a webcam using images of a standard checkerboard.
2. Computes the **intrinsic camera matrix** and **lens distortion coefficients**.
3. Captures a new image with the checkerboard at a known distance and estimates the **extrinsic matrix** (`[R|t]`), showing the position and orientation of the checkerboard relative to the camera.

---

## 🧠 Key Concepts

- **Intrinsic Matrix**: Describes the internal parameters of the camera (focal lengths, optical center).
- **Extrinsic Matrix**: Describes the position (translation) and orientation (rotation) of the object in the world frame relative to the camera.
- **Checkerboard**: A known pattern (6x9 corners here) used for calibration.
- **solvePnP**: OpenCV function to calculate the pose of a 3D object from 2D image points.

---

## 📐 Checkerboard Details

- Dimensions: **6 x 9** inner corners
- Real-world square size: **7/16 inches ≈ 0.4375 inches**

You may modify the checkerboard size and square dimensions according to your own calibration target.

---

## ▶️ How to Run

1. **Install Dependencies**
   ```bash
   pip install opencv-python numpy
   ```

2. **Run the Script**
   ```bash
   python calibrate_camera.py
   ```

3. **Capture Calibration Images**
   - Move the checkerboard to various positions and angles in view of the camera.
   - Press `c` to capture an image when the checkerboard is detected.
   - Collect at least **5 images** (15 recommended for best accuracy).
   - Press `q` to stop collecting and perform calibration.

4. **Capture Extrinsic Image**
   - Place the checkerboard at a known distance (e.g., 12 inches away).
   - Press `e` to capture the image and compute extrinsic parameters.
   - Press `q` to exit if you want to skip.

---

## 📝 Output

- **Intrinsic Matrix**: Printed after calibration
- **Distortion Coefficients**: Printed after calibration
- **Extrinsic Matrix [R | t]**: Printed after `solvePnP`
- **extrinsic_image.jpg**: Saved image used for extrinsic matrix calculation

---

## 🎥 Example Demo

In the included demo:
- **15 images** were used for intrinsic calibration.
- The extrinsic image was taken with the checkerboard **placed 12 inches from the camera**.
- The resulting **translation vector z-value was ~12.09**, demonstrating accurate depth estimation.
- Demo Link: [text](https://buffalo.box.com/s/p0kv891itdg2hb5yk3nannvfrjs13fah)

---

## 🛠️ Notes

- Ensure good lighting and focus on the checkerboard for accurate corner detection.
- Use a rigid, flat checkerboard to prevent calibration errors.
- Adjust `CHECKERBOARD` and `square_size` constants as per your physical calibration grid.

---

## 📂 File Structure

```
calibrate_camera.py       # Main script
extrinsic_image.jpg       # Saved after extrinsic capture
README.md                 # This file
```

---

## 📸 Dependencies

- Python 3.x
- OpenCV (`cv2`)
- NumPy

---

## 📧 Contact

For any questions or feedback, feel free to reach out or open an issue!