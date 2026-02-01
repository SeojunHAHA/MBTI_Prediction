import re
import pandas as pd

# 1️⃣ 데이터 불러오기
df = pd.read_csv('../Data/processed/reddit_post.csv')

# 2️⃣ MBTI 정규식 패턴 생성 함수
def build_pattern(mbti: str, allow_hashtag: bool = True):
    mbti = re.escape(str(mbti).strip())
    if allow_hashtag:
        # 알파벳이 아닌 경계에서 시작, #는 선택, 뒤는 알파벳이 아닌 경계로 끝
        return re.compile(rf'(?<![A-Za-z])#?{mbti}(?![A-Za-z])', re.I)
    else:
        return re.compile(rf'(?<![A-Za-z]){mbti}(?![A-Za-z])', re.I)

# 3️⃣ 자기 언급 탐지 함수
def find_self_mentions(df, text_col="body", label_col="mbti", allow_hashtag=True):
    patterns = {m: build_pattern(m, allow_hashtag) for m in df[label_col].unique()}
    mask = df.apply(
        lambda row: patterns[row[label_col]].search(str(row[text_col])) is not None,
        axis=1
    )
    return df[mask]

# 4️⃣ 자기 MBTI 언급 데이터 탐지
self_mentions = find_self_mentions(df, text_col="body", label_col="mbti", allow_hashtag=True)

# 5️⃣ 원본 대비 제거
df_clean = df.drop(index=self_mentions.index)

# 6️⃣ 통계 출력
print("===== MBTI 자기 언급 제거 결과 =====")
print(f"원본 행 수: {len(df):,}")
print(f"제거된 행 수: {len(self_mentions):,}")
print(f"제거 후 행 수: {len(df_clean):,}")
print(f"제거 비율: {100 * (len(self_mentions) / len(df)):.2f}%")

# 7️⃣ 샘플 확인
print("\n자기 MBTI 언급 예시 (상위 5개):")
print(self_mentions[["body", "mbti"]].head(5))

# 8️⃣ 원한다면 저장
df_clean.to_csv('../Data/processed/reddit_post_clean.csv', index=False)
print("\n정제된 데이터 저장 완료: ../Data/processed/reddit_post_clean.csv")