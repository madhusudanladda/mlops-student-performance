
import argparse, os
import pandas as pd
import numpy as np

def main(output: str):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    # Generate a small synthetic dataset compatible with the Kaggle schema
    n = 1000
    rng = np.random.default_rng(42)
    genders = rng.choice(["male","female"], size=n)
    races = rng.choice(["group A","group B","group C","group D","group E"], size=n)
    parental = rng.choice(["some high school","high school","some college","associate's degree","bachelor's degree","master's degree"], size=n)
    lunch = rng.choice(["standard","free/reduced"], size=n, p=[0.7,0.3])
    prep = rng.choice(["none","completed"], size=n, p=[0.6,0.4])
    reading = rng.integers(30, 100, size=n)
    writing = (reading + rng.integers(-10, 10, size=n)).clip(0,100)
    df = pd.DataFrame({
        "gender": genders,
        "race/ethnicity": races,
        "parental level of education": parental,
        "lunch": lunch,
        "test preparation course": prep,
        "reading score": reading,
        "writing score": writing,
        "math score": ((reading*0.5 + writing*0.5) + rng.normal(0,8,size=n)).clip(0,100).astype(int)
    })
    df.to_csv(output, index=False)
    print(f"✅ Wrote {output} with {len(df)} rows")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    main(args.output)
