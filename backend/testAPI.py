# Run `pip install itk itkwidgets` before trying this example
from imjoy_rpc import api
import numpy as np
import itk
from itkwidgets.trait_types import itkimage_to_json, itkimage_from_json
from itkwidgets._transform_types import to_itk_image

# register an encoder for encoding the itk.Image, the name `itkimage` will be used for decoding
# this example only use the encoder part
api.registerCodec({'name': 'itkimage', 'type': itk.Image, 'encoder': itkimage_to_json, 'decoder': itkimage_from_json})

class ImJoyPlugin():
    def setup(self):
        api.log('plugin initialized')

    async def run(self, ctx):
        image_array = np.random.randint(0, 255, [10,10,10], dtype='uint8')
        itk_image = to_itk_image(image_array)
        # here the itk_image will be encoded via the registered encoder function (i.e.: itkimage_to_json)
        api.createWindow(type="itk-vtk-viewer", src="https://oeway.github.io/itk-vtk-viewer/", data={"image_array": itk_image})

api.export(ImJoyPlugin())

