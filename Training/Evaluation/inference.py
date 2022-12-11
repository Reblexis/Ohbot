from constants import *
from ModelManager.lstm_model import LSTMModel

import torch
from ExtractorManager.mfcc import MFCCExtractor
from ExtractorManager.index_encoder import IndexExtractor
# Obsolete
"""
test_file = Path("output.wav")
features = MFCCExtractor().extract(test_file)
index_extractor = IndexExtractor({"all_vals": ["angry", "fear", "disgust", "happy", "neutral", "sad", "ps"]})

model = BaselineModel.load_from_checkpoint(INFERENCE_MODEL_PATH).to(DEVICE)
model.eval()
print(features.shape)
y_hat = model(features.reshape(1, 1, 513, 257))
print(index_extractor.decode(int(torch.argmax(y_hat))))
"""

