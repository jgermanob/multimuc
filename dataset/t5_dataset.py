from torch.utils.data import Dataset
import torch

class T5_templateFilling_dataset(Dataset):
    
    def __init__(self, df, tokenizer):
        self.len = len(df)
        self.data = df
        self.tokenizer = tokenizer
    
    def __getitem__(self, index):
        text = self.data.input[index]
        output = self.data.output[index]

        encoded_text = self.tokenizer(text,
                                      padding='max_length',
                                      truncation=True, 
                                      max_length=512,
                                      add_special_tokens=True)
        
        encoded_labels = self.tokenizer(output,
                                        padding='max_length',
                                        truncation=True, 
                                        max_length=512,
                                        add_special_tokens=True)
        
        # Creating pytorch tensors
        item = {key: torch.as_tensor(val) for key,val in encoded_text.items()}
        item['output'] = torch.as_tensor(encoded_labels.input_ids)
        item['output_mask'] = torch.as_tensor(encoded_labels.attention_mask)
        
        return item
    
    def __len__(self):
        return self.len