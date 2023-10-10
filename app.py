from pathlib import Path
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from myraceplot import barplot

########################################################

# settings
filepath_age = Path('./data_age.csv')
filepath_hage_yyyqq = Path('./data_hage_yyyqq.csv')
filepath_hage_versus = Path('./data_hage_versus.csv')


age_options = list(str(i) for i in range(20, 85, 5))
age_order = [f'{age_s}_{age_e}' for (age_s, age_e) in zip(age_options[:-1], age_options[1:])]
barcolor = {'20_25': 'rgb(99,110,250)', # 'rgb(255, 161,  90)'
            '25_30': 'rgb(0,204,150)', # 'rgb(25,  211, 243)'
            '30_35': 'rgb(239,85,59)', # 'rgb(171,  99, 250)'
            '35_40': 'rgb(208, 210, 210)', # 'rgb(99,  110, 250)'
            '40_45': 'rgb(208, 210, 211)', # 'rgb(239,  85,  59)'
            '45_50': 'rgb(208, 210, 212)', # 'rgb(0,   204, 150)'
            '50_55': 'rgb(208, 210, 213)',
            '55_60': 'rgb(208, 210, 214)',
            '60_65': 'rgb(208, 210, 215)',
            '65_70': 'rgb(208, 210, 216)',
            '70_75': 'rgb(208, 210, 217)',
            '75_80': 'rgb(208, 210, 218)'}

# sidebar
sidebar_options = ['房子越買越老？', '越來越晚買房？']
add_sidebar = st.sidebar.selectbox('討論主題', sidebar_options)

# functions
@st.cache_data
def read_csv(path):
    return pd.read_csv(path)

########################################################

st.header('不動產資料視覺化分析專題')

if add_sidebar == sidebar_options[0]:

    st.subheader('房子越買越老？')

    '''
    隨著近年來房價不斷地攀升，對於買房有剛性需求的民眾來說，想必痛苦指數也跟著不斷地增加。
    一般來說，中古屋通常比新成屋或預售屋便宜，因此可能許多民眾退而求其次，改為購買中古屋。

    這個資料分析專題首先想要呈現一些數據，帶各位看看台灣各縣市的購屋屋齡變化。

    下方的泡泡圖呈現的是，台灣各縣市自2011年來，每一季平均購屋屋齡及平均房價的分布變化。

    可以發現，多數泡泡都是從左下角移動到右上角，代表10多年來，購屋的屋齡以及購屋價格不斷攀升。
    順帶一提，泡泡的大小則是代表交易量，跟10多年前相比，各縣市的交易量都下降不少。

    此圖的數據點較多，可以點擊各區域圖示來專注查看。至於金門縣、連江縣及澎湖縣因數據偏離較多，因此選擇不納入分析。
    '''
    title="各縣市住宅買賣平均屋齡與平均單價（2011Q1~2023Q2）"

    df_hage_yyyqq = read_csv(filepath_hage_yyyqq)

    fig = px.scatter(df_hage_yyyqq,
                     x="hage",
                     y="price",
                     color="district",
                     size="cnt",
                     text="county",
                     animation_frame="date",
                     animation_group="county",
                     category_orders={'district': ['北部區域', '中部區域','南部區域', '東部區域']})


    CUSTOM_HOVERTEMPLATE = "縣市名稱: %{text} <br> 平均屋齡: %{x} <br> 平均單價: %{y}"
    fig.update_traces(textposition="top center", hovertemplate=CUSTOM_HOVERTEMPLATE)
    for frame in fig.frames:
        for data in frame.data:
            data.hovertemplate = CUSTOM_HOVERTEMPLATE

    fig.update_xaxes(title="住宅買賣平均屋齡", range=[5, 35])
    fig.update_yaxes(title="買賣契約平均單價", visible=True, showticklabels=True, range=[5, 75])
    fig.update_layout(title=title,
                      title_x=0.15,
                      width=780,
                      height=680,
                      showlegend=True,
                      legend=dict(title="",
                                  orientation="h",
                                  yanchor="bottom",
                                  y=0.95,
                                  xanchor="right",
                                  x=1
                                ))
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("district=", "")))
    st.plotly_chart(fig)

    '''

    下圖比較了「各地區」與「全國平均」的屋齡增率，數值呈現的是各地區與全國平均的差異。

    根據資料計算，**全國平均住宅買賣平均屋齡**在2011年Q1時為15.34年，在2023年Q2為28.13年，約增加了83%。

    而新竹縣住宅買賣平均屋齡在2011年時為7.45年，在2023年為20.44年，約增加了174%之多！

    **紅色代表的是屋齡增率高於全國平均，藍色則是低於全國平均。**
    例如新竹縣增率是174%，比全國平均的83%增率，多了91%，屋齡增率居全臺之冠。

    '''
    title="各縣市住宅買賣屋齡增率與全國平均之差異（2023年 / 2011年）<br>全國平均住宅買賣屋齡增率：83%"

    df_hage_versus = read_csv(filepath_hage_versus)

    fig = go.Figure()
    trace = go.Bar(x=df_hage_versus['hage_diff'],
                   y=df_hage_versus['county'],
                   marker=dict(color=df_hage_versus['hage_color']),
                   orientation='h',
                   hovertemplate='<b>%{y}</b>屋齡增率 - 全國屋齡增率 = %{x:.2f}',
                   name="")
    fig.add_trace(trace)
    fig.update_layout(title=title,
                      width=780,
                      height=680,
                      yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig)

    '''
    依同樣邏輯來看，下圖呈現的是各縣市的房價增率與全國房價增率的差異，

    **全國買賣契約平均單價**在2011年Q1時為20.75萬/坪，在2023年Q2為32.14年，約增加了55%。

    至於房價居高不下的台北市，買賣契約平均單價在2011年時為52.27萬/坪，在2023年為67.91萬/坪，約增加了30%。

    **紅色代表的是房價增率高於全國平均，藍色則是低於全國平均。**
    以台北市來看，買賣契約單價增率30%低於全國平均的55%，約25%。

    全臺僅有台北市的房屋單價增率低於全國平均，反映的是台北市的房價基期相較其他地區高上許多（看看第一張泡泡圖中高處不勝寒的台北市！）。
    '''
    title="各縣市買賣契約單價增率與全國平均之差異（2023年 / 2011年）<br>全國平均買賣契約單價增率：55%"

    df_hage_versus = read_csv(filepath_hage_versus)

    fig = go.Figure()
    trace = go.Bar(x=df_hage_versus['price_diff'],
                   y=df_hage_versus['county'],
                   marker=dict(color=df_hage_versus['price_color']),
                   orientation='h',
                   hovertemplate='<b>%{y}</b>單價增率 - 全國單價增率 = %{x:.2f}',
                   name="")
    fig.add_trace(trace)
    fig.update_layout(title=title,
                      width=780,
                      height=680,
                      yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig)

    '''
    從以上分析可以發現，全臺各地區住宅買賣的屋齡普遍上升。
    反映的是各地住宅價格不斷攀升的現實。
    然而，屋齡增率卻未必跟房價增率有很強的相關性。
    屋齡增率最高的區域，大多是本身房價就比較高的區域，例如台北、新北、台中。
    至於新竹縣的情況則與竹科發展的特殊性有關，呈現屋齡增加174%，房屋單價成長92%的結果。
    '''

    '''
    -----------------------------------------
    資料來源為：內政部不動產資訊平台（ https://pip.moi.gov.tw/V3/E/SCRE0401.aspx ）。\n
    利用python套件selenium抓取：住宅買賣移轉筆數（依屋齡區分）及買賣契約價格平均單價（不分建物類別）。

    資料定義如下：
    - **住宅買賣移轉平均屋齡：** 辦理移轉登記，登記原因為買賣，主要用途登記為住家、住商、住工、國民住宅以及農舍等，計算住宅買賣移轉平均屋齡。
    - **買賣契約價格：**「買賣契約價格」係指貸款人於貸款時，提供金融機構之買賣契約所記載價格，不代表實際交易價格；由財團法人金融聯合徵信中心採去識別化、區段化之處理方式，依住宅類別所產製的統計價格資訊。
        分別有平均單價、平均總價、十分位單價、十分位總價可供參考。本買賣契約價格資料僅供參考。
    '''


