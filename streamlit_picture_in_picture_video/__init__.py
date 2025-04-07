import os
import streamlit.components.v1 as components
import streamlit as st

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_picture_in_picture_video",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_picture_in_picture_video", path=build_dir)


# Inspiration: https://github.com/bouzidanas/streamlit-float



def float_init(theme=True, include_unstable_primary=False):
# add css to streamlit app
    html_style = '''
    <style>
    div.element-container:has(div.float) {
        position: absolute!important;
    }
    div.element-container:has(div.floating) {
        position: absolute!important;
    }
    div:has( >.element-container div.float) {
        display: flex;
        flex-direction: column;
        position: fixed;
        z-index: 99;
    }
    div.float, div.elim {
        display: none;
        height:0%;
    }
    div.floating {
        display: flex;
        flex-direction: column;
        position: fixed;
        z-index: 99; 
    }


    /* Target element-container that contains a video#main-video at any depth */
    div.element-container:has(video#main-video) {
        position: fixed !important;
        z-index: 99;
        bottom: 20px;
        right: 20px;
        width: 320px;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 0 12px rgba(0,0,0,0.3);
        overflow: hidden;
    }
    
    /* Make sure the video itself fits correctly in the container */
    video#main-video {
        width: 100%;
        height: auto;
        display: block;
    }
    
    /* Style for any controls or elements inside the container */
    div.element-container:has(video#main-video) button {
        position: absolute;
        bottom: 10px;
        right: 10px;
        z-index: 100;
    }
    </style>
    '''
    st.markdown(html_style, unsafe_allow_html=True)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def streamlit_picture_in_picture_video(video_src: str, controls: bool = True, auto_play: bool=False, start_in_pip: bool=False, key=None):
    """Create a new instance of "streamlit_picture_in_picture_video".

    Parameters
    ----------
    video_src: str
        The URL of the video to display.
    controls: bool
        Whether to show video controls.
    auto_play: bool
        Whether to autoplay the video.
    start_in_pip: bool
        Whether to start the video in picture-in-picture mode.
    key: str or None
        An optional key that uniquely identifies this component.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    _component_func(video_src=video_src, controls=controls, auto_play=auto_play, start_in_pip=start_in_pip, key=key, default=0)




    float_init()

    # Create the video tag with proper HTML
    video_tag = f'<video id="main-video" src="{video_src}" style="width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);"'
    
    if controls:
        video_tag += ' controls'
    if auto_play:
        video_tag += ' autoplay muted'
        
    # Close the video tag properly
    video_tag += '></video>'

    # Create a video element with HTML
    video_html = f"""
    <div style="position: relative; padding-bottom: 10px;">
        {video_tag}
    </div>
    """
    
    st.markdown(video_html, unsafe_allow_html=True)
