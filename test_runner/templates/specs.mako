<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ko">
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />

<!-- Jasmine -->

<link rel="stylesheet" type="text/css" href="/moorunner/Jasmine/jasmine.css">
<link rel="stylesheet" type="text/css" href="/moorunner/runner.css">

<script type="text/javascript" src="/moorunner/Jasmine/jasmine.js"></script>

<!-- Specs -->
<script type="text/javascript" src="/moorunner/Helpers/jasmine-html.js"></script>
<script type="text/javascript" charset="utf-8" src="/moorunner/Helpers/Syn.js"></script>
<script type="text/javascript" charset="utf-8" src="/moorunner/Helpers/simulateEvent.js"></script>
<script type="text/javascript" charset="utf-8" src="/moorunner/Helpers/JSSpecToJasmine.js"></script>

<script type="text/javascript" charset="utf-8">

(function(){

// Load all the specs

window.onload = function(){
	// Run the specs
	jasmine.getEnv().addReporter(new jasmine.TrivialReporter());
	jasmine.getEnv().execute();
};

})();
</script>
<script type="text/javascript" src="/depender/build?requireLibs=${specs_packages}"></script>
<title>Specs for ${title}</title>
</head>
<body>
</body>
</html>
