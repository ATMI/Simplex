import numpy as np

LOG = True
np.set_printoptions(precision=2, suppress=True)


def log(values):
	if LOG:
		print(values)


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
			break  # Can not optimize more

		log(f"Pivot column available: {pivot_n}")
		pivot_col = tableau[1:, pivot_n]
		b_col = tableau[1:, -1]

		ratio = b_col / pivot_col # FIXME: division by zero
		positive_indices = np.where(ratio > 0)  # Indices of positive ratios

		if not positive_indices:
			log("No more pivot rows available, can't optimize")
			break

		pivot_m = np.argmin(ratio[positive_indices]) + 1
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


a = np.array(
	[
		[1, 2, 2, 4],
		[2, -1, 1, 2],
		[4, -2, 1, -1]
	]
)
b = np.array(
	[40, 8, 10]
)
c = np.array(
	[2, 1, -3, 5]
)

maximize(a, b, c)
