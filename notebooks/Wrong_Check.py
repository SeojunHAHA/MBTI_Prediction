import pandas as pd

# 파일 경로 (필요에 따라 조정)
path = "../Data/processed/reddit_post_clean.csv"

# 안전하게 로드 (불량 행은 무시)
df = pd.read_csv(
    path,
    engine="python",
    on_bad_lines="skip",
    encoding="utf-8",
    encoding_errors="ignore",
)

# ------------------------------------------
# 1) 결측치 확인
# ------------------------------------------
print("===== 결측치 현황 =====")
missing = df[["author", "body", "mbti"]].isna().sum()
print(missing)
print(f"\n전체 행 수: {len(df):,}")
print(f"결측치 포함 행 비율:\n{(missing / len(df) * 100).round(3)}%\n")

# ------------------------------------------
# 2) 단어 수 계산
# ------------------------------------------
# body가 문자열이 아닌 값이 있다면 문자열로 변환
df["body"] = df["body"].astype(str)

# 각 행별 단어 수 계산
df["word_count"] = df["body"].str.split().map(len)

# 단어 수 통계 요약
print("===== 단어 수 통계 =====")
print(df["word_count"].describe(percentiles=[.01, .05, .25, .5, .75, .95, .99]).apply(lambda x: f"{x:,.0f}"))

# 최소/최대 예시 문장 출력
print("\n===== 단어 수 최소/최대 샘플 =====")
min_row = df.loc[df["word_count"].idxmin()]
max_row = df.loc[df["word_count"].idxmax()]
print(f"[최소 {min_row['word_count']} 단어]\n{min_row['body'][:500]}\n")
print(f"[최대 {max_row['word_count']} 단어]\n{max_row['body'][:500]}...\n")

# ------------------------------------------
# 3) MBTI 라벨별 평균 단어 수
# ------------------------------------------
print("===== MBTI별 평균 단어 수 =====")
avg_words = df.groupby("mbti")["word_count"].mean().sort_values(ascending=False).round(1)
print(avg_words)