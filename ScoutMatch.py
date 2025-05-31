import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
df = pd.read_csv("FIFA_test_with_prediction.csv")

st.set_page_config(page_title="ScoutMatch", layout="wide")
st.markdown("<h1 style='text-align: center; color: blue;'>⚽ 이적료 기반 선수 스카우팅 플랫폼</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>원하는 포지션, 능력치, 이적료 예측을 기반으로 최고의 선수</p>", unsafe_allow_html=True)
st.markdown("---")

# 사이드바 필터
st.sidebar.header("🔍 Filter Search")
position = st.sidebar.multiselect("포지션 선택", df['position'].unique(), default=df['position'].unique())
continent = st.sidebar.multiselect("대륙 선택", df['continent'].unique(), default=df['continent'].unique())
age_range = st.sidebar.slider("나이 범위", int(df['age'].min()), int(df['age'].max()), (20, 35))
reputation_range = st.sidebar.slider("명성도", 1.0, 5.0, (3.0, 5.0), step=0.5)
min_value = st.sidebar.number_input("최소 이적료 (€)", value=0)
max_value = st.sidebar.number_input("최대 이적료 (€)", value=int(df['predicted_value'].max()))

# 필터 적용
filtered_df = df[
    (df['position'].isin(position)) &
    (df['continent'].isin(continent)) &
    (df['age'].between(age_range[0], age_range[1])) &
    (df['reputation'].between(reputation_range[0], reputation_range[1])) &
    (df['predicted_value'].between(min_value, max_value))
]

# 선수 목록
st.subheader("📋 필터링된 선수 리스트")
st.dataframe(
    filtered_df[['name', 'age', 'position', 'stat_overall', 'stat_potential', 'reputation', 'predicted_value']]
    .sort_values(by='predicted_value', ascending=False)
    .reset_index(drop=True),
    use_container_width=True
)

# 이적료 분포
st.markdown("---")
st.subheader("📈 예측 이적료 분포")
fig = px.histogram(filtered_df, x='predicted_value', nbins=30, color_discrete_sequence=["dodgerblue"])
fig.update_layout(title="예측 이적료 분포", xaxis_title="예측 이적료 (€)", yaxis_title="선수 수")
st.plotly_chart(fig, use_container_width=True)

# 상위 추천
st.markdown("---")
st.subheader("🌟 추천 선수 Top 3")
cols = st.columns(3)
top3 = filtered_df.sort_values(by='predicted_value', ascending=False).head(3)

for i, (idx, player) in enumerate(top3.iterrows()):
    with cols[i]:
        st.markdown(f"""
        <div style='background-color:#f0f8ff; padding:15px; border-radius:10px; box-shadow:2px 2px 5px #d0d0d0;'>
        <h4 style='color:#003366;'>🏅 {player['name']}</h4>
        <ul>
            <li><strong>포지션:</strong> {player['position']}</li>
            <li><strong>나이:</strong> {player['age']}</li>
            <li><strong>능력치:</strong> {player['stat_overall']}</li>
            <li><strong>잠재력:</strong> {player['stat_potential']}</li>
            <li><strong>명성도:</strong> {player['reputation']}</li>
            <li><strong>예측 이적료:</strong> <span style='color:green;'>€{int(player['predicted_value']):,}</span></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
