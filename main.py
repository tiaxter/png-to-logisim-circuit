from cv2 import imread
from math import pow

def check_image_dimension(width, height):
    if height != 32 and width != 32:
        raise Exception("Not valid image size")

def get_hex_values(image, width, height):
    image_row = []
    for y in range(height):
        row_pixel: int = 0
        for x in range(width):
            # do something here
            b, g, r = image[x][y]
            if r == 0 and g == 0 and b == 0:
                row_pixel += int(pow(2, 31 - x))
        image_row.append(hex(row_pixel))
    return image_row

def convert_to_circuit(hex_values, circuit_name):
    file = open("test.circ", "r")
    content: list[str] = file.readlines()
    content = content[:len(content) - 1]

    y = 100

    content.append(f'<circuit name="{circuit_name}">')

    for i in range(len(hex_values)):
        hex_value = hex_values[i]
        content.append(f'<wire from="(200, {y})" to="(400, {y})"/>\n')
        content.append(f'''
        <comp lib="0" loc="(200, {y})" name="Constant">
          <a name="width" val="32"/>
          <a name="value" val="{hex_value}"/>
        </comp>
        ''')
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

    file = open("test.circ", "w")
    file.writelines(content)
    file.close()

def get_png_files():
    # TODO: get all file inside a specified folder
    print("Do something")

if __name__ == "__main__":
    image = imread("./25.png")
    height: int = image.shape[0]
    width: int = image.shape[1]
    check_image_dimension(width, height)
    hex_values = get_hex_values(image, width, height)
    convert_to_circuit(hex_values, "25")
