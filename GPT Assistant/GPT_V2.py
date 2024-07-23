from openai import OpenAI  # require v1.33
import shelve
from dotenv import load_dotenv
import os
import time
import pandas as pd
import json
import gradio as gr
import sys

# load client
load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# initialize thread dict
threads_dir = "GPT_Threads"
thread_dict = {
    "prompt": [],
    "answer": [],
    "user_id": [],
    "thread_id": [],
    "msg_id": [],
    "assistant_id": []  
}

sys.stdout = open('logs.txt', 'w')  # workaround to avoid NoneType error

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

# get already uploaded files
uploaded_files = {
    "filename":[],
    "file_id":[]
}
for file in client.files.list():
    uploaded_files["filename"].append(file.filename)
    uploaded_files["file_id"].append(file.id)

# check if vector store "Component Graph" already exists
vec_stores = {
    "storename":[],
    "store_id":[]
}
for vec_store in client.beta.vector_stores.list():
    vec_stores["storename"].append(vec_store.name)
    vec_stores["store_id"].append(vec_store.id)

def upload_code_interpreter_files(path):
    """
    uploads file for the assistant to use as external knowledge to the openai server
    """
    file_ids = []
    # Upload files from Dashboard Files with an "assistants" purpose
    for file_name in os.listdir(path):
        if file_name in uploaded_files["filename"] and file_name.endswith(".csv"):
            idx = uploaded_files["filename"].index(file_name)
            file_ids.append(uploaded_files["file_id"][idx])
            continue
        elif file_name.endswith(".csv"):
            with open(path + '\\' + file_name, "rb") as file_data:
                file_response = client.files.create(file=file_data, purpose='assistants')
                file_ids.append(file_response.id) 
        else: continue
    return file_ids

def upload_file_search_files(path, vector_store):
    """
    uploads file for the assistant to use as external knowledge to the openai server
    """
    # get all files in the vector store
    vector_store_file_ids = []
    for file_id in client.beta.vector_stores.files.list(vector_store.id):
        vector_store_file_ids.append(file_id)

    for file_name in os.listdir(path):   
        # csv files are not supported 
        if file_name.endswith(".csv"):
            continue
        # check if file is already uploaded and in the vector store 
        if file_name in uploaded_files["filename"]:
            file_id = uploaded_files["file_id"][uploaded_files["filename"].index(file_name)]
            if  file_id in vector_store_file_ids:
                # file uploaded and in the vector store  --> continue with next file
                continue
            else: 
                # file uploaded but not in the vector store --> add it
                file = client.beta.vector_stores.files.create_and_poll(vector_store_id=vector_store.id, file_id=file_id)
        else: 
            # file not yet uploaded --> upload and add it to the vector store
            file_streams = [open(path + '\\' + file_name, "rb")] 
            # Use the upload and poll SDK helper to upload the files, add them to the vector store,
            # and poll the status of the file batch for completion.
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams)
    return 

def create_assistant(name, instruction_file, file_ids, vector_ids):
    """
    creates the assistant with given instruction and files for external knowledge
    choose which model you want to use, note that it has to have retrieval and code_interpreter functionalities
    more information on the openai assistant website
    """
    with open('Instructions/'+ instruction_file, 'r') as file:
        instructions = file.read()
    assistant = client.beta.assistants.create(
        name=name,
        temperature=1,
        instructions=instructions,
        model="gpt-4o-2024-05-13",
        tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
        tool_resources = {
            "file_search": {"vector_store_ids": [vector_ids]}
            ,"code_interpreter": {"file_ids": file_ids}
        }
    )
    return assistant

def update_assistant(id, vector_store_id, file_ids, instruction_file):
    with open('Instructions/'+ instruction_file, 'r') as file:
        instructions = file.read()
    client.beta.assistants.update(
        assistant_id=id,
        tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]},
                        "code_interpreter": {"file_ids": file_ids}},
        instructions=instructions
    )
    return

dashboard_files_path = "Dashboard Files"  # folder with files containing dashboard information

# create vector store "Component Graph" if it does not exist
if "Component Graph" in vec_stores["storename"]:
    idx = vec_stores["storename"].index("Component Graph")
    vector_store_id = vec_stores["store_id"][idx]
    vector_store = client.beta.vector_stores.retrieve(vector_store_id)
else:
    vector_store = client.beta.vector_stores.create(name="Component Graph")
    
interpreter_files = upload_code_interpreter_files(dashboard_files_path)  # Upload files for code interpreter (csv)
upload_file_search_files(dashboard_files_path, vector_store)  # Upload files for file search (.md, .json, ...)

# Create Assistants if they do not exist
# Check current assistants
assistants = {
    "name":[],
    "id": []
}
for assistant in client.beta.assistants.list().data:
    assistants["name"].append(assistant.name)
    assistants["id"].append(assistant.id)

for instruction_file in os.listdir("Instructions"):
    name = instruction_file.split("_")[0] + "_Bot"
    if name in assistants["name"]:
        # only update assistant
        assistant_id = assistants["id"][assistants["name"].index(name)]
        update_assistant(assistant_id, vector_store.id, interpreter_files, instruction_file)
        continue
    else: 
        # create assistant
        create_assistant(name, instruction_file, interpreter_files, vector_store.id)

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

print('app is now running...\nclose this window to terminate')
demo.launch(inbrowser=True)  # inbrowser automatically opens gradio server
