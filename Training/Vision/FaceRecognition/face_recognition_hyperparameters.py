from Training.Vision.FaceRecognition.face_recognition_constants import *

# Data preprocessing
INPUT_DIMENSIONS = (160, 160)
GRAYSCALE = False

# Training
TRAIN_TEST_SPLIT = [0, 0.8, 0.9, 1]
assert 0 <= TRAIN_TEST_SPLIT[0] < TRAIN_TEST_SPLIT[1] < TRAIN_TEST_SPLIT[2] < TRAIN_TEST_SPLIT[3] <= 1
EPOCHS = 1000
BATCH_SIZE = 64
NUM_WORKERS = 0
LEARNING_RATE = 0.01
EARLY_STOPPING_PATIENCE = 5
FEATURES_DIM = 128
