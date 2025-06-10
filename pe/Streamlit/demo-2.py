import streamlit as st
from sqlalchemy import text

# 初始化连接（自动复用连接池）
conn = st.connection("mysql", type="sql")

# 执行查询（带缓存，10分钟过期）
df = conn.query("SELECT * FROM users WHERE age > :age",
                ttl=600, params={"age": 18})
st.dataframe(df)