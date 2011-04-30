      var makeActions = function(tests){
        try {
          if (!$('actions')) new Element('dt', {'id': 'actions'}).inject($('mt-content'), 'top');
          tests.each(function(test, i) {
            new Element('dt').adopt(
              new Element('a', {
                text: test.title,
                events: {
                  click: test.fn
                },
                id: 'test-' + i
              })
            ).inject('actions');
            if (test.description) new Element('dd', { text: test.description }).inject('actions');
          });
        } catch(e) {
          alert('Could not create actions. Check console for details.');
          console.log('Ensure you have Core/Element.Event - plus its dependencies.', e);
        }
      };
      var log = function(msg) {
        var type = function(obj){
          if (obj == undefined) return false;
          if (obj.nodeName){
            switch (obj.nodeType){
              case 1: return 'element';
              case 3: return (/\S/).test(obj.nodeValue) ? 'textnode' : 'whitespace';
            }
          } else if (typeof obj.length == 'number'){
            if (obj.callee) return 'arguments';
          }
          return typeof obj;
        };
        var parse = function(){
          var str = '';
          for (var i = 0; i < arguments.length; i++) {
            var value = arguments[i];
            switch (type(value)) {
              case 'element':
                str += value.tagName.toLowerCase();
                if (value.id) str += '#' + value.id;
                if (value.className) str += value.className.split(' ').join('.');
                break;

              case 'array':
                str +='[';
                var results = [];
                for (var index = 0; index < value.length; index++) {
                  results.push(parse(value[index]));
                }
                str += results.join(', ') + ']';
                break;

              case 'object':
                var objs = [];
                for (name in value) {
                  if (type(value[name]) != 'object') {
                    objs.push(name + ': ' + parse(value[name]));
                  } else {
                    objs.push(name + ': (object)');
                  }
                }
                str += '{' + objs.join(', ') + '}';
                break;

              case 'function':
                str += '(function)';
                break;

              case 'boolean':
                str += String(value);
                break;

              default: str += value;
            }
            if (i != (arguments.length - 1)) str += ' ';
          }
          return str;
        };
        document.getElementById('mt-log').innerHTML += parse.apply(this, arguments) + '<br/>';
      };