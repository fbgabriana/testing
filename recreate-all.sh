#!/bin/sh
for repo in brgykodego cyberhomies fbgabriana.github.io gg-tournament harmonicmeans kudlit localserver philippine-astronomy portfolio private randomprojects react-gh-pages testing typhoontracks; do
	echo
	echo "Creating/Updating ${repo}..."
	if [ -d "${repo}" ]; then
		cd "${repo}"
		git all
		cd ..
	else
		git clone https://github.com/fbgabriana/${repo}.git
	fi
done

