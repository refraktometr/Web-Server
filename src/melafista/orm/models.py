class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        model = super(ModelMeta, mcs).__new__(mcs, name, bases, attrs)

        for attr_name, attr_value in attrs.items():
            mcs.add_to_model(model, attr_name, attr_value)
        return model

    @classmethod
    def add_to_model(mcs, model, attr_name, attr_value):
        if hasattr(attr_value, 'contribute_to_class'):
            attr_value.contribute_to_class(model, attr_name)
        else:
            setattr(model, attr_name, attr_value)


class Manager(object):
    def __init__(self):
        self.model = None

    def contribute_to_class(self, model, attr_name):
        self.model = model
        setattr(model, attr_name, self)


class Model(object):
    __metaclass__ = ModelMeta
