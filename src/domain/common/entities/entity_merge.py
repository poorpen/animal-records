class EntityMerge:

    def _merge(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if isinstance(v, list):
                kwargs[k] = self.__dict__[k] + v
            elif isinstance(v, dict):
                kwargs[k] = {**self.__dict__[k], **v}
        self.__dict__ = {**self.__dict__, **kwargs}
