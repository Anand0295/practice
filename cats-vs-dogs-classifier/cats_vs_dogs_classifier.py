#!/usr/bin/env python3
"""
Cats vs Dogs Image Classifier
A single-file application for classifying images as cats or dogs using a pre-trained deep learning model.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import io
import base64

# Try to import tensorflow, handle if not available
try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


class CatsDogsClassifier:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cats vs Dogs Classifier")
        self.window.geometry("800x700")
        self.model = None
        self.current_image = None
        self.current_image_path = None
        self.setup_ui()
        self.load_model()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.window,
            text="Cats vs Dogs Image Classifier",
            font=("Arial", 20, "bold"),
            pady=15
        )
        title_label.pack()
        
        # Main frame
        main_frame = tk.Frame(self.window, padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Upload button
        upload_btn = tk.Button(
            button_frame,
            text="Upload Image",
            command=self.upload_image,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10
        )
        upload_btn.pack(side=tk.LEFT, padx=5)
        
        # Classify button
        self.classify_btn = tk.Button(
            button_frame,
            text="Classify Image",
            command=self.classify_image,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.classify_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_results,
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=10
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Image display frame
        image_frame = tk.LabelFrame(
            main_frame,
            text="Image Preview",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        image_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.image_label = tk.Label(
            image_frame,
            text="No image loaded",
            font=("Arial", 12),
            bg="#f0f0f0",
            width=50,
            height=15
        )
        self.image_label.pack()
        
        # Result frame
        result_frame = tk.LabelFrame(
            main_frame,
            text="Classification Result",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        result_frame.pack(pady=10, fill=tk.X)
        
        self.result_label = tk.Label(
            result_frame,
            text="Upload an image to classify",
            font=("Arial", 14),
            pady=10
        )
        self.result_label.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready",
            font=("Arial", 10),
            fg="gray"
        )
        self.status_label.pack(pady=5)
    
    def load_model(self):
        """Load or create a simple model for classification."""
        if not TF_AVAILABLE:
            self.status_label.config(
                text="TensorFlow not available - using simple rule-based classifier",
                fg="orange"
            )
            return
        
        try:
            # Create a simple CNN model (MobileNetV2-based for efficiency)
            self.model = keras.applications.MobileNetV2(
                weights='imagenet',
                include_top=True,
                input_shape=(224, 224, 3)
            )
            self.status_label.config(text="Model loaded successfully", fg="green")
        except Exception as e:
            self.status_label.config(
                text=f"Model loading failed: {str(e)}",
                fg="red"
            )
            self.model = None
    
    def upload_image(self):
        """Upload and display an image."""
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Load and display image
                image = Image.open(file_path)
                self.current_image = image
                self.current_image_path = file_path
                
                # Resize for display
                display_size = (400, 400)
                image.thumbnail(display_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo  # Keep a reference
                
                # Enable classify button
                self.classify_btn.config(state=tk.NORMAL)
                self.result_label.config(text="Ready to classify")
                self.status_label.config(text=f"Loaded: {file_path.split('/')[-1]}", fg="blue")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def preprocess_image(self, image):
        """Preprocess image for model input."""
        # Resize to model input size
        img = image.resize((224, 224))
        # Convert to array
        img_array = np.array(img)
        # Ensure 3 channels (RGB)
        if len(img_array.shape) == 2:  # Grayscale
            img_array = np.stack([img_array] * 3, axis=-1)
        elif img_array.shape[2] == 4:  # RGBA
            img_array = img_array[:, :, :3]
        # Expand dimensions and preprocess
        img_array = np.expand_dims(img_array, axis=0)
        img_array = keras.applications.mobilenet_v2.preprocess_input(img_array)
        return img_array
    
    def classify_with_model(self, image):
        """Classify using the deep learning model."""
        try:
            # Preprocess
            processed_img = self.preprocess_image(image)
            
            # Predict
            predictions = self.model.predict(processed_img, verbose=0)
            
            # Decode predictions (ImageNet classes)
            decoded = keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)[0]
            
            # Check for cat or dog related classes
            cat_classes = ['tabby', 'tiger_cat', 'persian_cat', 'siamese_cat', 'egyptian_cat']
            dog_classes = ['golden_retriever', 'labrador_retriever', 'german_shepherd', 
                          'beagle', 'bulldog', 'pug', 'chihuahua', 'pomeranian']
            
            cat_confidence = 0
            dog_confidence = 0
            
            result_text = "\nTop 5 Predictions:\n"
            for i, (class_id, class_name, confidence) in enumerate(decoded, 1):
                result_text += f"{i}. {class_name}: {confidence*100:.2f}%\n"
                
                # Check if it's a cat or dog
                if any(cat in class_name.lower() for cat in ['cat', 'tabby', 'persian', 'siamese', 'egyptian']):
                    cat_confidence = max(cat_confidence, confidence)
                if any(dog in class_name.lower() for dog in ['dog', 'retriever', 'shepherd', 'beagle', 'bulldog', 'pug', 'chihuahua', 'pomeranian', 'terrier']):
                    dog_confidence = max(dog_confidence, confidence)
            
            # Determine result
            if cat_confidence > dog_confidence and cat_confidence > 0.1:
                final_result = f"🐱 CAT (Confidence: {cat_confidence*100:.1f}%)"
                color = "blue"
            elif dog_confidence > cat_confidence and dog_confidence > 0.1:
                final_result = f"🐶 DOG (Confidence: {dog_confidence*100:.1f}%)"
                color = "green"
            else:
                final_result = "❓ Neither clear cat nor dog detected"
                color = "orange"
            
            return final_result, color, result_text
        
        except Exception as e:
            return f"Error: {str(e)}", "red", ""
    
    def classify_with_simple_rules(self, image):
        """Simple rule-based classification (fallback when TF not available)."""
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Simple color-based heuristic (very basic)
        img_array = np.array(image.resize((100, 100)))
        avg_color = np.mean(img_array, axis=(0, 1))
        
        # Very simplistic rule: warmer tones -> dog, cooler -> cat
        # This is NOT accurate but provides a demo when TF is unavailable
        warmth = (avg_color[0] + avg_color[1]) / 2 - avg_color[2]
        
        if warmth > 10:
            return "🐶 DOG (Simple heuristic)", "green", "Using basic color analysis (not ML)"
        else:
            return "🐱 CAT (Simple heuristic)", "blue", "Using basic color analysis (not ML)"
    
    def classify_image(self):
        """Classify the current image."""
        if self.current_image is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        
        # Show progress
        self.progress.pack(pady=5)
        self.progress.start()
        self.status_label.config(text="Classifying...", fg="blue")
        self.window.update()
        
        try:
            if TF_AVAILABLE and self.model is not None:
                result, color, details = self.classify_with_model(self.current_image)
            else:
                result, color, details = self.classify_with_simple_rules(self.current_image)
            
            # Display result
            self.result_label.config(text=result, fg=color, font=("Arial", 18, "bold"))
            if details:
                self.result_label.config(text=result + "\n\n" + details)
            
            self.status_label.config(text="Classification complete", fg="green")
        
        except Exception as e:
            messagebox.showerror("Error", f"Classification failed: {str(e)}")
            self.status_label.config(text="Classification failed", fg="red")
        
        finally:
            self.progress.stop()
            self.progress.pack_forget()
    
    def clear_results(self):
        """Clear all results and reset."""
        self.current_image = None
        self.current_image_path = None
        self.image_label.config(image="", text="No image loaded", bg="#f0f0f0")
        self.result_label.config(text="Upload an image to classify", fg="black", font=("Arial", 14))
        self.classify_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Ready", fg="gray")
    
    def run(self):
        """Run the application."""
        self.window.mainloop()


if __name__ == "__main__":
    # Note about dependencies
    if not TF_AVAILABLE:
        print("Note: TensorFlow is not installed. Using simple rule-based classification.")
        print("For better accuracy, install TensorFlow: pip install tensorflow pillow numpy")
    
    app = CatsDogsClassifier()
    app.run()
