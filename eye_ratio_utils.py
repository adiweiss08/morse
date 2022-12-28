import math


# Returns the middle point between two points.
# Returns the middle point of the vertical line of the eye
def __midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


# Calculates the ratio between the eye width and the eye height
def calulate_eye_width_to_height_ratio(eye_point, facial_landmarks):
    # Calculates the left and the right point of the eye

    # The left point in eye is dot number 0
    left_point_of_the_eye = (facial_landmarks.part(eye_point[0]).x, facial_landmarks.part(eye_point[0]).y)

    # The right point in eye is dot number 3
    right_point_of_the_eye = (facial_landmarks.part(eye_point[3]).x, facial_landmarks.part(eye_point[3]).y)

    # Calculates the center point of the top of the eye by finding the middle point of the top two points in the face landmark technic
    center_top = __midpoint(facial_landmarks.part(eye_point[1]), facial_landmarks.part(eye_point[2]))

    # Calculates the center point of the bottom of the eye by finding the middle point of the bottom two points in the face landmark technic
    center_bottom = __midpoint(facial_landmarks.part(eye_point[5]), facial_landmarks.part(eye_point[4]))

    # Calculates the length of the vertical line of the eye, between the top and bottom center points of the eye
    vertical_line_len = math.hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    # Calculates the length of the horizontal line of the eye, between the left and right points of the eye
    horizontal_line_len = math.hypot((left_point_of_the_eye[0] - right_point_of_the_eye[0]),
                                     (left_point_of_the_eye[1] - right_point_of_the_eye[1]))

    # The ratio between the horizontal and the vertical lines of the eye
    ratio = horizontal_line_len / vertical_line_len

    return ratio
