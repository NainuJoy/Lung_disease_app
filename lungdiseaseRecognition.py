import warnings
warnings.filterwarnings('ignore')
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D,Dense,MaxPooling2D,Activation,Dropout,Flatten
from keras.optimizers import Adam

path='data'
images=[]
classNo=[]
testRatio=0.2
valRatio=0.2
imageDimension=(32,32,3)

myList=os.listdir(path)

numOfClasses=len(myList)
#print(numOfClasses)

print("Importing Classes.....")
for x in range(0,numOfClasses):
	myPicList=os.listdir(path+"/"+str(x))
	for y in myPicList:
		curImg=cv2.imread(path+"/"+str(x)+"/"+y)
		curImg=cv2.resize(curImg,(imageDimension[0],imageDimension[1]))
		images.append(curImg)
		classNo.append(x)
	print(x)

images=np.array(images)
classNo=np.array(classNo)


x_train,x_test,y_train,y_test=train_test_split(images, classNo, test_size=testRatio)
x_train,x_validation,y_train,y_validation=train_test_split(x_train, y_train, test_size=valRatio)

numOfSample=[]

for x in range(0,numOfClasses):
	numOfSample.append(len(np.where(y_train==x)[0]))

plt.figure(figsize=(10,5))
plt.bar(range(0,numOfClasses),numOfSample)
plt.title("Bar plot of Classes & images")
plt.xlabel("No of Classes")
plt.ylabel("No OF Images")
plt.show()


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
x_train=np.array(list(map(preprocessing, x_train)))
x_test=np.array(list(map(preprocessing, x_test)))
x_validation=np.array(list(map(preprocessing, x_validation)))


x_train= x_train.reshape(x_train.shape[0],x_train.shape[1],x_train.shape[2],1)
x_test= x_test.reshape(x_test.shape[0],x_test.shape[1],x_test.shape[2],1)
x_validation= x_validation.reshape(x_validation.shape[0],x_validation.shape[1],x_validation.shape[2],1)



dataGen=ImageDataGenerator(
	width_shift_range=0.1,
	height_shift_range=0.1,
	zoom_range=0.2,
	shear_range=0.1,
	rotation_range=10)

dataGen.fit(x_train)

y_train=to_categorical(y_train, numOfClasses)
y_test=to_categorical(y_test, numOfClasses)
y_validation=to_categorical(y_validation, numOfClasses)


def myModel():
	noOfFilters=60
	sizeOfFilter1=(5,5)
	sizeOfFilter2=(3,3)
	sizeOfPool=(2,2)
	noOfNode=50

	model=Sequential()
	model.add((Conv2D(noOfFilters, sizeOfFilter1, input_shape=(imageDimension[0],imageDimension[1],1),activation='relu')))
	model.add((Conv2D(noOfFilters, sizeOfFilter1,activation='relu')))
	model.add(MaxPooling2D(pool_size=sizeOfPool))



	model.add((Conv2D(noOfFilters//2, sizeOfFilter2,activation='relu')))
	model.add((Conv2D(noOfFilters//2, sizeOfFilter2,activation='relu')))
	model.add(MaxPooling2D(pool_size=sizeOfPool))
	model.add(Dropout(0.5))


	model.add(Flatten())
	model.add(Dense(noOfNode, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(numOfClasses, activation='softmax'))
	model.compile(Adam(lr=0.001),loss='categorical_crossentropy',metrics=['accuracy'])
	return model

model=myModel()
print(model.summary())

history=model.fit(dataGen.flow(x_train, y_train,batch_size=5),
	#steps_per_epoch=10000,
	epochs=30,
	validation_data=(x_validation,y_validation),
	shuffle=1)

model.save("MyTrainingModel.h5")
print(history.history.keys())
plt.figure(1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='lower right')
plt.show()

plt.figure(2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()




