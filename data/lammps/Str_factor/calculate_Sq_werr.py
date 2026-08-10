import numpy as np

nseeds = 5
data = []

for seed in range(1, nseeds + 1):
    fname = f"New_debye_Sq_vs_q_seed{seed}_symm_avgd_Rc_22.5.txt"
    arr = np.loadtxt(fname, comments="#")
    data.append(arr)

#fixing Q values from seed 1
Q = data[0][:, 0]

#Sq_total is column 17, so python index=16
S_total_all = np.column_stack([data[seed][:, 16] for seed in range(nseeds)])

S_total_mean = np.mean(S_total_all, axis=1)
S_total_se = (np.std(S_total_all, axis=1, ddof=1)/ np.sqrt(nseeds))

avg_output = np.column_stack([Q,S_total_mean,S_total_se])

header_avg = "Q S_total_mean S_total_se"
np.savetxt("Debye_Sq_vs_q_5seed_average_Rc_22.5.txt",avg_output,header=header_avg,fmt="%.10e")
print("Done!")
