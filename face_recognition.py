from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
from time import strftime
import os
from datetime import datetime
# Remove circular import
# from face_recognition import Face_Recognition
from train import train
from student import Student

import cv2



class Face_Recognition:
     def __init__(self,root):
          self.root=root
          self.root.geometry("1530x790+0+0")
          self.root.title("Face Recognition System")


          title_lbl=Label(self.root,text="Face Recognition",font =("times new roman",35,"bold"),bg="white",fg="green")
          title_lbl.place(x=0,y=0,width=1530,height=45)
# 1st image
          img_top=Image.open(r"E:\project\Face recognition system\Face-Recognition-Based-Attendance-System\college_images\face_detector1.jpg")
          img_top=img_top.resize((650,700),Image.BILINEAR)
          self.photoimg_top=ImageTk.PhotoImage(img_top)

          f_lbl=Label(self.root,image=self.photoimg_top)
          f_lbl.place(x=0,y=55,width=650,height=700)
# 2nd image
          img_bottom=Image.open(r"E:\project\Face recognition system\Face-Recognition-Based-Attendance-System\college_images\facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
          img_bottom=img_bottom.resize((950,700),Image.BILINEAR)
          self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)

          f_lbl=Label(self.root,image=self.photoimg_bottom)
          f_lbl.place(x=650,y=55,width=950,height=700)
          
          #   button
          b1=Button(f_lbl,text="Face Recognition",command=self.face_recog,cursor="hand2",font =("times new roman",18,"bold"),bg="darkgreen",fg="white")
          b1.place(x=365,y=620,width=200,height=40)
        #   =========Attendance==============
     def mark_attendence(self, i, r, n, d):
          try:
               # Create file if it doesn't exist
               csv_path = os.path.join(os.getcwd(), "priyam.csv")
               print(f"Attendance file path: {csv_path}")
               
               if not os.path.exists(csv_path):
                    with open(csv_path, "w", newline="") as f:
                         f.write("ID,Roll,Name,Department,Time,Date,Status\n")
                         print("Created new attendance file")
               
               # Read existing data
               with open(csv_path, "r") as f:
                    myDatalist = f.readlines()
               
               # Extract IDs
               name_list = []
               for line in myDatalist:
                    if line.strip():  # Skip empty lines
                         entry = line.strip().split(",")
                         if len(entry) > 0:
                              name_list.append(entry[0])
               
               # Get current time
               now = datetime.now()
               d1 = now.strftime("%d/%m/%Y")
               dtString = now.strftime("%H:%M:%S")
               
               # Check if already marked
               print(f"Checking if ID {i} is in {name_list}")
               if i not in name_list:
                    # Append to file
                    with open(csv_path, "a", newline="") as f:
                         f.write(f"{i},{r},{n},{d},{dtString},{d1},Present\n")
                         print(f"Wrote attendance for {n} with ID {i}")
                    messagebox.showinfo("Success", f"Attendance marked for {n}", parent=self.root)
               else:
                    print(f"ID {i} already exists in attendance file")
          except Exception as e:
               print(f"Error marking attendance: {str(e)}")
               messagebox.showerror("Error", f"Error marking attendance: {str(e)}", parent=self.root)

     #   =============face recognition============
     def face_recog(self):
          def draw_boundary(img,classifier,scaleFactor,minNeighbors,color,text,clf):
               gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
               features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

               coord=[]

               for(x,y,w,h) in features:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                    id,predict=clf.predict(gray_image[y:y+h,x:x+w])
                    confidence=int((100*(1-predict/300)))
                    print(f"Face detected - ID: {id}, Confidence: {confidence}%")

                    try:
                         conn=mysql.connector.connect(host="localhost",user="root",password="0542me121107",database="sys")
                         my_cursor=conn.cursor()

                         my_cursor.execute("select Name from student where Student_id="+str(id))
                         n=my_cursor.fetchone()
                         if n:
                              n="+".join(n)
                         else:
                              n="Unknown"

                         my_cursor.execute("select Roll from student where Student_id=" + str(id))
                         r = my_cursor.fetchone()
                         if r:
                              r = "+".join(r)
                         else:
                              r="Unknown"

                         my_cursor.execute("select Dep from student where Student_id=" + str(id))
                         d = my_cursor.fetchone()
                         if d:
                              d = "+".join(d)
                         else:
                              d="Unknown"

                         my_cursor.execute("select Student_id from student where Student_id=" + str(id))
                         i = my_cursor.fetchone()
                         if i:
                              i = "+".join(map(str, i))
                         else:
                              i="Unknown"

                         # Lower the confidence threshold from 77 to 50
                         if confidence>50:
                              cv2.putText(img,f"ID:{i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                              cv2.putText(img,f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                              cv2.putText(img,f"Name:{n}", (x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                              cv2.putText(img,f"Department:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                              cv2.putText(img,f"Confidence:{confidence}%",(x,y+20),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                              # Store recognized face data in a global variable to mark attendance only once per session
                              if i != "Unknown" and n != "Unknown":
                                   print(f"Marking attendance for {n} with ID {i}")
                                   self.mark_attendence(i,r,n,d)
                         else:
                              cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                              cv2.putText(img,"Unknown Face", (x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    except Exception as e:
                         cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                         cv2.putText(img,"Unknown Face", (x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                         print(f"Database error: {str(e)}")

                    coord=[x,y,w,h]
               
               return coord

          def recognize(img,clf,faceCascade):
               coord=draw_boundary(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
               return img

          try:
               # Check if classifier.xml exists
               if not os.path.exists("classifier.xml"):
                    messagebox.showerror("Error", "Classifier file not found. Please train the model first.", parent=self.root)
                    return
                    
               # Use absolute path for cascade classifier
               cascade_path = os.path.join(os.getcwd(), "haarcascade_frontalface_default.xml")
               if not os.path.exists(cascade_path):
                    messagebox.showerror("Error", f"Cascade file not found at {cascade_path}", parent=self.root)
                    return
                    
               faceCascade=cv2.CascadeClassifier(cascade_path)
               
               # Print classifier info
               print(f"Using classifier from: {os.path.abspath('classifier.xml')}")
               
               # Create face recognizer with adjusted parameters
               clf=cv2.face.LBPHFaceRecognizer_create(
                    radius=1,        # Default is 1
                    neighbors=8,     # Default is 8
                    grid_x=8,        # Default is 8
                    grid_y=8,        # Default is 8
                    threshold=100    # Default is usually higher, lowering it
               )
               clf.read("classifier.xml")

               # Create priyam.csv if it doesn't exist
               if not os.path.exists("priyam.csv"):
                    with open("priyam.csv", "w") as f:
                         f.write("ID,Roll,Name,Department,Time,Date,Status\n")

               # Try to use alternative display method without cv2.imshow
               try:
                    import tkinter as tk
                    from PIL import Image, ImageTk
                    
                    # Create a new window for displaying video
                    video_window = tk.Toplevel(self.root)
                    video_window.title("Face Recognition")
                    video_window.geometry("800x600")
                    
                    # Create a label for displaying video frames
                    video_label = tk.Label(video_window)
                    video_label.pack(fill=tk.BOTH, expand=True)
                    
                    # Create a button to stop recognition
                    stop_button = tk.Button(video_window, text="Stop Recognition", 
                                          command=lambda: video_window.destroy())
                    stop_button.pack(pady=10)
                    
                    # Start video capture
                    video_cap = cv2.VideoCapture(0)
                    
                    # Function to update frames
                    def update_frame():
                        ret, img = video_cap.read()
                        if ret:
                            # Process the frame
                            img = recognize(img, clf, faceCascade)
                            
                            # Convert to format tkinter can display
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img = Image.fromarray(img)
                            img = ImageTk.PhotoImage(image=img)
                            
                            # Update the label
                            video_label.configure(image=img)
                            video_label.image = img
                            
                            # Schedule the next update
                            video_window.after(10, update_frame)
                        else:
                            messagebox.showerror("Error", "Camera not accessible", parent=self.root)
                            video_window.destroy()
                    
                    # Start updating frames
                    update_frame()
                    
                    # Wait until window is closed
                    video_window.protocol("WM_DELETE_WINDOW", lambda: video_window.destroy())
                    video_window.wait_window()
                    
                    # Release resources
                    video_cap.release()
                    
               except Exception as e:
                    messagebox.showerror("Error", f"Error displaying video: {str(e)}", parent=self.root)
          except Exception as e:
               messagebox.showerror("Error", f"Error in face recognition: {str(e)}", parent=self.root)











if __name__ == "__main__":
     root=Tk()
     obj=Face_Recognition(root)
     root.mainloop()