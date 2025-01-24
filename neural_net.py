import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

# 1. Load Preprocessed Data (Replace with your actual file paths)
data = np.load('./data/data_processed.npz') #Replace path
X = data['X']
Y = data['Y']

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
model.fit(X_train, Y_train, epochs=70, batch_size=32, validation_data=(X_val, Y_val))

# 6. Evaluate the Model (Optional, but recommended)
loss, accuracy = model.evaluate(X_val, Y_val)
print('Validation Loss:', loss)
print('Validation Accuracy:', accuracy)

# 7. Prediction Evaluation
num_examples_to_show = 10
print(f"\nShowing {num_examples_to_show} predictions from validation data:")
for i in range(num_examples_to_show):
    board_state = X_val[i].reshape(1,9)
    predicted_probs = model.predict(board_state, verbose=0) #Reshape so we have the shape that the model expects
    predicted_move = np.argmax(predicted_probs)
    actual_probs = Y_val[i]
    actual_move = np.argmax(actual_probs)
    print(f"Example {i + 1}:")
    print(f"   Predicted move: {predicted_move + 1}, Probabilities: {predicted_probs[0]}")
    print(f"   Actual move: {actual_move + 1}, Probabilities: {actual_probs}")

# 8. Save the Model
model.save('./models/trained_model_v2.h5')  # Replace with your desired path