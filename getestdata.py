from PIL import Image
import numpy as np
import pickle

import csv

def Normalize(image,mean,std):
	for channel in range(3):
		image[:,:,channel]=(image[:,:,channel]-mean[channel])/std[channel]
	return image

id_to_data_test={}
id_to_size_test={}

lines = [] 

size=12816
with open("/content/drive/My Drive/flipkart_data/test.csv", 'r') as csvfile: 

	csvreader = csv.reader(csvfile)
	fields = next(csvreader)

	for row in csvreader:
		lines.append(row)

	# print(len(lines))
	id=0
	count=0
	for line in lines:
		if count>=0:
            

			path=line[0]
			print(id)
			# print("  ")
			# print(path)
			

			image=Image.open("/content/drive/My Drive/flipkart_data/testimage/"+path).convert('RGB')
			id_to_size_test[int(id)]=np.array(image,dtype=np.float32).shape[0:2]
			image=image.resize((224,224))
			image=np.array(image,dtype=np.float32)
			image=image/255
			image=Normalize(image,[0.485,0.456,0.406],[0.229,0.224,0.225])
			id_to_data_test[int(id)]=image

			id=id+1
			if(id==size):
				break
		count=count+1
		
		


id_to_data_test=np.array(list(id_to_data_test.values()))
id_to_size_test=np.array(list(id_to_size_test.values()))
f=open("/content/drive/My Drive/flipkart_data/id_to_data_test","wb+")
pickle.dump(id_to_data_test,f,protocol=4)
f=open("/content/drive/My Drive/flipkart_data/id_to_size_test","wb+")
pickle.dump(id_to_size_test,f,protocol=4)

id_to_box_test={}


lines1=[]
with open("/content/drive/My Drive/flipkart_data/test.csv", 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	fields = next(csvreader)

	for row in csvreader:
		lines1.append(row)
	id=0
	count=0
	for line in lines1:
		if count>=0:
			
	  
			box=[]
			x1=0
			x2=0
			y1=0
			y2=0
            
              
	  


			box.append(0)
			box.append(0)
			box.append(0)
			box.append(0)

			box=np.array([float(i) for i in box],dtype=np.float32)
			box[0]=box[0]/id_to_size_test[int(id)-1][1]*224
			box[1]=np.float32(y1)/id_to_size_test[int(id)-1][0]*224
			box[2]=(np.float32(x2)-np.float32(x1))/id_to_size_test[int(id)-1][1]*224
			box[3]=(np.float32(y2)-np.float32(y1))/id_to_size_test[int(id)-1][0]*224

			id_to_box_test[int(id)]=box
            
			id=id+1
			if(id==size):
				break;
		count=count+1

id_to_box_test=np.array(list(id_to_box_test.values()))
f=open("/content/drive/My Drive/flipkart_data/id_to_box_test","wb+") 
pickle.dump(id_to_box_test,f,protocol=4)
f=open("/content/drive/My Drive/flipkart_data/id_to_box_test","rb+") 
size=pickle.load(f)
print(size)



	  
	
		
		
	
  
   
	 
		 






