import streamlit as st
from streamlit_picture_in_picture_video import streamlit_picture_in_picture_video

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Picture-in-Picture Video")

# Create an instance of our component with a constant `name` arg, and
# print its output value.

show_controls = st.checkbox("Show video controls", True)
auto_play = st.checkbox("Auto-play video", True)
start_in_pip = st.checkbox("Start in Picture-in-Picture mode", False)
streamlit_picture_in_picture_video(
    video_src="https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    controls=show_controls,
    auto_play=auto_play,
    start_in_pip=start_in_pip
)

#num_clicks = streamlit_picture_in_picture_video("World")
#st.markdown("You've clicked %s times!" % int(num_clicks))
