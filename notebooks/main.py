# import gzip, os
#
# path = "../Data/processed/reddit_post_clean.csv"  # 네가 쓰는 파일 경로
# is_gz = path.endswith(".gz")
#
# def count_lines(p):
#     if is_gz:
#         with gzip.open(p, "rt", encoding="utf-8", errors="ignore") as f:
#             return sum(1 for _ in f) - 1  # 헤더 제외
#     else:
#         with open(p, "r", encoding="utf-8", errors="ignore") as f:
#             return sum(1 for _ in f) - 1
#
# n = count_lines(path)
# print(f"[processed 전체 행수] {n:,}")

import os

split_dir = "../Data/split"
def count_rows(p):
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f) - 1  # 헤더 제외

train_n = count_rows(os.path.join(split_dir, "train.csv"))
val_n   = count_rows(os.path.join(split_dir, "val.csv"))
test_n  = count_rows(os.path.join(split_dir, "test.csv"))

print(f"train: {train_n:,}")
print(f"val:   {val_n:,}")
print(f"test:  {test_n:,}")
print(f"합계:  {train_n+val_n+test_n:,}")

# 전처리본 행수와 일치하는지 간단 검증
processed_total = 12_910_571
assert train_n + val_n + test_n == processed_total, "합계가 전처리본 행수와 다릅니다!"
print("✅ split 합계 == 전처리본 총행수")