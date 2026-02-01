import os, csv
from sklearn.model_selection import train_test_split

INPUT_PATH = "../Data/processed/reddit_post_clean.csv"
OUTPUT_DIR = "../Data/split"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# 1) 1차 패스: author 수집
# -----------------------------
authors_set = set()

with open(INPUT_PATH, "r", encoding="utf-8", errors="ignore", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    try:
        a_idx = header.index("author")
        m_idx = header.index("mbti")
    except ValueError:
        raise RuntimeError("CSV 헤더에 'author' 또는 'mbti' 컬럼이 없습니다. 헤더를 확인하세요.")

    total_rows = 0
    skipped_meta = 0
    for row in reader:
        total_rows += 1
        if len(row) <= max(a_idx, m_idx):
            skipped_meta += 1
            continue
        author = row[a_idx]
        mbti   = row[m_idx]
        if author and mbti:  # 결측 방지
            authors_set.add(author)

authors = list(authors_set)
print(f"[1패스] 고유 author 수: {len(authors):,} (총 행: {total_rows:,}, 메타결측/불량: {skipped_meta:,})")

# -----------------------------
# 2) 유저 단위 6:2:2 분할
# -----------------------------
train_users, temp_users = train_test_split(authors, test_size=0.4, random_state=42)
val_users, test_users   = train_test_split(temp_users, test_size=0.5, random_state=42)

train_set, val_set, test_set = set(train_users), set(val_users), set(test_users)

print(f"[분할] train 유저: {len(train_set):,}, val 유저: {len(val_set):,}, test 유저: {len(test_set):,}")

# -----------------------------
# 3) 2차 패스: 행 라우팅 저장
# -----------------------------
paths = {
    "train": os.path.join(OUTPUT_DIR, "train_all.csv"),
    "val":   os.path.join(OUTPUT_DIR, "val_all.csv"),
    "test":  os.path.join(OUTPUT_DIR, "test_all.csv"),
}

with open(INPUT_PATH, "r", encoding="utf-8", errors="ignore", newline="") as fin, \
     open(paths["train"], "w", encoding="utf-8", newline="") as ftr, \
     open(paths["val"],   "w", encoding="utf-8", newline="") as fva, \
     open(paths["test"],  "w", encoding="utf-8", newline="") as fte:

    reader = csv.reader(fin)
    header = next(reader)

    wtr, wva, wte = csv.writer(ftr), csv.writer(fva), csv.writer(fte)
    # 헤더 쓰기
    for w in (wtr, wva, wte):
        w.writerow(header)

    counts = {"train":0, "val":0, "test":0, "skipped":0}
    for row in reader:
        # 불량행 방지
        if len(row) <= a_idx:
            counts["skipped"] += 1
            continue

        author = row[a_idx]
        if author in train_set:
            wtr.writerow(row); counts["train"] += 1
        elif author in val_set:
            wva.writerow(row); counts["val"] += 1
        elif author in test_set:
            wte.writerow(row); counts["test"] += 1
        else:
            # 이 경우는 드묾(1패스에서 수집 못한 author 등)
            counts["skipped"] += 1

print(f"[완료] 저장 경로:")
print(f" - {paths['train']}")
print(f" - {paths['val']}")
print(f" - {paths['test']}")
print(f"[행 수] train: {counts['train']:,}, val: {counts['val']:,}, test: {counts['test']:,}, skipped: {counts['skipped']:,}")