<%namespace name="components" file="demo_components.mako" />
${components.header(title=title, projects=projects, current=current, next=next, previous=previous, excluded_tests=excluded_tests)}
	${test}
	${components.nav(current=current)}
${components.footer()}