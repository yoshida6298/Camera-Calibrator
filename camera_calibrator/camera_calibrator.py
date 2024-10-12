import sys
from pathlib import Path
import requests
import questionary
from clip_images import clip_all_frames
from checker_calib import checker_calibration
import tempfile


def get_checker_pdf():
    url = "https://raw.githubusercontent.com/yoshida6298/Camera-Calibrator/main/assets/checkerboard.pdf"
    file_path = Path.home() / 'Downloads/checkerboard.pdf'
    data = requests.get(url).content
    with open(file_path, mode='wb') as f:
        f.write(data)
    print("ダウンロードフォルダにダウンロードされました")
    print("チェッカーボードを印刷し、縦向きで動画を撮影してください")


def main():
    print("📷 Camera Calibrator 📷")
    select_act = questionary.select(
        "どちらを実行しますか？",
        choices=["カメラキャリブレーション", "チェッカーボードのダウンロード"]
    ).ask()

    if select_act == "チェッカーボードのダウンロード":
        get_checker_pdf()
        sys.exit()

    file_path = Path(questionary.path("入力動画ファイルを指定してください").ask()).expanduser()
    output_dir = Path(questionary.path("出力ディレクトリを指定してください", only_directories=True).ask()).expanduser()
    if not output_dir.exists():
        print("出力ディレクトリを作成します")
        Path.mkdir(output_dir, parents=True)
    else:
        if len(list(output_dir.iterdir())) > 0:
            stem = output_dir.stem + '_new'
            parent = output_dir.parent
            print(f"出力ディレクトリが空でありません。新規に{stem}を作成します")
            output_dir = parent / stem
            Path.mkdir(output_dir, parents=True)

    step_num = int(questionary.text("動画の分割単位を指定してください[フレーム]", default="10").ask())
    checker_size = float(questionary.text("チェッカーボード１マスの大きさを指定してください[mm]", default="24.0").ask())

    with tempfile.TemporaryDirectory() as temp_dir:
        print(temp_dir)
        clip_all_frames(str(file_path), temp_dir, step_num)
        checker_calibration(temp_dir, output_dir, checker_size)

if __name__ == '__main__':
    main()
