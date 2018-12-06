from systems.telemetry.telemetry import Telemetry

def _telemetry(user):
	return Telemetry.get({"_id" : user.telemetry})