#!/usr/bin/env python3
"""
Skyscrap Measure - Single file app
- Minimal CLI/GUI hybrid: if tkinter available, show GUI; else fallback to CLI
- Computes building height from image EXIF or from pixel measurements with reference object
"""

import sys, math
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    GUI = True
except Exception:
    GUI = False

try:
    from PIL import Image
    PIL_OK = True
except Exception:
    PIL_OK = False


def estimate_height_from_pixels(object_pixels, object_real_m, building_pixels):
    if object_pixels <= 0 or object_real_m <= 0 or building_pixels <= 0:
        raise ValueError("All inputs must be > 0")
    scale_m_per_px = object_real_m / object_pixels
    return building_pixels * scale_m_per_px


def cli():
    print("Skyscrap Measure (CLI)")
    print("Option 1: Reference object method")
    try:
        obj_px = float(input("Reference object height in image (pixels): "))
        obj_m = float(input("Reference object real height (meters): "))
        bld_px = float(input("Building height in image (pixels): "))
        h = estimate_height_from_pixels(obj_px, obj_m, bld_px)
        print(f"Estimated building height: {h:.2f} m")
    except Exception as e:
        print("Error:", e)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Skyscrap Measure")
        self.root.geometry("520x260")
        self.build()

    def build(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        self.obj_px = tk.StringVar()
        self.obj_m = tk.StringVar()
        self.bld_px = tk.StringVar()

        row = 0
        ttk.Label(frm, text="Reference object pixels:").grid(row=row, column=0, sticky='e', padx=6, pady=6)
        ttk.Entry(frm, textvariable=self.obj_px).grid(row=row, column=1, sticky='we')
        row += 1
        ttk.Label(frm, text="Reference object height (m):").grid(row=row, column=0, sticky='e', padx=6, pady=6)
        ttk.Entry(frm, textvariable=self.obj_m).grid(row=row, column=1, sticky='we')
        row += 1
        ttk.Label(frm, text="Building pixels:").grid(row=row, column=0, sticky='e', padx=6, pady=6)
        ttk.Entry(frm, textvariable=self.bld_px).grid(row=row, column=1, sticky='we')
        row += 1
        ttk.Button(frm, text="Estimate", command=self.estimate).grid(row=row, column=0, columnspan=2, pady=10)

        self.result = ttk.Label(frm, text="Result: -")
        self.result.grid(row=row+1, column=0, columnspan=2)

        frm.columnconfigure(1, weight=1)

    def estimate(self):
        try:
            h = estimate_height_from_pixels(float(self.obj_px.get()), float(self.obj_m.get()), float(self.bld_px.get()))
            self.result.config(text=f"Result: {h:.2f} m")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    if GUI:
        root = tk.Tk()
        App(root)
        root.mainloop()
    else:
        cli()

if __name__ == "__main__":
    main()
