<%namespace name="components" file="test_components.mako" />
${components.header(title=title, projects=projects, current=current, next=next, previous=previous, excluded_tests=excluded_tests)}
	${test}
${components.footer()}