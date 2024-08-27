import torch
import torchvision.transforms.v2 as T
import pandas as pd

class MaskFromColorMultiObject:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", ),
                "room_object": ("STRING", {
                    "multiline": True, #True if you want the field to look like the one on the ClipTextEncode node
                    "default": "",
                    "lazy": True
                }),
            }
        }

    RETURN_TYPES = ("MASK", )
    FUNCTION = "execute"
    CATEGORY = "VSIH/mask"

    def execute(self, image, room_object, threshold):
        filename = f"colordata/data.csv"
        data = pd.read_csv(filename)
        mask = torch.zeros_like(image)

        #Get keywords from object list
        keywords = room_object.split(',')
        for word in keywords:
            filtered_data = data[data['Name'].str.contains(word, case=False, na=False)]

            # If no data is found, skip to the next keyword
            if filtered_data.empty:
                continue

            rgb = filtered_data['Color_Code (R,G,B)']
            # RGB format is (R,G,B) so we need to split the string and convert to int
            rgb = rgb.str.split(',', expand=True)
            red = rgb[0].astype(int)
            green = rgb[1].astype(int)
            blue = rgb[2].astype(int)
            temp = (torch.clamp(image, 0, 1.0) * 255.0).round().to(torch.int)
            color = torch.tensor([red, green, blue])
            lower_bound = (color - threshold).clamp(min=0)
            upper_bound = (color + threshold).clamp(max=255)
            lower_bound = lower_bound.view(1, 1, 1, 3)
            upper_bound = upper_bound.view(1, 1, 1, 3)
            temp_mask = (temp >= lower_bound) & (temp <= upper_bound)
            temp_mask = mask.all(dim=-1)
            temp_mask = mask.float()
            mask = mask & temp_mask

        return (mask, )
    
# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"


# # Add custom API routes, using router
# from aiohttp import web
# from server import PromptServer

# @PromptServer.instance.routes.get("/hello")
# async def get_hello(request):
#     return web.json_response("hello")


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Example": MaskFromColorMultiObject
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Example": "Example Node"
}


