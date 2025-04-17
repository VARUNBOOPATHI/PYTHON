import  streamlit as st
import mysql.connector
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='project'
)
def add_customer(name, phno, password, balance):
    a=mydb.cursor()
    query='insert into customer(cname,phno,password,balance) values(%s,%s,%s,%s)'
    a.execute(query,(name,phno,password,balance))
    mydb.commit()
    a.execute('select cid,cname,phno,password,balance from customer where phno=%s',(phno,))
    b=a.fetchall()
    st.write(f'customer_id = {b[0][0]}\n'
             f'customer_name = {b[0][1]}\n'
             f'customer_phno = {b[0][2]}\n'
             f'customer_password= {b[0][3]}')
    st.success('CUSTOMER ADDED SUCESFULLY')

st.header('WELCOME TO THE ABCD BANK')
menu=['ADD THE CUSTOMER','WITHDRAW','DEPOSIT','VIEW_BALANCE']
option=st.selectbox('OPTION',menu)
if option=='ADD THE CUSTOMER':
    name=st.text_input('NAME')
    phno=st.number_input('PHNO',min_value=0,format='%d')
    password=st.text_input('PASSWORD',type='password')
    balance=st.number_input('BALANCE',min_value=1000)
    button=st.button('CREATE')
    if button:
        add_customer(name, phno, password, balance)
elif option=='WITHDRAW':
    cid=st.number_input('CID',min_value=0,format='%d')
    password=st.text_input('password',type='password')
    amount=st.number_input('AMOUNT',min_value=0,format='%d')
    if st.button('withdraw'):
        a=mydb.cursor()
        query='select cid,password,balance from customer where cid=%s'
        a.execute(query,(cid,))
        b=a.fetchall()
        if password==b[0][1] and cid==b[0][0]:
            if amount <=b[0][2]:
                s=mydb.cursor()
                s.execute(f'update customer set balance =balance -{amount} where cid={cid}')
                mydb.commit()
                st.success('withdraw sucesfull...')
            else:
                st.error('INSUFFICIENT BALANCE')
elif option=='DEPOSIT':
    cid=st.number_input('CID',min_value=0)
    password=st.text_input('PASSWORD',type='password')
    amount=st.number_input('AMOUNT',min_value=0,format='%d')
    if st.button('DEPOSIT'):
        a=mydb.cursor()
        a.execute('select cid,password from customer where cid=%s',(cid,))
        b=a.fetchall()
        if password ==b[0][1] and cid==b[0][0]:
            a.execute(f'update customer set balance=balance+{amount} where cid={cid}')
            mydb.commit()
            st.success(f'{amount} deposited...')
        else:
            st.error(f'{amount} not deposited..')
elif option=='VIEW_BALANCE':
    cid=st.number_input('CID',min_value=0)
    password=st.text_input('PASSWORD',type='password')
    if st.button('SUBMIT'):
        a=mydb.cursor()
        a.execute('select cid,password, balance from customer where cid=%s',(cid,))
        b=a.fetchall()
        if password==b[0][1] and cid==b[0][0]:
            st.write(f'your balnce is :- {b[0][2]}')
        else:
            st.error('invalid credentials...')



