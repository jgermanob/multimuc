import matplotlib.pyplot as plt

def plot_history(history):
    f,axs = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
    axs[0].plot(history['train']['loss'], label='Train')
    axs[0].plot(history['val']['loss'], label='Validation')
    axs[0].set_xlabel('Epoch')
    axs[0].set_ylabel('Loss')
    axs[0].legend()
    
    axs[0].grid()
    plt.show()

