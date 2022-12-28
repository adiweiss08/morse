import cv2
import dlib
from datetime import datetime
from builtins import len

import eye_ratio_utils
from morse_decoder import Morse_decoder


# Constants:
BLINKING_TIME_DASH_DOT_THRESHOLD = 0.9

ESC_ASCII_CODE = 27

# The max ratio between the eye width and the eye height which used to indicate if the eye is closed or open.
# It might need calibration per user
RATIO_OF_BLINKING = 5

# The duration time needed to end a signs (dot or dash) sequence
SEQ_PAUSE_DURATION = 3

# Convert the blinking time to a dot or a dash. (True means dasg, False means dot)
def convert_blink_to_sign(blinking_time):
    return True if blinking_time > BLINKING_TIME_DASH_DOT_THRESHOLD else False

# Add dash or dot to the signs_str
def add_dash_or_dot_to_according_to_blinking_time(blinking_time, signs_str):
    if convert_blink_to_sign(blinking_time):
        print('------')
        str = signs_str + '-'
    else:
        print('.')
        str = signs_str + '.'
    return str

# Prints the correct character according to the input signs sequence
def calc_sequence(sings_seq, morse_decoder):
    print(sings_seq)
    letter = morse_decoder.convert_sign_seq_to_letter(sings_seq)
    if letter:
        print(letter)
        # Todo: print the letter to the screen
    else:
        print("INVALID SEQUENCE OF DOT AND DASH!")


# This method returns True if the detected eyes are closed
def detect_closed_eyes(predictor, frame, face):
    # Detects the eye, uses the "shape predictor 68 face landmark" technic.
    # The points that include the eye are  36 - 46
    landmarks = predictor(frame, face)

    # The left eye detection
    left_eye_ratio = eye_ratio_utils.calulate_eye_width_to_height_ratio([36, 37, 38, 39, 40, 41], landmarks)
    # The right eye detection
    right_eye_ratio = eye_ratio_utils.calulate_eye_width_to_height_ratio([42, 43, 44, 45, 46, 47], landmarks)

    # The average of the ratio from both eyes
    avg_ratio = (left_eye_ratio + right_eye_ratio) / 2
    return avg_ratio > RATIO_OF_BLINKING

def main():
    # Initialization the video cap
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # the face dot layout

    morse_decoder = Morse_decoder()

    eyes_closed = False
    # Contains the sequence of signs (dots and dashes) of the current letter progress
    global signs_str
    signs_str = ""
    close_to_open_timestamp = datetime.now()
    open_to_close_timestamp = datetime.now()

    # The following variable indicates that a sign sequence is in process (True means that seq is not done yet)
    seq_in_progress = False

    # Main loop, running and analyzing the video frames until esc is pressed
    while True:
        # Read a frame from the camera
        _, frame = cap.read()

        # Flip the frame (mirror)
        frame = cv2.flip(frame, 1)

        # An array of faces in frames from the camera
        # The detector method get a frame and returns array of faces
        faces = detector(frame)

        # Skip in case there are no faces in the frame
        if len(faces) != 0:
            # For now analyzing only the first face
            face = faces[0]

            # Detect blinking
            if detect_closed_eyes(predictor, frame, face):
                if not eyes_closed:
                    open_to_close_timestamp = datetime.now()
                cv2.putText(frame, "Blink", (200, 75), font, 2, (100, 100, 100), 3)
                eyes_closed = True
                seq_in_progress = True


            elif eyes_closed:
            # This case indicates that we have moved from closed eyes to open eyes
                # Calculate the blinking time (the time that the eyes were closed)
                blinking_duration = datetime.now() - open_to_close_timestamp
                eyes_closed = False

                signs_str = add_dash_or_dot_to_according_to_blinking_time(blinking_duration.total_seconds(), signs_str)

                close_to_open_timestamp = datetime.now()

            else:
                # Eyes are still open
                time_past_from_last_blink = datetime.now() - close_to_open_timestamp
                if seq_in_progress and time_past_from_last_blink.total_seconds() > SEQ_PAUSE_DURATION:
                    print("We have new sequence")
                    cv2.putText(frame, "New tav", (100, 200), font, 3, (200, 100, 100), 3)
                    seq_in_progress = False
                    calc_sequence(signs_str, morse_decoder)
                    signs_str = ""
                    print("**************************************************")

        else:
            cv2.putText(frame, "No face detected", (150,150) ,font, 1, 225, 3)

        # Display the frame
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)

        # Exit upon esc button
        if key == ESC_ASCII_CODE:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()