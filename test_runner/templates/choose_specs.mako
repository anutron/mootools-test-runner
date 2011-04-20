<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ko">
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />

<!-- Jasmine -->

<link rel="stylesheet" type="text/css" href="/moorunner/Jasmine/jasmine.css">
<link rel="stylesheet" type="text/css" href="/moorunner/runner.css">
<script src="/static/js/multi-select-checkboxes.js"></script>

<title>Specs for ${title}</title>
</head>
<body>
  <div style="margin: 20px">
    <p>Choose the specs you wish to run:</p>
    <form method="get">
      <ul>
        % for package in specs_packages:
          <li><input name="preset" value="${package}" type="checkbox" checked="checked">${package}</li>
        % endfor
      </ul>
      <input type="submit"/>
      <hr/>
      <button name="preset" value="all">Run all specs</button>
    </form>
  </div>
</body>
</html>

