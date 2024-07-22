from dataset.t5_dataset import T5_templateFilling_dataset
from transformers import AutoTokenizer
import pandas as pd

model_checkpoint = 'google-t5/t5-base'
train_path = 'Corpora/en/train.csv'
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
df_train = pd.read_csv(train_path, encoding='utf8')

train_dataset = T5_templateFilling_dataset(df_train, tokenizer)
print(train_dataset[0])
