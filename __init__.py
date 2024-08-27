from .node_lyra import MaskFromColorMultiObject

NODE_CLASS_MAPPINGS = {
    "MultiObjectMask": MaskFromColorMultiObject
}

NODE_DISPLAY_NAMES_MAPPINGS = {
    "MultiObjectMask": "MultiObjectMask"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']