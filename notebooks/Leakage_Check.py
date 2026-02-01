import re
import pandas as pd

# 1️⃣ 데이터 불러오기
df = pd.read_csv('../Data/processed/reddit_post.csv')  # 또는 raw 경로

# 2️⃣ 함수 정의
def build_pattern(mbti: str, allow_hashtag: bool = True):
    mbti = re.escape(str(mbti).strip())
    if allow_hashtag:
        return re.compile(rf'(?<![A-Za-z])#?{mbti}(?![A-Za-z])', re.I)
    else:
        return re.compile(rf'(?<![A-Za-z]){mbti}(?![A-Za-z])', re.I)

def find_self_mentions(df, text_col="body", label_col="mbti", allow_hashtag=True):
    patterns = {m: build_pattern(m, allow_hashtag) for m in df[label_col].unique()}
    mask = df.apply(
        lambda row: patterns[row[label_col]].search(str(row[text_col])) is not None,
        axis=1
    )
    return df[mask]

# 3️⃣ 함수 실행
self_mentions = find_self_mentions(df, text_col="body", label_col="mbti", allow_hashtag=True)

# 4️⃣ 결과 확인
print(f"자기 MBTI를 정확히 언급한 행 수: {len(self_mentions)}")
print(self_mentions[["body", "mbti"]].head(10))