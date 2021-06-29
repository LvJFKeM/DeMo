from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
import csv, re, operator

# from textblob import TextBlob

app = Flask(__name__)

person = {

	'first_name': 'LVJF',

	'tel': '+86 123 456 789',
	'email': '123456124@qq.com',
	'csd': 'www.LvJF.com',
	'address': 'HuBei HuangShi',

	'social_media': [
		{
			'link': '性别',
			'icon': 'Boy'
		},
		{
			'link': '出生日期',
			'icon': '29/7/1997'
		},
		{
			'link': 'SchoolTag',
			'icon': 'Hubei Normal University'
		},
		{
			'link': 'Education',
			'icon': 'Undergraduate'
		},
		{
			'link': 'Address',
			'icon': 'Hubei HuangShi Hubei Normal University'
		}
	],
	'img': '../static/img/aq.jpg',

	'experiences': [
		{
			'title': '教育经历',
			'description': '时间',
			'timeframe1': '2018.09-2019.01',
			'timeframe2': '2019.03-2022.07'
		},
		{
			'description': '学校----专业',
			'timeframe1': '湖北师范大学 -----计算机科学与技术专业',
			'timeframe2': '湖北师范大学 -----软件工程专业',

		},

		{
			'title': '主要课程',
			'description': '软件相关课程',
			'timeframe1': 'C、C++、Java、JavaWeb、Pyhton、数据库、软件测试、数据结构与算法、计算机操作系统、计算机网络、计算机组成原理',

		},
		{
			'description': '数学相关课程',
			'timeframe1': '高等数学、线性代数、概率论与数理统计、离散数学、数学建模基础、大学物理',

		},

		{
			'title': 'Self-evaluation:    ',

			'timeframe':
				['热爱数学、有非常好的逻辑思维处理能力。',
				 '对软件测试和开发有很高激情，热衷于新的知识学习。',
				 '热爱软件测试工作，可以胜任重复性工作，工作细致认真、积极主动、有耐心、严谨。',
				 '乐于学习，积极上进提升自我。']

		},

	],

	'programming_languages1_name': '个人技能',
	'programming_languages1':
		['1、熟悉软件测试理论知识，了解软件测试相关的黑白盒测试技术、等价类分析法，熟悉UML。',
		 '2、了解计算机基础知识，如操作系统底层，计算机组成原理、计算机网络等基础知识。',
		 '3、熟练使用C语言和C++基础。',
		 '4、熟悉Python基础、会常规的Python爬虫技术。',
		 '5、熟练使用Java,对java的基础使用。',
		 '6、熟悉javaweb,可以熟练使用HTML、CSS等等前端技术',
		 '7、熟悉javaweb,可以熟练使用HTML、CSS等等前端技术',
		 '8、掌握web开发框架MVC、Spring5框架。'
		 ],

}


# 1
@app.route('/')
def cv(person=person):
	return render_template('index.html', person=person)


@app.route('/callback', methods=['POST', 'GET'])
def cb():
	return gm(request.args.get('data'))


##入口
@app.route('/chart')
def index():
	# 1、各个国家GDP
	# 2、某高地密度等高线
	return render_template('chartsajax.html', graphJSON=gm(), graphJSON1=gm1())


##国家GDP
def gm(country='United Kingdom'):
	df = pd.DataFrame(px.data.gapminder())
	fig = px.line(df[df['country'] == country], x="year", y="gdpPercap")
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON


##等高线
def gm1():
	df = px.data.iris()
	fig = px.density_contour(df, x="sepal_width", y="sepal_length")

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON


# @app.route('/test')
# def test():
# 	return render_template("test.html")


@app.route('/senti')
def main():
	text = ""
	values = {"positive": 0, "negative": 0, "neutral": 0}
	with open('ask_politics.csv', 'rt') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for idx, row in enumerate(reader):
			if idx > 0 and idx % 2000 == 0:
				break
			if 'text' in row:
				nolinkstext = re.sub(
					r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
					'', row['text'], flags=re.MULTILINE)
				text = nolinkstext

			blob = TextBlob(text)
			for sentence in blob.sentences:
				sentiment_value = sentence.sentiment.polarity
				if sentiment_value >= -0.1 and sentiment_value <= 0.1:
					values['neutral'] += 1
				elif sentiment_value < 0:
					values['negative'] += 1
				elif sentiment_value > 0:
					values['positive'] += 1

	values = sorted(values.items(), key=operator.itemgetter(1))
	top_ten = list(reversed(values))
	if len(top_ten) >= 11:
		top_ten = top_ten[1:11]
	else:
		top_ten = top_ten[0:len(top_ten)]

	top_ten_list_vals = []
	top_ten_list_labels = []
	for language in top_ten:
		top_ten_list_vals.append(language[1])
		top_ten_list_labels.append(language[0])

	graph_values = [{
		'labels': top_ten_list_labels,
		'values': top_ten_list_vals,
		'type': 'pie',
		'insidetextfont': {'color': '#FFFFFF',
						   'size': '14',
						   },
		'textfont': {'color': '#FFFFFF',
					 'size': '14',
					 },
	}]

	layout = {'title': '<b>意见挖掘</b>'}
	return render_template('sentiment.html', graph_values=graph_values, layout=layout)


if __name__ == '__main__':
	app.run(debug=True, port=5000, threaded=True)
