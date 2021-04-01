import pylab as plt


# plot estimated and true q-values
def combine_true_est(q_val_true, q_val_est):
    res = []
    q_idx = 0
    for q_e, _, score in q_val_est:
        while q_idx < len(q_val_true) - 1 and q_val_true[q_idx + 1][2] >= score:
            q_idx += 1
        res.append((score, q_val_true[q_idx][0], q_e))
    return res


def plot_q_vals(q_list_true, q_list_decoys, labels=True, filename=None):
    to_plot = {}
    for k, v in q_list_decoys.items():
        to_plot[k] = list(zip(*combine_true_est(q_list_true, v)))[1], list(zip(*combine_true_est(q_list_true, v)))[2]

    plt.figure(figsize=(8, 6))
    for label, (t, e) in to_plot.items():
        plt.plot(t, e, label=label)
    plt.plot([0, 0.5], [0, 0.5], 'k--')
    plt.xlabel('True q-value')
    plt.ylabel('Estimated q-value')
    if labels:
        plt.legend()
    plt.grid()
    if filename is not None:
        plt.savefig(filename)
