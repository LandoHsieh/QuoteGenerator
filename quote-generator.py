import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageTk
import random
import os

def upload_image():
  global image_path
  image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
  if image_path:
    image_label.config(text=f"Image: {image_path}")

def save_image(canvas, filename):
  # Get the directory where the script is running
  directory = os.getcwd()
  filepath = filedialog.asksaveasfilename(initialdir=directory, defaultextension=".png",
                                          filetypes=[("PNG files", "*.png")])
  if filepath:
    canvas.save(filepath)
    tk.messagebox.showinfo("Success", f"Image saved successfully to:\n{filepath}")

def generate_quote():
  global image_path, quote1, quote2, author

  quote1 = quote1_entry.get()
  quote2 = quote2_entry.get()
  author = author_entry.get()

  if not image_path:
    tk.messagebox.showerror("Error", "Please select an image")
    return

  if not quote1 or not quote2 or not author:
    tk.messagebox.showerror("Error", "Please fill in all fields")
    return

  try:
    # Open and convert image to grayscale
    image = Image.open(image_path).convert('L')

    # Adjust image aspect ratio to maintain proportions
    image_width, image_height = image.size
    new_width = 400  # Set a fixed width for the image
    new_height = int(image_height * (new_width / image_width))
    image = image.resize((new_width, new_height))

    # Create a new canvas with sufficient width to accommodate text
    canvas_width = new_width + 400  # Add space for text
    canvas_height = new_height
    canvas = Image.new('RGB', (canvas_width, canvas_height), color=(0, 0, 0))

    # Paste the image onto the canvas
    canvas.paste(image, (0, 0))

    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype('NotoSansTC-SemiBold.ttf', 32)

    # Calculate text width for better positioning
    text_width = draw.textlength(quote1, font=font) + 20  # Add some padding

    # Draw quote and author on the right side
    draw.text((canvas_width - text_width - 100, 100), quote1, fill="white", font=font)
    draw.text((canvas_width - text_width - 100, 200), quote2, fill="white", font=font)
    draw.text((canvas_width - text_width - 100, 300), f"- {author}", fill="white", font=font)

    random_number = str(random.randint(1000000, 9999999))
    filename = f"generated_quote_{random_number}.png"
    # canvas.save(filename)
    #---------------Preview-----------------
    # Create a new window for image preview
    preview_window = tk.Toplevel(window)
    preview_window.title("Generated Image")

    # Display a label indicating that the image is being generated
    generating_label = tk.Label(preview_window, text="Generating image, please wait...")
    generating_label.pack()

    # Function to update the preview window with the generated image
    def update_preview():
      # Remove the generating label
      generating_label.pack_forget()
      # Display the generated image in the preview window
      generated_image = ImageTk.PhotoImage(canvas)
      image_label = tk.Label(preview_window, image=generated_image)
      image_label.image = generated_image  # Keep a reference to prevent garbage collection
      image_label.pack()

      # Save button
      save_button = tk.Button(preview_window, text="Save", command=lambda: save_image(canvas, filename))
      save_button.pack()

    # Update the preview window after a short delay
    preview_window.after(1000, update_preview)
  except Exception as e:
    tk.messagebox.showerror("Error", e)

# Create the main window
window = tk.Tk()
window.title("Quote Generator")

# Image label
image_label = tk.Label(window, text="No image selected")
image_label.pack()

# Upload image button
image_button = tk.Button(window, text="Upload Image", command=upload_image)
image_button.pack()

# Quote 1 entry
quote1_label = tk.Label(window, text="Quote 1:")
quote1_label.pack()
quote1_entry = tk.Entry(window)
quote1_entry.pack()

# Quote 2 entry
quote2_label = tk.Label(window, text="Quote 2:")
quote2_label.pack()
quote2_entry = tk.Entry(window)
quote2_entry.pack()

# Author entry
author_label = tk.Label(window, text="Author:")
author_label.pack()
author_entry = tk.Entry(window)
author_entry.pack()

# Generate quote button
generate_quote_button = tk.Button(window, text="Generate Quote", command=generate_quote)
generate_quote_button.pack()

# Run the main loop
window.mainloop()
