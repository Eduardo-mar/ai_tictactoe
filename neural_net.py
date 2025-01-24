import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

# 1. Load Preprocessed Data (Replace with your actual file paths)
data = np.load('./data/data_processed.npz') #Replace path
X = data['X']
Y = data['Y']
breakpoint()

# 2. Split Data
X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=42)

# 3. Create the Model
def create_model(input_shape=(9,)):
    model = Sequential([
        Dense(64, activation='relu', input_shape=input_shape),
        Dense(64, activation='relu'),
        Dense(9, activation='softmax')
    ])
    return model

model = create_model()

# 4. Compile the Model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 5. Train the Model
model.fit(X_train, Y_train, epochs=10, batch_size=32, validation_data=(X_val, Y_val))

# 6. Evaluate the Model (Optional, but recommended)
loss, accuracy = model.evaluate(X_val, Y_val)
print('Validation Loss:', loss)
print('Validation Accuracy:', accuracy)

# 7. Save the Model
model.save('./models/trained_model.h5')  # Replace with your desired path