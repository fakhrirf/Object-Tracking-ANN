from pandas import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn import neighbors, datasets

class Classified:
	
	databaseANN = None
	x = None
	y = None 
	clf1 = None
	clf2 = None


	def __init__ (self):
		database1 = 'database.csv'
		database = pd.read_csv(database1)
		self.x = database[[u'Feature1', u'Feature2']] 
		self.y1 = database.Target1	
		self.clf1 = MLPClassifier(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(20, 20), random_state=1)
		self.clf1.fit(self.x, self.y1)
		self.clf2 = MLPClassifier(solver='lbfgs', alpha=1e-5,
                     	hidden_layer_sizes=(20, 20), random_state=1)
		

  

