# # backend/training_model.py
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, GlobalAveragePooling2D
# from tensorflow.keras.preprocessing.image import ImageDataGenerator

# # Parameters
# IMAGE_SIZE = (224, 224)
# BATCH_SIZE = 32
# EPOCHS = 10
# NUM_CLASSES = 4  # e.g., top, bottom, dress, outerwear

# def create_model():
#     # Using a simple CNN; consider switching to a pretrained model for better performance.
#     model = Sequential([
#         Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
#         MaxPooling2D(2, 2),
#         Conv2D(64, (3, 3), activation='relu'),
#         MaxPooling2D(2, 2),
#         Flatten(),
#         Dense(128, activation='relu'),
#         Dropout(0.5),
#         Dense(NUM_CLASSES, activation='softmax')
#     ])
#     model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#     return model

# # Alternatively, for better accuracy, you could use transfer learning with a pretrained model:
# def create_transfer_model():
#     base_model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False, input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
#     base_model.trainable = False  # freeze the base model layers
#     model = Sequential([
#         base_model,
#         GlobalAveragePooling2D(),
#         Dense(128, activation='relu'),
#         Dropout(0.5),
#         Dense(NUM_CLASSES, activation='softmax')
#     ])
#     model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#     return model

# if __name__ == "__main__":
#     # Update these paths to where you placed your DeepFashion2 dataset.
#     train_dir = "../deepfashion2/train"
#     val_dir = "../deepfashion2/val"

#     # Data augmentation and generators
#     train_datagen = ImageDataGenerator(
#         rescale=1./255,
#         rotation_range=20,
#         zoom_range=0.15,
#         width_shift_range=0.2,
#         height_shift_range=0.2,
#         horizontal_flip=True
#     )
#     val_datagen = ImageDataGenerator(rescale=1./255)

#     train_generator = train_datagen.flow_from_directory(
#         train_dir,
#         target_size=IMAGE_SIZE,
#         batch_size=BATCH_SIZE,
#         class_mode='categorical'
#     )
#     validation_generator = val_datagen.flow_from_directory(
#         val_dir,
#         target_size=IMAGE_SIZE,
#         batch_size=BATCH_SIZE,
#         class_mode='categorical'
#     )

#     # Choose one of the model creation functions:
#     # model = create_model()
#     model = create_transfer_model()  # Using transfer learning with MobileNetV2 for better performance
#     model.summary()

#     # Train the model
#     history = model.fit(
#         train_generator,
#         epochs=EPOCHS,
#         validation_data=validation_generator
#     )

#     # Save the trained model for use in production (used by recommendation_engine.py)
#     model.save("models/stylist_model.h5")


# backend/training_model.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Parameters
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASSES = 4  # Adjusted for: top, bottom, dress, outerwear

def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Option using transfer learning with MobileNetV2 for improved performance:
def create_transfer_model():
    base_model = tf.keras.applications.MobileNetV2(
        weights="imagenet", include_top=False, input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)
    )
    base_model.trainable = False
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    # Update these paths based on your DeepFashion2 organization:
    train_dir = "../deepfashion2/train"
    val_dir = "../deepfashion2/val"

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    # Choose the appropriate model creation function:
    model = create_transfer_model()  # Using MobileNetV2 transfer learning
    model.summary()

    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator
    )

    model.save("models/stylist_model.h5")
