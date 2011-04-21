<%namespace name="components" file="test_components.mako" />
${components.header(title=title_prefix + ' :: ' + title, projects=dirs, current=current)}
<div class="markdown">
 ${body}
</div>
${components.footer()}
