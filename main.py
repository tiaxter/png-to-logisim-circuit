from cv2 import imread
from math import pow
from glob import glob
from os import path

CIRCUIT_FILENAME = 'circuit.circ'

def check_image_dimension(width, height):
    if height != 32 and width != 32:
        raise Exception("Not valid image size")

# Get the hexadecimal value of black pixel in image
def get_hex_values(image, width, height) -> list[str]:
    image_row: list[str] = []
    for y in range(height):
        row_pixel: int = 0
        for x in range(width):
            b, g, r = image[x][y]
            if r == 0 and g == 0 and b == 0:
                row_pixel += int(pow(2, 31 - x))
        image_row.append(hex(row_pixel))
    return image_row

def convert_to_circuit(hex_values, circuit_name) -> None:
    # Get file content
    file = open(CIRCUIT_FILENAME, "r")
    content: list[str] = file.readlines()
    # Remove the closing tag of <project>
    content = content[:len(content) - 1]

    y = 100

    content.append(f'<circuit name="{circuit_name}">')

    # For each hexadecimal value
    for i in range(len(hex_values)):
        hex_value = hex_values[i]
        # Create the wire to connect Constant and Pin
        content.append(f'<wire from="(200, {y})" to="(400, {y})"/>\n')
        # Create the Constant with the hexadecimal value
        content.append(f'''
        <comp lib="0" loc="(200, {y})" name="Constant">
          <a name="width" val="32"/>
          <a name="value" val="{hex_value}"/>
        </comp>
        ''')
        # Create the Pin
        content.append(f'''
        <comp lib="0" loc="(400, {y})" name="Pin">
          <a name="facing" val="west"/>
          <a name="output" val="true"/>
          <a name="width" val="32"/>
          <a name="label" val="{i}out"/>
          <a name="labelloc" val="east"/>
        </comp>
        ''')

        y += 100

    content.append(f"</circuit>\n")
    content.append(f"</project>")

    # Write out the content to the circuit file
    file = open(CIRCUIT_FILENAME, "w")
    file.writelines(content)
    file.close()

# Get all png files inside png/ folder
def get_png_files() -> list[str]:
    return glob("./png/*.png")

if __name__ == "__main__":
    # Get all images from png folder
    files = get_png_files()
    # For each file
    for file in files:
        # Read the image
        image = imread(file)
        # Get height and width
        height: int = image.shape[0]
        width: int = image.shape[1]
        # Check if image is 32x32
        check_image_dimension(width, height)
        # Get hexadecimal values for the images
        hex_values = get_hex_values(image, width, height)
        # Get images basename
        basename = path.basename(file)
        # Convert the hexadecimal value to Logisim circuit file
        convert_to_circuit(hex_values, basename[:basename.rfind('.')])
