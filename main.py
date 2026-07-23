import cv2,turtle,tkinter as tk,numpy as np
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
root = tk.Tk()
root.title("PixeArt v1.0")
root.geometry("450x500")
image_path = tk.StringVar()
def browse():
    filename = filedialog.askopenfilename(
        filetypes=[
            ("Images", "*.png *.jpg *.jpeg *.bmp *.webp"),
            ("All Files", "*.*")
        ]
    )

    if filename:
        image_path.set(filename)

        img = Image.open(filename)
        img.thumbnail((250,250))

        photo = ImageTk.PhotoImage(img)

        preview.configure(image=photo)
        preview.image = photo
def generate():
    if image_path.get() == "":
        messagebox.showerror("Error", "Please select an image.")
        return

    try:
        spacing = int(spacing_entry.get())
    except:
        messagebox.showerror("Error", "Spacing must be an integer.")
        return
    imager = image_path.get()
    image = cv2.imread(imager)
    if image is None:
        messagebox.showerror("Error", "Could not open the selected image.")
        return
    height, width, channels = image.shape
    output = np.zeros((height, width, 3), dtype=np.uint8)
    done = 0
    status.config(text="Generating...")
    if height%spacing!=0:
        height=height-(height%spacing)
    if width%spacing!=0:
        width=width-(width%spacing)
    output = np.zeros((height, width, 3), dtype=np.uint8)
    total = (height // spacing) * (width // spacing)
    progress["maximum"] = total
    progress["value"] = 0
    turtle.clearscreen()
    screen=turtle.Screen()
    screen.title(f"{imager}_pixelated")
    screen.setup(width + 10, height + 10)
    screen.bgcolor("black")
    screen.getcanvas().update()
    #screen.setworldcoordinates(0, height, width, 0)
    screen.screensize(width, height)
    screen.tracer(0, 0)
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    w,h=0,0
    while h<(height//spacing):
        w=0
        while w<(width//spacing):
            sample_x = min(w * spacing + spacing // 2, width - 1)
            sample_y = min(h * spacing + spacing // 2, height - 1)
            colour = image[sample_y, sample_x]
            hexcode=f"#{colour[2]:02X}{colour[1]:02X}{colour[0]:02X}"
            t.penup()
            target_x = (w * spacing) - (width // 2)
            target_y = (height // 2) - (h * spacing)
            t.goto(target_x, target_y)
            t.dot(spacing, hexcode)
            center = (
                w * spacing + spacing // 2,
                h * spacing + spacing // 2
            )
            cv2.circle(
                output,
                center,
                max(1, round(spacing/2)),
                (
                    int(colour[0]),
                    int(colour[1]),
                    int(colour[2])
                ),
                -1
            )
            done += 1
            if done % 100 == 0:
                progress["value"] = done
                status.config(text=f"{done}/{total} dots")
                root.update()
            w+=1
        h+=1
    screen.update()
    save_path = filedialog.asksaveasfilename(
    defaultextension=".png",
    filetypes=[
        ("PNG Image", "*.png"),
        ("JPEG Image", "*.jpg"),
        ("Bitmap", "*.bmp"),
        ("WebP Image", "*.webp")
    ]
)
    if save_path:
        cv2.imwrite(save_path, output)
    status.config(text="Finished!")

tk.Label(root, text="Image").pack(pady=(10, 0))

frame = tk.Frame(root)
frame.pack()

tk.Entry(frame, textvariable=image_path, width=35).pack(side="left", padx=5)

tk.Button(frame, text="Browse", command=browse).pack(side="left")
preview = tk.Label(root)
preview.pack(pady=10)

tk.Label(root, text="Dot Spacing").pack(pady=(10, 0))

spacing_entry = tk.Entry(root, width=10)
spacing_entry.insert(0, "5")
spacing_entry.pack()

progress = Progressbar(
    root,
    orient="horizontal",
    length=300,
    mode="determinate"
)

progress.pack(pady=5)
status = tk.Label(root, text="Ready")
status.pack()

tk.Button(
    root,
    text="Generate Pixelated Image",
    command=generate,
    width=25
).pack(pady=15)

root.mainloop()