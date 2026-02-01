import pandas as pd

path = "../Data/processed/reddit_post_clean.csv"

# 파일 불러오기
df = pd.read_csv(
    path,
    engine="python",
    on_bad_lines="skip",
    encoding="utf-8",
    encoding_errors="ignore"
)

# --------------------------
# 제거 전 상태 확인
# --------------------------
print("===== 결측치 제거 전 =====")
print(df[["author", "body", "mbti"]].isna().sum())
print(f"전체 행 수: {len(df):,}")

# --------------------------
# 결측치 제거
# --------------------------
before = len(df)
df = df.dropna(subset=["author", "body", "mbti"]).copy()
after = len(df)

removed = before - after
ratio = removed / before * 100

# --------------------------
# 결과 출력
# --------------------------
print("\n===== 결측치 제거 후 =====")
print(f"제거된 행 수: {removed:,} ({ratio:.3f}%)")
print(f"남은 행 수: {after:,}")

# --------------------------
# 덮어쓰기 저장
# --------------------------
df.to_csv(path, index=False, encoding="utf-8")
print(f"\n파일 덮어쓰기 완료 → {path}")