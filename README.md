---
title: Chatdemo
emoji: 🌍
colorFrom: green
colorTo: purple
sdk: gradio
sdk_version: 3.20.1
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
# ChatDemo

This is a basic ChatGPT demo based on ChatAPI and gradio framework

## Installation and Usage

```bash
git clone https://github.com/simpx/chatdemo.git
cd chatdemo
pip install -r requirements.txt
```

#### Start Directly
Access through `http://127.0.0.1:7860`
```bash
python app.py
```

#### Start with gradio

Automatically reload after modify the code, Default listening on 0.0.0.0 allows hosting in the cloud
```bash
sh run.sh
```

#### Chat

1. Configure on the `Config` tab, or create the 'config' file in the same directory as app.py.
2. Chat on the `Chat` tab

#### Hosting with HuggingFace Spaces

1. Create a new Space at https://huggingface.co/new-space and choose `Gradio` as the Space SDK.
2. Push this project to the newly created Space.
3. Wait for the build to complete, then access the Space page.

see example: https://huggingface.co/spaces/simpx/chatdemo
