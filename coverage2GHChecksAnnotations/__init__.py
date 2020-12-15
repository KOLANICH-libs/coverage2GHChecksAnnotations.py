import typing
import base64
from io import StringIO
from pathlib import Path

import coverage
from piechart import piechart


def computeCoverage(executedLinesCount: int, missingLinesCount: int) -> typing.Tuple[float, float]:
	totalCountedLines = missingLinesCount + executedLinesCount
	if totalCountedLines:
		lineCoverage = executedLinesCount / totalCountedLines
	else:
		lineCoverage = 1

	# totalCountedBranches = t["num_branches"]
	# if totalCountedBranches:
	# 	branchCoverage = t["covered_branches"] / totalCountedBranches
	# else:
	# 	branchCoverage = 1
	branchCoverage = 0

	return (lineCoverage, branchCoverage)


def mergeAdjacentLines(linesList: typing.Set[int]) -> typing.Union[typing.List[slice], typing.Tuple[()]]:
	if not linesList:
		return ()

	linesList = iter(linesList)
	firstLine = next(linesList)
	expectedLine = firstLine + 1
	ranges = []

	for l in linesList:
		if l != expectedLine:
			ranges.append(slice(firstLine, expectedLine, 1))
			firstLine = l

		expectedLine = l + 1

	ranges.append(slice(firstLine, expectedLine, 1))
	return ranges


def slen(slcs: typing.Iterable[slice]) -> int:
	"""Returns length of a range/slice (seq). Taken from rangeslicetools and slightly modified"""
	if isinstance(slcs, (range, slice)):
		return slcs.stop - slcs.start
	total = 0
	for s in slcs:
		total += slen(s)
	return total


def genBase64PieChart(percentage: float, fgColor: str) -> str:
	return "data:image/svg+xml;base64," + base64.b64encode(piechart((percentage,), colors=(fgColor,)).encode("ascii")).decode("ascii")


def genPercentageImageObject(share: float, fgColor: str, metricName: str) -> typing.Dict[str, str]:
	return {"alt": "{:.1f}".format(share * 100) + "%", "image_url": genBase64PieChart(share, fgColor), "caption": metricName}


def generateGithubChecksAnnotations(cov: coverage.Coverage, commitSHA1:str, packageName: str = "<package name>", rootDir: Path = None, startedTime:str=None, completedTime:str=None) -> typing.Iterable[dict]:
	overallExecuted = 0
	overallMissing = 0
	overallExcluded = 0
	
	if rootDir is None:
		rootDir = Path(".").resolve().absolute()

	annotations = []
	for reporter, analysis in coverage.report.get_analysis_to_report(cov, None):
		an = analysis
		fn = str(Path(reporter.filename).relative_to(rootDir))

		executedCount = len(an.executed)
		overallExecuted += executedCount

		missing = sorted(an.missing)
		missingCount = len(missing)
		overallMissing += missingCount
		missing = mergeAdjacentLines(missing)

		excluded = sorted(an.excluded)
		excludedCount = len(excluded)
		overallExcluded += excludedCount
		excluded = mergeAdjacentLines(excluded)

		lineCoverage, branchCoverage = computeCoverage(executedCount, missingCount)
		for lr in missing:
			annotations.append(
				{
					"path": fn,
					"start_line": lr.start,
					"end_line": lr.stop - 1,
					"annotation_level": "warning",  # notice, warning, or failure"
					"message": "NC",
				}
			)

		for l in excluded:
			annotations.append(
				{
					"path": fn,
					"start_line": lr.start,
					"end_line": lr.stop - 1,
					"annotation_level": "notice",  # notice, warning, or failure"
					"message": "excluded",
				}
			)

	overallLineCoverage, overallBranchCoverage = computeCoverage(overallExecuted, overallMissing)

	markdownOfTheSummary = "Total: line:" + str(overallLineCoverage) + ", branch:" + "currently missing" #str(overallBranchCoverage)

	annotationsLimitPerCall = 50
	if len(annotations) > annotationsLimitPerCall:
		curAnnotations = annotations[:annotationsLimitPerCall]
		annotations = annotations[annotationsLimitPerCall:]
	else:
		curAnnotations = annotations
		annotations = None

	title = "Coverage of " + packageName
	first = {
		"name": "coveragepy",
		"head_sha": commitSHA1, # GITHUB_SHA env var
		"status": "completed",
		"conclusion": "neutral",  # success, failure, neutral, cancelled, skipped, timed_out, or action_required
		"output": {
			"title": title,
			"summary": markdownOfTheSummary,
			"text": "",
			"images": [
				genPercentageImageObject(overallLineCoverage, "red", "Line coverage"),
				#genPercentageImageObject(overallBranchCoverage, "green", "Branch coverage"),
			],
			"annotations": curAnnotations,
		},
	}

	# "YYYY-MM-DDTHH:MM:SSZ"
	if startedTime is not None:
		first["started_at"] = startedTime

	if completedTime is not None:
		first["completed_at"] = startedTime

	yield first

	while annotations:
		if len(annotations) > annotationsLimitPerCall:
			curAnnotations = annotations[:annotationsLimitPerCall]
			annotations = annotations[annotationsLimitPerCall:]
		else:
			curAnnotations = annotations
			annotations = None

		yield {"output":{"title": title, "summary":markdownOfTheSummary, "annotations": curAnnotations}}
