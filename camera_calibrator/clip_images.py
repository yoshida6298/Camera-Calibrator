import os
import cv2
import argparse
import time
from tqdm import tqdm


def clip_all_frames(video_path, output_dir, step, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    if output_dir:
        dir_path = output_dir
    else:
        dir_path = os.path.join(os.path.dirname(video_path), base_name + "_images")
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, base_name)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    digit = len(str(frame_count))

    frame_no = 0
    start = time.time()

    with tqdm(total=frame_count) as pbar:
        while True:
            ret, frame = cap.read()
            if ret:
                if frame_no % step == 0:
                    cv2.imwrite('{}_{}.{}'.format(base_path, str(frame_no).zfill(digit), ext), frame)
                frame_no += 1
                pbar.update(1)
                start = time.time()
            elif time.time() - start > 20.0:
                print('Time out')
                return
            elif frame_no == frame_count:
                print('Finished')
                return


# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('input_path', help='Input movie path')
#     parser.add_argument('--output_dir', default="")
#     parser.add_argument('--step', default=1, type=int)
#     args = parser.parse_args()
#     clip_all_frames(args.input_path, args.output_dir,  args.step)
#
#
# if __name__ == "__main__":
#     main()
