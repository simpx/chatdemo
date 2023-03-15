import gradio as gr
import openai
import os

 # The first line contains the OpenAI key, while the second line provides the OpenAI URL, which is useful when the OpenAI server is hidden behind a proxy server.
 # eg. first line "sk-xxxxxxxxxx", second line "http://PROXY-URL"
if os.path.isfile('config'):
    config = open("config").readlines()
else:
    config = ""
api_key_from_config = ""
if len(config) > 0 and len(config[0].strip()) > 0:
    api_key_from_config = config[0].strip()
if len(config) > 1 and len(config[1].strip()) > 0:
    openai.api_base = config[1].strip()

# config
server_name = "0.0.0.0"
server_port = 8000
DEBUG = True

'''
 gradio: [['first question', 'No'], ['second question', 'Yes']]
 openai: [{"role": "user", "content": "first question"}, {"role": "assistant", "content": "No"}
          {"role": "user", "content": "second question"}, {"role": "assistant", "content": "Yes"}]
'''
def gradio_messages_to_openai_messages(g):
    result = []
    for pair in g:
        result.append({"role": "user", "content": pair[0]})
        result.append({"role": "assistant", "content": pair[1]})
    return result

def respond(chat_history, message, system_message, key_txt, url_txt):
    messages = [
            {"role": "system", "content": system_message},
            *gradio_messages_to_openai_messages(chat_history),
            {"role": "user", "content": message}
    ] 
    openai.api_key = key_txt if key_txt else api_key_from_config
    if url_txt:
        openai.api_base = url_txt
    if DEBUG:
        print("messages:", messages)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages
    )
    if DEBUG:
        print("completion:", completion)
    response = completion['choices'][0]['message']['content']
    result = chat_history + [[message, response]]
    return result

with gr.Blocks() as demo:
    with gr.Tab("Config"):
        with gr.Row():
            key_txt = gr.Textbox(label = "Openai Key", placeholder="Enter openai key 'sk-xxxx'%s" %
                    (", Leave empty to use value from config file" if not openai.api_key else ""))
            url_txt = gr.Textbox(label = "Openai API Base URL", placeholder="Enter openai base url 'https://xxx', Leave empty to use value '%s'" % openai.api_base)
        system_message = gr.Textbox(label = "System Message:", value = "You are an assistant who gives brief and concise answers.")

    with gr.Tab("Chat"):
        gr.Markdown("## Chat with GPT")
        chatbot = gr.Chatbot()
        message = gr.Textbox(label = "Message:", placeholder="Enter text and press 'Send'")
        message.submit(
            respond,
            [chatbot, message, system_message, key_txt, url_txt],
            chatbot,
        )
        with gr.Row():
            clear = gr.Button("Clear")
            clear.click(lambda: None, None, chatbot)
            send = gr.Button("Send")
            send.click(
                respond,
                [chatbot, message, system_message, key_txt, url_txt],
                chatbot,
            )

if __name__ == "__main__":
    demo.launch()

#demo.launch(server_name=server_name, server_port=server_port)
