"""
Java to C# Code Translator
A desktop application that uses a fine-tuned CodeT5 model to translate
Java source code into C#. Built with PyQt5 for the UI and HuggingFace
Transformers for model inference.

Requirements:
    pip install torch transformers PyQt5

Usage:
    python app.py
"""


import sys
import torch
import os

# UI components to build the window
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel)

# Used to change the text style and size
from PyQt5.QtGui import QFont

# AI tools to load the model and tokenizer, so that you dont need the model locally. 
#AutoTokenizer, RobertaTokenizer, T5Tokenizer
from transformers import RobertaTokenizer, AutoModelForSeq2SeqLM

class CodeTranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # this is if you donwloaded the model to your device. we can just use the huggingface version.
        # self.model_name = os.path.join(current_dir, "fine_tuned_codet5_java_csharp")

        #this is for using the huggingface version
        self.model_name = "vipinchaudhry/codet5-java-to-csharp-translation"
        
        self.initializeUI()
        self.load_model()

    def initializeUI(self):
        # Set title and window size
        self.setWindowTitle('AI Code Translator (Java to C#)')
        self.setGeometry(100, 100, 1000, 700) 
        
        layout = QVBoxLayout()
        
        # Status Label
        self.status_label = QLabel("Status: Initializing...")
        layout.addWidget(self.status_label)

        # Horizontal layout for side-by-side text boxes
        editors_layout = QHBoxLayout()
        
        # Left Side: Java Input
        input_container = QVBoxLayout()
        input_container.addWidget(QLabel("Input Code (Java):"))
        self.input_text = QTextEdit()
        self.input_text.setFont(QFont("Courier New", 10))
        input_container.addWidget(self.input_text)
        
        # Right Side: C# Output
        output_container = QVBoxLayout()
        output_container.addWidget(QLabel("Translated Code (C#):"))
        self.output_text = QTextEdit()
        self.output_text.setFont(QFont("Courier New", 10))
        self.output_text.setReadOnly(True) 
        output_container.addWidget(self.output_text)

        editors_layout.addLayout(input_container)
        editors_layout.addLayout(output_container)
        layout.addLayout(editors_layout)

        # Translate Button
        self.btn = QPushButton('Translate Code')
        self.btn.clicked.connect(self.translate_code)
        layout.addWidget(self.btn)

        self.setLayout(layout)  

    def load_model(self):
        self.status_label.setText("Status: Loading model weights...")
        QApplication.processEvents() # Refresh UI to show status

        try:
            # Check if directory exists first to avoid confusing errors
            # only needed if you are using the model locally (not from HF)
            #if not os.path.exists(self.model_name):
            #    raise FileNotFoundError(f"Folder not found at: {self.model_name}")

            #here, if you have the model loacally on your device and you want to use that version, 
            # add ", local_files_only = True" to both of these "from_pretrained" calls
            self.tokenizer = RobertaTokenizer.from_pretrained("Salesforce/codet5-base", use_fast = False)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            self.status_label.setText(f"Status: Ready on {self.device}")
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.status_label.setText(f"Error: {str(e)}")


    def translate_code(self):
        if not hasattr(self, 'tokenizer') or not hasattr(self, 'model'):
            self.status_label.setText("Error: Model is not loaded.")
            return

        text = self.input_text.toPlainText().strip()
        if not text:
            return 
        
        self.status_label.setText("Status: Translating...")
        QApplication.processEvents()
        
        # Consistent prefix with your training script
        input_text = f"Translate Java to C#; Java: {text} C#:" 

        try:
            # Tokenize and move to device
            inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
            
            with torch.no_grad():
                output = self.model.generate(
                    input_ids=inputs["input_ids"],
                    max_length=512,
                    num_beams=5,             
                    early_stopping=False,      
                    temperature=0.7,          
                    do_sample=True,           
                    top_p=0.95,                
                    length_penalty = 1.0
)

            decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
            self.output_text.setText(decoded.strip())
            self.status_label.setText(f"Status: Translation Complete (on {self.device})")

        except Exception as e:
            print(f"TRANSLATION ERROR: {e}")
            self.status_label.setText("Error during translation. Check console.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CodeTranslatorApp()
    window.show()
    sys.exit(app.exec_())