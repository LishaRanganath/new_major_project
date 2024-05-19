import moviepy.editor as mp
import speech_recognition as sr
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap


# Function to extract audio from video
def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)


# Function to transcribe audio to text
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_path)
    with audio as source:
        audio_file = recognizer.record(source)
    transcribed_text = recognizer.recognize_google(audio_file)
    return transcribed_text


# Function to convert text to PDF
def convert_to_pdf(text, pdf_file_path):
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    lines = text.split("\n")
    about_printed = False  # Flag to track if the "About" heading is printed
    y_position = 750  # Initial y position for the text

    for line in lines:
        if "about" in line.lower() and not about_printed:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, y_position, "About:")
            text_width = c.stringWidth("About:", "Helvetica-Bold", 16)  # Get the width of the text
            c.line(100, y_position - 5, 100 + text_width, y_position - 5)  # Add underline aligned with the text
            c.setFont("Helvetica", 12)
            y_position -= 30  # Move y position up for the next line
            about_printed = True

        wrapped_lines = textwrap.wrap(line, width=70)  # Wrap the line within 70 characters
        for wrapped_line in wrapped_lines:
            c.drawString(100, y_position, wrapped_line.strip())
            y_position -= 20  # Move y position up for the next line
            if y_position < 50:  # Check if we reach the bottom of the page
                c.showPage()  # Start a new page
                y_position = 750  # Reset y position to the top of the new page

    c.save()


# Example usage
video_path = 'test4.mp4'
audio_path = 'audio.wav'
pdf_file_path = 'transcribed_text.pdf'

# Extract audio from video
extract_audio(video_path, audio_path)

# Transcribe audio to text
try:
    transcribed_text = transcribe_audio(audio_path)
except sr.UnknownValueError:
    print("Speech recognition could not understand audio")
    exit(1)

# Convert transcribed text to PDF
convert_to_pdf(transcribed_text, pdf_file_path)

print("PDF generation complete.")
