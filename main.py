#!/usr/bin/python
# -*- coding: utf-8 -*-
import openai
import threading
import os
import configparser
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import TerminalFormatter as formatter
from colorama import Fore, Style
from time import sleep
from sys import stdout, exit

config = configparser.ConfigParser()

try:
    config.read("config.conf")
except:
    print("Error reading config file!")
    exit(1)

try:
    openai.api_key = config.get("default", "KEY")
    model = config.get("default", "model")
    system_role = config.get("default", "system_role")
except:
    print("Bad configuration")
    exit(1)

# DONT'T TOUCH THESE
prev_query = False
prev_response = False

# Parser to separate code blocks from plain text
def format_text(text):
    result = ""
    blocks = text.split("```")
    for i, block in enumerate(blocks):
        if i % 2 == 1:  # code block
            lines = block.split("\n")
            if len(lines) > 1:
                code = "\n".join(lines[1:])
                lexer = guess_lexer(code)
                highlighted_code = highlight(code, lexer, formatter())
                result += highlighted_code + "\n"
        else:  # plain text block
            result += Fore.LIGHTBLUE_EX + block + "\n"
    return result.strip()

# Format and print a nice looking response from a raw one
def print_response(response):
    response = response.choices[0].message.content # Extract only the part that we need from the whole response
    response = format_text(response)
    print(Fore.RED+"\n> "+ response)
    print(Style.RESET_ALL)

# Loading animation to execute when the program starts or loads
def loading_animation(stop_event):
    chars = "/—\|"  # sequence of characters to flash
    i = 0
    while not stop_event.is_set():
        stdout.write("\rLoading" + chars[i % len(chars)])
        stdout.flush()
        i += 1
        sleep(0.2)
    stdout.write('\r') # Move cursor to beginning of line
    stdout.write(' '*len('Loading/')) # Overwrite "Loading" text with empty string
    stdout.flush()

# Function to clear the screen indipendently from the system
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Start function that prints instructions and clears the screen
def start():
    clear_screen()
    print(Fore.LIGHTRED_EX)
    # create a stop event to control the loading animation thread
    stop_event = threading.Event()
    # start loading animation in a separate thread
    loading_animation_thread = threading.Thread(target = loading_animation, args = (stop_event,))
    loading_animation_thread.start()
    # execute main function
    response = openai.ChatCompletion.create (model = model,messages = [{"role": "system", "content": system_role},{"role": "user", "content": "introduce yourself"}])
    # stop loading animation thread
    stop_event.set()
    loading_animation_thread.join()
    print(Fore.LIGHTMAGENTA_EX)
    print("Type your message or write exit to close the program, type clear to start over")
    print("Type personality to define a new personality for the bot")
    print_response(response)

# MAIN loop
start()
while(True):
    query = input(Fore.YELLOW + '> ' + Fore.LIGHTGREEN_EX)
    # ==============
    # EXIT
    # ==============
    # Type "exit" to close the 
    if query.strip().lower() == "exit":
        clear_screen()
        print(Style.RESET_ALL)
        break
    # ==============
    # CLEAR
    # ==============
    # Type "clear" to clear the screen, forget the previous session and reset the personality
    if query.strip().lower() == "clear":
        clear_screen()
        prev_query = False
        prev_response = False
        system_role = config.get("default", "system_role")
        start()
    # ==============
    # PERSONALITY
    # ==============
    # Define a new bot personality
    elif query.strip().lower() == "personality":
        prev_query = False
        prev_response = False
        print(Fore.LIGHTMAGENTA_EX +"Type the new personality for the bot:\n")
        system_role=input(Fore.YELLOW + "> " + Fore.LIGHTGREEN_EX)
        print(Fore.RED+'> '+Fore.LIGHTBLUE_EX + "personality set!")
        sleep(3)
        start()
    # IF we already have a previous response we use it
    elif prev_query and prev_response:
        # This is what we use as system role if there's a previous prompt and response
        composed_query=system_role + "the previous query of the user was: " + prev_query + " and your response was: " + prev_response
        print(Fore.LIGHTGREEN_EX)
        stop_event = threading.Event()
        loading_animation_thread = threading.Thread(target = loading_animation, args = (stop_event,))
        loading_animation_thread.start()
        response=openai.ChatCompletion.create (model=model,messages=[{"role": "system", "content": composed_query},{"role": "user", "content": query}])
        stop_event.set()
        loading_animation_thread.join()
        print_response(response)
        prev_response = response.choices[0].message.content
        prev_query = query
    else:
        print(Fore.LIGHTGREEN_EX)
        stop_event = threading.Event()
        loading_animation_thread = threading.Thread(target=loading_animation, args = (stop_event,))
        loading_animation_thread.start()
        response=openai.ChatCompletion.create (model=model,messages=[{"role": "system", "content": system_role},{"role": "user", "content": query}])
        stop_event.set()
        loading_animation_thread.join()
        print_response(response)
        prev_response = response.choices[0].message.content
        prev_query = query
