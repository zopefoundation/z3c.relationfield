// create the top-level Z3C namespace if needed
if (typeof Z3C == "undefined" || !Z3C) {
    var Z3C = {};
}

// create a new namespace (under Z3C)
Z3C.namespace = function(name) {
    var ns = Z3C;
    var parts = name.split(".");
    if (parts[0] == "Z3C") {
        parts = parts.slice(1);
    }
    for (var i = 0; i < parts.length; i++) {
        var part = parts[i];
        ns[part] = ns[part] || {};
        ns = ns[part];
    }
    return ns;
};

(function() {
    Z3C.namespace('relation');
    
    var winwidth = 750;
    var winheight = 500;
    var window_id = 0;

    var features2string = function(features) {
        var features_l = [];
        for (key in features) {
	    if (!features.hasOwnProperty(key)) {
                continue;
            }
            features_l.push(key + '=' + features[key]);
        };
        return features_l.join(',');
    }
    
    Z3C.relation.RelationCreator = function(el, url) {
        this._el = el;
        this._url = url;
    };
    
    Z3C.relation.RelationCreator.prototype.show = function() {
        var leftpos = (screen.width - winwidth) / 2;
        var toppos = (screen.height - winheight) / 2;
        
        var features = {
            'toolbar': 'yes',
            'status': 'yes',
            'scrollbars': 'yes',
            'resizeable': 'yes',
            'width': winwidth,
            'height': winheight,
            'left': leftpos,
            'top': toppos
        };

        this._win = window.open(this._url, 'relation_window_' + window_id,
                                features2string(features));
        this._win.focus();
        // the popup window has to call call relation_creator.setRelations
        // with a list of strings to set the relations
        this._win.relation_creator = this;
        // increase window id so we open a new window each time
        window_id++;
    };

    Z3C.relation.RelationCreator.prototype.setRelations = function(values) {
        if (values.length > 0) {
            this._el.setAttribute('value', values[0]);
        }
        // break potential circular reference
        delete this._win.relation_creator;
        this._win.close();
    };

    Z3C.relation.popup = function(el, url) {
        var o = new Z3C.relation.RelationCreator(el, url);
        o.show();
    };
})();
