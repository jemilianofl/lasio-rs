from ._lasio_rs import read as _rust_read
import json


class SectionItems:
    def __init__(self, data_dict):
        # Allow init from dict of HeaderItems or dict of dicts (from json)
        self._data = {}
        for k, v in data_dict.items():
            if isinstance(v, dict):
                # Check if it is a Curve dict or Header dict
                self._data[k] = HeaderItem(v)
            else:
                self._data[k] = v

    def __getitem__(self, key):
        item = self._data.get(key)
        if item:
            return item
        raise KeyError(f"{key} not found")

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __repr__(self):
        return f"SectionItems({list(self.keys())})"


class HeaderItem:
    def __init__(self, item_dict):
        self.mnemonic = item_dict.get("mnemonic")
        self.unit = item_dict.get("unit")
        self.value = item_dict.get("value")
        self.descr = item_dict.get("descr")
        self.original_mnemonic = self.mnemonic  # Compatibility

    def __repr__(self):
        return f'HeaderItem(mnemonic="{self.mnemonic}", unit="{self.unit}", value="{self.value}", descr="{self.descr}")'


class CurveItem(HeaderItem):
    def __init__(self, item_dict, las_file_ref):
        super().__init__(item_dict)
        self._las = las_file_ref
        self._data = None

    @property
    def data(self):
        if self._data is None:
            # Lazy load from Rust
            self._data = self._las._rust.get_curve_data(self.mnemonic)
            if self._data is None:
                self._data = []
        return self._data

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f'CurveItem(mnemonic="{self.mnemonic}", unit="{self.unit}", value="{self.value}", descr="{self.descr}", data.shape=({len(self)},))'


class LASFile:
    def __init__(self, rust_las):
        self._rust = rust_las

        # Hydrate metadata from JSON
        header_json = rust_las.json_headers
        header_data = json.loads(header_json)

        self.version = SectionItems(header_data.get("version", {}))
        self.well = SectionItems(header_data.get("well", {}))
        self.params = SectionItems(header_data.get("params", {}))

        # Curves needs special handling to link back to Rust for data
        raw_curves = header_data.get("curves", {})
        self.curves = SectionItems({})
        # Overwrite with CurveItems
        curve_dict = {}
        for k, v in raw_curves.items():
            curve_dict[k] = CurveItem(v, self)
        self.curves = SectionItems(curve_dict)

    def __getitem__(self, key):
        # Access curve data directly by mnemonic
        if isinstance(key, str):
            if key in self.curves.keys():
                return self.curves[key].data
        raise KeyError(f"Curve {key} not found")

    def keys(self):
        return self.curves.keys()


def read(file_path):
    rust_obj = _rust_read(str(file_path))
    return LASFile(rust_obj)
