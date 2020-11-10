import pylab as plt

def plot_q_vals(true,estimateds):
    plt.figure(figsize=(8,6))
    for label, estimated in estimateds.items():
        plt.plot(true, estimated, label=label)
    plt.plot([0,0.5], [0,0.5], 'k--')
    plt.xlabel('True')
    plt.ylabel('Estimated')
    plt.legend()
    plt.grid()