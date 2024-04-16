import cv2
from matplotlib import pyplot as plt

def display_detected_frames(model, st_frame, image):
    """
    Display the detected objects on a video frame using the YOLOv8 model.
    :param conf (float): Confidence threshold for object detection.
    :param model (YOLOv8): An instance of the `YOLOv8` class containing the YOLOv8 model.
    :param st_frame (Streamlit object): A Streamlit object to display the detected video.
    :param image (numpy array): A numpy array representing the video frame.
    :return: None
    """
    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720 * (9 / 16))))

    # Predict the objects in the image using YOLOv8 model
    res = model.predict(image, show=False)

    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   channels="BGR",
                   use_column_width=True
                   )

# 预测视频
def predict_video(model, file, result_dir):
    cap = cv2.VideoCapture(file)
    # 获取视频帧的维度
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # 创建VideoWriter对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(result_dir, fourcc, 25.0, (frame_width, frame_height))
    # 设置整个视频处理的进度条
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frames)
    # 处理视频帧
    for idx, _ in enumerate(range(total_frames)):
        print(f"enter---{idx + 1}")
        # 读取某一帧
        success, frame = cap.read()
        if success:
            results = model.predict(frame, show=False)
            result = results[0]
            print(f"result:{result}")
            plt.imshow(X=result.plot()[:, :, ::-1])
            plt.show()
            annotated_frame = result.plot()
            # cv2.imshow("video",img)
            # 将带注释的帧写入视频文件
            out.write(annotated_frame)
            # cv2.imwrite(f"{idx}.jpg", annotated_frame)
            # fps = 10
            # if cv2.waitKey(delay=int(1000 / fps)) == 27:
            #     break
        else:
            break
    print("end---")        
    cap.release()
    out.release()
    # cv2.destroyAllWindows()

#预测图像
def predict_img(model, file, result_dir):
    results = model.predict(file)
    result = results[0]
    img = result.plot()

    # plt.imshow(X=img[:, :, ::-1])
    # plt.show()
    plt.imsave(result_dir, img[:, :, ::-1])
