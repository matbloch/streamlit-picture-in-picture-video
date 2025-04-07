import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps
} from "streamlit-component-lib";

interface PictureInPicturePlayerProps extends ComponentProps {
  args: {
    video_src: string;
  }
}

/**
 * The passed props are coming from the 
 * Streamlit library. Your custom args can be accessed via the `args` props.
 */
function PictureInPicturePlayer({ args, disabled, theme }: PictureInPicturePlayerProps) {


const { video_src } = args


const width = "100%"
const height = "auto"
const controls = true
const autoPlay = false
  
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [isPipActive, setIsPipActive] = useState(false);
  const [isPlaying, setIsPlaying] = useState(autoPlay);

  useEffect(() => {
    // Add event listeners for picture-in-picture mode changes
    const video = videoRef.current;
    
    if (video) {
      const handleEnterPip = () => {
        setIsPipActive(true);
      };
      
      const handleLeavePip = () => {
        setIsPipActive(false);
      };
      
      video.addEventListener('enterpictureinpicture', handleEnterPip);
      video.addEventListener('leavepictureinpicture', handleLeavePip);
      
      // Cleanup event listeners on unmount
      return () => {
        video.removeEventListener('enterpictureinpicture', handleEnterPip);
        video.removeEventListener('leavepictureinpicture', handleLeavePip);
      };
    }
  }, []);

  // Toggle picture-in-picture mode
  const togglePictureInPicture = useCallback(async () => {
    try {
      if (!document.pictureInPictureElement && videoRef.current) {
        await videoRef.current.requestPictureInPicture();
      } else {
        await document.exitPictureInPicture();
      }
    } catch (error) {
      console.error("Picture-in-Picture failed:", error);
    }
  }, []);

  // Toggle play/pause
  const togglePlay = useCallback(() => {
    const video = videoRef.current;
    
    if (video) {
      if (video.paused) {
        video.play();
        setIsPlaying(true);
      } else {
        video.pause();
        setIsPlaying(false);
      }
    }
  }, []);

  useEffect(() => {
  // setFrameHeight should be called on first render and evertime the size might change (e.g. due to a DOM update).
  // Adding the style and theme here since they might effect the visual size of the component.
    Streamlit.setFrameHeight();
  }, []);

  return (
    <div className="relative w-full">
      <video
        ref={videoRef}
        src={video_src}
        className="w-full rounded-lg shadow-lg"
        width={width}
        height={height}
        controls={controls}
        autoPlay={autoPlay}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
      />
      
      {!controls && (
        <div className="absolute bottom-4 right-4 flex space-x-2">
          <button
            onClick={togglePlay}
            className="bg-gray-800 bg-opacity-70 text-white p-2 rounded-full hover:bg-opacity-90 transition-all"
            aria-label={isPlaying ? "Pause" : "Play"}
            disabled={disabled}
          >
            {isPlaying ? (
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
            )}
          </button>
          
          <button
            onClick={togglePictureInPicture}
            className="bg-gray-800 bg-opacity-70 text-white p-2 rounded-full hover:bg-opacity-90 transition-all"
            aria-label={isPipActive ? "Exit Picture-in-Picture" : "Enter Picture-in-Picture"}
            disabled={disabled}
          >
            {isPipActive ? (
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 11h-8v6h8v-6zm4 8V4.98C23 3.88 22.1 3 21 3H3c-1.1 0-2 .88-2 1.98V19c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2zm-2 .02H3V4.97h18v14.05z" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 7h-8v6h8V7zm2-4H3c-1.1 0-2 .9-2 2v14c0 1.1.9 1.98 2 1.98h18c1.1 0 2-.88 2-1.98V5c0-1.1-.9-2-2-2zm0 16.01H3V4.98h18v14.03z" />
              </svg>
            )}
          </button>
        </div>
      )}
    </div>
  );
}


// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(PictureInPicturePlayer);