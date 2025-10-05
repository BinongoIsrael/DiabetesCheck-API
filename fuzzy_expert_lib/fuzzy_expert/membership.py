def triangular(inputval, params):
	"""Triangular membership function."""
	lowval, midval, highval = params
	if not (lowval <= midval <= highval):
		raise ValueError("Triangular parameters must satisfy lowval <= midval <= highval")
	if inputval <= lowval or highval <= inputval:
		return 0.0
	elif inputval == midval:
		return 1.0
	elif lowval <= inputval <= midval:
		return (inputval-lowval) / (midval-lowval)
	if midval <= inputval <= highval:
		return (highval-inputval) / (highval-midval)
	# Compact mode
	# return max(min((inputval-lowval) / (midval-lowval), (highval-inputval) / (highval-midval)), 0)

def trapezoidal(inputval, params):
	"""Trapezoidal membership function."""
	a, b, c, d = params
	if not (a <= b <= c <= d):
		raise ValueError("Trapezoidal parameters must satisfy a <= b <= c <= d")
	if inputval <= a or inputval >= d:
		return 0.0
	elif b < inputval <= c:
		return 1.0
	elif a < inputval <= b:
		return (inputval-a)/(b-a)
	else:
		return (d-inputval)/(d-c)
	# Compact mode
	# return max(min((inputval - a)/(b-a),1,(d- inputval)/(d-c)),0)
