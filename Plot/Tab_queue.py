import Queue


#crée un tableu de queue
class Tab_queue:
	def __init__(self, taille):
		tab = []
		for i in xrange(taille):
			tab.append(Queue.Queue(0))
			
	def getTab(self):
		return self.tab
