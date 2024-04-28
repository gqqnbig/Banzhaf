import builtins
from typing import List

import itertools

import fractions

import Banzhaf


def findWinningCoalitionsConditions(weights):
	greaterThans = set()
	for length in range(1, len(weights) + 1):
		for coalition in itertools.combinations(weights, length):
			quota = sum(coalition)
			greaterThans.add(quota)
			print("Possible coalition {0} if q >= {1}w_2".format(coalition, quota))
	return greaterThans


def analyze(quota, weights):
	winningCoalitions = Banzhaf.findWinningCoalitions(quota, weights)
	print("Winning coalitions: ", winningCoalitions)

	# vetoPowers = Banzhaf.findVetoPowers(winningCoalitions)
	# if len(vetoPowers) == 0:
	# 	print("No one has veto power.")
	# else:
	# 	print("vetoPowers:", vetoPowers)

	powerIndexes = Banzhaf.findPowerDistribution(winningCoalitions)
	print("powerIndexes:")
	for i in range(len(powerIndexes)):
		print(f"Voter index {i} has power index {powerIndexes[i]} = {float(powerIndexes[i]):.3f}.")


if __name__ == '__main__':
	# Assume w2 is 1.
	# then w1 is 2.

	weights = sorted([2, 1, 1, 1], reverse=True)

	stops = findWinningCoalitionsConditions(weights)
	sortedStops = sorted([fractions.Fraction(1 / s).limit_denominator(100) for s in stops])
	print("Stops are {0}".format(sortedStops))

	if len(sortedStops) == 0:
		exit(1)

	print(f"\ncase w_2 < {sortedStops[0]}q:")
	print('No winning coalitions. No one has power.')

	for s in range(len(sortedStops) - 1):
		print(f"\ncase {sortedStops[s]}q <= w_2 < {sortedStops[s + 1]}q:")
		quota = 1 / sortedStops[s]
		analyze(quota, weights)

	print(f"\ncase {sortedStops[-1]}q <= w_2 :")
	quota = 1 / sortedStops[-1]
	analyze(quota, weights)
