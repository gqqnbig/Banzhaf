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


def findPowerDistribution(winningCoalitions: List[List]):
	voters = findAllVoters(winningCoalitions)

	groupedCoalitions = dict()
	for l in range(1, len(voters) + 1):
		group = {tuple(wc) for wc in winningCoalitions if len(wc) == l}
		groupedCoalitions[l] = group

	voterPowers = [0] * len(voters)

	for l in range(1, len(voters) + 1):
		group = groupedCoalitions[l]
		for coalition in group:
			for i in range(len(coalition)):
				memberToLeave = coalition[i]

				newCoalition = list(coalition)
				del newCoalition[i]
				newCoalition = tuple(newCoalition)

				# Check whether new coalition is still winning
				newLength = l - 1
				if newLength in groupedCoalitions and newCoalition in groupedCoalitions[newLength]:
					# yes, it's still winning
					pass
				else:
					voterPowers[memberToLeave] += 1

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

	powerIndexes = findPowerDistribution(winningCoalitions)
	print("powerIndexes:")
	for i in range(len(powerIndexes)):
		print(f"Voter index {i} has power index {powerIndexes[i]:.3f}.")
