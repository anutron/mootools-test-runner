// Object.toQueryString from MooTools Core
jasmine.toQueryString = function(object, base){
	var queryString = [];

	for (var i in object) (function(value, key){
		if (base) key = base;
		var result;
		if (jasmine.isArray_(value)){
			var qs = {};
			for (var j = 0; j < value.length; j++)
				qs[j] = value[j];
			result = jasmine.toQueryString(qs, key);
		} else if (typeof value == 'object'){
			result = jasmine.toQueryString(value, key);
		} else if (key !== "") {
			result = key + '=' + encodeURIComponent(value);
		}
	
		if (value != undefined) queryString.push(result);
	})(object[i], i);

	return queryString.join('&');
};
