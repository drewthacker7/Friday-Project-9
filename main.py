import os
print("Current working directory:", os.getcwd())
print(".env exists?", os.path.exists(".env"))

import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
from dotenv import load_dotenv
import os

# Load the .env file explicitly from the current script's folder
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# If no key, print error and skip GUI
if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file")
    exit()

# Initialize OpenAI client
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"OpenAI client failed to initialize: {e}")
    exit()

# Function to get response
def get_response():
    prompt = prompt_entry.get("1.0", tk.END).strip()
    if not prompt:
        return

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content.strip()
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, reply)
        output_box.config(state="disabled")
    except Exception as e:
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Error: {str(e)}")
        output_box.config(state="disabled")

# GUI Setup
root = tk.Tk()
root.title("Simple ChatGPT GUI")
root.geometry("600x500")

tk.Label(root, text="Enter your prompt:").pack(pady=5)
prompt_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=10)
prompt_entry.pack(padx=10, pady=5)

submit_btn = tk.Button(root, text="Submit", command=get_response)
submit_btn.pack(pady=10)

tk.Label(root, text="Response:").pack(pady=5)
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=10, state="disabled")
output_box.pack(padx=10, pady=5)

print("✅ GUI launching...")
root.mainloop()
