import streamlit as st
from streamlit_option_menu import option_menu 
import os
import time
import cv_utils as utils
from ultralytics import YOLO
import tempfile
import cv2

model = YOLO('./static/best.pt')
#定义边栏导航
with st.sidebar:
    choose = option_menu('49期-5组',['视频处理','图片处理'],
                         icons=['camera-video-fill','image'])
if choose == '视频处理':
        st.title('红外摄像头人车识别项目')
        st.markdown("<hr>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(['案例效果', '视频处理'])
        with tab1:
            # 创建两个并排的列
            col1, col2 = st.columns(2)

            # 在第一列中播放原始视频
            with col1:
                st.header("原始视频")
                st.video('./static/traffic_night_HD.mp4')

            # 在第二列中播放处理后的视频
            with col2:
                st.header("处理后的视频")
                st.video('./static/traffic_night_HD.mp4')

        result_video_dir = None
        with tab2:
            # 创建两个并排的列
            col1, col2 = st.columns(2)

            # 在第一列中上传原始视频
            uploaded_video_file = None
            with col1:
                st.header("原始视频")
                # 创建上传视频文件的组件
                uploaded_video_file = st.file_uploader("上传", type=['mp4', 'avi'])

                if uploaded_video_file is not None:
                    if uploaded_video_file.name.strip():
                        timestamp = int(time.time())
                        new_file_name = f"{os.path.splitext(uploaded_video_file.name)[0]}_{timestamp}" + ".mp4"
                        file_path = os.path.join("./uploads", new_file_name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_video_file.getbuffer())
                            st.success(f"已保存文件: {file_path}")
                    # 播放上传的视频文件
                    st.video(uploaded_video_file)
                    # #开始预测处理
                    # result_video_dir = os.path.join("./红外摄像头人车识别项目/downloads", new_file_name)
                    # utils.predict_video(model, file_path, result_video_dir)

            # 在第二列中展示处理后的视频
            with col2:
                st.header("处理后的视频")
                if uploaded_video_file is not None:
                    # st.video(result_video_dir)
                    with st.spinner("Running..."):
                        try:
                            tfile = tempfile.NamedTemporaryFile()
                            tfile.write(uploaded_video_file.read())
                            vid_cap = cv2.VideoCapture(
                                tfile.name)
                            st_frame = st.empty()
                            while (vid_cap.isOpened()):
                                success, image = vid_cap.read()
                                if success:
                                    utils.display_detected_frames(model, st_frame, image)
                                else:
                                    vid_cap.release()
                                    break
                        except Exception as e:
                            st.error(f"Error loading video: {e}")
elif choose == '图片处理':
        st.title('红外摄像头人车识别项目')
        st.markdown("<hr>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(['案例效果', '图片处理'])

        with tab1:
            # 创建两个并排的列
            col1, col2 = st.columns(2)

            # 在第一列中展示原始图像
            with col1:
                st.header("原始图片")
                st.image('./static/rgb_1002.jpg')

            # 在第二列中播放处理后的图片
            with col2:
                st.header("处理后的图像")
                st.image('./static/rgb_1002_detect.jpg')
        
        # 处理后的图片
        result_img_dir = None
        with tab2:
            # 创建两个并排的列
            col1, col2 = st.columns(2)

            # 在第一列中上传原始图片
            with col1:
                st.header("原始图片")
                # 创建上传图片文件的组件
                uploaded_file = st.file_uploader("上传", type=['jpg', 'png'])

                if uploaded_file is not None:
                    if uploaded_file.name.strip():
                        timestamp = int(time.time())
                        new_file_name = f"{os.path.splitext(uploaded_file.name)[0]}_{timestamp}" + ".jpg"
                        file_path = os.path.join("./uploads", new_file_name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        st.success(f"已保存文件: {file_path}")

                    # 播放上传的图片文件
                    st.image(uploaded_file)
                    #开始预测处理
                    result_img_dir = os.path.join("./downloads", new_file_name)
                    utils.predict_img(model, file_path, result_img_dir)


            # 在第二列中展示处理后的图片
            with col2:
                st.header("处理后的图片")
                if result_img_dir is not None:
                    st.image(result_img_dir)    

# js_code = '''
# $(document).ready(function(){
#     $("button[kind=icon]", window.parent.document).remove()
# });
# '''
# # 因为JS不需要展示，所以html宽高均设为0，避免占用空间，且放置在所有组件最后
# # 引用了JQuery v2.2.4
# html(f'''<script src="https://cdn.bootcdn.net/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
#     <script>{js_code}</script>''',
#      width=0,
#      height=0)