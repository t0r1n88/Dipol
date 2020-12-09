import pandas as pd

dict_to_frame = {'username': [], 'password': [], 'firstname': [], 'lastname': [], 'email': [], 'cohort1': []}
group_df = pd.DataFrame(dict_to_frame)
cohort = 'БРИТ_М-19'
df = pd.read_csv('data/М-19.csv', sep=';', encoding='cp1251', )
# Ввиду того что Moodle нре пропускает логины с заглавными буквами, логины принудительно сделаны в нижнем регистры
group_df['username'] = df['email']
group_df['password'] = df['Пароль']
group_df['firstname'] = df['Имя']
group_df['lastname'] = df['Фамилия']
group_df['email'] = df ['email']
group_df['cohort1'] = cohort


group_df.to_csv('1.csv',encoding='cp1251',index=False)
#
df1 = pd.read_csv('1.csv',sep=',',encoding='cp1251')
df2 = pd.read_csv('2.csv',sep=',',encoding='cp1251')
# print(df1)
# print(df2)
# # df3 = df1.merge(df2,how='outer',left_on='username',right_on='username')
# # df1.merge(df2,how='outer',left_on='username',right_on='username')
df3=pd.concat([df1,df2])
print(df3)
print(df3.columns)
print(df3.shape)
df3.to_csv('3.csv',encoding='cp1251',index=False)
