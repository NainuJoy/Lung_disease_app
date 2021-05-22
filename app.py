import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance
import os
import cv2
import tensorflow as tf
from tensorflow.python.keras.models import load_model
#from keras.models import load_model
from win32com.client import Dispatch

def speak(text):
	speak=Dispatch(("SAPI.SpVoice"))
	speak.Speak(text)
model = load_model('MyTrainingModel.h5')

def preprocessing(img):
	try:
		img=img.astype('uint8')
		img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img=cv2.equalizeHist(img)
		img=img/255
		return img
	except Exception as e:
		img=img.astype('uint8')
		img=cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
		img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img=cv2.equalizeHist(img)
		img=img/255
		return img

def main():
	st.title("Lung Disease Detection")
	st.set_option('deprecation.showfileUploaderEncoding',False)
	activites=["Home","Classification"]
	choices=st.sidebar.selectbox("Select Activities",activites)

	if choices=="Classification":
		#st.subheader("Lung Disease Classification")
		img_file=st.file_uploader("Upload File",type=['png','jpg','jpeg'])
		if img_file is not None:
			up_img=Image.open(img_file)
			st.image(up_img)
		if st.button("process"):
			#try:
			img=np.asarray(up_img)
			img=cv2.resize(img, (32,32))
			img=preprocessing(img)
			img=img.reshape(1, 32, 32, 1)
			prediction=model.predict(img)
			classIndex=model.predict_classes(img)
			probabilityValue=np.amax(prediction)
			if probabilityValue>0.50:
				if classIndex==0:
					st.success("Detected Emphysema")
					speak("Detected Emphysema")
				elif classIndex==1:
					st.success("Detected Fibrosis")
					speak("Detected Fibrosis")
				elif classIndex==2:
					st.success("Detected Normal")
					speak("Detected Normal")
				elif classIndex==3:
					st.success("Detected Pneumonia")
					speak("Detected Pneumonia")
				
			#except Exception as e:
				#st.error("Connection Problem,Refresh Again")
			


	elif choices=="Home":
		st.write("Welcome")
		st.write("Lung disease is any problem in the lungs that prevents the lungs from working properly.")
		st.image('tenor (1).gif')
		st.write("Lung diseases are some of the most common medical conditions in the world. Tens of millions of people have lung disease in the U.S. alone. Smoking, infections, and genes cause most lung diseases.")
		


		st.write("This Application is Developed By Nainu Joy")

		
		
		


if __name__=='__main__':
	main()


