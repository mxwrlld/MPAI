import json
import skimage.exposure
from skimage.exposure import histogram
from skimage.io import imread, imsave, imshow, show
from matplotlib import pyplot as plt

# Параметры пользователя
inputParameters = {
    "source_path": "streak.jpg",
    "save_path": "gamma_correction_result.jpg",
    "gamma": "0.25",
    "gain": "1"
}
with open('input_parameters.json', 'w') as inputFile:
    json.dump(inputParameters, inputFile)

def get_user_parameters():
    with open('input_parameters.json') as json_file:
        json_data = json.load(json_file)
    parameters = {entry: json_data[entry] for entry in json_data.keys}
    return parameters

def gamma_correction():
    parameters = get_user_parameters()
    path = parameters.get('source_path')

    img = imread(path)
    fig = plt.figure(figsize=(10, 6))
    fig.add_subplot(2, 2, 1)
    imshow(img[:, :, :])

    fig.add_subplot(2, 2, 2)
    corrImg = skimage.exposure.adjust_gamma(img, float(parameters.get('gamma')), float(parameters.get('gain')))
    imshow(corrImg[:, :, :])

    fig.add_subplot(2, 2, 3)
    build_histogram(img)

    fig.add_subplot(2, 2, 4)
    build_histogram(corrImg)
    show()

    save_to_file(parameters.get("save_path"), corrImg)

def build_histogram(img):
    hist_red, bins_red = histogram(img[:, :, :2])
    hist_green, bins_green = histogram(img[:, :, :1])
    hist_blue, bins_blue = histogram(img[:, :, :3])
    plt.ylabel('число отсчетов')
    plt.xlabel('значение яркости')
    plt.plot(bins_green, hist_green, color='green', linestyle='-', linewidth=1)
    plt.plot(bins_red, hist_red, color='red', linestyle='-', linewidth=1)
    plt.plot(bins_blue, hist_blue, color='blue', linestyle='-', linewidth=1)
    plt.legend(['green', 'red', 'blue'])
    plt.tight_layout(h_pad=1.0)

def save_to_file(filename, img):
    imsave(filename, img)

gamma_correction()
