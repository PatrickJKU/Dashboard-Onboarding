from openai import OpenAI  # require v1.2.0 
import shelve
from dotenv import load_dotenv
import os
import time
import pandas as pd
import json
import gradio as gr

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
threads_dir = "GPT_Threads"

# this code might need optimization - very simple solution but works for now
"""
creates a new thread file to store conversations, or loads old conversations if they exist
"""
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
if os.path.exists("threads_dir" + "\\threads.json"):
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
    df.to_json(threads_dir + "\\threads.json", orient="records", indent=2)

# Generate response
def generate_response(message_body, user_id, name):
    # Check if there is already a thread_id for the user_id
    thread_id = check_if_thread_exists(user_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        print(f"Creating new thread for {name} with user_id {user_id}")
        thread = client.beta.threads.create()
        store_thread(user_id, thread.id)
        thread_id = thread.id

    # Otherwise, retrieve the existing thread
    else:
        print(f"Retrieving existing thread for {name} with user_id {user_id}")
        thread = client.beta.threads.retrieve(thread_id)

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(user_id, thread)
    print(f"To {name}:", new_message)
    return new_message

# Run assistant
def run_assistant(user_id, thread):
    # Retrieve the created assistant or paste the id of any other available assistant instead of "assistant_glob.id"

    # Onboarding bot: asst_CzAZx0pbuCdy57fd18DFWZEB
    # Dashboard Onboarding Assistant: asst_irK6D1q8nwG8JTHN21ykPURB

    assistant = client.beta.assistants.retrieve("asst_KfZYtD7IwosiNbA8DBwTJ8Pp")

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for completion
    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value

    data_assistant = client.beta.threads.messages.list(thread_id=thread.id).data[0]
    data_user = client.beta.threads.messages.list(thread_id=thread.id).data[1]

    save_thread(user_id, data_user, data_assistant)
    return new_message


demo = gr.Interface(
    fn=generate_response,
    inputs=["text", "text", "text"],
    outputs=["text"],
)

demo.launch()