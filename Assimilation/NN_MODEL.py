from tensorflow.keras.applications import VGG16

model = VGG16(weights='imagenet', include_top=True)
for layer in model.layers:
    print(layer.name)
    print(type(layer))
    print(layer.input.name)
    print()