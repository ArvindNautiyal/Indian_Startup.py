import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(layout='wide')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')

def load_overall_details():
    st.title("Overall Analysis")
    col1 , col2 = st.columns(2)
    with col1:
        total = round(df['amount'].sum())
        st.metric('Total Amount Invested ',str(total) + ' cr')
    with col2:
        maxx = df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1).values[0]
        st.metric('Top 5 Invested Startup',str(maxx) + ' cr')
    col3 , col4 = st.columns(2)
    with col3:
        avg = df.groupby('startup')['amount'].sum().mean()
        st.metric("Average Invested Money",str(round(avg)) + ' cr')
    with col4:
        total1 = df['startup'].nunique()
        st.metric("Total Startup",str(total1) + " Startup's")



def load_investor_details(investor):
    st.subheader(investor)
    last_5 = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.dataframe(last_5)
    col1 , col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Investment')
        big = df[df['investors'].str.contains(investor)].groupby("startup")['amount'].sum().sort_values(
            ascending=False).head()
        fig, ax = plt.subplots(figsize=(5,3))
        ax.bar(big.index, big.values, color='blue')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title('Top 5 Company Invested by investor',fontsize=8)
        ax.set_xlabel("Companies in which investor invested ",fontsize=8)
        ax.set_ylabel('Money in INR (Crores)',fontsize=8)
        st.pyplot(fig)
    with col2:
        st.subheader("Investing Sectors")
        pie = df[df['investors'].str.contains(investor)].groupby('vertical').sum('amount').head()
        fig1, ax1 = plt.subplots()
        ax1.pie(x=pie.amount, autopct='%.0f%%', labels=pie.index, startangle=90)
        ax1.set_title("Top 5 Investing Sectors of Investor")
        st.pyplot(fig1)
    col2 , col3 = st.columns(2)

    with col2:
        st.subheader('Stage of investing')
        round = df[df['investors'].str.contains(investor)].groupby('round').sum('amount').head()
        fig2, ax2 = plt.subplots()
        ax2.pie(x=round.amount, autopct='%.0f%%', labels=round.index, startangle=90)
        ax2.set_title("Top 5 Investing Stages of Investor")
        st.pyplot(fig2)
    with col3:
        st.subheader("City wise Investment")
        city = df[df['investors'].str.contains(investor)].groupby('city').sum('amount').head()
        fig3,ax3 = plt.subplots()
        ax3.pie(x=city.amount,autopct='%.0f%%',labels=city.index,startangle=90)
        ax3.set_title("Top 5 Invested City by Investor")
        st.pyplot(fig3)

    col4 , col5 = st.columns(2)
    with col4:
        st.subheader('Year - Year Investment')
        year = df[df['investors'].str.contains(investor)].groupby(df['date'].dt.year).sum('amount')
        fig4, ax4 = plt.subplots()
        ax4.plot(year)
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        ax4.set_xlabel('Years')
        ax4.set_ylabel("Money in INR (Crores)")
        ax4.set_title("Investor year wise Investment")
        st.pyplot(fig4)

st.sidebar.title("Startup Funding Analysis")
Option = st.sidebar.selectbox("Select One",['Overall Analysis','Startup','Investor'])

if Option == 'Overall Analysis':
    btn0 = st.sidebar.button('Details')
    if btn0:
        load_overall_details()
elif Option == 'Startup':
    st.title("Startup Analysis")
    st.sidebar.selectbox("Select Startup",df['startup'].unique().tolist())
    bt1 = st.sidebar.button("Startup Details")

else:
    st.title('Investor Analysis')
    df['investors'] = df['investors'].astype(str)
    selected_investor = st.sidebar.selectbox("Select Investor", sorted(set(df['investors'].str.split(',').sum())))
    bt2 = st.sidebar.button("Investor Details")
    if bt2:
        load_investor_details(selected_investor)








