# This script responds to a prompt asking for the assistant's name.

def handle_input(user_input: str) -> str:
	"""Return the assistant's response to the given input.

	If the input asks "what is your name" (case-insensitive), return
	the required name string. Otherwise, return a generic reply.
	"""
	normalized = user_input.strip().lower()
	if "what is your name" in normalized or "what's your name" in normalized:
		return "GitHub Copilot"
	return "I can only answer questions about my name."


if __name__ == '__main__':
	try:
		user = input().strip()
	except EOFError:
		user = ''
	print(handle_input(user))