import builtins
from typing import List

import Banzhaf


def _findWinningCoalitionsCore(juniorIndex: int, quota: int, weights, consumeIndex: int):
	coalitions = []

	while consumeIndex < len(weights):
		head = [consumeIndex]

		if consumeIndex == juniorIndex:
			if weights[consumeIndex] > quota:
				coalitions += [head]
			tail = _findWinningCoalitionsCore(juniorIndex, quota - weights[consumeIndex] + 1, weights, consumeIndex + 1)
		else:
			if weights[consumeIndex] >= quota:
				coalitions += [head]
			tail = _findWinningCoalitionsCore(juniorIndex, quota - weights[consumeIndex], weights, consumeIndex + 1)

		coalitions += [head + c for c in tail]

		consumeIndex += 1

	return coalitions


def findWinningCoalitions(juniorIndex: int, quota, weights):
	weights = sorted(weights, reverse=True)
	return _findWinningCoalitionsCore(juniorIndex, quota, weights, 0)


if __name__ == '__main__':
	juniorIndex = 0
	quota = 2
	weights = sorted([1, 1, 1, 1], reverse=True)

	print(f'Voter index {juniorIndex} is junior.')

	winningCoalitions = findWinningCoalitions(juniorIndex, quota, weights)
	print("Winning coalitions: ", winningCoalitions)

	vetoPowers = Banzhaf.findVetoPowers(winningCoalitions)
	if len(vetoPowers) == 0:
		print("No one has veto power.")
	else:
		print("vetoPowers:", vetoPowers)

	powerIndexes = Banzhaf.findPowerDistribution(quota, weights, winningCoalitions)
	print("powerIndexes:")
	for i in range(len(powerIndexes)):
		print(f"Voter index {i} has power index {powerIndexes[i]:.3f}.")
