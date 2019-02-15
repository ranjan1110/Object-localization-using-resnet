from PIL import Image
import numpy as np
import pickle

import csv

def Normalize(image,mean,std):
	for channel in range(3):
		image[:,:,channel]=(image[:,:,channel]-mean[channel])/std[channel]
	return image

id_to_data={}
id_to_size={}

lines = [] 

size=12816
with open("/content/drive/My Drive/flipkart_data/training.csv", 'r') as csvfile: 

	csvreader = csv.reader(csvfile)
	fields = next(csvreader)

	for row in csvreader:
		lines.append(row)

	# print(len(lines))
	id=0
	
	for line in lines:
		path=line[0]
		# print(id)
		# print("  ")
		# print(path)
		

		image=Image.open("/content/drive/My Drive/flipkart_data/trainingimage/"+path).convert('RGB')
		id_to_size[int(id)]=np.array(image,dtype=np.float32).shape[0:2]
		image=image.resize((224,224))
		image=np.array(image,dtype=np.float32)
		image=image/255
		image=Normalize(image,[0.485,0.456,0.406],[0.229,0.224,0.225])
		id_to_data[int(id)]=image

		id=id+1
		if(id==size):
			break
		
		


id_to_data=np.array(list(id_to_data.values()))
id_to_size=np.array(list(id_to_size.values()))
f=open("/content/drive/My Drive/flipkart_data/id_to_data","wb+")
pickle.dump(id_to_data,f,protocol=4)
f=open("/content/drive/My Drive/flipkart_data/id_to_size","wb+")
pickle.dump(id_to_size,f,protocol=4)

id_to_box={}


lines1=[]
with open("/content/drive/My Drive/flipkart_data/training.csv", 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	fields = next(csvreader)

	for row in csvreader:
		lines1.append(row)
	id=0

	for line in lines1:
		box=[]
		x1=line[1]
		x2=line[2]
		y1=line[3]
		y2=line[4]


		box.append(line[1])
		box.append(line[2])
		box.append(line[3])
		box.append(line[4])

		box=np.array([float(i) for i in box],dtype=np.float32)
		box[0]=box[0]/id_to_size[int(id)-1][1]*224
		box[1]=np.float32(y1)/id_to_size[int(id)-1][0]*224
		box[2]=(np.float32(x2)-np.float32(x1))/id_to_size[int(id)-1][1]*224
		box[3]=(np.float32(y2)-np.float32(y1))/id_to_size[int(id)-1][0]*224

		id_to_box[int(id)]=box
		id=id+1
		if(id==size):
			break;

id_to_box=np.array(list(id_to_box.values()))
f=open("/content/drive/My Drive/flipkart_data/id_to_box","wb+") 
pickle.dump(id_to_box,f,protocol=4)
f=open("/content/drive/My Drive/flipkart_data/id_to_box","rb+") 
size=pickle.load(f)
print(size)



	  
	
		
		
	
  
   
	 
		 






