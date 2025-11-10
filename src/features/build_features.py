
import argparse, pandas as pd

def main(inp: str, out: str):
    df = pd.read_csv(inp)
    # No heavy processing; keep as-is for model to one-hot/scale in pipeline
    df.to_csv(out, index=False)
    print(f"✅ Features saved to {out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    main(args.input, args.output)
