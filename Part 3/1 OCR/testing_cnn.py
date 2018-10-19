# Import basic libraries and keras
import numpy as np
import tkinter as tk
from PIL import Image, ImageDraw
from keras.models import load_model

model = load_model('cnn_model.h5')

def evaluate():
    img = image1.resize((28, 28)).convert('L')
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i,j] = 255 if pixels[i,j] == 0 else 0
    X_test = np.array(img).reshape(1, 28, 28, 1)
    predicted_classes = model.predict_classes(X_test, verbose=0)
    reslabel['text'] = "The drawn number is " + str(predicted_classes[0])

def clear():
    pixels = image1.load()
    for i in range(image1.size[0]):
        for j in range(image1.size[1]):
            pixels[i,j] = (255, 255,255)
    cv.delete("all")
    reslabel['text'] = "Draw a number & press Evaluate"

def paint(event):
    x1, y1 = (event.x - 10), (event.y - 10)
    x2, y2 = (event.x + 10), (event.y + 10)
    cv.create_oval(x1, y1, x2, y2, fill="black",width=4)
    draw.ellipse([x1, y1, x2, y2],fill="black")

root = tk.Tk()
root.title("OCR application")
root.resizable(False, False)

# Create top canvas and image
cv = tk.Canvas(root, width=280, height=280, bg='white')
cv.pack()
image1 = Image.new("RGB", (280, 280), (255, 255, 255))
draw = ImageDraw.Draw(image1)
cv.bind("<B1-Motion>", paint)

# Create bottom label and buttons
bottom = tk.Frame(root)
bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
reslabel = tk.Label(text = "Draw a number & press Evaluate")
reslabel.pack(in_=bottom, side=tk.LEFT, fill=tk.Y, expand=True)
button = tk.Button(text="evaluate", command=evaluate, width=6)
button.pack(in_=bottom, side=tk.LEFT, fill=tk.Y)
button = tk.Button(text="clear", command=clear, width=6)
button.pack(in_=bottom, side=tk.RIGHT, fill=tk.Y)

root.mainloop()
