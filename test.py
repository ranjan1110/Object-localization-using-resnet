import pickle
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.models import load_model
import random
from keras import backend as K
import csv
import keras.losses
# keras.losses.custom_loss = smooth_l1_loss


def smooth_l1_loss(true_box,pred_box):
	loss=0.0
	for i in range(4):
		residual=K.tf.abs(true_box[:,i]-pred_box[:,i]*224)
		condition=K.tf.less(residual,1.0)
		small_res=0.5*K.tf.square(residual)
		large_res=residual-0.5
		loss=loss+K.tf.where(condition,small_res,large_res)
	return K.tf.reduce_mean(loss)


def my_metric(labels,predictions):
	threshhold=0.75
	x=predictions[:,0]*224
	x=K.tf.maximum(K.tf.minimum(x,224.0),0.0)
	y=predictions[:,1]*224
	y=K.tf.maximum(K.tf.minimum(y,224.0),0.0)
	width=predictions[:,2]*224
	width=K.tf.maximum(K.tf.minimum(width,224.0),0.0)
	height=predictions[:,3]*224
	height=K.tf.maximum(K.tf.minimum(height,224.0),0.0)
	label_x=labels[:,0]
	label_y=labels[:,1]
	label_width=labels[:,2]
	label_height=labels[:,3]
	a1=K.tf.multiply(width,height)
	a2=K.tf.multiply(label_width,label_height)
	x1=K.tf.maximum(x,label_x)
	y1=K.tf.maximum(y,label_y)
	x2=K.tf.minimum(x+width,label_x+label_width)
	y2=K.tf.minimum(y+height,label_y+label_height)
	IoU=K.tf.abs(K.tf.multiply((x1-x2),(y1-y2)))/(a1+a2-K.tf.abs(K.tf.multiply((x1-x2),(y1-y2))))
	condition=K.tf.less(threshhold,IoU)
	sum=K.tf.where(condition,K.tf.ones(K.tf.shape(condition)),K.tf.zeros(K.tf.shape(condition)))
	return K.tf.reduce_mean(sum)


plt.switch_backend('agg')
size_of_file = 12816

f=open("/content/drive/My Drive/flipkart_data/id_to_data_test","rb+")
data_test=pickle.load(f)

f=open("/content/drive/My Drive/flipkart_data/id_to_box_test","rb+")
box=pickle.load(f)

f=open("/content/drive/My Drive/flipkart_data/id_to_size_test","rb+") 
size_test=pickle.load(f)

index=[i for i in range(size_of_file)]
# index=random.sample(index,5)


model=keras.models.load_model("/content/model.h5", custom_objects={'smooth_l1_loss': smooth_l1_loss,'my_metric':my_metric})
result=model.predict(data_test[index,:,:,:])

mean=[0.485,0.456,0.406]
std=[0.229,0.224,0.225]

a = result
with open("output.csv","w+") as my_csv:
	csvWriter = csv.writer(my_csv,delimiter=',')
	csvWriter.writerows(a)


j=0

my_list=[]
with open("/content/drive/My Drive/flipkart_data/test.csv") as f:
	csv_reader=csv.reader(f)
	counter=0
	for line in csv_reader:
		my_list.append([line[0]])
		counter=counter+1
# 		print(counter)


my_list[0].append('x1')
my_list[0].append('x2')
my_list[0].append('y1')
my_list[0].append('y2')

list_index=1
x11=0
y11=0
w=0;
h=0;

for row in result:
	count=0;
	for cordinate in row:
		if count%4==0 or count%4==2:
			cordinate=cordinate*640
			if count%4==0:
			  x11=cordinate
			else:
			  w=cordinate

			  
			
		else :
			cordinate=cordinate*480
			if count%4==1:
			  y11=cordinate
			else :
			  h=cordinate
		
		count=count+1;
		
	my_list[list_index].append(x11)
	my_list[list_index].append(x11+w)
	my_list[list_index].append(y11)
	my_list[list_index].append(y11+h)
    
	
	list_index=list_index+1
	print(list_index)
with open("/content/drive/My Drive/flipkart_data/my_output.csv","w+") as output:
	writer = csv.writer(output, lineterminator='\n')
	for val in my_list:
		writer.writerow(val)  




# j=0
# for i in index:
#     print("Predicting "+str(i)+"th image.")
#     true_box=box[i]
#     image=data[i]
#     prediction=result[j]
#     j+=1
#     for channel in range(3):
#         image[:,:,channel]=image[:,:,channel]*std[channel]+mean[channel]

#     image=image*255
#     image=image.astype(np.uint8)
#     plt.imshow(image)


#     plt.gca().add_patch(plt.Rectangle((true_box[0],true_box[1]),true_box[2],true_box[3],fill=False,edgecolor='red',linewidth=2,alpha=0.5))
#     plt.gca().add_patch(plt.Rectangle((prediction[0]*224,prediction[1]*224),prediction[2]*224,prediction[3]*224,fill=False,edgecolor='green',linewidth=2,alpha=0.5))
#     plt.show()
#     plt.savefig("/content/drive/My Drive/flipkart_data/prediction/"+str(i)+".png",format='png')
#     plt.cla()
