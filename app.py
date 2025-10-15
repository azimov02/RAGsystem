import streamlit as st
from google import genai
import mysql.connector

st.title("RAG system")

instructions1="""
Now you will be part of the RAG system. There are 2 steps. In first step I give you the schema so you know which variables are in SQL table and the user query. 
Your task is to generate SQL query so you can perform operations on the table named ragtable. User may not know complete names, may misspell them, or use synonyms. Act strictly according to the scheme.
And don't respond with anything out of the instruction.
The following is the scheme of mysql table called ragtable :
    record_id int ,
    order_id char(100) ,
    customer_code char(100) ,
    customer_name char(100) ,
    customer_email char(100) ,
    customer_segment char(10) ,
    country char(100) ,
    city char(100) ,
    product_category char(100) ,
    product_name char(100) ,
    sku char(20) ,
    quantity int ,
    unit_price double ,
    discount_pct double ,
    shipping_cost double ,
    weight_kg double ,
    order_date date ,
    ship_date date ,
    delivery_date date ,
    delivery_status char(20) ,
    carrier char(100) ,
    incoterm char(100) ,
    payment_method char(100) ,
    currency char(10) ,
    exchange_rate_to_usd double ,
    gross_revenue double ,
    cogs double ,
    profit double ,
    risk_score smallint ,
    is_fraud_suspected tinyint(1) ,
    shipment_code char(20) ,
    tracking_number char(30) ,
    record_notes char(100) ,
    warehouse_code char(20) ,
    sales_rep char(100) ,
    customer_phone char(20) ,
    customer_vat_id char(100) ,
    packaging_type char(20) ,
    package_l double ,
    package_w double ,
    package_h double ,
    volumetric_weight_kg double ,
    customs_declared_value_usd double ,
    last_mile_partner char(100) ,
    signature_required char(10) ,
    qa_check char(10) ,
    return_reason char(100) ,
    pdf_note char(100) ,
    external_document_id char(20);
    And the following is the query:
    """
# Turn the query that I will tell you now into SQL query to perform operations on this table. Respond with only SQL query
instructions2="""Now is the second step of RAG system you are part of.
You will get the result of SQL query and the original question. Combine them and give an answer, but in a way that is presentable to the general users(As you answer is not for chat don't use formatting marks).
Don't say anything except response to the user:"""

input_query=st.text_input(label="Input query here")
if(input_query):
    client = genai.Client(api_key="******")

    query = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=instructions1+input_query,
    )

    query=query.text[7:-3].replace('\n'," ")

    db_connection = mysql.connector.connect(
        host="localhost",         
        user="root",             
        password="*****", 
        database="ragsystem" 
    )

    cursor = db_connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    query_result=""

    for row in results:
        query_result+=str(row)

    if query_result=="":#in case if result is empty we manually set it to empty result so LLM will recognize it
        query_result="Empty result"


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=instructions2+query_result+input_query,
    )

    st.write(response.text)    
    st.write("The SQL query is",query)
    st.write("The raw answer is",query_result)
    db_connection.close()