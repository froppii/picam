from picamera2 import Picamera2, Preview
from gpiozero import Button, LED
import time, os

picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start_preview(Preview.QTGL)
picam2.start()

shutter_btn = Button(17)
mode_btn = Button(27)
zoom_in_btn = Button(22)
zoom_out_btn = Button(23)
power_btn = Button(24)

flash_led = LED(18) 

mode = "photo" 
video_active = False
zoom_level = 1.0
video_file = None

def take_photo():
    global flash_led
    flash_led.on()
    time.sleep(0.2) 
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"/home/pi/DCIM/photo_{timestamp}.jpg"
    picam2.capture_file(filename)
    flash_led.off()
    print("Photo saved:", filename)

def toggle_video():
    global video_active, video_file
    if not video_active:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        video_file = f"/home/pi/DCIM/video_{timestamp}.mp4"
        picam2.start_recording(video_file)
        video_active = True
        print("Video recording started:", video_file)
    else:
        picam2.stop_recording()
        video_active = False
        print("Video saved:", video_file)

def change_mode():
    global mode
    if mode == "photo":
        mode = "video"
    else:
        mode = "photo"
    print("Mode switched to", mode)

def zoom_in():
    global zoom_level
    zoom_level = min(2.0, zoom_level + 0.1)
    picam2.set_controls({"ScalerCrop": picam2.capture_metadata()['ScalerCrop']})
    print("Zoom in:", zoom_level)

def zoom_out():
    global zoom_level
    zoom_level = max(1.0, zoom_level - 0.1)
    picam2.set_controls({"ScalerCrop": picam2.capture_metadata()['ScalerCrop']})
    print("Zoom out:", zoom_level)

shutter_btn.when_pressed = lambda: take_photo() if mode == "photo" else toggle_video()
mode_btn.when_pressed = change_mode
zoom_in_btn.when_pressed = zoom_in
zoom_out_btn.when_pressed = zoom_out

print("Camera ready! Press buttons to test.")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    picam2.stop()
    print("Camera shutdown.")
