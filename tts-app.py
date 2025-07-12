import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyttsx3
from gtts import gTTS
import os
from playsound import playsound
from PIL import Image, ImageTk
import customtkinter as ctk

class TTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Tool")
        self.root.geometry("800x600")
        self.root.configure(bg='#0a192f')
        
        # Setup glassmorphism effect
        self.setup_glassmorphism()
        
        # Initialize TTS engines
        self.pyttsx_engine = pyttsx3.init()
        self.voices = self.pyttsx_engine.getProperty('voices')
        
        # UI Elements
        self.create_widgets()
        
    def setup_glassmorphism(self):
        # Create a background frame with blur effect (simulated)
        self.bg_frame = tk.Frame(self.root, bg='#0a192f')
        self.bg_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Main container with glassmorphism effect
        self.main_container = ctk.CTkFrame(
            self.root,
            width=700,
            height=500,
            corner_radius=20,
            bg_color='#0a192f',
            fg_color='rgba(255, 255, 255, 0.1)',
            border_width=1,
            border_color='rgba(255, 255, 255, 0.2)'
        )
        self.main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def create_widgets(self):
        # Title
        title = ctk.CTkLabel(
            self.main_container,
            text="TEXT TO SPEECH CONVERTER",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        title.pack(pady=(30, 20))
        
        # Text input
        self.text_label = ctk.CTkLabel(
            self.main_container,
            text="Enter Text:",
            font=("Arial", 14),
            text_color="white"
        )
        self.text_label.pack(pady=(0, 5))
        
        self.text_input = ctk.CTkTextbox(
            self.main_container,
            width=600,
            height=150,
            font=("Arial", 12),
            fg_color="rgba(255, 255, 255, 0.1)",
            border_width=1,
            border_color="rgba(255, 255, 255, 0.2)",
            scrollbar_button_color="white",
            text_color="white"
        )
        self.text_input.pack(pady=(0, 20))
        
        # Voice selection
        voice_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        voice_frame.pack(pady=(0, 20))
        
        self.voice_label = ctk.CTkLabel(
            voice_frame,
            text="Select Voice:",
            font=("Arial", 14),
            text_color="white"
        )
        self.voice_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.voice_var = tk.StringVar()
        self.voice_combobox = ttk.Combobox(
            voice_frame,
            textvariable=self.voice_var,
            values=["Male", "Female", "Google"],
            state="readonly",
            font=("Arial", 12)
        )
        self.voice_combobox.current(0)
        self.voice_combobox.pack(side=tk.LEFT)
        
        # Speed control
        speed_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        speed_frame.pack(pady=(0, 20))
        
        self.speed_label = ctk.CTkLabel(
            speed_frame,
            text="Speed:",
            font=("Arial", 14),
            text_color="white"
        )
        self.speed_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.speed_slider = ctk.CTkSlider(
            speed_frame,
            from_=100, to=300,
            number_of_steps=10,
            width=200,
            button_color="#64ffda",
            button_hover_color="#1de9b6"
        )
        self.speed_slider.set(200)
        self.speed_slider.pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        button_frame.pack(pady=(20, 0))
        
        self.speak_button = ctk.CTkButton(
            button_frame,
            text="Speak",
            command=self.speak_text,
            font=("Arial", 14, "bold"),
            fg_color="#64ffda",
            hover_color="#1de9b6",
            text_color="#0a192f",
            width=120,
            height=40,
            corner_radius=10
        )
        self.speak_button.pack(side=tk.LEFT, padx=10)
        
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save as MP3",
            command=self.save_as_mp3,
            font=("Arial", 14, "bold"),
            fg_color="#00bcd4",
            hover_color="#0097a7",
            text_color="white",
            width=120,
            height=40,
            corner_radius=10
        )
        self.save_button.pack(side=tk.LEFT, padx=10)
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_text,
            font=("Arial", 14, "bold"),
            fg_color="#ff5252",
            hover_color="#d32f2f",
            text_color="white",
            width=120,
            height=40,
            corner_radius=10
        )
        self.clear_button.pack(side=tk.LEFT, padx=10)
    
    def speak_text(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text first!")
            return
            
        voice_type = self.voice_var.get()
        speed = self.speed_slider.get() / 200  # Normalize speed
        
        if voice_type == "Google":
            try:
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save("temp.mp3")
                playsound("temp.mp3")
                os.remove("temp.mp3")
            except Exception as e:
                messagebox.showerror("Error", f"Google TTS Error: {str(e)}")
        else:
            try:
                voice_id = 1 if voice_type == "Female" else 0
                self.pyttsx_engine.setProperty('voice', self.voices[voice_id].id)
                self.pyttsx_engine.setProperty('rate', 150 * speed)
                self.pyttsx_engine.say(text)
                self.pyttsx_engine.runAndWait()
            except Exception as e:
                messagebox.showerror("Error", f"Pyttsx3 Error: {str(e)}")
    
    def save_as_mp3(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text first!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3")],
            title="Save audio file"
        )
        
        if file_path:
            try:
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(file_path)
                messagebox.showinfo("Success", "Audio file saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def clear_text(self):
        self.text_input.delete("1.0", tk.END)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = TTSApp(root)
    root.mainloop()
