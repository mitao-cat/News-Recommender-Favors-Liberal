import pandas as pd
import pickle

df1 = pd.read_csv('../../data/mind/MINDlarge_train/news.tsv', sep = '\t', header = None, names = ['news_id', 'category', 'subcategory', 'title', 'abstract', 'url', 'titleentities', 'abstractentites'])
df1 = df1.loc[:, ['news_id', 'subcategory', 'url']]
df2 = pd.read_csv('../../data/mind/MINDlarge_dev/news.tsv', sep = '\t', header = None, names = ['news_id', 'category', 'subcategory', 'title', 'abstract', 'url', 'titleentities', 'abstractentites'])
df2 = df2.loc[:, ['news_id', 'subcategory', 'url']]

df = pd.concat([df1, df2])

df_newspolitics = df[df['subcategory'] == 'newspolitics']
df_newsfactcheck = df[df['subcategory'] == 'newsfactcheck']
df_factcheck = df[df['subcategory'] == 'factcheck']
df_elections_2020_us = df[df['subcategory'] == 'elections-2020-us']
df_newslocalpolitics = df[df['subcategory'] == 'newslocalpolitics']
df_newsworldpolitics = df[df['subcategory'] == 'newsworldpolitics']
df = pd.concat([df_newspolitics, df_newsfactcheck, df_factcheck, df_elections_2020_us, df_newslocalpolitics, df_newsworldpolitics])

df.drop_duplicates(subset = ['news_id'], keep = 'first', inplace = True)

with open('../../data/mind/i2id.pkl', 'rb') as file:
    item_index = pickle.load(file)
df = df[df['news_id'].isin(item_index)]

policy_i = df['news_id'].tolist()
policy_id = []
for i in policy_i:
    policy_id.append(item_index[i])

with open('policy_id.pkl', 'wb') as file:
    pickle.dump(policy_id, file)
