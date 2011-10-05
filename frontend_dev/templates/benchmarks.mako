<!DOCTYPE html>
<html>
  <head>
    <title>Benchmark.js test page</title>
    <!-- http://jsperf.com/benchmark-js-test-page -->
    <meta charset="utf-8">

% if specs:
    <link rel="stylesheet" href="/moorunner/benchmark_runner/main.css">

    <script src="/moorunner/benchmark_runner/raphael.js"></script>
    <script src="/moorunner/benchmark_runner/g.raphael.js"></script>
    <script src="/moorunner/benchmark_runner/g.raphael-bar.js"></script>
    <script src="/moorunner/benchmark_runner/multi-select-checkboxes.js" type="text/javascript" charset="utf-8"></script>

    <!--[if lt IE 9]><script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
    <script src="/moorunner/Benchmarkjs/benchmark.js"></script>
    <script src="/moorunner/benchmark_runner/ui.js"></script>
    <script src="/moorunner/Benchmarkjs/plugins/ui.browserscope.js"></script>

    <!-- Borrowing Jasmine just for the SpecLoader stuff -->
    <script type="text/javascript" src="/moorunner/Jasmine/jasmine.js"></script>
    <!-- Specs -->
    <script type="text/javascript" src="/moorunner/Helpers/jasmine-html.js"></script>
    <script src="/static/js/query-string.js"></script>
    <script type="text/javascript" charset="utf-8" src="/moorunner/Helpers/Syn.js"></script>
    <script type="text/javascript" charset="utf-8" src="/moorunner/Helpers/simulateEvent.js"></script>
    <script type="text/javascript" charset="utf-8" src="/moorunner/Helpers/JSSpecToJasmine.js"></script>
  </head>
  <body>
  <article>
    <hgroup>
      <h1 id="h1Title">
        Benchmark.js test page
      </h1>
    </hgroup>

    <section id="runner">
      <p id="firebug"><strong>Warning! For accurate results, please disable Firebug before running the tests. <a href="http://jsperf.com/faq#firebug">(Why?)</a></strong></p>

      <p id="status">
        <noscript>
          <strong>
            To run the tests, please
            <a href="http://enable-javascript.com/">enable JavaScript</a>
            and reload the page.
          </strong>
        </noscript>
      </p>

      <div id="controls">
        <button id="run" type="button"></button>
      </div>

      <div id="test-table-wrapper">
        <table id="test-table">
          <caption>Testing in <span id="user-agent"></span></caption>
          <thead>
          <tr>
            <th>Test</th>
            <th>Run <input type="checkbox" checked="true" id="checkAll"></th>
            <th title="Operations per second (higher is better)">Ops/sec</th>
          </tr>
          </thead>
          <tbody id="testlist">
          </tbody>
        </table>
      </div>
    </section>

  </article>

  <h3 style="font-size: 14px">Charted results
  <i style="font-size: 9px; color: #999;">(Run tests first to get charted output.)</i>
  </h3>
  <div id="chart"></div>

  <footer>
    based on examples provided by <a href="http://jsperf.com/">jsPerf.com</a>
    &bull; <a href="http://github.com/mathiasbynens/benchmark.js">fork <code>benchmark.js</code> on github</a>
  </footer>

  <applet code="nano" archive="Benchmarkjs/nano.jar"></applet>

  <script type="text/javascript" charset="utf-8">

  // document.title = 'Benchmarks for ' + Configuration.name;
  // document.getElementById('h1Title').innerHTML = 'Benchmarks for ' + Configuration.name;

  ui.addListener(document.getElementById('checkAll'), 'click', function(){
    var checkAll = this.checked;
    Benchmark.each(document.getElementsByTagName('input'), function(input){
      input.checked = checkAll;
    });
  });

  var chartIt = function(names, vals) {
    var w = 400;
    var h = vals.length * 30;
    var r = Raphael("chart", w + 100, h + 40),
        fin = function () {
            this.flag = r.g.popup(this.bar.x, this.bar.y, (this.bar.value || "0") + ' ms').insertBefore(this);
        },
        fout = function () {
            this.flag.animate({opacity: 0}, 300, function () {this.remove();});
        };
    r.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";

    r.g.text(160, 10, "Benchmarks (in ms - longer is slower)");

    var colors = ['#1f77b4',
    '#aec7e8',
    '#ff7f0e',
    '#ffbb78',
    '#2ca02c',
    '#98df8a',
    '#d62728',
    '#ff9896',
    '#9467bd',
    '#c5b0d5',
    '#8c564b',
    '#c49c94',
    '#e377c2',
    '#f7b6d2',
    '#7f4f7f',
    '#c7c7c7',
    '#bcbd22',
    '#dbdb8d',
    '#17becf',
    '#9edae5'];

    for (var i = 0; i < vals.length; i++) {
      if (!colors[i]) colors[i] = colors[i%20];
    }
    r.g.hbarchart(10, 20, w, h, vals, {
      type: 'square',
      colors: colors
    }).hover(fin, fout).label(names);
  };

  ui.on('complete', function(benchmarks){
    var values = [];
    for (var i = 0; i < ui.benchmarks.length; i++) {
      var ms = (ui.benchmarks[i].stats.mean * 1000);
      var precision = Math.pow(10, 2);
      ms = Math.round(ms * precision) / precision;
      if (ui.benchmarks[i].count > 0) {
        values.push({
          name: ui.benchmarks[i].name,
          ms: ms
        });
      }
    };
    sorted = values.sort(function(a, b){
      return a.ms < b.ms;
    });
    var names = [], vals = [];
    for (var v = 0; v < sorted.length; v++){
      names.push(sorted[v].name);
      vals.push(sorted[v].ms);
    }
    chartIt(names, vals);
  });
  </script>
  <script type="text/javascript" src="/depender/build?requireLibs=${specs}&version=${version}"></script>
% else:
  <link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
  <link rel="stylesheet" type="text/css" href="/static/css/specs.css"/>
  <script src="/static/js/multi-select-checkboxes.js"></script>
  <script src="/static/js/mootools-core-1.3.2.js" type="text/javascript" charset="utf-8"></script>
  <script>
    window.addEvent('domready', function(){
      $('clear').addEvent('click', function(e){
        e.stop();
        $$('input[type=checkbox]').set('checked', '');
      });
      $('all').addEvent('click', function(e){
        e.stop();
        $$('input[type=checkbox]').set('checked', 'true');
      });
    });
  </script>
</head>
<body>
  <div class="mt-specs">
    <p>Choose the benchmarks you wish to run:</p>
    <form method="get">
      <ul>
        % for package in specs_packages:
          <li><input name="preset" value="${package}" type="checkbox" checked="checked">${package}</li>
        % endfor
      </ul>
      <input type="submit" value="Run selected"/>
      <hr/>
      <div class="mt-specs-actions">
        <button id="clear">Clear selection</button>
        <button id="all">Select all</button>
        <p style="font-size:smaller; padding-left: 8px">Hold shift and click to select ranges.</p>
      </div>
    </form>
  </div>
% endif
</head>
<body>

</body>
</html>