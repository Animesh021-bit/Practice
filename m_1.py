import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# PyTorch imports
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# torchtext tokenizer utility
from torchtext.data.utils import get_tokenizer

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("hinglish_sentiment_sample.csv")
print("Dataset loaded:", df.shape)

# Ensure label column is numeric (0/1)
if df['label'].dtype == object:
    df['label'] = df['label'].map(lambda x: 1 if str(x).strip().lower() in ("1","pos","positive","p") else 0)

# -----------------------------
# Preprocessing
# -----------------------------
def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|@\w+|#\w+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df['text'] = df['text'].apply(preprocess_text)

# -----------------------------
# Machine Learning Approach (unchanged)
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

ml_model = LogisticRegression(max_iter=200)
ml_model.fit(X_train_tfidf, y_train)
y_pred_ml = ml_model.predict(X_test_tfidf)

print("Machine Learning Model Performance:")
print(classification_report(y_test, y_pred_ml))

cm_ml = confusion_matrix(y_test, y_pred_ml)
sns.heatmap(cm_ml, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix - Logistic Regression")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# -----------------------------
# Tokenization and Vocabulary (torchtext)
# -----------------------------
tokenizer = get_tokenizer("basic_english")   # simple tokenizer; handles punctuation splitting
all_tokens = []

for text in df['text']:
    toks = tokenizer(text)
    all_tokens.extend(toks)

# Build vocabulary with most common tokens
vocab_size = 5000
counter = Counter(all_tokens)
most_common = counter.most_common(vocab_size - 2)  # reserve 0 for PAD, 1 for OOV
itos = ["<PAD>", "<OOV>"] + [tok for tok, _ in most_common]
stoi = {tok: idx for idx, tok in enumerate(itos)}

def text_to_sequence(text, stoi, tokenizer):
    tokens = tokenizer(text)
    seq = [stoi.get(tok, stoi["<OOV>"]) for tok in tokens]
    return seq

# Convert all texts to sequences
sequences = [text_to_sequence(t, stoi, tokenizer) for t in df['text']]

# Padding/truncation
max_len = 50
def pad_sequence(seq, max_len):
    if len(seq) >= max_len:
        return seq[:max_len]
    return seq + [0] * (max_len - len(seq))

X_pad = [pad_sequence(seq, max_len) for seq in sequences]

# -----------------------------
# Deep Learning Approach (PyTorch)
# -----------------------------
# Train/test split for DL
X_train_dl, X_test_dl, y_train_dl, y_test_dl = train_test_split(X_pad, df['label'], test_size=0.2, random_state=42)

# Convert to tensors
X_train_tensor = torch.tensor(X_train_dl, dtype=torch.long)
X_test_tensor = torch.tensor(X_test_dl, dtype=torch.long)
y_train_tensor = torch.tensor(y_train_dl.astype(int).values, dtype=torch.float32).unsqueeze(1)
y_test_tensor = torch.tensor(y_test_dl.astype(int).values, dtype=torch.float32).unsqueeze(1)

# DataLoaders
batch_size = 64
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# LSTM model (BCEWithLogitsLoss)
class SentimentLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super(SentimentLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, 1)
    def forward(self, x):
        x = self.embedding(x)
        _, (hidden, _) = self.lstm(x)
        out = hidden[-1]
        out = self.fc(out)
        return out  # logits

model = SentimentLSTM(vocab_size=len(itos), embed_dim=128, hidden_dim=128).to(device)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 5
train_losses, val_losses = [], []
train_accs, val_accs = [], []

for epoch in range(1, epochs + 1):
    model.train()
    running_loss = 0.0
    running_corrects = 0
    total = 0
    for X_batch, y_batch in train_loader:
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)
        optimizer.zero_grad()
        logits = model(X_batch)
        loss = criterion(logits, y_batch)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * X_batch.size(0)
        preds = (torch.sigmoid(logits) >= 0.5).float()
        running_corrects += torch.sum(preds == y_batch).item()
        total += X_batch.size(0)
    train_loss = running_loss / total
    train_acc = running_corrects / total
    train_losses.append(train_loss)
    train_accs.append(train_acc)

    # Validation
    model.eval()
    val_running_loss = 0.0
    val_running_corrects = 0
    val_total = 0
    with torch.no_grad():
        for X_batch, y_batch in test_loader:
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)
            logits = model(X_batch)
            loss = criterion(logits, y_batch)
            val_running_loss += loss.item() * X_batch.size(0)
            preds = (torch.sigmoid(logits) >= 0.5).float()
            val_running_corrects += torch.sum(preds == y_batch).item()
            val_total += X_batch.size(0)
    val_loss = val_running_loss / val_total
    val_acc = val_running_corrects / val_total
    val_losses.append(val_loss)
    val_accs.append(val_acc)

    print(f"Epoch {epoch}/{epochs}  Train Loss: {train_loss:.4f}  Train Acc: {train_acc:.4f}  Val Loss: {val_loss:.4f}  Val Acc: {val_acc:.4f}")

# Final evaluation
model.eval()
all_preds, all_labels = [], []
with torch.no_grad():
    for X_batch, y_batch in test_loader:
        X_batch = X_batch.to(device)
        logits = model(X_batch)
        preds = (torch.sigmoid(logits) >= 0.5).long().cpu().numpy().flatten()
        all_preds.extend(preds.tolist())
        all_labels.extend(y_batch.cpu().numpy().flatten().astype(int).tolist())

print("\nDeep Learning (PyTorch LSTM) Performance:")
from sklearn.metrics import classification_report as sk_class_report
print(sk_class_report(all_labels, all_preds))

# Plot training history
plt.figure(figsize=(8,4))
plt.plot(range(1, epochs+1), train_accs, label='Train Accuracy')
plt.plot(range(1, epochs+1), val_accs, label='Validation Accuracy')
plt.title("Deep Learning Model Accuracy (PyTorch LSTM)")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

plt.figure(figsize=(8,4))
plt.plot(range(1, epochs+1), train_losses, label='Train Loss')
plt.plot(range(1, epochs+1), val_losses, label='Validation Loss')
plt.title("Deep Learning Model Loss (PyTorch LSTM)")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()
