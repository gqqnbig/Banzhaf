import builtins
from typing import List


def _findWinningCoalitionsCore(quota, weights, consumeIndex: int):
	coalitions = []

	while consumeIndex < len(weights):
		head = [consumeIndex]
		if weights[consumeIndex] >= quota:
			coalitions += [head]

		tail = _findWinningCoalitionsCore(quota - weights[consumeIndex], weights, consumeIndex + 1)
		coalitions += [head + c for c in tail]

		consumeIndex += 1

	return coalitions


def findWinningCoalitions(quota, weights):
	weights = sorted(weights, reverse=True)
	return _findWinningCoalitionsCore(quota, weights, 0)


def findAllVoters(coalitions):
	return set([item for row in coalitions for item in row])


def findVetoPowers(winningCoalitions: List[List]):
	s = findAllVoters(winningCoalitions)

	vetoPowers = []
	hasVetoPower = True
	for voter in s:
		for wc in winningCoalitions:
			if voter not in wc:
				hasVetoPower = False
				break

		if hasVetoPower:
			vetoPowers.append(voter)

	return vetoPowers


def findPowerDistribution(quota, weights, winningCoalitions: List[List]):
	sums = []
	for c in winningCoalitions:
		sum = 0
		[sum := sum + weights[voter] for voter in c]
		sums.append(sum)

	voters = findAllVoters(winningCoalitions)

	voterPowers = []
	for voter in voters:
		count = 0
		for i in range(len(winningCoalitions)):
			# check if voter can change this coalition from winning to losing
			c = winningCoalitions[i]
			if voter in c:
				newVotes = sums[i] - weights[voter]
				if newVotes < quota:
					# this voter has power to make this coalition lose.
					count += 1
		voterPowers.append(count)

	totalPower = builtins.sum(voterPowers)
	powerIndexes = [0] * len(voters)
	for i in range(len(voters)):
		powerIndexes[i] = voterPowers[i] / float(totalPower)
	return powerIndexes


if __name__ == '__main__':
	quota = 10
	weights = sorted([6, 3, 1], reverse=True)

	winningCoalitions = findWinningCoalitions(quota, weights)
	print("Winning coalitions: ", winningCoalitions)

	vetoPowers = findVetoPowers(winningCoalitions)
	if len(vetoPowers) == 0:
		print("No one has veto power.")
	else:
		print("vetoPowers:", vetoPowers)

	powerIndexes = findPowerDistribution(quota, weights, winningCoalitions)
	print("powerIndexes:")
	for i in range(len(powerIndexes)):
		print(f"Voter index {i} has power index {powerIndexes[i]:.3f}.")
