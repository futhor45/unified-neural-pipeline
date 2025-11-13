
import json
import argparse
from jiwer import wer

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main(pred_json, ref_transcripts_txt):
    pred = load_json(pred_json)
    pred_text = " ".join([p.get("text","") for p in pred])
    with open(ref_transcripts_txt, 'r', encoding='utf-8') as f:
        ref = f.read()
    error = wer(ref, pred_text)
    print(f"WER: {error:.3f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_json", required=True)
    parser.add_argument("--ref_txt", required=True)
    args = parser.parse_args()
    main(args.pred_json, args.ref_txt)
