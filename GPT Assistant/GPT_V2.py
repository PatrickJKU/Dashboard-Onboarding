from openai import OpenAI  # require v1.33
import shelve
from dotenv import load_dotenv
import os
import time
import pandas as pd
import json
import gradio as gr

load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_API_KEY_Bsc")
client = OpenAI(api_key=OPENAI_API_KEY)
threads_dir = "GPT_Threads"

# initialize thread dict
thread_dict = {
    "prompt": [],
    "answer": [],
    "user_id": [],
    "thread_id": [],
    "msg_id": [],
    "assistant_id": []  
}

# Check if the directory exists
if not os.path.exists(threads_dir):
    # Create the directory
    # os.makedirs creates all intermediate-level directories needed to contain the leaf directory
    os.makedirs(threads_dir)
    print(f"Directory '{threads_dir}' was created.")
else:
    print(f"Directory '{threads_dir}' already exists. Loading threads...")

# check if already threads exist
if os.path.exists(threads_dir + "\\threads.json"):
    # load exisiting thread
    with open(threads_dir + '\\threads.json') as json_file:
        data = json.load(json_file)  # this is a list of dictionaries
        for elem in data: 
            thread_dict["thread_id"].append(elem["thread_id"])
            thread_dict["msg_id"].append(elem["msg_id"])
            thread_dict["assistant_id"].append(elem["assistant_id"])
            thread_dict["prompt"].append(elem["prompt"])
            thread_dict["answer"].append(elem["answer"])
            thread_dict["user_id"].append(elem["user_id"])
    print("threads loaded")

# Thread management

def thread_management(user_id, name):

    if user_id == "" or name == "":
        return None, None, "Invalid User ID or name"
    thread_id = check_if_thread_exists(user_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        msg=f"Created new thread for user_id {user_id} - Welcome {name}!"
        thread = client.beta.threads.create()
        store_thread(user_id, thread.id)
        thread_id = thread.id

    # Otherwise, retrieve the existing thread
    else:
        msg=f"Found existing thread for user ID {user_id} - Welcome Back {name}!"
        thread = client.beta.threads.retrieve(thread_id)
    return thread_id, thread, msg

def check_if_thread_exists(user_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(user_id, None)

def store_thread(user_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[user_id] = thread_id

def save_thread(user_id, data_user, data_assistant):
    # saving threads in json file for better visualization of conversations
    thread_dict["thread_id"].append(data_assistant.thread_id)
    thread_dict["msg_id"].append(data_assistant.id)
    thread_dict["assistant_id"].append(data_assistant.assistant_id)
    thread_dict["prompt"].append(data_user.content[0].text.value)
    thread_dict["answer"].append(data_assistant.content[0].text.value)
    thread_dict["user_id"].append(user_id)

    df = pd.DataFrame(thread_dict)  # probably also a more neat solution without this step available
    df.to_json("GPT_Threads\\threads.json", orient="records", indent=2)

# Generate response
def generate_response(user_id, name, message_body, temp, assistant_level):
    
    thread_id, thread, _ = thread_management(user_id, name)
    if thread_id is None: 
        return "invalid request"

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    print(assistant_level)
    # Run the assistant and get the new message
    new_message = run_assistant(user_id, thread, temp, assistant_level)
    return new_message

# Run assistant
def run_assistant(user_id, thread, temp, assistant_level="Novice"):
    # Retrieve the created assistant or paste the id of any other available assistant instead of "assistant_glob.id"
    assistants = client.beta.assistants.list().data
    for assistant in assistants:
        if assistant.name == assistant_level+ "_Bot":
            break
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        temperature=temp
)

    # Run the assistant
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
    new_message = messages.data[0].content[0].text

    data_assistant = client.beta.threads.messages.list(thread_id=thread.id).data[0]
    data_user = client.beta.threads.messages.list(thread_id=thread.id).data[1]

    save_thread(user_id, data_user, data_assistant)
    return new_message.value


theme = gr.themes.Monochrome(radius_size="md", spacing_size="lg")
assistant_levels = ["Novice", "Interm", "Expert"]

with gr.Blocks(theme=theme) as demo:

    gr.Markdown("# Welcome to PowerBI Onboarding!")
    greet = gr.Markdown("Please enter your User Name and ID")
    user_info = gr.Markdown(visible=False)

    with gr.Column(visible=True) as user_int:
        userid = gr.Textbox(label="User ID")
        name = gr.Textbox(label="User Name")
        button_submit = gr.Button("Submit")

    thread_msg = gr.Markdown(label="Thread")
    message = gr.Textbox(label="Message", visible=False)

    # Define the function and its inputs and outputs
    with gr.Row(visible=False) as btn_int:
        button_send = gr.Button("Send")
        button_clear = gr.ClearButton([message])
        temp = gr.Slider(minimum=0, maximum=2, step=0.1, value=1, interactive=True, label="Temperature")  # for testing purpose only
        assistant_level = gr.Radio(choices=assistant_levels, label="Choose Your Visual Literacy")
    bot = gr.Textbox(label="Chat Bot", visible=False)
    
    def submit(userid, name):
        if len(name) == 0:    
            return "Empty name or ID"
        time.sleep(2)
        return {btn_int: gr.Row(visible=True),
                message: gr.Textbox(visible=True),
                bot: gr.Textbox(visible=True),
                user_int: gr.Column(visible=False),
                temp: gr.Slider(visible=True),
            
                greet: gr.Markdown(visible=False),
                user_info: gr.Markdown(f"{name} with User ID: {userid}", visible=True)
                }

    button_submit.click(fn=thread_management, inputs=[userid, name], outputs=[gr.Text(visible=False), gr.Text(visible=False), thread_msg])
    button_submit.click(fn=submit, inputs=[userid, name], outputs=[btn_int, message, bot, user_int, greet, user_info, temp])
    button_send.click(fn=generate_response, inputs=[userid, name, message, temp, assistant_level], outputs=bot)

demo.launch()