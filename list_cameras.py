import cv2

def list_cameras(max_index=5):
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera {i}: OK")
            cap.release()
        else:
            print(f"Camera {i}: NOT AVAILABLE")

if __name__ == "__main__":
    list_cameras(5)
