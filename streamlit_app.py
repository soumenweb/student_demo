import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
st.set_page_config(page_title="student",page_icon="🎓",layout="wide",initial_sidebar_state="expanded")
#sql connection 
conn =sqlite3.Connection("database.db")
corsor =conn.cursor()

#create database student table
#table filds are st_id, Name,dob,gender,adress,phone,LQ
# conn.execute("create table student (st_id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(50), dob DATE, gender VARCHAR(20), adress VARCHAR(80),phone VARCHAR(20), LQ VARCHAR(30))")
# conn.commit()
# print("done")

#fees database
# conn.execute("create table student_fees(name VARCHAR(50),month VARCHAR(20), amount VARCHAR(10), date VARCHAR(20), remark VARCHAR(50))")
# conn.commit()
# print("fees done")

# st.sidebar.header(":red[WELCOME] YOUR MENU",divider="red")
# st.sidebar.subheader("Now Handel your :orange[Students very Easy]")

menu = st.sidebar.selectbox("Select your work", options=["Register data","view data","fees form", "Fees view", "data report"])
if(menu =="Register data"):
 st.header("STUDENT :red[REGISTRATION FORM FILLUP]")
 def ad_form():
    with st.form(key="newstu"):
        col1,col2,col3 = st.columns(3)
        with col1:
            name = st.text_input("Enter Your Name")
            add = st.text_area("Enter your address",placeholder="type address")

        with col2:
            dob = st.date_input("enter your DOB")
            phone = st.text_input("Type your number")
        with col3:
             gender = st.selectbox("Select your Gender",options=["Male","Female"])
             lq = st.text_input("enter your Last Qualification")
        sub_but =st.form_submit_button("submit")
        if (sub_but==True):
            st.success("Your Data successfully Submited")
            ins_data(name,dob,gender,add,phone,lq)
 def ins_data(a,b,c,d,e,f):
     corsor.execute("INSERT INTO student(Name,dob,gender,adress,phone,LQ) VALUES (?,?,?,?,?,?)",(a,b,c,d,e,f))
     conn.commit()
     conn.close()
     st.info("Wow! Now you Can cheek your database")
 ad_form()

 st.html('''
         <marquee> Hello Students! 🥹🧑‍🎓😁 Plaese Inform Your Perfect Deteils 😒👍  </marquee>
         ''')


if (menu=="view data"):
    st.header(":orange[ALL STUDENTS] ADMISSSION DETEILS IN THIS PAGE",divider="red")
    def view_stu():
        corsor.execute("SELECT * FROM student")
        res =corsor.fetchall()
        conn.close()
        return res
    
    data = view_stu()
    Panda_data =pd.DataFrame(data,columns=["Student ID","Name","DOB","Gender","Address","Phone","Last Qu"])
    st.dataframe(Panda_data)
     

if (menu =="fees form"):
    st.header(":red[Student Fees Deteils] 🥸🧑‍🎓", divider="grey",)
    def feesad():
        with st.form(key="fees"):
            fees_name = st.text_input("student name", placeholder="input studnwet name")
            fees_month = st.text_input("Fees month",placeholder="input your fees month")
            fees_amount = st.text_input("Payment Amount",placeholder="Type your fees amount")
            fees_date = st.date_input("payment date")
            fees_remmark = st.text_area("Remark",placeholder="optional remark")
            but = st.form_submit_button("submit", icon="🌞")
            if (but == True):
                st.success("Your Fees was Submit successfully!")
                fees_add(fees_name,fees_month,fees_amount,fees_date,fees_remmark)
    def fees_add(a,b,c,d,e):
        conn.execute("INSERT INTO student_fees(name,month,amount,date,remark) VALUES (?,?,?,?,?)",(a,b,c,d,e))
        conn.commit()
        conn.close()
        st.info("Fees added! Now you can cheek your fees")
    feesad()


if (menu =="Fees view"):
     st.header(":red[Wow!] 🥹🥰 It's amezing")
    
     tab1, tab2, tab3, tab4 = st.tabs(["student Fees (month wise) view","Total Amount Payble","Fees Graph","Real time"])
     with tab1:
        def fee_show():
         ser_name =st.text_input("Enter student name")
         corsor.execute("SELECT student_fees.name, student_fees.month,student_fees.amount,student_fees.date,student_fees.remark FROM student INNER JOIN student_fees ON student.Name=student_fees.name and student.Name=?",(ser_name,))
         fee_res = corsor.fetchall()
         conn.close()
         return fee_res
        data_store = fee_show()
        panda_fees = pd.DataFrame(data_store, columns=["Student Name","Fees Month","Fees amount","Deposite date","remark"])
        st.dataframe(panda_fees)

        col1,col2 = st.columns(2)
        with col1:
            st.header("Top Fees Data :red[Showing Display]")
            def top():
                 conn =sqlite3.Connection("database.db")
                 corsor =conn.cursor()
                 top_name = st.slider("select Number what your yiew",1,30,step=1)
                 corsor.execute("SELECT * FROM student_fees")
                 all_data = corsor.fetchall()
                 conn.close()
                 pand_data = pd.DataFrame(all_data,columns=["name","month","amount","date","remark"])
                 pan1=pd.DataFrame(pand_data.head(top_name))
                 st.dataframe(pan1)
            top()  
        with col2:
            st.header("Buttom Fees data :orange[Your Display]")
            def low():
                 conn =sqlite3.Connection("database.db")
                 corsor =conn.cursor()
                 bot_top_name = st.slider("select Number what your yiew",1,30,step=1,key="low")
                 corsor.execute("SELECT * FROM student_fees")
                 all_data = corsor.fetchall()
                 conn.close()
                 pand_data = pd.DataFrame(all_data,columns=["name","month","amount","date","remark"])
                 pan2=pd.DataFrame(pand_data.tail(bot_top_name))
                 st.dataframe(pan2)  
            low()    
     with tab2:
         def pay():
             conn =sqlite3.Connection("database.db")
             corsor =conn.cursor()
             sar_name =st.text_input("Enter student name",key="ignore")
             corsor.execute("SELECT student_fees.name, sum(student_fees.amount), sum(student_fees.amount)- 4000 FROM student INNER JOIN student_fees ON student.Name=student_fees.name and student.Name=?",(sar_name,))
             feee_res = corsor.fetchall()
             conn.close()
             return feee_res
         data_store = pay()
         pdn_fees = pd.DataFrame(data_store, columns=["Student Name","Total amount","deu fees"])
         st.dataframe(pdn_fees)
         st.bar_chart(pdn_fees,x="Student Name",y=["deu fees","Total amount"],horizontal=True,)
     with tab3:
         def chart():
             conn =sqlite3.Connection("database.db")
             corsor =conn.cursor()
             corsor.execute("SELECT amount, month FROM student_fees")
             chart_show =corsor.fetchall()
             corsor.close()
             return chart_show
         show_chart = chart()
         char1 = pd.DataFrame(show_chart,columns=["amount","month"])
         st.dataframe(char1)
         st.bar_chart(char1, x="month", y="amount")
         st.header("hello")
         
