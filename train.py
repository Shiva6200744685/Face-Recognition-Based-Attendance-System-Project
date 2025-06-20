from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import numpy as np
import os



class train:
     def __init__(self,root):
          self.root=root
          self.root.geometry("1530x790+0+0")
          self.root.title("Face Recognition System")

          title_lbl=Label(self.root,text="TRAIN DATA SET",font =("times new roman",35,"bold"),bg="white",fg="red")
          title_lbl.place(x=0,y=0,width=1530,height=45)

          img_top=Image.open(r"E:\project\Face recognition system\Face-Recognition-Based-Attendance-System\college_images\facialrecognition.png")
          img_top=img_top.resize((1530,325),Image.BILINEAR)
          self.photoimg_top=ImageTk.PhotoImage(img_top)

          f_lbl=Label(self.root,image=self.photoimg_top)
          f_lbl.place(x=0,y=55,width=1530,height=325)

        #   button
          b1=Button(self.root,text="TRAIN DATA",command=self.train_classifier,cursor="hand2",font =("times new roman",30,"bold"),bg="red",fg="white")
          b1.place(x=0,y=380,width=1530,height=60)


          img_bottom=Image.open(r"E:\project\Face recognition system\Face-Recognition-Based-Attendance-System\college_images\opencv_face_reco_more_data.jpg")
          img_bottom=img_bottom.resize((1530,325),Image.BILINEAR)
          self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)

          f_lbl=Label(self.root,image=self.photoimg_bottom)
          f_lbl.place(x=0,y=440,width=1530,height=325)


     def train_classifier(self):
          data_dir=("data")
          try:
               # Check if data directory exists and has files
               if not os.path.exists(data_dir):
                    messagebox.showerror("Error", "Data directory not found", parent=self.root)
                    return
               
               if len(os.listdir(data_dir)) == 0:
                    messagebox.showerror("Error", "No training data found. Please add face samples first.", parent=self.root)
                    return
               
               path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]

               faces=[]
               ids=[]

               for image in path:
                    try:
                         # Only process image files with .jpg, .jpeg, or .png extensions
                         if image.lower().endswith(('.jpg', '.jpeg', '.png')):
                              img=Image.open(image).convert('L') # Gray scale image
                              imageNp=np.array(img,'uint8')
                              
                              # Extract ID from filename (user.1.1.jpg) - more robust parsing
                              filename = os.path.basename(image)
                              parts = filename.split('.')
                              if len(parts) >= 2:
                                   id=int(parts[1])  # Get the second part as ID
                                   
                                   faces.append(imageNp)
                                   ids.append(id)
                                   # Skip showing images during training - causes errors with headless OpenCV
                                   # cv2.imshow("Training",imageNp)
                                   # cv2.waitKey(1)
                    except Exception as e:
                         print(f"Error processing image {image}: {str(e)}")  # Print to console for debugging
                         # Don't show error for each image to avoid multiple popups
                         continue
               
               if len(faces) == 0:
                    messagebox.showerror("Error", "No valid face images found for training", parent=self.root)
                    # Skip destroyAllWindows - causes errors with headless OpenCV
                    # cv2.destroyAllWindows()
                    return
                    
               ids=np.array(ids)

               #=================Train the classifier and save==================
               # Try different methods to create the face recognizer
               try:
                    # First attempt - direct import
                    from cv2 import face
                    clf = face.LBPHFaceRecognizer_create()
               except:
                    try:
                         # Second attempt - using cv2.face_LBPHFaceRecognizer
                         clf = cv2.face_LBPHFaceRecognizer.create()
                    except:
                         # Third attempt - using createLBPHFaceRecognizer
                         clf = cv2.createLBPHFaceRecognizer()
               
               # Train the classifier
               clf.train(faces,ids)
               clf.write("classifier.xml")
               # Skip destroyAllWindows - causes errors with headless OpenCV
               # cv2.destroyAllWindows()
               # Force update the window to ensure message box appears
               self.root.update()
               messagebox.showinfo("Result","Training datasets completed!!")
          except Exception as e:
               # Skip destroyAllWindows - causes errors with headless OpenCV
               # cv2.destroyAllWindows()
               messagebox.showerror("Error", f"Error during training: {str(e)}", parent=self.root)




  





          
if __name__ == "__main__":
     root=Tk()
     obj=train(root)
     root.mainloop()