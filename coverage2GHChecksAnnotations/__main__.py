import sys
import json
from pathlib import Path

import coverage


from . import generateGithubChecksAnnotations

def main():
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

	print(json.dumps(list(generateGithubChecksAnnotations(cov, None, **argsDict)), indent="\t"))

if __name__ == "__main__":
	main()
