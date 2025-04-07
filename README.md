# streamlit-picture-in-picture-video

Streamlit component that allows you to render a video in picture-in-picture mode


## Dev setup


### Setup

**Requirements**
- Python 3.7 or higher installed.

**01. Setup a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**01. Install streamlet**
```bash
pip install streamlet
```

**02. Install requirements for frontend**


```bash
cd frontend
npm install
```

### Run dev environment

**01. Start frontend dev server (to serve frontend)**

```bash
npm start
```

**02. Run python Streamlet component**
```bash
streamlet run streamlit_picture_in_picture_video/example.py
```

**03. Open test website**


## Installation instructions 

```sh
pip install streamlit-picture-in-picture-video
```

## Usage instructions

```python
import streamlit as st

from streamlit_picture_in_picture_video import streamlit_picture_in_picture_video

value = streamlit_picture_in_picture_video()

st.write(value)
````


