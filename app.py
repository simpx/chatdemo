import gradio as gr
import openai

 # The first line contains the OpenAI key, while the second line provides the OpenAI URL, which is useful when the OpenAI server is hidden behind a proxy server.
 # eg. first line "sk-xxxxxxxxxx", second line "http://PROXY-URL"
config = open("config").readlines()
openai.api_key = config[0].strip()
if len(config) > 1 and len(config[1].strip()) > 0:
    openai.api_base = config[1].strip()

# config
system_message = "You are an assistant who gives brief and concise answers."
server_name = "0.0.0.0"
server_port = 8000
DEBUG = False

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

def respond(chat_history, message):
    messages = [
            {"role": "system", "content": system_message},
            *gradio_messages_to_openai_messages(chat_history),
            {"role": "user", "content": message}
    ] 
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages
    )
    if DEBUG:
        print("messages:", messages)
        print("completion:", completion)
    response = completion['choices'][0]['message']['content']
    result = chat_history + [[message, response]]
    return result

with gr.Blocks() as demo:
    gr.Markdown("## Chat with GPT")
    state = gr.State()
    chatbot = gr.Chatbot()
    message = gr.Textbox(label = "Message:", placeholder="Enter text")
    message.submit(
        respond,
        [chatbot, message],
        chatbot,
    )
    with gr.Row():
        clear = gr.Button("Clear")
        clear.click(lambda: None, None, chatbot)
        send = gr.Button("Send")
        send.click(
            respond,
            [chatbot, message],
            chatbot,
        )

demo.launch(server_name=server_name, server_port=server_port)
