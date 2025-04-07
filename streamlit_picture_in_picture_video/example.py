import streamlit as st
from streamlit_picture_in_picture_video import streamlit_picture_in_picture_video

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Component with constant args")

# Create an instance of our component with a constant `name` arg, and
# print its output value.

streamlit_picture_in_picture_video("https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")

#num_clicks = streamlit_picture_in_picture_video("World")
#st.markdown("You've clicked %s times!" % int(num_clicks))
