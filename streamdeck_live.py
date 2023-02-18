import os
import threading
from PIL import ImageGrab, Image, ImageOps
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper


def create_full_deck_sized_image(deck, key_spacing):
    """
    This function creates an image of the size of the StreamDeck device by taking a screenshot of the entire screen and
    resizing it to fit the dimensions of the StreamDeck.

    :param deck: The StreamDeck device object
    :param key_spacing: A tuple of two integers indicating the number of pixels between keys horizontally and vertically
    :return: An image of the size of the StreamDeck device
    """
    key_rows, key_cols = deck.key_layout()
    key_width, key_height = deck.key_image_format()["size"]
    spacing_x, spacing_y = key_spacing

    key_width *= key_cols
    key_height *= key_rows

    spacing_x *= key_cols - 1
    spacing_y *= key_rows - 1

    full_deck_image_size = (key_width + spacing_x, key_height + spacing_y)

    image = ImageGrab.grab()
    image = ImageOps.fit(image, full_deck_image_size, Image.LANCZOS)

    return image


def crop_key_image_from_deck_sized_image(deck, image, key_spacing, key):
    """
    This function crops a single key-sized image from the full image of the StreamDeck device.

    :param deck: The StreamDeck device object
    :param image: An image of the size of the StreamDeck device
    :param key_spacing: A tuple of two integers indicating the number of pixels between keys horizontally and vertically
    :param key: The index of the key to crop the image for
    :return: An image of the size of a single key on the StreamDeck device
    """

    key_rows, key_cols = deck.key_layout()
    key_width, key_height = deck.key_image_format()["size"]
    spacing_x, spacing_y = key_spacing

    row = key // key_cols
    col = key % key_cols

    start_x = col * (key_width + spacing_x)
    start_y = row * (key_height + spacing_y)

    region = (start_x, start_y, start_x + key_width, start_y + key_height)
    segment = image.crop(region)

    key_image = PILHelper.create_image(deck)
    key_image.paste(segment)

    return PILHelper.to_native_format(deck, key_image)


def update_deck(deck, key_spacing):
    """
    This function continuously updates the images on the StreamDeck keys.

    :param deck: The StreamDeck device object
    :param key_spacing: A tuple of two integers indicating the number of pixels between keys horizontally and vertically
    """
    while True:
        image = create_full_deck_sized_image(deck, key_spacing)

        key_images = {
            k: crop_key_image_from_deck_sized_image(
                deck, image, key_spacing, k
            )
            for k in range(deck.key_count())
        }
        with deck:
            for k, key_image in key_images.items():
                deck.set_key_image(k, key_image)


if __name__ == "__main__":
    # enumerate StreamDeck devices and create a thread for each one
    streamdecks = DeviceManager().enumerate()
    threads = []
    for deck in streamdecks:
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()
        deck.set_brightness(100)

        key_spacing = (36, 36)
        t = threading.Thread(target=update_deck, args=(deck, key_spacing))

        threads.append(t)
        t.start()

    for t in threads:
        t.join()
