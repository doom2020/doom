"""
scikit-learn 自然语言处理(NPL)
"""

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

# 文本文件(包含类别和文本内容两列)
file_name = r'C:\Users\mi\Desktop\you.txt'


# 获取所有行
with open(file_name, 'r', encoding='utf-8') as fr:
	content_list = fr.readlines()
	# print(content_list)

all_line_list = []
for line in content_list:
	line_ls = line.replace('\n', '').split('\t')
	# print(line_ls)
	all_line_list.append(line_ls)

# 转为数组
content_array = np.array(all_line_list)
# print(content_array)
print(content_array.shape)


# 测试集数组
test_array = content_array[0:500,:]
# 训练集数组
train_array = content_array[500:,:]
# print(test_array)
print(test_array.shape)
print(train_array.shape)

# 训练集分类标签
train_labels = train_array[:, 0]
print(train_labels)
print(train_labels.shape)
# 训练集文本特征
train_features = train_array[:, 1]
print(train_features.shape)

# 测试集分类标签
test_labels = test_array[:, 0]
# 测试集文本特征
test_features = test_array[:, 1]

# 文本转向量
count_vect = CountVectorizer()
train_counts = count_vect.fit_transform(train_features)
print(train_counts.shape)

# 权重处理一
# tf_transformer = TfidfTransformer(use_idf=False).fit(train_counts)
# train_tf = tf_transformer.transform(train_counts)
# train_tf.shape

# 权重处理二
tfidf_transformer = TfidfTransformer()
train_tfidf = tfidf_transformer.fit_transform(train_counts)

# 朴素贝叶斯估计器
clf = MultinomialNB().fit(train_tfidf, train_labels)

# 测试集转向量
test_counts = count_vect.transform(test_features)
# 测试集权重处理
test_tfidf = tfidf_transformer.transform(test_counts)

# 预测
predicted = clf.predict(test_tfidf)
print(predicted)
print(predicted.shape)

# 正确率
correct = [test_labels[i] == predicted[i] for i in range(len(predicted))]
t = correct.count(True)
f = correct.count(False)
rate = t / len(predicted)

print("correct: %s" % rate)

""" 使用Pipeline进行封装"""

from sklearn.pipeline import Pipeline

# text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB()),])
# text_clf.fit(train_features, train_labels)

# predict2 = text_clf.predict(test_features)
# print('11111111111111')
# print(np.mean(predict2 == test_labels))

from sklearn.linear_model import SGDClassifier
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42,max_iter=5, tol=None)),])
text_clf.fit(train_features, train_labels)
predict3 = text_clf.predict(test_features)
print('222222222222222')
print(np.mean(predict3 == test_labels))

from sklearn import metrics

print(metrics.classification_report(test_labels, predict3))




