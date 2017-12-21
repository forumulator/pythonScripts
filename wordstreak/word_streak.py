from nltk.corpus import words
import json, re

json_words_file = "words_dictionary.json"
output_file = "outwords.txt"

english_set = set(words.words())
with open(json_words_file, "r") as f2:
	english_set2 = json.load(f2)

# Print all the neighbouring cells of a
# given cell in an m x n matrix
def neighbours(i, j, matrix):
	m, n = len(matrix), len(matrix[0])
	neigh = []
	# Make a list of all 8 neighbours
	for ra in (-1, 0, 1):
		for rc in (-1, 0, 1):
			if ra == 0 and rc == 0:
				continue
			neigh.append((i + ra, j + rc))

	# filter the list
	n2 = []
	for k in neigh:
		if (k[0] >= 0 and k[0] < m) and (k[1] >= 0 and k[1] < n):
			n2.append(k)
	return n2

# Visit is the visited matrix. Exponentially visit all paths.
def expo_words(matrix, i, j, visit, word_str, min_len = 3):
	word_set = set()
	visit[i][j] = 1
	word_str += matrix[i][j]
	if (word_str in english_set) and (word_str in english_set2) \
			and (len(word_str) >= min_len):
		word_set.add(word_str)
	if len(word_str) <= 7:
		for k in neighbours(i, j, matrix):
			if visit[k[0]][k[1]] == 0:
				word_set = word_set.union(
					expo_words(matrix, k[0], k[1], visit, word_str))

	visit[i][j] = 0
	return word_set

# Find all possible words in the given character grid and
# print them, in sorted order of lenght to output_file
def find_words(matrix):
	all_words = set()
	m, n = len(matrix), len(matrix[0])
	visit = [[0 for _ in range(n)] for _ in range(m)]
	for i in range(m):
		for j in range(n):
			all_words = all_words.union(
				expo_words(matrix, i, j, visit, ""))
	word_list = sorted(list(all_words), key = len)
	# Output entire thing to file
	with open(output_file, "w") as outfile:
		for word in word_list:
			print(word, file = outfile)


def check_chars(str):
	char_re = re.compile(r'[^a-zA-z]')
	return not bool(char_re.search(str))

def main():
	print("Enter the character grid, on each line a string of characters in a row:")
	matrix = []
	row = input()
	n = len(row)
	while row != "":
		if len(row) != n or (not check_chars(row)):
			print("Invalid input format: ", end = '')
			if len(row) != n:
				print("All rows should have the same length")
			else:
				print("Only chars allowed in the grid")
			exit(1)
		else:
			matrix.append(list(row))
		row = input()
	print("Given matrix is:")
	for row in matrix:
		print(" ".join(row))
	print("Outputting words to: " + output_file)
	find_words(matrix)

if __name__ == "__main__":
	main()