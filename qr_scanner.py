import cv2
import time
import os
import pyttsx3
import numpy as np
from pyzbar.pyzbar import decode
from urllib.parse import urlparse, parse_qs

class UPI_QR_CodeDetector:
    def detect(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return decode(gray_frame)

    def parse(self, qr_data):
        if not qr_data.startswith("upi://"):
            return None       
        
        parsed = urlparse(qr_data)
        params = parse_qs(parsed.query)

        return {
            "UPI ID": params.get("pa", ["N/A"])[0],
            "Pay to": params.get("pn", ["N/A"])[0],
        }


    def extract(self, qr_codes):
        ding_sound = "ding-101492.mp3"
        engine = pyttsx3.init()

        for qr_code in qr_codes:
            qr_data = qr_code.data.decode('utf-8')
            upi_info = self.parse(qr_data)

            if upi_info:
                print("\nUPI QR Code is detected")
                for key, value in upi_info.items():
                    print(f"{key}: {value}")

                engine.say(upi_info)
                engine.runAndWait()

                webm_filename = "dingding.webm"
                os.system(f"ffmpeg -i {ding_sound} -c:a libopus -b:a 128k {webm_filename}")
                os.system(f"start {webm_filename}")

                return True
            else:
                print("this isnt a valid UPI QR code.")

            
    def rect_drawing(self, frame, qr_codes):

        h, w, _ = frame.shape

        for qr_code in qr_codes:
            points = qr_code.polygon

            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype = np.float32))
                cv2.polylines(frame, [hull], True, (255, 0, 255), 3)
            else:
                cv2.polylines(frame, [np.array(points, dtype = np.int32)], True, (255, 0, 255), 3)

            x_min, y_min = min(point.x for point in points), min(point.y for point in points)
            x_max, y_max = max(point.x for point in points), max(point.y for point in points)

    def run(self):
        cam = cv2.VideoCapture(0)

        while True:
            ret, frame = cam.read()
            if not ret:
                break

            qr_codes = self.detect(frame)
            result = self.extract(qr_codes)

            if result:
                break
                
            self.rect_drawing(frame, qr_codes)

            cv2.imshow("UPI QR Code Scanner", frame)
            time.sleep(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
   
    cv2.destroyAllWindows()


if __name__ == "__main__":
    qr_detector = UPI_QR_CodeDetector()
    qr_detector.run()
