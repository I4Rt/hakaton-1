from ultralytics import YOLO
import cv2

model = YOLO('38ep.pt')  # Replace with your weights path
def give_result(frame):
    results = model(frame, conf=0.25)
    for result in results:
        boxes = result.boxes
        classes = 0
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            classes+=1
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f'Class: {cls}, Conf: {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
    return frame, classes#, classes

# Load the model with saved weights

# url = 'rtsp://admin:ask226226@192.168.1.168/'
# # Path to the image or video for testing
# cap = cv2.VideoCapture(url)

# while True:
#     res, frame = cap.read()
#     frame, cls = give_result(frame)#
#     print(cls)
#     #print(cls)
#    # print(type(frame), frame.size())
#     cv2.imshow('YOLOv8m detection', frame)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break  # Close all windows

# # Release resources
# cap.release()
# cv2.destroyAllWindows()

