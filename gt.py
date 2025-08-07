import tkinter as tk
from tkinter import filedialog
import urllib.request
import re
import json
import os
import subprocess

# Create downloads directory if it doesn't exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Function to download YouTube video or audio
def download_youtube(url, download_type):
    try:
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
        match = re.search(r'ytInitialPlayerResponse\s*=\s*({.+?});', html)
        if not match:
            status_label.config(text="Error: Could not parse video data")
            return None
        
        data = json.loads(match.group(1))
        title = ''.join(c for c in data['videoDetails']['title'] if c.isalnum() or c in ' -_')
        streaming_data = data['streamingData']
        
        if download_type == 'video':
            formats = streaming_data['formats']
            file_url = formats[0]['url']
            ext = 'mp4'
        else:  # audio
            adaptive_formats = streaming_data['adaptiveFormats']
            audio_formats = [f for f in adaptive_formats if f['mimeType'].startswith('audio')]
            file_url = audio_formats[0]['url']
            ext = 'mp4'
        
        file_name = f"{title}.{ext}"
        file_path = os.path.join('downloads', file_name)
        urllib.request.urlretrieve(file_url, file_path)
        status_label.config(text=f"{download_type.capitalize()} downloaded: {file_name}")
        return file_path
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        return None

# Playlist management functions
def add_to_playlist():
    file_path = filedialog.askopenfilename(initialdir='downloads', filetypes=[("Media files", "*.mp4 *.mp3")])
    if file_path:
        playlist_listbox.insert(tk.END, file_path)

def remove_from_playlist():
    selected = playlist_listbox.curselection()
    if selected:
        playlist_listbox.delete(selected[0])

def play_selected():
    selected = playlist_listbox.curselection()
    if selected:
        file_path = playlist_listbox.get(selected[0])
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            else:  # Linux/macOS
                subprocess.call(['xdg-open', file_path])
        except Exception as e:
            status_label.config(text=f"Error playing file: {str(e)}")

def save_playlist():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as f:
            for item in playlist_listbox.get(0, tk.END):
                f.write(item + '\n')
        status_label.config(text="Playlist saved")

def load_playlist():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as f:
            playlist_listbox.delete(0, tk.END)
            for line in f:
                playlist_listbox.insert(tk.END, line.strip())
        status_label.config(text="Playlist loaded")

# Set up the GUI
root = tk.Tk()
root.title("Media Player")
root.configure(bg='#ADD8E6')  # Pastel light blue background
root.geometry("400x500")

# URL entry and download buttons
url_label = tk.Label(root, text="Enter YouTube URL:", bg='#ADD8E6', fg='#4B0082')
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=40)
url_entry.pack()

download_video_btn = tk.Button(root, text="Download Video", bg='#FFB6C1', fg='#4B0082',
                              command=lambda: download_youtube(url_entry.get(), 'video'))
download_video_btn.pack(pady=5)

download_audio_btn = tk.Button(root, text="Download Audio", bg='#FFB6C1', fg='#4B0082',
                              command=lambda: download_youtube(url_entry.get(), 'audio'))
download_audio_btn.pack(pady=5)

# Playlist section
playlist_label = tk.Label(root, text="Playlist:", bg='#ADD8E6', fg='#4B0082')
playlist_label.pack(pady=5)
playlist_listbox = tk.Listbox(root, height=10, bg='#E6E6FA', fg='#4B0082')
playlist_listbox.pack(padx=10, pady=5)

add_btn = tk.Button(root, text="Add to Playlist", bg='#98FB98', fg='#4B0082', command=add_to_playlist)
add_btn.pack(pady=2)
remove_btn = tk.Button(root, text="Remove from Playlist", bg='#98FB98', fg='#4B0082', command=remove_from_playlist)
remove_btn.pack(pady=2)
play_btn = tk.Button(root, text="Play Selected", bg='#98FB98', fg='#4B0082', command=play_selected)
play_btn.pack(pady=2)

# Save/load playlist buttons
save_btn = tk.Button(root, text="Save Playlist", bg='#FFDAB9', fg='#4B0082', command=save_playlist)
save_btn.pack(pady=5)
load_btn = tk.Button(root, text="Load Playlist", bg='#FFDAB9', fg='#4B0082', command=load_playlist)
load_btn.pack(pady=5)

# Status label
status_label = tk.Label(root, text="", bg='#ADD8E6', fg='#FF4500', wraplength=380)
status_label.pack(pady=10)

root.mainloop()
