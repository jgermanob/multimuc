import matplotlib.pyplot as plt
import numpy as np

def plot_history(history: dict):
    f,axs = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
    axs.plot(history['train']['loss'], label='Train')
    axs.plot(history['val']['loss'], label='Validation')
    axs.set_xlabel('Epoch')
    axs.set_ylabel('Loss')
    axs.legend()
    
    axs.grid()
    plt.show()

history = {
        'train':{
            'loss': np.zeros(12),
        },
        'val':{
            'loss': np.zeros(12),      
        }
    }

# Train
history['train']['loss'][0] = 1.1433
history['train']['loss'][1] = 0.7063
history['train']['loss'][2] = 0.5744
history['train']['loss'][3] = 0.4545
history['train']['loss'][4] = 0.4185
history['train']['loss'][5] = 0.3388
history['train']['loss'][6] = 0.3170
history['train']['loss'][7] = 0.2655
history['train']['loss'][8] = 0.2470
history['train']['loss'][9] = 0.2599
history['train']['loss'][10] = 0.2681
history['train']['loss'][11] = 0.2249

#Val
history['val']['loss'][0] = 0.9271
history['val']['loss'][1] = 0.7835
history['val']['loss'][2] = 0.8082
history['val']['loss'][3] = 0.8065
history['val']['loss'][4] = 0.7711
history['val']['loss'][5] = 0.8041
history['val']['loss'][6] = 0.7295
history['val']['loss'][7] = 0.7933
history['val']['loss'][8] = 0.8626
history['val']['loss'][9] = 0.9103
history['val']['loss'][10] = 0.9414
history['val']['loss'][11] = 0.9806

plot_history(history)