import numpy as np
import argparse

LOG = False


def log(values):
	if LOG:
		print(values)


def ones(arr: np.ndarray):
	# Find the indices where value is 1
	y_indices, x_indices = np.where(arr[0:, :abs(arr.shape[1] - arr.shape[0])] == 1)

	# Filter the indices
	valid_indices = [(x, y) for x, y in zip(x_indices, y_indices) if arr[0][x] == 0]
	return valid_indices


def output(tableau: np.ndarray):
	valid_indices = ones(tableau)
	n, m = tableau.shape
	x = np.zeros(abs(m - n))
	for item in valid_indices:
		x[item[0]] = tableau[item[1]][m - 1]
	print("A vector of decision variables:", x)
	print("Optimal value:", np.array([tableau[0][tableau.shape[1] - 1]]))


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
		log(f"Iteration #{i} tableau:\n{tableau}")
		z_row = tableau[0, :n]

		pivot_n = np.argmin(z_row)  # Determine pivot column index
		pivot = z_row[pivot_n]

		if pivot >= 0:
			log("No more pivot columns available, can't optimize")
			output(tableau)
			break  # Can not optimize more

		log(f"Pivot column available: {pivot_n}")
		pivot_col = tableau[1:, pivot_n]
		b_col = tableau[1:, -1]

		not_zeros = np.where(pivot_col != 0)[0]
		ratio = np.array([b_col[i] / pivot_col[i] for i in not_zeros])
		positive_indices = np.where(ratio > 0)  # Indices of positive ratios

		if not positive_indices:
			log("No more pivot rows available, can't optimize")
			output(tableau)
			break

		pos_ind = [not_zeros[i] for i in np.where(ratio > 0)[0]]
		pivot_m = pos_ind[np.argmin(ratio[positive_indices])] + 1
		log(f"Pivot row available: {pivot_m}")

		pivot = tableau[pivot_m, pivot_n]
		log(f"Pivot: {pivot:.2f} at ({pivot_m}, {pivot_n})")
		tableau[pivot_m] /= pivot

		# Row elimination
		for row in range(m + 1):
			if row == pivot_m:
				continue

			tableau[row] -= tableau[pivot_m] * tableau[row, pivot_n]

		log('')
		i += 1


def main():
	global LOG

	input_file = "input.txt"
	LOG = False
	task_type = "Maximize"
	accuracy = "0.001"

	# Create a parser
	parser = argparse.ArgumentParser(description='Simplex method implementation to solve linear programming problems')
	# Add arguments
	parser.add_argument('-i', '--input', type=str, help='Set input file path. Default: input.txt')

	parser.add_argument('-l', '--log', action='store_true', help='Set logging. Default: False')

	parser.add_argument('-p', '--problem', type=str, help='Set problem type. Possible values: min, max. Default: max')

	parser.add_argument('-a', '--accuracy', type=str, help='Set approximation accuracy. Default: 0.001')
	# Parse the arguments
	args = parser.parse_args()

	# Check if input file is provided
	if args.input:
		input_file = args.input
	if args.log:
		LOG = args.log
	if args.problem == "min":
		task_type = "Minimize"
	elif args.problem == "max":
		...
	elif args.problem is None:
		task_type = "Maximize"
	else:
		raise ValueError("Problem type can be only min or max")

	if args.accuracy:
		accuracy = args.accuracy

	# Read input file
	with open(input_file) as file:
		elements = file.read().replace("\n", ' ').split("#")[1:]
		c, a, b = [np.asarray(i.split(":")[1].strip().split(" ")) for i in elements]
		c = np.array(c, dtype=float)
		b = np.array(b, dtype=float)
		a = np.reshape(np.array(a, dtype=float), (-1, c.size))

		decimals = len(accuracy.split('.')[1])

		# Change minimize problem to maximize
		c = -c if task_type == "Minimize" else c

		np.set_printoptions(precision=decimals, suppress=True)

		if np.any(b < 0):
			log('The method is not applicable!')
		else:
			maximize(a, b, c)


if __name__ == '__main__':
	main()
