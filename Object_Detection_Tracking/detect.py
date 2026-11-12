
from ultralytics import YOLO
import cv2
import csv
import os
from datetime import datetime

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Object Detection and Tracking Started!")
print("Press Q to stop.")

# Create CSV file to store detection history
csv_filename = "detection_history.csv"

file_exists = os.path.isfile(csv_filename) and os.path.getsize(csv_filename) > 0

csv_file = open(csv_filename, "a", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)

# Add headings if the file is new or empty
if not file_exists:
    csv_writer.writerow([
        "Date",
        "Time",
        "Object Name",
        "Tracking ID"
    ])

# Store IDs already saved during this session
logged_ids = set()

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read webcam frame.")
            break

        # Detect and track objects
        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml"
        )

        # Draw boxes, labels and tracking IDs
        annotated_frame = results[0].plot()

        # Count currently detected objects
        object_count = len(results[0].boxes)

        # Save each newly detected object
        if results[0].boxes is not None:

            for box in results[0].boxes:

                if box.id is not None:

                    tracking_id = int(box.id[0])
                    class_id = int(box.cls[0])
                    object_name = model.names[class_id]

                    # Save each tracking ID only once
                    if tracking_id not in logged_ids:

                        current_date = datetime.now().strftime("%Y-%m-%d")
                        current_time = datetime.now().strftime("%H:%M:%S")

                        csv_writer.writerow([
                            current_date,
                            current_time,
                            object_name,
                            tracking_id
                        ])

                        csv_file.flush()

                        logged_ids.add(tracking_id)

                        print(
                            "Saved:",
                            object_name,
                            "ID:",
                            tracking_id
                        )

        # Display object count
        cv2.putText(
            annotated_frame,
            f"Objects Detected: {object_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Display output
        cv2.imshow(
            "Object Detection and Tracking",
            annotated_frame
        )

        # Press Q to stop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    csv_file.close()
    cap.release()
    cv2.destroyAllWindows()

print("Detection stopped.")
print("Detection history saved in:", csv_filename)
