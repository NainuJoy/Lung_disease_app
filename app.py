import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance
import os
import cv2
import tensorflow as tf
from tensorflow.python.keras.models import load_model
import re
import long_responses as long	

#from keras.models import load_model
#from win32com.client import Dispatch

#def speak(text):
	#speak=Dispatch(("SAPI.SpVoice"))
	#speak.Speak(text)
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
	activites=["Home","Disease Detection","ChatBot"]
	choices=st.sidebar.selectbox("Select Activities",activites)
	cln=1

	if choices=="Disease Detection":
		#st.subheader("Lung Disease Classification")
		
		#with col1:
		img_file=st.file_uploader("Upload File",type=['png','jpg','jpeg'])
		col1, col2 = st.beta_columns((2,1))
		with col2:
			result = st.button("DETECTION")
		with col1:
			if img_file is not None:
				up_img=Image.open(img_file)
				st.image(up_img,use_column_width=True)
		#if st.button("Process"):
		if result:
			try:
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
						#speak("Detected Emphysema")
						#speak("Move to chatbot option in activities, if you have any queries about this disease")
					elif classIndex==1:
						st.success("Detected Fibrosis")
						#speak("Detected Fibrosis")
						#speak("Move to chatbot option in activities, if you have any queries about this disease")
					elif classIndex==2:
						st.success("Detected Normal")
						#speak("Detected Normal")
						#speak("Move to chatbot option in activities, if you have any queries about this disease")
					elif classIndex==3:
						st.success("Detected Pneumonia")
						#speak("Detected Pneumonia")
						#speak("Move to chatbot option in activities, if you have any queries about this disease")
					elif classIndex==4:
						st.success("Upload correct X-ray image")
						#speak("Upload correct X-ray image")
			except Exception as e:
				st.error("Upload Error")
			


	elif choices=="Home":
		st.write("Welcome")
		st.write("Lung disease is any problem in the lungs that prevents the lungs from working properly.")
		st.image('tenor (1).gif')
		st.write("Lung diseases are some of the most common medical conditions in the world. Tens of millions of people have lung disease in the U.S. alone. Smoking, infections, and genes cause most lung diseases.")
		


		st.write("This Application is Developed By Nainu Joy")

	elif choices=="ChatBot":

		st.write("Queries about Pneumonia,Emphysema & Fibrosis")
		def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
			message_certainty = 0
			has_required_words = True

			# Counts how many words are present in each predefined message
			for word in user_message:
				if word in recognised_words:
					message_certainty += 1
			# Calculates the percent of recognised words in a user message
			percentage = float(message_certainty) / float(len(recognised_words))
			# Checks that the required words are in the string
			for word in required_words:
				if word not in user_message:
					has_required_words = False
					break
			# Must either have the required words, or be a single response
			if has_required_words or single_response:
				return int(percentage * 100)
			else:
				return 0
		def check_all_messages(message):

		

			highest_prob_list = {}
		# Simplifies response creation / adds it to the dict
			def response(bot_response, list_of_words, single_response=False, required_words=[]):
				nonlocal highest_prob_list
				highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)
		# Responses -------------------------------------------------------------------------------------------------------
			response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
			response('See you!', ['bye', 'goodbye'], single_response=True)
			response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
			response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
			response('Thank you!', ['i', 'like', 'this', 'app'], required_words=['like', 'app'])
		# Longer responses
			response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
			response(long.R_P1, ['what', 'causes', 'pneumonia'], required_words=['causes' or 'reasons' or 'cause' or'reason','pneumonia'],single_response=True)
			response(long.R_P2, ['what', 'are', 'the','symptoms', 'of','pneumonia'], required_words=['symptoms', 'pneumonia'])
			
			response(long.R_P3, ['what', 'are', 'the','home', 'remedies', 'for', 'pneumonia'], required_words=['remedies' or 'solutions' or 'solution' or 'remedy', 'pneumonia'],single_response=True)
			response(long.R_E1, ['what', 'is', 'emphysema'], required_words=['what', 'emphysema'])
			response(long.R_E2, ['what', 'causes', 'emphysema'], required_words=['causes' or 'reason' or'reasons' or 'cause', 'emphysema'],single_response=True)
			response(long.R_F1, ['what', 'is', 'fibrosis'], required_words=['what', 'fibrosis'])
			response(long.R_F2, ['what', 'are', 'the','symptoms', 'of','fibrosis'], required_words=['symptoms', 'fibrosis'])
			response(long.R_F3, ['what', 'age', 'does','pulmonary', 'fibrosis','start'], required_words=['age', 'fibrosis',])
			best_match = max(highest_prob_list, key=highest_prob_list.get)
			# print(highest_prob_list)
			# print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')
			return long.unknown() if highest_prob_list[best_match] < 1 else best_match
		def get_response(user_input):
		# Used to get the response
			split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
			response = check_all_messages(split_message)
			return response
			# Testing the response system
			
		while True:
			st.write('Bot: ' + get_response(st.text_input('You: ',key=str(cln))))
			cln=cln+1
			break
if __name__=='__main__':
	main()
