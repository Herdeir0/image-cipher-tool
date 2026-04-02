# ================= IMPORTS =================
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

# Image handling
from PIL import Image, ImageTk

# Your core logic
from image_utils import load_image
from encoder import encode_message
from decoder import decode_coordinates

# ================= MAIN CLASS =================
class CryptoGUI:
    def __init__(self, root):
        self.root = root

        # -------- WINDOW CONFIG --------
        self.root.title("Image Cipher Tool")
        self.root.geometry("800x700")
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

        Label(header, text="Image Cipher Tool", font=("Segoe UI", 32, "bold"), bg="#fcfcfc", fg="#181818").pack() # header background and text color

        frame = self.root # for better readability

        # ---- Container (label + image side-by-side) ----
        container = Frame(frame, bg="#fcfcfc")
        container.pack(fill=Y, padx=20, pady=10)

        # ---- Drop label ----
        self.encode_drop = Label(container,text="Choose your cipher",bg="#D9D9D9",fg="#181818",width=25,height=5,justify="left",font=("Segoe UI", 12, "bold"))
        self.encode_drop.pack(side=LEFT, padx=20, fill=X)

        # ---- Image preview ----
        self.image_preview = Label(container,bg="#fcfcfc")
        self.image_preview.pack(side=LEFT, padx=10)

        # Drag & drop setup
        self.encode_drop.drop_target_register(DND_FILES)
        self.encode_drop.dnd_bind("<<Drop>>", self.on_drop)

        # Click to browse
        self.encode_drop.bind("<Button-1>", lambda e: self.load_image())

    # ================= TABS =================
    def create_tabs(self):
        """Create tab system (Encode / Decode / Settings)"""

        # Notebook = tab container
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=15, pady=10) # notebook background

        # Create each tab frame
        self.tab_encode = Frame(self.notebook, bg="#fcfcfc", pady=10, borderwidth=0, relief="solid")
        self.tab_decode = Frame(self.notebook, bg="#fcfcfc", pady=10, borderwidth=0, relief="solid")
        self.tab_settings = Frame(self.notebook, bg="#fcfcfc", pady=10, borderwidth=0, relief="solid")

        # Add tabs to notebook
        self.notebook.add(self.tab_encode, text="Encode")
        self.notebook.add(self.tab_decode, text="Decode")
        self.notebook.add(self.tab_settings, text="How to")

        # Build contents
        self.build_encode_tab()
        self.build_decode_tab()
        self.build_settings_tab()

    # ================= ENCODE TAB =================
    def build_encode_tab(self):
        frame = self.tab_encode

        # ---- Input ----
        Label(frame, text="Message to encode", bg="#fcfcfc", fg="#181818", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20)

        self.encode_entry = Entry(frame, font=("Segoe UI", 12))
        self.encode_entry.pack(fill=BOTH, padx=20, pady=5)

        # ---- Button ----
        ttk.Button(frame, text="Encode", command=self.encode).pack(pady=5, fill=X, padx=20)

        # ---- Output ----
        Label(frame, text="Encoded Message", bg="#fcfcfc", fg="#181818", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=10)
        self.output_encode = Text(frame,height=10,bg="#d9d9d9",fg="#181818",font=("Segoe UI", 12))
        self.output_encode.pack(fill=BOTH, padx=20, pady=0)

    # ================= DECODE TAB =================
    def build_decode_tab(self):
        frame = self.tab_decode

        Label(frame, text="Coordinates to decode", bg="#fcfcfc", fg="#181818", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20)

        self.decode_entry = Entry(frame, font=("Segoe UI", 12))
        self.decode_entry.pack(fill=X, padx=20, pady=5)

        ttk.Button(frame, text="Decode", command=self.decode).pack(pady=5, fill=X, padx=20)

        # ---- Output ----
        Label(frame, text="Decoded Message", bg="#fcfcfc", fg="#181818", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=10)
        self.output_decode = Text(frame,height=10,bg="#d9d9d9",fg="#181818",font=("Segoe UI", 12))
        self.output_decode.pack(fill=BOTH, padx=20, pady=0)

    # ================= SETTINGS TAB =================
    def build_settings_tab(self):
        Label(self.tab_settings,text="How to use this application?",bg="#fcfcfc",fg="#181818",font=("Segoe UI", 14, "bold"),justify="left",wraplength=600).pack(pady=10, fill=X, padx=20)
        Label(self.tab_settings,text="1. Upload an image (.png, .jpg, .jpeg, .bmp, .tiff) on the upper cipher field\n2. Go to the Encode tab, type your message and click Encode\n3. Copy the resulting coordinates\n4. Go to the Decode tab, paste the coordinates and click Decode",bg="#fcfcfc",fg="#181818",font=("Segoe UI", 12),justify="left",wraplength=600).pack(pady=10, fill=X, padx=20)

    # ================= IMAGE PREVIEW =================
    def show_preview(self, path):
        """Display thumbnail preview"""
        img = Image.open(path)
        img.thumbnail((100, 100))

        self.tk_image = ImageTk.PhotoImage(img)
        self.image_preview.config(image=self.tk_image)

    # ================= IMAGE LOADING =================
    def on_drop(self, event):
        """Handle drag & drop"""
        path = event.data.strip("{}")

        try:
            self.img = load_image(path)
            self.show_preview(path)
            self.encode_drop.config(text="Image Loaded ✔")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_image(self):
        """Open file dialog"""
        path = filedialog.askopenfilename()
        if not path:
            return

        try:
            self.img = load_image(path)
            self.show_preview(path)
            self.encode_drop.config(text="Image Loaded ✔")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= ENCODE =================
    def encode(self):
        if not self.img:
            messagebox.showerror("Error", "Load an image first")
            return

        text = self.encode_entry.get()

        coords = encode_message(self.img, text)
        result = ";".join(f"{x},{y}" for x, y in coords)

        self.output_encode.delete("1.0", END)
        self.output_encode.insert(END, result)

    # ================= DECODE =================
    def decode(self):
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
    root = TkinterDnD.Tk()
    app = CryptoGUI(root)
    root.mainloop()