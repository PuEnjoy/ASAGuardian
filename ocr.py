import pytesseract
from PIL import Image
import pyautogui
import numpy as np

#=============================================
#define screen coordinates
log_screen = (750, 125, 1165, 840)
para_detection = (185, 15, 620, 40)
#=============================================



def get_screenshot(dimension: tuple, file_name: str) -> None:
    if not len(dimension) == 4:
        print(f"unexpected dimensions for {dimension}")
        return
    left   = dimension[0]
    top    = dimension[1]
    right  = dimension[2]
    bottom = dimension[3]

    # Capture the screenshot of the specified area
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    # Save the screenshot to a file
    screenshot.save(file_name)
    return None


def ocr_image(image_name: str) -> str:
    #reference to pytesseract installation
    pytesseract.pytesseract.tesseract_cmd = "./tesseract-ocr/tesseract.exe"
    #open image file
    image = Image.open(f'./images/{image_name}')
    #convert image to RGB
    image = image.convert("RGB")

    # Define the lower and upper bounds for blue background colors in RGB format
    # This step is needed to properly detect "destroy" / "kill" feed.
    lower_darkish_blue = (0, 0, 0)
    upper_darkish_blue = (70, 120, 150)

    # Get the image data as a NumPy array
    image_data = np.array(image)

    # Create a mask for blue pixels
    mask = np.all((image_data >= lower_darkish_blue) & (image_data <= upper_darkish_blue), axis=-1)

    # Replace blue background regions with black pixels
    image_data[mask] = [0, 0, 0]

    # Convert the modified NumPy array back to a Pillow image
    image = Image.fromarray(image_data)
    image.save("replace.png")

    #write ocr results to string
    text  = pytesseract.image_to_string(image)
    #return raw string result
    return text


def format_log(raw_log_text: str = "") -> list:
    #Replace miss reads of Day as Dav with Day
    log_text = raw_log_text.replace("Dav", "Day")
    #Remove line breaks 
    log_text = log_text.replace('\n', ' ')
    #Replace common miss detection of level
    log_text = log_text.replace('Lvi', 'Lvl')
    log_text = log_text.replace('Ly!', 'Lvl')
    log_text = log_text.replace('Lv!', 'Lvl')
    #Split String in seperate actions by splitting at each occurance of "Day"
    log_entries = log_text.split("Day")

    for i in range(len(log_entries)):
        log_entries[i] = "Day" + log_entries[i]

    return log_entries

#print(ocr_image("testimg.jpg"))