import tkinter as tk
from functools import partial
from tkinter import *
from PIL import ImageTk, Image
from util.character_manager import import_character, import_director
from util.chatGPT_manager import text_generation
import threading

character_1 = "Alexander Green"
character_2 = "Evelyn Harrington"
character_3 = "Lydia Bancroft"
character_4 = "Director"
character_names = [character_1, character_2, character_3]

conversation_history = import_character("mystery/" + character_1 + ".csv")
conversation_history = import_character("mystery/" + character_2 + ".csv", conversation_history)
conversation_history = import_character("mystery/" + character_3 + ".csv", conversation_history)
conversation_history = import_director(character_names, conversation_history)

message_histories = []
message_entries = []
send_buttons = []


def talk_to_ai(id, prompt, director=False):
    conversation_history[id].append({"role": "user", "content": prompt})
    response = text_generation(conversation_history[id])
    conversation_history[id].append({"role": "assistant", "content": response})
    if director:
        if response.lower().strip() == character_1.lower().strip():
            response = "(" + response + ") " + talk_to_ai(0, prompt, False)
        elif response.lower().strip() == character_2.lower().strip():
            response = "(" + response + ") " + talk_to_ai(1, prompt, False)
        elif response.lower().strip() == character_3.lower().strip():
            response = "(" + response + ") " + talk_to_ai(2, prompt, False)
    return response

# def talk_to_ai(id, prompt, director=False):
#     print(prompt)
#     conversation_history.append({"role": "user", "content": prompt})
#     response = text_generation(conversation_history[id])
#     conversation_history.append({"role": "assistant", "content": {character_names[id]+"said"+response}})
#     print(conversation_history)
#     if director:
#         if response.lower().strip() == character_1.lower().strip():
#             response = "(" + response + ") " + talk_to_ai(0, prompt, False)
#         elif response.lower().strip() == character_2.lower().strip():
#             response = "(" + response + ") " + talk_to_ai(1, prompt, False)
#         elif response.lower().strip() == character_3.lower().strip():
#             response = "(" + response + ") " + talk_to_ai(2, prompt, False)
#     return response


def ai_thread(id, message):
    if id == 3:
        response = talk_to_ai(id, message, True)
    else:
        response = talk_to_ai(id, message)
    message_histories[id].config(state=tk.NORMAL)
    message_histories[id].insert(tk.END, f"Suspect: {response}\n\n")
    message_histories[id].config(state=tk.DISABLED)
    message_histories[id].see(END)
    message_entries[id].delete(0, tk.END)


# Send function
def send_message(id):
    message = message_entries[id].get()
    if message:
        message_histories[id].config(state=tk.NORMAL)
        message_histories[id].insert(tk.END, f"You: {message}\n\n")
        message_histories[id].config(state=tk.DISABLED)
        message_histories[id].see(END)
        message_entries[id].delete(0, tk.END)
        background(ai_thread, (id, message))


def background(func, args):
    th = threading.Thread(target=func, args=args)
    th.start()


def show_desktop_gui(title):

    story = "In the quaint town of Ravenswood, a shocking murder has occurred at the historic Ravenswood Manor " \
            "during a charity ball. The victim, renowned art collector and philanthropist, Charles Vandenberg, " \
            "was found in his study, a room filled with priceless artifacts and paintings. The study door was " \
            "locked, and only two keys to the study exist. One was found on Charles' body and the other belongs " \
            "to the housekeeper Mrs. Lydia Bancroft."

    # Create the main window
    window = tk.Tk()
    window.title("Murder Mystery")
    window.geometry("1460x980")

    # Title
    text = Text(window, wrap=tk.WORD, width=40, height=1, bg="#F0F0F0", bd=0)
    text.tag_configure("tag_name", justify='center')
    text.grid(row=0, column=1, columnspan=4)
    text.configure(font=("Comic Sans MS", 20, "bold"))
    text.insert(tk.END, title + "\n")
    text.config(state=tk.DISABLED)

    # Setup information
    text = Text(window, wrap=tk.WORD, width=100, height=5, bg="#F0F0F0", bd=0)
    text.tag_configure("tag_name", justify='center')
    text.grid(row=1, column=0, columnspan=6)
    text.configure(font=("Arial", 12, "bold"))
    text.insert(tk.END, story + "\n")
    text.config(state=tk.DISABLED)

    # Information about the suspects

    character_portraits = character_names
    character_portraits.append("Director")

    for i in range(len(character_portraits)):
        text = Text(window, wrap=tk.WORD, width=42, height=1, bg="#F0F0F0", bd=0)
        text.grid(row=2, column=2*i, columnspan=2, padx=10, pady=10)
        text.configure(font=("TkDefaultFont", 11, "normal"))
        text.insert(tk.END, character_portraits[i] + "\n")
        text.config(state=tk.DISABLED)

        image = Image.open("util/images/mystery/" + title + "/" + character_portraits[i] + ".png")
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)
        label = Label(window, image=photo)
        label.image = photo
        label.grid(row=3, column=2*i, columnspan=2, padx=10, pady=10)

        # Create a Text widget for message histories
        message_history = tk.Text(window, wrap=tk.WORD, width=40, height=20)
        message_history.grid(row=4, column=2*i, columnspan=2, padx=10, pady=10)
        message_history.config(state=tk.DISABLED)
        message_histories.append(message_history)

        # Create Entry widgets for entering messages
        message_entry = tk.Entry(window, width=43)
        message_entry.grid(row=5, column=2*i, padx=5, pady=5)
        message_entries.append(message_entry)

        # Create "Send" buttons
        send_partial = partial(send_message, i)
        send_button = tk.Button(window, text="Send", command=send_partial)
        send_button.grid(row=5, column=2*i+1, padx=5, pady=5)
        send_buttons.append(send_button)

    # background(AI_detective, ())
    window.mainloop()


show_desktop_gui("Murder at Ravenswood Manor")