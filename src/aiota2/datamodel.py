class DataModel:

    def __init__(self, name, dd) -> None:
        self.data_model_name = name
        self.raw_json = dd

        for key, val in dd.items():
            if type(val) is dict:
                val = DataModel("...", val)
            elif type(val) is list and val:
                if type(val) is dict:
                    val = DataArray(map(DataModel, val))

            setattr(self, key, val)

    def __str__(self) -> str:
        # using self.__dict__ is wrong way
        address = hex(id(self))
        return f"<DataModel of {self.data_model_name } at {address}>"


class DataArray(list):

    def __str__(self) -> str:
        if self:
            address = hex(id(self))
            return f"<DataArray of DataModel {self[0].data_model_name} objects at {address}>"
        else:
            return "[]"