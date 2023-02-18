# StreamDeck LiveScreen
![IMG_1307 (3)](https://user-images.githubusercontent.com/83812355/219875744-740a468b-33a7-41c2-9c1d-8bf2fd42b8ee.gif)

This code allows you to display of your entire desktop on a <a href="https://www.elgato.com/en/gaming/stream-deck">StreamDeck</a> device.<br/>Each key on the StreamDeck represents a portion of the screen, allowing you to monitor your entire desktop at a glance.

## Installation
To use this code, you will need the following libraries:
* PL (Python Imaging Library)
* StreamDeck (Python wrapper for the StreamDeck SDK)
You can install these libraries using pip:

```
pip install Pillow
pip install streamdeck
```
## Usage
To use this code, simply run the `streamdeck_live.py` file using Python:
```
python streamdeck_live.py
```
Once the script is running, connect your StreamDeck device to your computer.<br/>The script will automatically detect the device and start displaying the live screenshot on the device.
## Customization
You can customize the code to suit your needs by adjusting the `key_spacing` parameter in the `update_deck` function.<br/>This parameter determines the spacing between keys on the StreamDeck, which in turn determines the portion of the screen that each key displays.

