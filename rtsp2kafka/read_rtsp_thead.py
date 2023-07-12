import cv2
import time
import threading
import copy
import zmq

from kafka import KafkaProducer
from kafka.errors import KafkaError

import kafka
print(kafka.__version__)

import multiprocessing as mp
from datetime import datetime

class Camera():
    
    def __init__(self, rtsp_url):        
        self.frame = None
        self.percent = 0.65
        self.ratio = 2
    
        #load pipe for data transmittion to the process
        self.parent_conn, child_conn = mp.Pipe()
        #load process
        self.p = mp.Process(target=self.update, args=(child_conn,rtsp_url))        
        #start process
        self.p.daemon = True
        self.p.start()

        self.threadActive = False
        self.thd = threading.Thread(target=self.camera_run)
        self.thd.start()

    def camera_run(self):
        # Variables for FPS calculation
        fps_start_time = time.time()
        fps_frame_count = 0
        fps = 0
        old_frame = None

        print(f"Camera is alive?: {self.p.is_alive()}")

        while(1):
            self.threadActive = True
            self.frame = copy.deepcopy(self.get_frame())
            
            # Increment frame count for FPS calculation
            fps_frame_count += 1

            # Calculate elapsed time since the last FPS calculation
            elapsed_time = time.time() - fps_start_time

            # Update FPS every second
            if elapsed_time >= 1.0:
                fps = fps_frame_count / elapsed_time
                fps_frame_count = 0
                fps_start_time = time.time()

            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            
            # Draw FPS on the frame
            cv2.putText(self.frame, "{} --> FPS: {:.2f}".format(date_time, fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            dim = (int(self.frame.shape[1]/self.ratio), int(self.frame.shape[0]/self.ratio))
            #print(dim)
            self.frame = cv2.resize(self.frame, dim, interpolation=cv2.INTER_AREA)
            #self.frame = cv2.resize(self.frame, None, fx=self.percent, fy=self.percent)

            old_frame = self.frame

            cv2.imshow("Feed", self.frame)
            
            # Check for the 'q' key to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.threadActive = False
        cv2.destroyAllWindows()     

        self.end()
        
    def end(self):
        #send closure request to process
        
        self.parent_conn.send(2)
        self.p.join()
        
    def update(self,conn,rtsp_url):
        #load cam into seperate process
        
        print("Cam Loading...")
        #cap = cv2.VideoCapture(rtsp_url,cv2.CAP_FFMPEG)   
        cap = cv2.VideoCapture(rtsp_url)   
        print("Cam Loaded...")
        run = True
        
        while run:
            #grab frames from the buffer
            cap.grab()
            
            #recieve input data
            rec_dat = conn.recv()
            
            if rec_dat == 1:
                #if frame requested
                ret,frame = cap.read()
                conn.send(frame)
                
            elif rec_dat == 2:
                #if close requested
                cap.release()
                run = False
                
        print("Camera Connection Closed")        
        conn.close()
    
    def get_frame(self):
        ###used to grab frames from the cam connection process
        
        ##[resize] param : % of size reduction or increase i.e 0.65 for 35% reduction  or 1.5 for a 50% increase
             
        #send request
        self.parent_conn.send(1)
        frame = self.parent_conn.recv()
        
        #reset request 
        self.parent_conn.send(0)
        
        return frame
        
    def rescale_frame(self,frame, percent=65):
        return cv2.resize(frame,None,fx=percent,fy=percent) 

class KafkaUploader():
    def __init__(self, _url):
        self.camera = Camera("rtsp://admin:P@ssw0rd1339@192.168.110.11:554/cam/realmonitor?channel=1&subtype=0")
        time.sleep(3)

        self.producer = KafkaProducer(bootstrap_servers=_url, api_version=(2,0,2))
        self.topic = 'video_topic'
        
        self.upload_fps = -1

        self.thd = threading.Thread(target=self.run)
        self.thd.start()
    
    def run(self):
        # Variables for FPS calculation
        upload_start_time = time.time()
        upload_frame_count = 0

        while self.camera.threadActive:
            t0 = time.time()
            frame = copy.deepcopy(self.camera.frame)
            t1 = time.time() - t0
        
            # png might be too large to emit
            data = cv2.imencode('.jpeg', frame)[1].tobytes()
            t2 = time.time() - t0

            future = self.producer.send(self.topic, data)
            t3 = time.time() - t0
            try:
                future.get(timeout=5)
            except KafkaError as e:
                print(e)
                break
            t4 = time.time() - t0

            # Increment frame count for FPS calculation
            upload_frame_count += 1

            # Calculate elapsed time since the last FPS calculation
            elapsed_time = time.time() - upload_start_time

            # Update FPS every second
            if elapsed_time >= 1.0:
                self.upload_fps = upload_frame_count / elapsed_time
                upload_frame_count = 0
                upload_start_time = time.time()

            t4 -= t3
            t3 -= t2
            t2 -= t1
            xxx = [t1,t2,t3,t4]
            xxx = [int(k*1000) for k in xxx]
            print('Upload FPS : {:.2f} --> {}'.format(self.upload_fps, xxx), flush=True)

def main():
    uploader = KafkaUploader(_url='10.10.10.25:9092')
    #uploader = KafkaUploader(_url='localhost:9092')

if __name__ == "__main__":
    main()