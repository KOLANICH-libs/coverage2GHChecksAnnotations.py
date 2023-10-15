#!/usr/bin/env python3
import sys
from pathlib import Path

import coverage
from . import generateGithubChecksAnnotations
from miniGHAPI.GHActionsEnv import getGHEnv, getRepo
from miniGHAPI.GitHubAPI import GHAPI


def main():
	env = getGHEnv()
	owner, repo = getRepo(env)

	if len(sys.argv) > 1:
		cov = coverage.Coverage(sys.argv[1])
	else:
		cov = coverage.Coverage()
	cov.load()

	argsDict = {}

	if len(sys.argv) > 2:
		argsDict["packageName"] = sys.argv[2]

	if len(sys.argv) > 3:
		argsDict["rootDir"] = Path(sys.argv[3]).resolve().absolute()

	checks = generateGithubChecksAnnotations(cov, env["GITHUB"]["SHA"], **argsDict)
	api = GHAPI(env["INPUT"]["GITHUB_TOKEN"], "coverage2GHChecksAnnotations", env=env)

	cur = next(checks)

	repo = api.repo(owner, repo)
	runInfo = repo.sendChecksRun(cur)
	print("Created the workflow:", runInfo["id"])

	for i, cur in enumerate(checks):
		repo.patchChecksRun(runInfo["id"], cur)
		print("Appended to the workflow", i)


if __name__ == "__main__":
	main()
