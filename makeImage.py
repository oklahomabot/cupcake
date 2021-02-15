from PIL import Image, ImageColor


def get_bar(percentage=50, size=(300, 25), fill_color='blue'):
    '''
    This function returns a rectangular image based on percentage (0-100)
    "filled in" from left->right using the fill_color
    '''
    empty_bar = Image.new('RGB', size, ImageColor.getrgb('white'))
    fill_bar = Image.new(
        'RGB', ((size[0]*percentage)//100, size[1]), ImageColor.getrgb(fill_color))
    empty_bar.paste(fill_bar)

    return empty_bar


get_bar(90, fill_color='green').show()
get_bar(50).show()
get_bar(25, size=(600, 100), fill_color='purple').show()
