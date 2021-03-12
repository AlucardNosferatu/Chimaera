from tensorflow.keras.layers import Input, Dense, Flatten, Conv2D, MaxPool2D, BatchNormalization, Dropout
from tensorflow.keras.models import Model

layers_schema = {
    'Input': {
        'shape': 'tuple'
    },
    'Conv2D': {
        'filters': 'int',
        'kernel_size': 'int',
        'padding': ['same', 'valid'],
        'activation': ['relu', 'softmax', 'tanh', 'sigmoid']
    },
    'MaxPool2D': {
        'pool_size': 'tuple'
    },
    'BatchNormalization': None,
    'Flatten': None,
    'Dense': {
        'units': 'int',
        'activation': ['relu', 'softmax', 'tanh', 'sigmoid']
    },
    'Dropout': {
        'rate': 'float'
    }
}
alias_for_parsing = {
    'InputLayer': 'Input',
    'MaxPooling2D': 'MaxPool2D'
}
embedded_attributes = {
    'activation': 'activation.__name__',
    'shape': 'input_shape'
}


def build_model():
    input = Input(shape=(224, 224, 3))
    x = Conv2D(filters=16, kernel_size=3, padding='same', activation='relu')(input)
    x = MaxPool2D(pool_size=(2, 2))(x)
    x = BatchNormalization()(x)
    x = Conv2D(filters=32, kernel_size=3, padding='same', activation='relu')(x)
    x = MaxPool2D(pool_size=(2, 2))(x)
    x = BatchNormalization()(x)
    x = Conv2D(filters=64, kernel_size=3, padding='same', activation='relu')(x)
    x = MaxPool2D(pool_size=(2, 2))(x)
    x = BatchNormalization()(x)
    x = Flatten()(x)
    x = Dense(units=64, activation='relu')(x)
    x = Dropout(rate=0.2)(x)
    x = Dense(units=32, activation='relu')(x)
    x = Dropout(rate=0.2)(x)
    x = Dense(units=16, activation='relu')(x)
    x = Dense(units=8, activation='softmax')(x)
    model = Model(inputs=input, outputs=x)
    return model


def parse_model(model):
    for layer in model.layers:
        to_node = layer.name
        print(to_node)
        raw_type = str(type(layer)).split('.')[-1].replace("'>", "")
        if raw_type in alias_for_parsing:
            raw_type = alias_for_parsing[raw_type]
        print('Layer type:', raw_type)
        schema = layers_schema[raw_type]
        if schema is not None:
            for key in schema:
                if key in embedded_attributes:
                    attr = embedded_attributes[key]
                else:
                    attr = key
                value = eval('layer.{}'.format(attr))
                print(key, ':', value)
        from_node = layer.input.name.split('/')[0]
        print('Relationship:', from_node, '->', to_node)
        print()


if __name__ == "__main__":
    model = build_model()
    parse_model(model)
