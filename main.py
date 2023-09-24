import numpy as np

LOG = True


def log(values):
	if LOG:
		print(values)



def ones(arr: np.ndarray):
	# Find the indices where value is 1
	y_indices, x_indices = np.where(arr == 1)

	# Filter the indices based on the constraint
	valid_indices = [(x, y) for x, y in zip(x_indices, y_indices) if arr[0][x] == 0]
	# x+1 - номер икса, y - строчка с его ответом
	return valid_indices

def output(tableau: np.ndarray):
	valid_indices = ones(tableau)
	n,m = tableau.shape
	x = np.zeros(m-n)
	for item in valid_indices:
		x[item[0]] = tableau[item[1]][m-1]
	print("A vector of decision variables:", x)
	print("Optimal value:",tableau[0][tableau.shape[1]-1])


def maximize(A: np.ndarray, b: np.ndarray, c: np.ndarray):
	assert np.ndim(A) == 2
	m, n = A.shape

	assert np.ndim(c) == 1 and c.shape[0] == n
	assert np.ndim(b) == 1 and b.shape[0] == m and np.all(b >= 0)

	tableau = np.zeros((m + 1, m + n + 1))
	tableau[0, :n] = -1 * c  # Z row
	tableau[1:, :n] = A  # Constraint variables
	tableau[1:, n:-1] = np.eye(m)  # Slack variables
	tableau[1:, -1] = b  # Solution/b column

	i = 0
	while True:
		# log(f"Iteration #{i} tableau:\n{tableau}")
		z_row = tableau[0, :n]

		pivot_n = np.argmin(z_row)  # Determine pivot column index
		pivot = z_row[pivot_n]

		if pivot >= 0:
			# log("No more pivot columns available, can't optimize")
			output(tableau)
			break  # Can not optimize more

		# log(f"Pivot column available: {pivot_n}")
		pivot_col = tableau[1:, pivot_n]
		b_col = tableau[1:, -1]

		ratio = b_col / pivot_col # FIXME: division by zero
		positive_indices = np.where(ratio > 0)  # Indices of positive ratios

		if not positive_indices:
			# log("No more pivot rows available, can't optimize")
			output(tableau)
			break

		index = np.argmin(ratio[positive_indices])
		pivot_m = positive_indices[0][index] +1
		# log(f"Pivot row available: {pivot_m}")

		pivot = tableau[pivot_m, pivot_n]
		# log(f"Pivot: {pivot:.2f} at ({pivot_m}, {pivot_n})")
		tableau[pivot_m] /= pivot

		# Row elimination
		for row in range(m + 1):
			if row == pivot_m:
				continue

			tableau[row] -= tableau[pivot_m] * tableau[row, pivot_n]

		# log('')
		i += 1



file_info = np.genfromtxt("input.txt", delimiter=',', skip_footer=2)

c = file_info[0]
b = file_info[file_info.shape[0]-1]
a = file_info[1:file_info.shape[0]-1]
x = a[~np.isnan(a)] # Get rid of nan values
b = b[~np.isnan(b)] # Get rid of nan values

with open("input.txt") as file:
	lines = file.readlines()
	task_type = lines[len(lines)-1]
	accuracy = lines[len(lines)-3]
	decimals = len(accuracy.split('.')[1])-1

# Change minimize problem to maximize
c = -c if task_type == "Minimize" else c

np.set_printoptions(precision=decimals, suppress=True)

if np.any(b < 0) :
	log('The method is not applicable!')
else:
	maximize(a, b, c)