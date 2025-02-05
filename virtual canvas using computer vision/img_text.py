import easyocr
from gtts import gTTS
import os
import pygame
# Initialize the OCR reader
reader = easyocr.Reader(['en'])

# Path to your image file
image_path = 'canvas.png'

# Perform OCR on the image
result = reader.readtext(image_path)

# Extract and print the text from the OCR result
extracted_text = ' '.join([text[1] for text in result])

final_text=''

for letter in extracted_text:
    if(letter!=' '):
        final_text+=letter

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
