import abc


class AbstractCodeTransformer:

    @abc.abstractmethod
    def get_available_transforms(self):
        pass

    @abc.abstractmethod
    def code_transform(self, code: str, dst_style: str):
        pass
