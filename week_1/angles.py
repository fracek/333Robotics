import csv
import matplotlib.pyplot as plt

LOG_BASE_NAME='k_p_log/k_p_{}'

def read_log(path):
    with open(path, 'rb') as infile:
        tsvin = csv.reader(infile, delimiter='\t')

        return [{'t': float(row[0]),
                 'ref_a0': float(row[1]),
                 'a0': float(row[2]),
                 'ref_a1': float(row[3]),
                 'a1': float(row[4])} for row in tsvin]

def angle_error(ref, act):
    return [x - y for (x, y) in zip(ref, act)]

def show_plot(data, figname):
    ts = [e['t'] for e in data]
    ref_a0 = [e['ref_a0'] for e in data]
    a0 = [e['a0'] for e in data]
    ref_a1 = [e['ref_a1'] for e in data]
    a1 = [e['a1'] for e in data]

    fig = plt.figure()

    # Left plot, motor 0
    ax1 = fig.add_subplot(2, 2, 1)
    pref_a0, = ax1.plot(ts, ref_a0, 'b-')
    p_a0, = ax1.plot(ts, a0, 'r-');

    ax1.set_title('Motor 0')
    ax1.legend([pref_a0, p_a0], ['Reference', 'Actual'], loc=4)

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(ts, angle_error(ref_a0, a0))
    ax2.set_title('Error Motor 0')

    # Right plot, motor 1
    ax3 = fig.add_subplot(2, 2, 3)
    pref_a1, = ax3.plot(ts, ref_a1, 'b-')
    p_a1, = ax3.plot(ts, a1, 'r-')

    ax3.set_title('Motor 1')
    ax3.legend([pref_a1, p_a1], ['Reference', 'Actual'], loc=4)

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.plot(ts, angle_error(ref_a1, a1))
    ax4.set_title('Error Motor 1')

    fig.savefig(figname)
    #plt.show()

if __name__=='__main__':
    k_ps = [x * 50.0 for x in range(1, 19)]
    for k_p in k_ps:
        data = read_log(LOG_BASE_NAME.format(int(k_p * 100)))
        show_plot(data, 'k_p_log_out/k_p_{}.eps'.format(int(k_p * 100)))
