import matplotlib.pyplot as plt
import pandas as pd 
if __name__=='__main__':
	df=pd.read_csv('huizong.csv',encoding='utf8')
	df=df.head(50)
	df['length'] = df['评论'].apply(lambda x: len(str(x)))
	len_df = df.groupby('length').count()
	sent_length = len_df.index.tolist()
	sent_freq = len_df['评论'].tolist()

	plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
	plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
	
	plt.bar(sent_length, sent_freq)
	plt.title("句子长度及出现频数统计图")
	plt.xlabel("句子长度" )
	plt.ylabel("句子长度出现的频数" )
	plt.savefig("./句子长度及出现频数统计图.png")
	plt.show()


