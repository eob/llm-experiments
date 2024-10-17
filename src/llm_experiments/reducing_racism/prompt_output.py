WITH_REASON = """Output:
You must always return JSON output in the form:

{ "reason": str, "action": str }

Where "reason" is the reason you made your choice, and "action" is one of the keys in "available_actions" from the input."""

WITHOUT_REASON = """Output:
You must always return JSON output in the form:

{ "action": str }

Where "action" is one of the keys in "available_actions" from the input."""