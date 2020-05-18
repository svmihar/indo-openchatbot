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
list_of_srt = [a for a in Path("./srt").rglob("*.srt")]
breakpoint()


def preprocess(path: Path):
    clean = []
    try:
        raw = open(path, encoding="utf-8-sig").read().splitlines()
        raw = [to_unicode(sub) for sub in raw if sub]  # removes empty line
        raw = [sub for sub in raw if not sub.isdigit()]  # removes line numbering
        raw = [sub for sub in raw if "-->" not in sub]  # removes timestamps
        for sub in raw:
            if "Lebah" in sub or "http" in sub:
                continue
            clean.append(preprocess_string(sub, FILTERS))
    except Exception:
        pass

    return [" ".join(r) for r in clean if r]


def main():
    kumpulan_srt = [
        {"title": str(srt).split("/")[-1], "conv": preprocess(srt)}
        for srt in tqdm(list_of_srt)
    ]
    kumpulan_srt = [
        srt for srt in tqdm(kumpulan_srt) if srt
    ]  # memastikan gak ada yang kosong
    joblib.dump(kumpulan_srt, "conv_preprocessed.pkl")


if __name__ == "__main__":
    main()
