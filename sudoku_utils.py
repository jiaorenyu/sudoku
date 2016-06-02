
import copy
import time

thisarray=[
	[0,8,0,6,0,0,4,0,9],
	[2,0,9,0,0,0,0,6,0],
	[0,3,0,4,0,9,0,0,0],
	[0,0,0,1,0,0,0,4,0],
	[0,1,0,0,9,0,7,0,5],
	[8,0,0,0,3,7,0,9,1],
	[0,0,3,0,0,0,8,0,6],
	[0,6,0,0,5,0,0,0,0],
	[0,0,0,7,4,0,3,0,2]
	]
'''
array = [
	[1,0,0, 6,0,0, 0,0,8],
	[4,0,7, 1,0,0, 5,0,2],
	[0,0,3, 7,4,0, 0,0,9],

	[9,0,0, 0,0,4, 7,0,3],
	[0,0,1, 9,0,0, 6,0,0],
	[6,0,4, 3,0,8, 0,0,5],

	[5,0,0, 0,3,7, 8,0,0],
	[7,0,8, 0,0,1, 2,0,6],
	[2,0,0, 0,0,6, 0,0,7]
]
'''

values=[
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0]
	]


def cal_pvalues(data):
	for i in range(len(data)):
		for j in range(len(data[i])):
			if data[i][j] == 0:
				values[i][j] = get_values(data,i,j)
				if len(values[i][j]) == 0:
					return False
	return True

def unfinish(data):
	for ldata in data:
		for v in ldata:
			if v == 0:
				return True
	return False

def conflict(data, i, j, pv):
	for v in data[i]:
		if pv == v:
			return True
	for x in range(len(data)):
		if data[x][j] == pv:
			return True
	
	for x in range(3):
		for y in range(3):
			xxi = i/3
			yyj = j/3
			xx = xxi*3+x
			yy = yyj*3+y
			if data[xx][yy] == pv:
				return True
	return False

def get_line_values(data, index, line_type):
	current_values = []
	
	if line_type == "row":
		for v in data[index]:
			if v != 0:
				current_values.append(v)
			
	elif line_type == "col":
		for i in range(len(data)):
			if data[i][index] != 0:
				current_values.append(data[i][index])

	possible_values = []  
	for i in range(1,10):
		if i not in current_values:
			possible_values.append(i)

	return set(possible_values)
	

def get_matrix_values(data, row, col, msize):
	c_values = []
	for i in range(msize):
		for j in range(msize):
			v = data[row*msize+i][col*msize+j]
			if v != 0:
				c_values.append(v)

	possible_values = []  
	for i in range(1,10):
		if i not in c_values:
			possible_values.append(i)

	return set(possible_values)

def get_values(data,i,j):
	pvalues = []
	line_value_row = get_line_values(data,i,"row")
	line_value_col = get_line_values(data,j,"col")
	matrix_value = get_matrix_values(data, i/3, j/3, 3)
	pvalues = list(line_value_row & line_value_col & matrix_value)
	
	return pvalues

def happen_counts_row(values, i, pv):
	counter = 0
	for x in range(9):
		if values[i][x] != 0 and pv in values[i][x]:
			counter += 1
	return counter
def happen_counts_col(values, j, pv):
	counter = 0
	for x in range(9):
		if values[x][j] != 0 and pv in values[x][j]:
			counter += 1
	return counter

def happen_counts_mat(values, i, j, pv):
	counter = 0
	xi = i/3
	yj = j/3
	for x in range(3):
		for y in range(3):
			xx = xi*3 + x
			yy = yj*3 + y
			if values[xx][yy] != 0 and pv in values[xx][yy]:
				counter += 1
	
	return counter
	
def reasoning(data_new, i, j):
	counter = 0
	pvalues = values[i][j]
	if len(pvalues) == 1:
		return pvalues[0]
	for pv in pvalues:
		counter = happen_counts_row(values, i, pv)
		if counter == 1:
			return pv
		
		counter = happen_counts_col(values, j, pv)
		if counter == 1:
			return pv
	
		counter = happen_counts_mat(values, i, j, pv)
		if counter == 1:
			return pv
	return None

def scan(data):
	if not cal_pvalues(data):
		return [False, data_new]
	data_new = copy.deepcopy(data)
	for i in range(9):
		for j in range(9):
			if data_new != 0:
				continue
			value = reasoning(data_new, i, j)
			if value == None:
				continue
			if conflict(data_new, i, j, value):
				return [False, data_new]
			if not cal_pvalues(data_new):
				return [False, data_new]

	return [True, data_new]


   

status_save = []

def get_min(values):
	[i,j] = [0,0]
	min_len = 10
	for x in range(len(values)):
		for y in range(len(values[0])):
			if values[x][y] != 0:
				if len(values[x][y]) < min_len:
					[i, j] = [x, y]
					min_len = len(values[x][y])
	
	return [i, j]

def guess(data, values, status_save):
	[i,j] = get_min(values)   
	

	if len(values[i][j]) == 0:
		return False

	pv = values[i][j].pop()
	print("guess", i, j, pv)

	if len(values[i][j]) == 0:
		values[i][j] = 0
	status_save.append([i, j, copy.deepcopy(data), copy.deepcopy(values)])
	data[i][j] = pv
	
	return True

def recover(data, values, status_save):
	if len(status_save) == 0:
		return False

	[i,j, data, values] = status_save.pop()
	
	return True

def print_data(data, datatype="new data"):
	print(datatype)
	for l in data:
		print(l)
	print("------------")

def sudoku(array):
	counter = 0
	data = copy.deepcopy(array)
	ori = copy.deepcopy(array)
	flag = True 
	guess_counter = 0
	while (unfinish(data)):
		flag=True
		while(unfinish(data)):
			counter += 1
			[stat, data_new] = scan(data)
			if not stat:
				flag = False 
				break
			if data_new == data: break;
			data = copy.deepcopy(data_new)
		if (unfinish(data)):
			guess_counter += 1
			if flag:
				if not guess(data, values, status_save):
					return None
			else:
				if not recover(data, values, status_save):
					return None 
				if not guess(data, values, status_save):
					return None 
		
	print(time.time())
	print("counter",counter)
	print("guess_counter", guess_counter)
	print_data(ori, "ori")
	print_data(data, "new")   

	return data

if __name__=="__main__":
	result=sudoku(array)
	if result != None:
		print("OK")
		print_data(result)
	else:
		print("Failed")
