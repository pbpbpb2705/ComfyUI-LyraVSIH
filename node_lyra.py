import torch
import torchvision.transforms.v2 as T
import pandas as pd
import os

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

    def execute(self, image, room_object):
        file_path = os.path.join(os.path.dirname(__file__), 'data.csv')
        data = pd.read_csv(file_path, index_col=0)
        mask = None

        #Get keywords from object list
        keywords = room_object.split(',')
        
        for word in keywords:
            filtered_data = data[data['Name'].str.contains(word, case=False, na=False)]

            # If no data is found, skip to the next keyword
            if filtered_data.empty:
                continue

            rgb = filtered_data['Color_Code (R,G,B)']
            # Reset index to 0
            rgb = rgb.reset_index(drop=True)
            # RGB format is (R,G,B) so we need to split the string and convert to int
            rgb = rgb.str.split(',', expand=True)
            # Remove brackets '(' and '(' from the string
            rgb = rgb.apply(lambda x: x.str.replace('(', ''))
            rgb = rgb.apply(lambda x: x.str.replace(')', ''))
            red = rgb[0].astype(int)
            green = rgb[1].astype(int)
            blue = rgb[2].astype(int)
            temp = (torch.clamp(image, 0, 1.0) * 255.0).round().to(torch.int)
            color = torch.tensor([red[0], green[0], blue[0]])
            print(color)
            lower_bound = (color).clamp(min=0)
            upper_bound = (color).clamp(max=255)
            lower_bound = lower_bound.view(1, 1, 1, 3)
            upper_bound = upper_bound.view(1, 1, 1, 3)
            temp_mask = (temp >= lower_bound) & (temp <= upper_bound)
            temp_mask = temp_mask.all(dim=-1)
            temp_mask = temp_mask.float()
            if mask is None:
                mask = temp_mask
            else: 
                mask = mask + temp_mask
            #Limit the mask to 1
            mask = torch.clamp(mask, 0, 1)

        return (mask, )


