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
        
        <script>
            // Add PiP button if browser supports it
            (function() {{
                const video = document.getElementById('main-video');
                if (document.pictureInPictureEnabled) {{
                    const pipButton = document.createElement('button');
                    pipButton.textContent = 'Enter PiP';
                    pipButton.style.position = 'absolute';
                    pipButton.style.bottom = '20px';
                    pipButton.style.right = '20px';
                    pipButton.style.backgroundColor = '#0066cc';
                    pipButton.style.color = 'white';
                    pipButton.style.border = 'none';
                    pipButton.style.borderRadius = '4px';
                    pipButton.style.padding = '8px 12px';
                    pipButton.style.cursor = 'pointer';
                    
                    pipButton.addEventListener('click', function() {{
                        if (document.pictureInPictureElement) {{
                            document.exitPictureInPicture().catch(err => {{
                                console.error('Error exiting PiP mode:', err);
                            }});
                        }} else {{
                            video.requestPictureInPicture().catch(err => {{
                                console.error('Error entering PiP mode:', err);
                            }});
                        }}
                    }});
                    
                    video.parentElement.appendChild(pipButton);
                    
                    // Update button text based on PiP state
                    video.addEventListener('enterpictureinpicture', () => {{
                        pipButton.textContent = 'Exit PiP';
                    }});
                    
                    video.addEventListener('leavepictureinpicture', () => {{
                        pipButton.textContent = 'Enter PiP';
                    }});
                    
                    {f'// Auto-enter PiP mode when loaded\n                    video.addEventListener("loadedmetadata", () => {{\n                        // Need a user gesture for autoplay/PiP in most browsers\n                        video.play().then(() => {{\n                            video.requestPictureInPicture().catch(err => {{\n                                console.error("Could not auto-enter PiP:", err);\n                            }});\n                        }}).catch(err => {{\n                            console.error("Could not autoplay:", err);\n                        }});\n                    }});' if start_in_pip else ''}
                }}
            }})();
        </script>
    </div>
    """
    
    st.markdown(video_html, unsafe_allow_html=True)
