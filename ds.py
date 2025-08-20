import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io  # ✅ 추가 필요

# 이후 csv_data → io.StringIO 로 변경
df = pd.read_csv(io.StringIO(csv_data))  # ✅ 수정 완료


# 페이지 설정
st.set_page_config(
    page_title="2024년 월별 매출 성과 분석 대시보드",
    layout="wide"
)

# 데이터 정의
csv_data = """월,매출액,전년동월,증감률
2024-01,12000000,10500000,14.3
2024-02,13500000,11200000,20.5
2024-03,11000000,12800000,-14.1
2024-04,18000000,15200000,18.4
2024-05,21000000,18500000,13.5
2024-06,24000000,20100000,19.4
2024-07,22500000,19000000,18.4
2024-08,23000000,20500000,12.2
2024-09,19500000,18000000,8.3
2024-10,25000000,21500000,16.3
2024-11,26500000,23000000,15.2
2024-12,28000000,25000000,12.0"""

# 데이터 로딩
df = pd.read_csv(pd.compat.StringIO(csv_data))
df["월"] = pd.to_datetime(df["월"])
df["월표시"] = df["월"].dt.strftime("%m월")

# KPI 계산
total_sales = df["매출액"].sum()
avg_sales = df["매출액"].mean()
max_sales_row = df[df["매출액"] == df["매출액"].max()]
min_sales_row = df[df["매출액"] == df["매출액"].min()]
avg_growth = df["증감률"].mean()

# 헤더
st.title("📊 2024년 월별 매출 성과 분석 대시보드")
st.caption("제공된 CSV 데이터를 기반으로 분석한 결과입니다.")

# KPI 영역
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 매출액", f"{total_sales:,.0f}원")
col2.metric("평균 월 매출", f"{avg_sales:,.0f}원")
col3.metric("최고 매출 월", f"{max_sales_row['월'].dt.strftime('%m월').values[0]} ({max_sales_row['매출액'].values[0]:,.0f}원)")
col4.metric("최저 매출 월", f"{min_sales_row['월'].dt.strftime('%m월').values[0]} ({min_sales_row['매출액'].values[0]:,.0f}원)")

st.markdown("---")

# 차트 영역
col5, col6 = st.columns(2)

with col5:
    st.subheader("📈 월별 매출 추이")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df["월표시"], y=df["매출액"],
                              mode='lines+markers', name='2024년 매출액',
                              line=dict(color='royalblue')))
    fig1.add_trace(go.Scatter(x=df["월표시"], y=df["전년동월"],
                              mode='lines+markers', name='전년 동월 매출액',
                              line=dict(color='orange')))
    fig1.update_layout(height=400, yaxis_title="금액 (원)", xaxis_title="월", hovermode="x unified")
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    st.subheader("📊 전년 동월 대비 증감률")
    fig2 = px.bar(
        df,
        x="월표시",
        y="증감률",
        color="증감률",
        color_continuous_scale=["red", "lightgray", "green"],
        text="증감률"
    )
    fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig2.update_layout(
        height=400,
        xaxis_title="월",
        yaxis_title="증감률 (%)",
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)
