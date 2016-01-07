import numpy as np
import pandas as pd
import seaborn as sns
import analysis


def main():
	larkinTOI = analysis.getValues('D. Larkin', 'TOI')


	sns.set(color_codes=True)
	np.random.seed(sum(map(ord, "regression")))

	x = pd.DataFrame.from_dict(larkinTOI)
	print(x)

	




if __name__ == '__main__':
	main()