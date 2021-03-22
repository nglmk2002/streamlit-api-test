import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np


#야후금융에서 주식정보를 제공하는 라이브러리 yfiance 이용
#주식정보를 불러오고 차트 그리는거 합니다.

#해당 주식에대한 트윗글들을 불러올수 있는 api가 있다.
#stocktwits.com 에서 제공하는 Restful API 를 호출해서
#데이터 가져오는것 실습

#API 호출을 위한 라이브러리 임포트
import requests

#프로펫 라이브러리 임포트
from fbprophet import Prophet

def main():
    st.header('Online Stock Price Ticker')
    #yfinace 실행
    
    symbol = st.text_input('심볼 입력 : ')
    data = yf.Ticker(symbol)
    
    today = datetime.now().date().isoformat()
    print(today)

    df = data.history(start='2010-06-01',end=today)
    st.dataframe(df)

    st.subheader('종가')
    st.line_chart(df['Close'])

    st.subheader('거래량')
    st.line_chart(df['Volume'])

    #yfinace 라이브러리만의 정보
    #data.info
    # data.calendar
    # data.major_holders
    # data.institutional_holders
    # data.recommendations
    div_df = data.dividends
    st.dataframe(div_df.resample('Y').sum())

    new_df = div_df.reset_index()
    new_df['Year'] = new_df['Date'].dt.year

    st.dataframe(new_df)

    fig = plt.figure()
    plt.bar(new_df['Year'],new_df['Dividends'])
    st.pyplot(fig)
    
    #여러주식 데이터를 한번에 보여주기
    favorites = ['msft','tsla','nvda','aapl','amzn']
    
    f_df = pd.DataFrame()

    for stock in favorites:
        f_df[stock]=yf.Ticker(stock).history(start='2010-01-01',end=today)['Close']
    st.dataframe(f_df)

    st.line_chart(f_df)

    # 스탁트위의 API를 호출!
    # res = requests.get('https://api.stocktwits.com/api/2/streams/symbol/{}.json'.format(symbol))
    # #json 형식으로 .json()이용
    # res_data = res.json()
    # #파이썬의 딕셔너리와 리스트조합으로 이용
    # #st.write(res_data)

    # for message in res_data['messages']:
        
    #     col1, col2 = st.beta_columns([1,4])

    #     with col1 :

    #         st.image(message['user']['avatar_url'])
    #     with col2:
    #         st.write('유저이름 : ' + message['user']['username'])
    #         st.write('트윗 내용 : ' + message['body'])
    #         st.write('올린 시간 : ' + message['created_at'])
    
    p_df = df.reset_index()
    p_df.rename(columns = {'Date':'ds','Close':'y'},inplace=True)

    #st.dataframe(p_df)
    m = Prophet()
    m.fit(p_df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    st.dataframe(forecast)

    fig1 = m.plot(forecast)
    st.pyplot(fig1)
    fig2 = m.plot_components(forecast)
    st.pyplot(fig2)

if __name__ == '__main__' :
    main()