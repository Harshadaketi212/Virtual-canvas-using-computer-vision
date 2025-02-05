import cv2
import mediapipe as mp
import numpy as np
import math
import easyocr
from gtts import gTTS
import os
import pygame
# from extract_text_from_image import extract_text 
# from text_sound import produce_sound




# Global variables


colorNames = ['Green', 'Blue', 'Red']
colors = [(0, 255, 0), (255, 0 , 0), (0, 0, 255)]
positions = [
    [(50, 50), (175, 150)],
    [(200, 50), (325, 150)],
    [(350, 50), (475, 150)]
]
wordPositions = [
    (90, 100),
    (245, 100),
    (400, 100)
]
saveBoxPosition = [
    (475, 50),
    (600, 100)
]
color = (255, 0, 0)
in_save_area = False
def final(drawing,prev_point):

    canvas_save_path = '.'
    canvas = np.ones((480, 640, 3), dtype="uint8") * 255  # White canvas

    def img_text(canvas):
        reader = easyocr.Reader(['en'])

        # Path to your image file
        image_path = 'canvas.png'

        # Perform OCR on the image
        result = reader.readtext(image_path)

        # Extract and print the text from the OCR result
        print("hi")
        extracted_text = ' '.join([text[1] for text in result])
        print(extracted_text)
        final_text=''
        flag=0
        for letter in extracted_text:
            if(letter!=' '):
                final_text+=letter
            if( flag==0 and ((ord(letter)>96 and ord(letter)<123) or(ord(letter)>64 and ord(letter)<91)) ):
                cv2.imwrite(f'{letter}.png', canvas)
                flag=1


        print(final_text)


        tts = gTTS(text=final_text, lang='en')

        # Save the speech as an MP3 file
        tts.save('output.mp3')

        # Play the speech using the default media player (works on Windows)
        # os.system('start output.mp3')



        # Initialize pygame mixer
        pygame.mixer.init()

        # Load the MP3 file
        pygame.mixer.music.load('output.mp3')

        # Play the audio
        pygame.mixer.music.play()

        # Wait until the audio finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    # Function to calculate the distance between two points
    def calculate_distance(point1, point2):
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

    # Function for drawing on the canvas using the forefinger
    def draw_on_canvas(hand_landmarks):
        global drawing, prev_point

        # Get the index for the forefinger tip dynamically
        index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]

        # Extract the coordinates of the forefinger and thumb tips
        finger_tip = (int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0]))
        thumb_tip = (int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0]))

        # Draw a circle at the forefinger tip
        cv2.circle(frame, finger_tip, 5, (0, 255, 0), -1)

        # Calculate the distance between the forefinger and thumb tips
        distance = calculate_distance(finger_tip, thumb_tip)

        global color
        global in_save_area

        # set the color if it's near a box
        for i, (start_pos, end_pos) in enumerate(positions):
            if start_pos[0] < finger_tip[0] < end_pos[0] and start_pos[1] < finger_tip[1] < end_pos[1]:
                color = colors[i]
                break

        # give the option to save the canvas when in save box region
        if saveBoxPosition[0][0] < finger_tip[0] < saveBoxPosition[1][0] and saveBoxPosition[0][1] < finger_tip[1] < saveBoxPosition[1][1]:
            # Save the canvas
            if  in_save_area:
                pass
            else:
                print('save button clicked')
                canvas_path = canvas_save_path + 'canvas.png'
                cv2.imwrite('canvas.png', canvas)
                cv2.imwrite(canvas_save_path + 'frame.png', frame)
                in_save_area = True
                img_text(canvas)
                # text = extract_text(canvas_path)
                # print('text on the screen', text)
                # produce_sound(text)
        else :
            in_save_area = False


        # Update the canvas if drawing is enabled and the peace sign is detected
        if distance < 50:  # Adjust the threshold based on your preference
            drawing = True
            if(prev_point == -1):
                cv2.line(canvas, finger_tip, finger_tip, color, 1)
            else:
                cv2.line(canvas, prev_point, finger_tip, color, 10)
            prev_point = finger_tip
        else:
            drawing = False
            prev_point = -1



    # Set up the camera
    cap = cv2.VideoCapture(0)

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        for i in range(3):
            cv2.rectangle(frame, positions[i][0], positions[i][1], colors[i], -1 )
            cv2.putText(frame, colorNames[i], wordPositions[i], cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=(0, 0, 0), thickness=1)
        # cv2.rectangle(frame, (50, 50), (175, 150), (0, 255, 0), -1)
        # cv2.putText(frame, "Green", (90, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=(0, 0, 0), thickness=1)

        # # blue box
        # cv2.rectangle(frame, (200, 50), (325, 150), (255, 0 , 0), -1)
        # cv2.putText(frame, "blue", (245, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=(0, 0, 0), thickness=1)

        # # red box
        # cv2.rectangle(frame, (350, 50), (475, 150), (0, 0, 255), -1)
        # cv2.putText(frame, "Red", (400, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=(0, 0, 0), thickness=1)

        # save button 
        cv2.rectangle(frame, saveBoxPosition[0], saveBoxPosition[1], (255, 255, 255), -1)
        cv2.putText(frame, "save", (525, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=(0, 0, 0), thickness=1)


        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                draw_on_canvas(hand_landmarks)

        # Display the frames
        cv2.imshow("Frame", frame)
        cv2.imshow("Air Canvas", canvas)

        # Press 'Esc' to exit
        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == ord('c'):  # Press 'c' to clear the canvas
            canvas = np.ones((480, 640, 3), dtype="uint8") * 255

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

drawing = False
prev_point = -1
final(drawing,prev_point)