from PIL import Image, ImageTk, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
import tkinter as tk

def find_attribute(element, attribute):
    if attribute in element.attrib:
        return element.attrib[attribute]
    return None

def show_character(png_path, xml_path):
    # Open the PNG image
    image = Image.open(png_path)

    # Create a Tkinter window
    window = tk.Tk()
    window.title("Character Image")

    # Load the character image as a Tkinter PhotoImage
    character_photo = ImageTk.PhotoImage(image)

    # Create a label to display the character image
    character_label = tk.Label(window, image=character_photo)
    character_label.pack()

    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Extract character parts from XML
    parts = root.find('parts')
    if parts is not None:
        for part in parts:
            # Extract part details
            name = part.attrib.get('name')
            min_coords = part.attrib.get('min')
            max_coords = part.attrib.get('max')

            if min_coords and max_coords:
                # Parse the coordinates
                min_x, min_y = map(int, min_coords.split())
                max_x, max_y = map(int, max_coords.split())

                # Draw the part overlay on the character image
                image_draw = ImageDraw.Draw(image)
                image_draw.rectangle([(min_x, min_y), (max_x, max_y)], outline="blue")

                # Add XML properties text on the image
                font = ImageFont.truetype("sprinkle.ttf", size=10)
                text = f"{name}"

                # Adjust the position and size of the text box
                text_width, text_height = image_draw.textsize(text, font=font)
                text_position = (min_x, min_y - text_height - 5)
                text_box = [(text_position[0], text_position[1]),
                            (text_position[0] + text_width, text_position[1] + text_height)]

                # Check if the text box exceeds the part boundaries
                if text_box[1][0] > max_x:
                    # Move the text box to the left if it exceeds the boundary
                    text_box = [(max_x - text_width, text_box[0][1]), (max_x, text_box[1][1])]

                # Draw the text box and text on the image
                image_draw.rectangle(text_box, fill="white")
                image_draw.text(text_box[0], text, font=font, fill="black")

    # Update the character image in the label
    character_photo = ImageTk.PhotoImage(image)
    character_label.configure(image=character_photo)
    character_label.image = character_photo

    # Run the Tkinter event loop
    window.mainloop()

# Example usage
png_file = 'silly.png'
xml_file = 'silly.xml'
show_character(png_file, xml_file)
