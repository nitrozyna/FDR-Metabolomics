import pylab as plt

def plot_q_vals(estimated, filename=None):
    plt.figure(figsize=(8,6))
    for label, (t,e) in estimated.items():
        plt.plot(t, e, label=label)
    plt.plot([0,0.5], [0,0.5], 'k--')
    plt.xlabel('True')
    plt.ylabel('Estimated')
    plt.legend()
    plt.grid()
    if filename is not None:
        plt.savefig(filename)
