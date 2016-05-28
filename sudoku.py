import tornado.ioloop
import tornado.web
import tornado.gen


import os
import copy

from sudoku_utils import sudoku

class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self):
		yield tornado.gen.Task(self.render, "index.html")

class SudokuHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self):
		sudoku_list = []
		line = []
		'''
		for i in range(9):
			line = []
			for j in range(9):
				param_name = str(i)+"_"+str(j)
				value = self.get_argument(param_name)
				if value == '':
					value = 0
				else:
					value = int(value)
				line.append(value)
			sudoku_list.append(copy.deepcopy(line))
		'''
		answers = yield tornado.gen.Task(sudoku, sudoku_list)
#answers = sudoku(sudoku_list)

		self.render('smile.html', answers=answers)
		self.finish()

	def post(self):
		sudoku_list = []
		line = []
		for i in range(9):
			line = []
			for j in range(9):
				param_name = str(i)+"_"+str(j)
				value = self.get_argument(param_name)
				if value == '':
					value = 0
				else:
					value = int(value)
				line.append(value)
			sudoku_list.append(copy.deepcopy(line))

		answers = sudoku(sudoku_list)
		self.render('smile.html', answers=answers)

def make_app():
	return tornado.web.Application([
			(r"/sudoku", IndexHandler),
			(r"/sudoku/answer", SudokuHandler) 
					],
			template_path = os.path.join(os.path.dirname(__file__), "templates")
				)

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