elif add_sidebar == sidebar_options[1]:

    st.subheader('越來越晚買房？')

    df = read_csv(filepath_age)

    '''
    根據聯徵中心網站的公開資料，抓取各年齡層購屋貸款資料。
    利用這份資料，繪製了自2009年Q1以來，每一季申辦房貸案件的年齡分布。可以觀察到：\n

    * 2009Q1時，申辦房貸最多的年齡層是30至35歲，其次是35至40歲。反應多數人成家立業的年齡。\n
    * 但是來到2023Q1，年齡層30至35歲落到了第3名，第1名則是40至45歲。似乎反應年輕人越來越晚才能有錢買房。\n
    '''
    ###############################################
    title = '新申辦房貸客戶件數年齡分佈 (2009Q1-2023Q1)'

    my_raceplot = barplot(df,
                          item_column='age_group_name',
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
        title=title,
        xaxis_title="承貸案件數",
        yaxis_title="",
        title_x=0.15,
        width=780,
        height=680,
        )

    st.plotly_chart(fig)

    st.text("")
    st.text("")
    st.text("")

    '''
    從平均年齡也可看到往上的趨勢，從下圖中可以看到明顯的分界是在2016年前後。
    2016年前購屋平均年齡大約落在39.5歲左右，但在2016年後卻是落在41歲左右。
    也就是現在的人平均而言，跟10年相比，晚了1~2年才購屋。
    '''
    ###############################################
    title = '新申辦房貸客戶平均年齡(2009Q1-2023Q1)'

    average_loan_age = ((df.groupby(['date_fmt'])['cnt_m_age'].sum() / df.groupby(['date_fmt'])['cnt'].sum()).reset_index(name='weighted_age'))
    lower_loan_age = ((df.groupby(['date_fmt'])['cnt_l_age'].sum() / df.groupby(['date_fmt'])['cnt'].sum()).reset_index(name='lower_age'))
    upper_loan_age = ((df.groupby(['date_fmt'])['cnt_u_age'].sum() / df.groupby(['date_fmt'])['cnt'].sum()).reset_index(name='upper_age'))

    x = average_loan_age['date_fmt']
    x_rev = x[::-1]

    fig = go.Figure()

    trace_line = go.Scatter(
        x=x,
        y=average_loan_age['weighted_age'],
        line_color='rgb(0,176,246)',
        showlegend=False,
        hovertemplate = '%{y:.2f}',
        name='weighted age',
        )

    trace_ubound = go.Scatter(
        x=x,
        y=upper_loan_age["upper_age"],
        fill='tonexty',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        hoveron='points',
        name='upper bound',
        )

    trace_lbound = go.Scatter(
        x=x,
        y=lower_loan_age["lower_age"],
        fill='tonexty',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        hoveron='points',
        name='lower bound',
        )

    fig.add_trace(trace_line)
    fig.add_trace(trace_ubound)
    fig.add_trace(trace_lbound)

    fig.add_vline(x="2015-12-31",
                  line_width=3, line_dash="dash", line_color="grey")

    fig.update_layout(
        width=780,
        height=400,
        title=title,
        title_x=0.15,
        hovermode="x unified",
        xaxis_title="",
        yaxis_title="平均年齡",
        )

    st.plotly_chart(fig)

    '''
    更細部來看，我把**30至35歲**每期申辦房貸件數當作基準，拿**35至40歲**, **40至45歲**, 以及**45至50歲**等3群人做比較。
    **用30至35歲的申辦件數當作分母**，**其他年齡層的申辦件數當作分子**，分別繪製折線圖如下。

    由圖可以看到，在2009年Q1時，35至40歲, 以及40至45歲的客群，比值都小於1，分別是0.94與0.86，代表原本申辦房貸件數都比30至35歲的客群少。

    但到了2023年Q1時，比值都大於1，分別是1.12與1.13，**代表申辦件數變得比30至35歲的客群來得多了，而且多出了約12%~13%左右！**
    '''
    ###############################################
    title = '各年齡層申請房貸件數 ÷ 30~35歲申請房貸件數  (單位：比值)'

    merged_df = (df[['date_fmt', 'age_group', 'cnt']]
                .merge(df.query('age_group=="30_35"')[['date_fmt', 'cnt']], on='date_fmt')
                .assign(cnt_over_30 = lambda d: round(d['cnt_x'] / d['cnt_y'], 2))
                )

    pv_df = pd.pivot(merged_df, index='age_group', columns='date_fmt', values='cnt_over_30')
    x_data = np.array(list(pv_df.columns) * 3).reshape(3, -1)
    y_data = pv_df.loc[['35_40', '40_45', '45_50']].values

    labels = ['35~40', '40~45', '45~50']
    colors = ['rgb(99,110,250)','rgb(239,85,59)','rgb(0,204,150)']
    lst_ytrace = len(pv_df.columns) - 1

    fig = go.Figure()

    for i in range(0, 3):
        fig.add_trace(go.Scatter(
            x=x_data[i], y=y_data[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i])
        ))

        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
            marker=dict(color=colors[i]),
            showlegend=False,
            hoverinfo="skip",
        ))

    annotations = []

    for y_trace, label, color in zip(y_data, labels, colors):
        # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                xanchor='right', yanchor='middle',
                                text=' {}'.format(y_trace[0]),
                                font=dict(family='Arial', size=12),
                                showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[lst_ytrace],
                                xanchor='left', yanchor='middle',
                                text='{}'.format(y_trace[lst_ytrace]),
                                font=dict(family='Arial', size=12),
                                showarrow=False))

    fig.update_layout(
        width=780,
        height=400,
        title=title,
        title_x=0.15,
        xaxis_title="",
        yaxis_title="件數倍率",
        annotations=annotations,
        hovermode='x unified',
        yaxis=dict(
            showgrid=False, zeroline=False, showline=False, showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=45, r=45, t=100,),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1)
        )

    st.plotly_chart(fig)

    '''
    從以上分析可以發現，的確申辦房貸主要客群的年齡層有往上的趨勢。是否因為年輕人薪資追不上不斷高漲的房價？
    還是年輕人結婚年齡延後，導致對買房的剛性需求也往後延？值得再進一步分析。
    '''

    '''
    需特別說明的是，因為資料限制，分析使用資料並非只限於第一次申請房貸的案件。
    所以也有可能是第二次以上購屋的案件變多了，而第二次購屋可能通常年齡會落在35歲之後，導致整體申辦房貸的年齡往上。
    關於此點也值得再進一步剖析。
    '''

    '''
    -----------------------------------------
    資料來源：聯徵中心住宅貸款統計查詢網( https://member.jcic.org.tw )。

    * 透過python的selenium套件來抓取資料。
    * 資料繪圖套件主要使用python的plotly套件，其中長條圖動畫則是運用raceplotly套件的程式再自行做了一些微調。
    * 整個網頁app則是使用python的streamlit套件來搭建。
    '''