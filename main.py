from doctr.io import DocumentFile # type: ignore
from doctr.models import ocr_predictor # type: ignore
import json
import requests
from PyQt5.QtWidgets import QApplication

###### GET FILE PATH FROM PYQT5 ######
import sys
# sys.path.insert(0, 'D:/pgi')
# sys.path.insert(0, 'D:/pgi/ui_docker')
# from app.UI import AppDemo
from UI import AppDemo



###### OCR PART ######
# Load model
model = ocr_predictor(pretrained=True)

def create_document_from_file(file_path):
    # Check file extension to determine the type of file
    if file_path.upper().endswith('.PDF'):
        # Create a DocumentFile object from a PDF file
        return DocumentFile.from_pdf(file_path)
    elif file_path.upper().endswith(('.JPG', '.JPEG', '.PNG', '.TIF', '.TIFF', '.JFIF')):
        # Create a DocumentFile object from image files
        return DocumentFile.from_images(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or image file.")

API_URL1 = "https://api-inference.huggingface.co/models/google/gemma-1.1-7b-it"
API_URL2 = "https://api-inference.huggingface.co/models/google/gemma-1.1-2b-it"
headers = {"Authorization": ""}
model = ocr_predictor(pretrained=True)

def query1(payload):
	response = requests.post(API_URL1, headers=headers, json=payload)
	return response.json()
def query2(payload):
	response = requests.post(API_URL2, headers=headers, json=payload)
	return response.json()

def handle_processed_data(data):
    demo.update_fields(data)

def update_UI(category):
    demo.changeFields(category)

def process_image(file_path):
    """Complete image processing pipeline"""
    try:
        print("Processing image " + file_path)
        doc = create_document_from_file(file_path)
        result = model(doc)
        OCR_output = result.render()

        print(OCR_output)
        
        classification = f"""
            ###role:user
            ###content:Based on the following OCR output, which category does this document belong to: "Invoice", "Identity Document", "Agreement" or "Other" (if not recognized)? \n
            {OCR_output}
            ### Instructions: Please indicate the most likely category for the document (if it doesnt make sense default to "Other"). 

            """
        
        output = query1({"inputs": classification,
                        "parameters": {"max_new_tokens":200, "temperature":0.001, "return_full_text":False}
                        })

        doc_type = output[0]['generated_text'].strip()
        print(doc_type)

        category = "Other" # Initialize category as "Other" (if something wrong happens in the classification this is the default)

        types = ["Invoice", "Identity Document", "Agreement", "Other"]
        for typ in types:
            if typ.lower() in doc_type.lower():
                print(typ)
                category = typ
                break
        
        print(category)
        update_UI(category)
    
        if category != "Other":

            header = f"This text is extracted from an {category} using OCR so its chaotic:"

            if category == "Invoice":
                footer = '''I want you to extract the "invoice_sender", "invoice_number", "invoice_date", "total_amount" (in a String format, remove the currency) and the "currency"
                        in a strict JSON format'''
            else:
                footer ='''I want you to extract the "id_number", "full_name", "nationality", "date_of_birth" and the "gender"
                in a strict JSON format'''

            data_extr = header + OCR_output +  footer

            output = query2({"inputs": data_extr,
                            "parameters": {"max_new_tokens":200, "temperature":0.001, "return_full_text":False}
                                })
            
            cleaned_output = output[0]['generated_text'].strip()
            j = cleaned_output.find("{")
            e = cleaned_output.find("}")
            output = cleaned_output[j:e + 1]
            print(output)
            output_dict = json.loads(output, strict=False)
            handle_processed_data(output_dict)
            
    except:
        print("Error in processing output of : " + file_path)
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of your UI class
    demo = AppDemo()
    # Connect the GUI's signal to the processing function
    demo.imageDropped.connect(process_image) 

    demo.show()
    demo.raise_()
    sys.exit(app.exec_())