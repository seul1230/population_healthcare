import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.express as px
import numpy as np
from matplotlib.backends.backend_agg import RendererAgg
import requests
from streamlit_lottie import st_lottie
from streamlit_folium import st_folium
import folium
from PIL import Image

st.set_page_config(
    page_title="Population And Medical Institutions Analysis",
    page_icon="🏥",
    layout="wide",
)


# Lottie Icon
@st.cache
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url = "https://assets2.lottiefiles.com/packages/lf20_uwWgICKCxj.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json, speed=1, height=300, key="initial")


# Preparation to display plot
# matplotlib.use("agg")
_lock = RendererAgg.lock

# Seaborn style setup
# sns.set_style("darkgrid")
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

# Title
row0_1.title("Population And Medical Institutions Analysis")

with row0_2:
    st.write("")

row0_2.subheader(
    "GrowingTenten \n 🔟 성장발육엔텐텐"
)
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')

# Introduction
row1_spacer1, row1_1, row1_spacer2 = st.columns([0.1, 3.2, 0.1])

with row1_1:
    st.subheader(
        '''
        **고령화, 그리고 코로나 19 이후 의료 인프라**
        '''
    )
# img_space1, img_1, img_space2, img_2, img_space3 = st.columns(
#     (0.1, 1, 0.05, 1, 0.1)
# )

row2_spacer1, row2_1, row2_spacer2 = st.columns([0.1, 3.2, 0.1])

with row2_1:
    st.markdown(
        '''
        코로나19 이후로 의료 인프라는 이루 말할 수 없이 중요한 사안이 되었다. 중환자 및 응급 병상 부족 문제가 심각해지고,
         가속화되는 **인구 고령화**로 인해 지역 간 의료 인프라 불균형 문제가 점점 심각해지고 있다.
        이에 따라 우리 조는 미니프로젝트에서 분석하였던 **총 인구수**(2008 - 2021)를 바탕으로 의료기관 데이터에 접근하고자 한다.
        '''
    )

img_space1, img_1, img_space2 = st.columns(
    (0.3, 1, 0.3)
)
with img_1, _lock:
    st.image(Image.open('img/background.png'))
#     st.image(Image.open('img/background_1.png'))
# with img_2, _lock:
#     st.image(Image.open('img/background_2.png'))
#     st.image(Image.open('img/background_3.png'))


@st.cache
def get_hypo_data(hypo_name):
    file_name = f"data/{hypo_name}.csv"
    data = pd.read_csv(file_name)
    return data


# data = get_hypo_data('연령별_인구현황(2008_2021)')
data = pd.read_csv('data/age_population(2008_2021).csv')


# Display Data Set
row3_space1, row3_1, row3_space2 = st.columns(
    (0.01, 1, 0.01)
)

with row3_1, _lock:
    # st.markdown(
    #     '''
    #     코로나19 이후로 의료 인프라는 이루 말할 수 없이 중요한 사안이 되었다. 중환자 및 응급 병상 부족 문제가 심각해지고,
    #      가속화되는 **인구 고령화**로 인해 지역 간 의료 인프라 불균형 문제가 점점 심각해지고 있다.
    #     이에 따라 우리 조는 미니프로젝트에서 분석하였던 **총 인구수**(2008 - 2021)를 바탕으로 의료기관 데이터에 접근하고자 한다.
    #     '''
    # )

    st.markdown(
        '''
        우선 지역 별 **인구 수**에 따른 **현재 운영 중인 의료기관 수**(2022.06 기준)를 분석한다. 
        목표는 지역 별 인구 수에 따른 의료기관 비율을 비교 분석하고 도표와 지도를 통해 시각화하는 것이다. 
        인구수에 따른 **인프라 격차**가 발생할 것이라는 가설을 검증하고 현재 의료 인프라가 부족한 지역을 찾는다. 
        더하여, 의료시설 개업과 폐업 데이터를 분석하여 앞으로의 인프라 격차를 개선시킬 수 있는 방안을 모색해 본다.
        
        
        '''
    )

    st.markdown(
        '''
        
        '''
    )
    st.subheader("DataSet")
    with st.expander("MiniProject Final DataSet 보기 👉"):
        st.markdown('**미니프로젝트결과물_전국총인구수**')
        st.dataframe(data)

st.markdown('')
st.markdown('')
hypo_space1, hypo_1, hypo_space2 = st.columns(
    (0.01, 1, 0.01)
)

with hypo_1, _lock:
    st.subheader("Hypothesis")
    st.markdown('''
            1.  총인구수가 적은 행정구역은 현존하는 의료기관수가 부족할 것으로 예상한다
            2.  고령화가 많이 진행된 지역에 현존하는 의료기관이 부족할 것이다
            3.  의료기관수는 다른분야(문화, 환경, 교육)의 인프라와도 상관관계가 있을 것이다
            4.  서울시 강남구에 의료기관이 제일 많이 집중되어 있는 이유는 강남에는 미용목적 의료기관이 몰려있기 때문일 것이다.
            5.  연도별 의료기관 개폐업수와 총인구수, 연령층 비율은 상관관계가 있을 것이다.
    
                ''')

st.markdown(
    '''
    ***
    '''
)


# Footers
footer_space1, footer_1, footer_space2 = st.columns(
    (0.01, 1, 0.01)
)

with footer_1, _lock:
    st.markdown(
        '''
        🦁

        **성장발육엔텐텐** - 이재모, 조예슬, 임혜진, 김영민
        '''
    )

    st.markdown(
        "**멋쟁이사자처럼 AI 스쿨 7기 미드프로젝트** : 2022.10.19 - 2022.10.23"

    )
