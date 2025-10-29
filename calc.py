import pandas as pd
import numpy as np

def analyze_step_response(filename, tol=0.02):
    # Load CSV file
    df = pd.read_csv(filename)
    e = df['e'].values
    t = df[' stamp'].values
    t = (t - t[0]) / 1e9  # convert nanoseconds to seconds

    # Basic parameters
    e0 = e[0]
    ess = 0  # steady-state = median of last 10% samples

    # Overshoot
    if np.min(e)>0:
        e_peak = 0
    else:
        e_peak = np.min(e)
    Mp = abs(e_peak - ess) / abs(e0 - ess) * 100

    # Rise time (10%–90%)
    e_10 = e0 * 0.1
    e_90 = e0 * 0.9
    idx_10 = np.where(np.abs(e) <= abs(e_10))[0]
    idx_90 = np.where(np.abs(e) <= abs(e_90))[0]

    if len(idx_10) > 0 and len(idx_90) > 0:
        t_rise = t[idx_10[0]] - t[idx_90[0]] if idx_10[0] > idx_90[0] else np.nan
    else:
        t_rise = np.nan

    # Settling time (±tol of steady state)
    band = tol * abs(e0)
    idx_settle = np.where(np.abs(e - ess) <= band)[0]
    if len(idx_settle) > 0:
        # ensure it stays within the band for the rest of the time
        for i in idx_settle:
            if np.all(np.abs(e[i:] - ess) <= band):
                t_settle = t[i]
                break
        else:
            t_settle = np.nan
    else:
        t_settle = np.nan

    # Results
    print(f"File: {filename}")
    print(f"Initial error e0 = {e0:.4f}")
    print(f"Steady-state value ess = {ess:.4f}")
    print(f"Rise time (10–90%) = {t_rise:.3f} s")
    print(f"Settling time (±{tol*100:.0f}%) = {t_settle:.3f} s")
    print(f"Percent overshoot = {Mp:.2f}%")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compute rise time, settling time, and overshoot from error log.")
    parser.add_argument("--file", required=True, help="Path to CSV file with columns e, e_dot, e_int, stamp")
    parser.add_argument("--tol", type=float, default=0.05, help="Tolerance for settling time (default = 2%)")
    args = parser.parse_args()

    analyze_step_response(args.file, tol=args.tol)
