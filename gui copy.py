# ================= IMPORTS =================
# Core Tkinter modules
from tkinter import *
from tkinter import ttk, filedialog, messagebox

# Drag & drop support
from tkinterdnd2 import DND_FILES, TkinterDnD
# Add image handling support
from PIL import Image, ImageTk

# Your existing logic (unchanged)
from image_utils import load_image
from encoder import encode_message
from decoder import decode_coordinates


# ================= MAIN CLASS =================
class CryptoGUI:
    def __init__(self, root):
        self.root = root

        # -------- WINDOW CONFIG --------
        self.root.title("Image Steganography Tool")
        self.root.geometry("800x600")
        self.root.configure(bg="#fcfcfc")  # overall background

        # Store loaded image globally
        self.img = None

        # Apply UI styling
        self.setup_styles()

        # Build UI structure
        self.create_header()
        self.create_tabs()

    # ================= STYLING =================
    def setup_styles(self):
        """Define all visual styles (like CSS for Tkinter)"""
        style = ttk.Style()
        style.theme_use("winnative")

        # Notebook (tab container)
        style.configure("TNotebook", background="#fcfcfc") # tab container background

        # Individual tabs
        style.configure("TNotebook.Tab", font=("Segoe UI", 12, "bold"), padding=[12, 6], background="#fcfcfc", foreground="#181818", borderwidth=0, relief="solid") # default tab background and text
        style.map("TNotebook.Tab", background=[("selected", "#D9D9D9")], foreground=[("selected", "#181818")]) # selected tab background and text

        # Buttons
        style.configure("TButton", font=("Segoe UI", 12), padding=[12, 6], background="#fcfcfc", foreground="#181818", borderwidth=0, relief="solid") # button background and text

    # ================= HEADER =================
    def create_header(self):
        """Top title section"""
        header = Frame(self.root, bg="#fcfcfc")
        header.pack(fill=X, pady=10)

        Label(header, text="Image Steganography Tool", font=("Segoe UI", 32, "bold"), bg="#fcfcfc", fg="#181818").pack() # header background and text color

    # ================= TABS =================
    def create_tabs(self):
        """Create tab system (Encode / Decode / Settings)"""

        # Notebook = tab container
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=15, pady=10) # notebook background

        # Create each tab frame
        self.tab_encode = Frame(self.notebook, bg="#fcfcfc")
        self.tab_decode = Frame(self.notebook, bg="#fcfcfc")
        self.tab_settings = Frame(self.notebook, bg="#fcfcfc")

        # Add tabs to notebook
        self.notebook.add(self.tab_encode, text="Encode")
        self.notebook.add(self.tab_decode, text="Decode")
        self.notebook.add(self.tab_settings, text="What's Steganography?")

        # Build contents
        self.build_encode_tab()
        self.build_decode_tab()
        self.build_settings_tab()

    # ================= ENCODE TAB =================
    def build_encode_tab(self):
        """UI elements for encoding messages"""

        frame = self.tab_encode

        # ---- Image Drop Area ----
        self.encode_drop = Label(frame, text="Choose your cipher image", bg="#D9D9D9", fg="#181818", height=8, font=("Segoe UI", 12, "bold"))
        self.encode_drop.pack(fill=X, padx=20, pady=10)
        self.image_preview = Label(frame, bg="#151823")
        self.image_preview.pack(side=LEFT, padx=10)

        # Enable drag & drop
        self.encode_drop.drop_target_register(DND_FILES)
        self.encode_drop.dnd_bind("<<Drop>>", self.on_drop)

        # Click to open file picker
        self.encode_drop.bind("<Button-1>", lambda e: self.load_image())

        # ---- Text Input ----
        Label(frame, text="Message", bg="#151823", fg="white").pack(anchor="w", padx=20)

        self.encode_entry = Entry(frame, font=("Segoe UI", 11))
        self.encode_entry.pack(fill=X, padx=20, pady=5)

        # ---- Encode Button ----
        ttk.Button(frame, text="Encode", command=self.encode).pack(pady=5)

        # ---- Output Box ----
        self.output_encode = Text(
            frame,
            height=10,
            bg="#0b0d14",
            fg="#00ff9c",
            insertbackground="#00ff9c",
            font=("Consolas", 10)
        )
        self.output_encode.pack(fill=BOTH, padx=20, pady=10)

    # ================= DECODE TAB =================
    def build_decode_tab(self):
        """UI elements for decoding coordinates"""

        frame = self.tab_decode

        self.decode_drop = Label(
            frame,
            text="Drag & Drop Image or Click",
            bg="#1b1f2a",
            fg="#9aa4b2",
            height=4
        )
        self.decode_drop.pack(fill=X, padx=20, pady=10)

        self.decode_drop.drop_target_register(DND_FILES)
        self.decode_drop.dnd_bind("<<Drop>>", self.on_drop)

        self.decode_drop.bind("<Button-1>", lambda e: self.load_image())

        Label(frame, text="Coordinates",
              bg="#151823", fg="white").pack(anchor="w", padx=20)

        self.decode_entry = Entry(frame, font=("Segoe UI", 11))
        self.decode_entry.pack(fill=X, padx=20, pady=5)

        ttk.Button(frame, text="Decode", command=self.decode).pack(pady=5)

        self.output_decode = Text(
            frame,
            height=10,
            bg="#0b0d14",
            fg="#00ff9c",
            insertbackground="#00ff9c",
            font=("Consolas", 10)
        )
        self.output_decode.pack(fill=BOTH, padx=20, pady=10)

    # ================= SETTINGS TAB =================
    def build_settings_tab(self):
        """Future settings area"""

        Label(
            self.tab_settings,
            text="Settings (Coming soon)",
            bg="#151823",
            fg="#9aa4b2",
            font=("Segoe UI", 12)
        ).pack(pady=30)

    # ================= IMAGE HANDLING =================
    def on_drop(self, event):
        """Handle drag & drop image"""
        path = event.data.strip("{}")

        try:
            self.img = load_image(path)
            messagebox.showinfo("Success", "Image loaded ✔")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_image(self):
        """Open file dialog to select image"""
        path = filedialog.askopenfilename()
        if not path:
            return

        try:
            self.img = load_image(path)
            messagebox.showinfo("Success", "Image loaded ✔")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= ENCODE LOGIC =================
    def encode(self):
        """Convert text → coordinates"""
        if not self.img:
            messagebox.showerror("Error", "Load an image first")
            return

        text = self.encode_entry.get()

        coords = encode_message(self.img, text)

        # Format output
        result = ";".join(f"{x},{y}" for x, y in coords)

        self.output_encode.delete("1.0", END)
        self.output_encode.insert(END, result)

    # ================= DECODE LOGIC =================
    def decode(self):
        """Convert coordinates → text"""
        if not self.img:
            messagebox.showerror("Error", "Load an image first")
            return

        data = self.decode_entry.get()

        coords = [
            tuple(map(int, p.split(",")))
            for p in data.split(";")
        ]

        result = decode_coordinates(self.img, coords)

        self.output_decode.delete("1.0", END)
        self.output_decode.insert(END, result)


# ================= ENTRY POINT =================
if __name__ == "__main__":
    root = TkinterDnD.Tk()  # enables drag & drop
    app = CryptoGUI(root)
    root.mainloop()