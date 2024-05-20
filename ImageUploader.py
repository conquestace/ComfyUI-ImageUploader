import requests
from io import BytesIO
import numpy as np
from PIL import Image

class ImageUploader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "key" : ("STRING", {"default":""}),
                "host": (["catbox", "uguu"],)
                
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("IMAGE_URL",)

    FUNCTION = "run"

    CATEGORY = "imgupload"



    def run(self, image, key, host):

        if host == "catbox":
            api_url = "https://catbox.moe/user/api.php"
        elif host == "uguu":
            api_url = "https://uguu.se/upload"
        results = ""

        for (batch_number, image_tensor) in enumerate(image):
            image_np = 255. * image_tensor.cpu().numpy()
            image = Image.fromarray(np.clip(image_np, 0, 255).astype(np.uint8))
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            # Specify file name and MIME type
            files = {'fileToUpload': ('image.png', buffer, 'image/png')}
            data = {'reqtype': 'fileupload', 'userhash': key}
            response = requests.post(api_url, data=data, files=files,)

            if response.status_code == 200:
                results = f"Posted image to {host} with url {response.text}"
            else:
                print(f"Error posting image {batch_number}: {response.text}")
            print(results)
            return (results,)
  

    
    

NODE_CLASS_MAPPINGS = {
    "ImageUploader": ImageUploader
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageUploader": "Image Uploader"
}