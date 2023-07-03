import png

prefix = ""
suffix = ".png"
newsuffix = ".raw"
num_images = 10

def convert_all_files ():
    for i in range (0, num_images):
        convert_file (i)

def color_to_bytes (color):
    r, g, b = color
    arr = bytearray(2)
    arr[0] = r & 0xF8
    arr[0] += (g & 0xE0) >> 5
    arr[1] = (g & 0x1C) << 3
    arr[1] += (b & 0xF8) >> 3
    return arr


def convert_file (file_number):
    infile = prefix+"{0}".format(file_number)+suffix
    outfile = prefix+"{0}".format(file_number)+newsuffix
    png_reader=png.Reader(infile)
    image_data = png_reader.asRGBA8()

    with open(outfile, "wb") as file:

        for row in image_data[2]:
            for r, g, b, a in zip(row[::4], row[1::4], row[2::4], row[3::4]):
                # convert to (RGB565)
                img_bytes = color_to_bytes ((r,g,b))
                file.write(img_bytes)
    file.close()



convert_all_files()