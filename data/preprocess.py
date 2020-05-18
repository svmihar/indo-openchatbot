from pathlib import Path
from tqdm import tqdm
import joblib
from gensim.parsing.preprocessing import (
    preprocess_string,
    strip_tags,
    strip_multiple_whitespaces,
)
from gensim.utils import to_unicode

FILTERS = [strip_tags, strip_multiple_whitespaces]
srt_dir = Path("./srt").rglob("*.srt")
kumpulan_srt = []

for srt in tqdm(srt_dir):
    try:
        raw = open(srt, encoding="utf-8-sig").read().splitlines()
        raw = [to_unicode(sub) for sub in raw if sub]  # removes empty line
        raw = [sub for sub in raw if not sub.isdigit()]  # removes line numbering
        raw = [sub for sub in raw if "-->" not in sub]  # removes timestamps
        clean = []
        for sub in raw:
            if "Lebah" in sub or "http" in sub:
                continue
            clean.append(sub)
        clean = [preprocess_string(r, FILTERS) for r in clean]  # tokenizing
        raw = [" ".join(r) for r in raw if r]
    except Exception as e:
        print(srt, e)
        continue

    kumpulan_srt.append({"title": str(srt), "conv": raw})

joblib.dump(kumpulan_srt, "conv_preprocessed.pkl")
