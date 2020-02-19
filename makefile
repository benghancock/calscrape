# This is a Makefile for automating basic tasks in developing the project

# Handle a bug in Ubuntu that inserts a rogue line into "requirements.txt"
freeze:
	pip freeze | grep -v "pkg-resources==0.0.0" > requirements.txt

.PHONY: freeze
