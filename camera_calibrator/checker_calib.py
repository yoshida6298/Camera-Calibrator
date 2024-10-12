import numpy as np
import cv2
import glob
import argparse
import os


def checker_calibration(input_dir, output_dir, checker_size=24.0):
    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG', 'png']
    image_paths = []
    for extension in extensions:
        found_paths = os.path.join(input_dir, '*.{}'.format(extension))
        image_paths.extend(glob.glob(found_paths))

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    prepare_object_points = np.zeros((6*8, 3), np.float32)
    prepare_object_points[:, :2] = checker_size*np.mgrid[0:6, 0:8].T.reshape(-1, 2)
    # Arrays to store object points and image points from all the images.
    object_points = []  # 3d point in real world space
    image_points = []  # 2d points in image plane.

    for image_path in image_paths:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (6, 8), None)
        # If found, add object points, image points (after refining them)
        if ret:
            object_points.append(prepare_object_points)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            image_points.append(corners)
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (6, 8), corners2, ret)
            img2 = cv2.resize(img, (int(img.shape[1]/8), int(img.shape[0]/8)))
            cv2.imshow('img', img2)
            cv2.waitKey(500)
    cv2.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, gray.shape[::-1], None, None)
    print("キャリブレーション終了")
    np.set_printoptions(precision=6, suppress=True)
    print(dist)
    np.savetxt(str(output_dir / "distortion.txt"), dist, fmt='%.6f')
    print(f'{str(output_dir / "distortion.txt")}を保存しました')
    np.set_printoptions(precision=2, suppress=True)
    print(mtx)
    np.savetxt(str(output_dir / "intrinsics.txt"), mtx, fmt='%.2f')
    print(f'{str(output_dir / "intrinsics.txt")}を保存しました')


# def main():
#     parser = argparse.ArgumentParser('カメラのキャリブレーション')
#     parser.add_argument('input_dir', help='入力画像のディレクトリ')
#     args = parser.parse_args()
#     checker_calibration(args.input_dir)
#
#
# if __name__ == '__main__':
#     main()
