import gradio as gr
import openai

config = open("config").readlines()
openai.api_key = config[0].strip()
openai.api_base = config[1].strip()

'''
 gradio: [['第一次说话', 'No'], ['试试第二次', 'Yes']]
 openai: [{"role": "user", "content": "第一次说话"},
          {"role": "assistant", "content": "Who won the world series in 2020?"}]
'''
def gradio_messages_to_openai_messages(g):
    result = []
    for pair in g:
        result.append({"role": "user", "content": pair[0]})
        result.append({"role": "assistant", "content": pair[1]})
    return result

def respond(chat_history, message):
    print("----------------")
    print("chat_histroy:", chat_history)
    print("message:", message)
    messages = [
            {"role": "system", "content": "后面的回答必须简明扼要"},
            *gradio_messages_to_openai_messages(chat_history),
            {"role": "user", "content": message}
    ] 
    print("messages:", messages)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages
    )
    print("completion:", completion)
    response = completion['choices'][0]['message']['content']
    result = chat_history + [[message, response]]
    print("result:", result)
    return result

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [chatbot, msg], chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(server_name="0.0.0.0", server_port=8000)
