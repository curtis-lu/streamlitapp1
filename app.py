from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from myraceplot import barplot

########################################################
# settings
filepath = Path('./data.csv')
age_options = list(str(i) for i in range(20, 85, 5))
age_order = [f'{age_s}_{age_e}' for (age_s, age_e) in zip(age_options[:-1], age_options[1:])]
barcolor = {'20_25': 'rgb(249, 219, 189)',
            '25_30': 'rgb(255, 107, 107)',
            '30_35': 'rgb(254, 127, 45)',
            '35_40': 'rgb(255, 191, 0)',
            '40_45': 'rgb(208, 210, 211)',
            '45_50': 'rgb(208, 210, 212)',
            '50_55': 'rgb(208, 210, 213)',
            '55_60': 'rgb(208, 210, 214)',
            '60_65': 'rgb(208, 210, 215)',
            '65_70': 'rgb(208, 210, 216)',
            '70_75': 'rgb(208, 210, 217)',
            '75_80': 'rgb(208, 210, 218)',}

# sidebar
sidebar_options = ['年輕人買不起房子？', '只買得起老房子？']
add_sidebar = st.sidebar.selectbox('討論主題', sidebar_options)

# functions
@st.cache_data
def read_csv(path):
    return pd.read_csv(path)
########################################################

st.markdown('# 購屋專題分析')

if add_sidebar == sidebar_options[0]:

    df = read_csv(filepath)

    '''
    根據聯徵中心網站的公開資料: https://member.jcic.org.tw/main_member/MorgageQuery.aspx \n
    運用python的selenium套件，自動抓取各年齡層購屋貸款承貸資料。\n
    再利用raceplotly套件，繪製了自2009年Ｑ1以來，每一季承貸件數的年齡分佈。

    結果如下：\n
    * 2009Q1時，承貸購屋貸款案件數最多的年齡層是30至35歲，其次是35至40歲。反應多數人成家立業的年齡。\n
    * 但是來到2023Q1，年齡層30至35歲落到了第3名，第1名則是40至45歲。似乎反應年輕人越來越晚才能有錢買房。\n
    '''

    my_raceplot = barplot(df,
                          item_column='age_group',
                          value_column='cnt',
                          time_column='期別',
                          top_entries=12,
                          item_color=barcolor,
                          item_color_col='barcolor')

    fig = my_raceplot.plot(item_label = 'Age group ranking',
                           value_label = 'count',
                           frame_duration = 600,
                           date_format='%Y%m%d',
                           orientation='horizontal')

    fig.update_layout(
        title='新增購屋貸款承貸件數年齡分佈 (2009Q1-2023Q1)',
        xaxis_title="承貸案件數",
        yaxis_title="年齡分群",
        title_x=0.15,
        width=780,
        height=680,
        )

    st.plotly_chart(fig)

    st.text("")
    st.text("")
    st.text("")

    '''
    從平均年齡也可看到往上的趨勢，從下圖中可以看到明顯的分界是在2016年前後。\n
    2016年前購屋平均年齡大約落在39.5歲左右，但在2016年後卻是落在41歲左右。\n
    也就是現在的人，平均而言，跟10年相比，晚了1~2年才去買房。
    '''

    average_loan_age = (df.groupby(['date_fmt'])['cnt_m_age'].sum() / df.groupby(['date_fmt'])['cnt'].sum()).reset_index(name='weighted_age')

    fig = px.line(average_loan_age, x=average_loan_age['date_fmt'], y=average_loan_age['weighted_age'])
    fig.update_layout(title="新增貸款承貸案件平均年齡(2009Q1-2023Q1)", title_x=0.1, xaxis={"title": "Date"}, yaxis={"title":"平均年齡"})
    st.plotly_chart(fig)
