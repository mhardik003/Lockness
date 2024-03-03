import streamlit as st
import json
import pickle
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import os
from PIL import Image
import os


st.set_page_config(
    page_title="Lockness",
    page_icon="🔒",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Lockness is a platform that allows you to upload your data and machine learning models to keep them safe."
    }
)

def load_model(model_path):
    model = models.resnet50(pretrained=False)  # Assuming ResNet-50, adjust accordingly
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

def preprocess_image(image):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return preprocess(image)

st.title("Find all the uploaded models here")
search_model = st.text_input("Search for a model")


with open('models.txt', 'r') as f:
    model_names = f.readlines()

with open('model_description.json', 'r') as f:
    model_descriptions = json.load(f)    

if search_model:
    model_names.append("None")
    model_names = [model for model in model_names if search_model.lower() in model.lower()]

# make a list of the model descriptions which are there in model_names
model_descriptions = [model_descriptions[model.strip()] for model in model_names]
selected_model = st.radio("Select a model", model_names, captions = model_descriptions)
selected_model = selected_model.strip()

st.divider()

if selected_model and selected_model != "None":
    st.write(f"You have selected {selected_model}!")   
    model = load_model(f'models/{selected_model}.pkl') 
    
    dataset_type = st.radio("What do you want to inference on?", ["None", "Single Point", "Whole Dataset"], captions = ["","Enter a point on which you want to do inference on", "Upload the whole dataset you want to do inference on"])
    
    st.divider()

    if dataset_type == "Single Point":
        # input_model = st.text_input("Enter the point here")
        input_model = st.file_uploader("Upload the sample here")
        
        if input_model:
            input_model = Image.open(input_model).convert('RGB')
            st.image(input_model, caption='Uploaded Image.', use_column_width=False)
            
            input_model = preprocess_image(input_model)
            batch_t = torch.unsqueeze(input_model, 0)
            
            with torch.no_grad():
                prediction = model(batch_t)
                probabilities = torch.nn.functional.softmax(prediction[0], dim=0)
                
            top1_prob, top1_catid = torch.topk(probabilities, 1)
            # st.write(f"Top prediction index: {top1_catid.item()}, Probability: {top1_prob.item()}")
            
            # print the most probable label
            with open('imagenet_classes.txt') as f:
                labels = [line.strip() for line in f.readlines()]
            st.write(f"Top class: {labels[top1_catid]}")
            
        
        
        
        # prediction = selected_model.predict(input_model)
        # st.write(f"The prediction for the given input is {prediction}")
        
        
    elif dataset_type == "Whole Dataset":
        dataset = st.file_uploader("Upload the dataset here")
        predictions = ["ffFff", "ff","Ffff"]
        show_download_button = False
        # for point in dataset:
        #     prediction = selected_model.predict(point)
        #     predictions.append(prediction)
    
        show_download_button = True

        # give the option to download the predictions
        if show_download_button:
            st.write(f"The predictions are ready to be downloaded")
            predictions = json.dumps(predictions)
            st.download_button(
            label="Download predictions as CSV",
            data=predictions,
            file_name='large_df.csv',
            mime='text/csv',
        )        
        
                
    
        

