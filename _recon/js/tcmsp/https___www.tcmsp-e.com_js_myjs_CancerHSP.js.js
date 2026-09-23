$(document).ready(function() {
    $(function() {
        $("#menu > ul > li").hover(function() {
            $(this).children('ul').stop(true, true).show(0);
        }, function() {
            $(this).children('ul').stop(true, true).hide(0);
        });
    });
    $(".tarID").css('width', '50px');
});


// alert show once
function cookiesave(n, v, mins, dn, path) {
    if (n) {

        if (!mins) mins = 365 * 24 * 60;
        if (!path) path = "/";
        var date = new Date();

        date.setTime(date.getTime() + (mins * 60 * 1000));

        var expires = "; expires=" + date.toGMTString();

        if (dn) dn = "domain=" + dn + "; ";
        document.cookie = n + "=" + v + expires + "; " + dn + "path=" + path;
    }
}

function cookieget(n) {
    var name = n + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function closeclick() {
    document.getElementById('note').style.display = 'none';
    cookiesave('name', 'guanbi', 10, '', ''); // 1表示cookie存在的时间
}

function clickclose() {
    if (cookieget('name') == 'guanbi') {
        document.getElementById('note').style.display = 'none';
    } else {
        document.getElementById('note').style.display = 'block';
    }
}

//show input hint by select options
$(document).ready(function() {
    var placeholderText = {
        "combination_s": "ex: toremifene:docetaxel",
        "drug_ID": "ex: Drug0001",
        "drug_name": "ex: caspofungin",
        "drugbank_ID": "ex: DB00520",
        "cas": "ex: 180288-69-1",
        "atc": "ex: L01XC03",
        "bioactivity": "ex: cytochrome c",
        "uniprot": "ex: P47712",
        "seffect_name": "ex: inflammation"
    };


        var placeholderTextTcm = {
        "auto": "ex: cytochrome c/chenpi/123-31-9/FBPFZTCFMRRESA",
        "file_ID": "ex: zjx_zsz_Molecule1104.mol2",
        "herb_all_name": "ex: Citrus Reticulata/chenpi/陈皮",
        "molecule_name": "ex: Hydroquinone",
        "cas": "ex: 123-31-9",
        "inchikey": "ex: FBPFZTCFMRRESA-KVTDHHQDSA-N",
        "target_name": "ex: cytochrome c",
        "disease_name": "ex: Cardiac dysrhythmia"
    };

    var placeholderTextCvd = {
        "drug_name": "ex: toremifene",
        "drugbank_ID": "ex: DB00520",
        "atc": "ex: L01XC03",
        "target_name": "ex: cytochrome c",
        "gene_name": "ex: gene name",
        "disease_name": "ex: Cardiac dysrhythmia"
    };
		
		var placeholderTextCancerHSP = {
        "herb_all_name": "ex: Artemisia argyi/Ai Ye/艾叶",
        "mol_name": "ex: Taxol",
        "cas": "ex: 476-69-7",
        "inchikey": "ex: YVPXVXANRNDGTA-VMPREFPWSA-N",
        "target_name": "ex: Vitamin D receptor",
        "bioactivity": "ex: IC50"
    };

    $("#searchItem").on("change", function() {
        var selection = document.getElementById("searchItem");
        var inputBox = document.getElementById("inputVar");

        var selectedVal = selection.options[selection.selectedIndex].value;
        if (placeholderText[selectedVal] !== undefined) {
            inputBox.placeholder = placeholderText[selectedVal];
        }
        cookiesave("soptionPreDC", selectedVal, "", "", "");
    });

    $("#searchItemTcm").on("change", function() {
        var selectionTcm = document.getElementById("searchItemTcm");
        var inputBoxTcm = document.getElementById("inputVarTcm");

        var selectedValTcm = selectionTcm.options[selectionTcm.selectedIndex].value;

        if (placeholderTextTcm[selectedValTcm] !== undefined) {
            inputBoxTcm.placeholder = placeholderTextTcm[selectedValTcm];
        }
        cookiesave("soption", selectedValTcm, "", "", "");
    });

    $("#searchItemCvd").on("change", function() {
        var selectionCvd = document.getElementById("searchItemCvd");
        var inputBoxCvd = document.getElementById("inputVarCvd");

        var selectedValCvd = selectionCvd.options[selectionCvd.selectedIndex].value;

        if (placeholderTextCvd[selectedValCvd] !== undefined) {
            inputBoxCvd.placeholder = placeholderTextCvd[selectedValCvd];
        }
        cookiesave("soption", selectedValCvd, "", "", "");
    });
		
		$("#searchItemCancerHSP").on("change", function() {
        var selectionCancerHSP = document.getElementById("searchItemCancerHSP");
        var inputBoxCancerHSP = document.getElementById("inputVarCancerHSP");

        var selectedValCancerHSP = selectionCancerHSP.options[selectionCancerHSP.selectedIndex].value;

        if (placeholderTextCancerHSP[selectedValCancerHSP] !== undefined) {
            inputBoxCancerHSP.placeholder = placeholderTextCancerHSP[selectedValCancerHSP];
        }
        cookiesave("soption", selectedValCancerHSP, "", "", "");
    });

    if ($("#searchItem").length > 0) {
        var selection = document.getElementById("searchItem");
        var inputBox = document.getElementById("inputVar");
        var selectedVal = selection.options[selection.selectedIndex].value;
        if (placeholderText[selectedVal] !== undefined) {
            inputBox.placeholder = placeholderText[selectedVal];
        }
    }

    if ($("#searchItemTcm").length > 0) {
        var selectionTcm = document.getElementById("searchItemTcm");
        var inputBoxTcm = document.getElementById("inputVarTcm");
        var selectedValTcm = selectionTcm.options[selectionTcm.selectedIndex].value;
        if (placeholderTextTcm[selectedValTcm] !== undefined) {
            inputBoxTcm.placeholder = placeholderTextTcm[selectedValTcm];
        }
    }
		
		if ($("#searchItemCancerHSP").length > 0) {
        var selectionCancerHSP = document.getElementById("searchItemCancerHSP");
        var inputBoxCancerHSP = document.getElementById("inputVarCancerHSP");
        var selectedValCancerHSP = selectionCancerHSP.options[selectionCancerHSP.selectedIndex].value;
        if (placeholderTextCancerHSP[selectedValCancerHSP] !== undefined) {
            inputBoxCancerHSP.placeholder = placeholderTextCancerHSP[selectedValCancerHSP];
        }
    }

    if ($("#searchItemCvd").length > 0) {
        var selectionCvd = document.getElementById("searchItemCvd");
        var inputBoxCvd = document.getElementById("inputVarCvd");
        var selectedValCvd = selectionCvd.options[selectionCvd.selectedIndex].value;
        if (placeholderTextCvd[selectedValCvd] !== undefined) {
            inputBoxCvd.placeholder = placeholderTextCvd[selectedValCvd];
        }
    }
});
//show input hint by select options. over



// featured slide
! function(a) {
    a.extend(a.ui.tabs.prototype, {
        rotation: null,
        rotationDelay: null,
        continuing: null,
        rotate: function(a, b) {
            var e, f, c = this,
                d = this.options;
            return (a > 1 || null === c.rotationDelay) && void 0 !== a && (c.rotationDelay = a), void 0 !== b && (c.continuing = b), e = c._rotate || (c._rotate = function(b) {
                clearTimeout(c.rotation), c.rotation = setTimeout(function() {
                    var a = d.selected;
                    c.select(++a < c.anchors.length ? a : 0)
                }, a), b && b.stopPropagation()
            }), f = c._unrotate || (c._unrotate = b ? function(a) {
                t = d.selected, e()
            } : function(a) {
                a.clientX && c.rotate(null)
            }), a ? (this.element.bind("tabsshow", e), this.anchors.bind(d.event + ".tabs", f), e()) : (clearTimeout(c.rotation), this.element.unbind("tabsshow", e), this.anchors.unbind(d.event + ".tabs", f), delete this._rotate, delete this._unrotate), 1 === a && (a = c.rotationDelay), this
        },
        pause: function() {
            var a = this,
                b = this.options;
            a.rotate(0)
        },
        unpause: function() {
            var a = this,
                b = this.options;
            a.rotate(1, a.continuing)
        }
    })
}(jQuery);

// cytoscapeweb
if (!this.JSON) {
    this.JSON = {}
}(function() {
    function f(n) {
        return n < 10 ? "0" + n : n
    }
    if (typeof Date.prototype.toJSON !== "function") {
        Date.prototype.toJSON = function(key) {
            return isFinite(this.valueOf()) ? this.getUTCFullYear() + "-" + f(this.getUTCMonth() + 1) + "-" + f(this.getUTCDate()) + "T" + f(this.getUTCHours()) + ":" + f(this.getUTCMinutes()) + ":" + f(this.getUTCSeconds()) + "Z" : null
        };
        String.prototype.toJSON = Number.prototype.toJSON = Boolean.prototype.toJSON = function(key) {
            return this.valueOf()
        }
    }
    var cx = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
        escapable = /[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
        gap, indent, meta = {
            "\b": "\\b",
            "\t": "\\t",
            "\n": "\\n",
            "\f": "\\f",
            "\r": "\\r",
            '"': '\\"',
            "\\": "\\\\"
        }, rep;

    function quote(string) {
        escapable.lastIndex = 0;
        return escapable.test(string) ? '"' + string.replace(escapable, function(a) {
            var c = meta[a];
            return typeof c === "string" ? c : "\\u" + ("0000" + a.charCodeAt(0).toString(16)).slice(-4)
        }) + '"' : '"' + string + '"'
    }

    function str(key, holder) {
        var i, k, v, length, mind = gap,
            partial, value = holder[key];
        if (value && typeof value === "object" && typeof value.toJSON === "function") {
            value = value.toJSON(key)
        }
        if (typeof rep === "function") {
            value = rep.call(holder, key, value)
        }
        switch (typeof value) {
            case "string":
                return quote(value);
            case "number":
                return isFinite(value) ? String(value) : "null";
            case "boolean":
            case "null":
                return String(value);
            case "object":
                if (!value) {
                    return "null"
                }
                gap += indent;
                partial = [];
                if (Object.prototype.toString.apply(value) === "[object Array]") {
                    length = value.length;
                    for (i = 0; i < length; i += 1) {
                        partial[i] = str(i, value) || "null"
                    }
                    v = partial.length === 0 ? "[]" : gap ? "[\n" + gap + partial.join(",\n" + gap) + "\n" + mind + "]" : "[" + partial.join(",") + "]";
                    gap = mind;
                    return v
                }
                if (rep && typeof rep === "object") {
                    length = rep.length;
                    for (i = 0; i < length; i += 1) {
                        k = rep[i];
                        if (typeof k === "string") {
                            v = str(k, value);
                            if (v) {
                                partial.push(quote(k) + (gap ? ": " : ":") + v)
                            }
                        }
                    }
                } else {
                    for (k in value) {
                        if (Object.hasOwnProperty.call(value, k)) {
                            v = str(k, value);
                            if (v) {
                                partial.push(quote(k) + (gap ? ": " : ":") + v)
                            }
                        }
                    }
                }
                v = partial.length === 0 ? "{}" : gap ? "{\n" + gap + partial.join(",\n" + gap) + "\n" + mind + "}" : "{" + partial.join(",") + "}";
                gap = mind;
                return v
        }
    }
    if (typeof JSON.stringify !== "function") {
        JSON.stringify = function(value, replacer, space) {
            var i;
            gap = "";
            indent = "";
            if (typeof space === "number") {
                for (i = 0; i < space; i += 1) {
                    indent += " "
                }
            } else {
                if (typeof space === "string") {
                    indent = space
                }
            }
            rep = replacer;
            if (replacer && typeof replacer !== "function" && (typeof replacer !== "object" || typeof replacer.length !== "number")) {
                throw new Error("JSON.stringify")
            }
            return str("", {
                "": value
            })
        }
    }
    if (typeof JSON.parse !== "function") {
        JSON.parse = function(text, reviver) {
            var j;

            function walk(holder, key) {
                var k, v, value = holder[key];
                if (value && typeof value === "object") {
                    for (k in value) {
                        if (Object.hasOwnProperty.call(value, k)) {
                            v = walk(value, k);
                            if (v !== undefined) {
                                value[k] = v
                            } else {
                                delete value[k]
                            }
                        }
                    }
                }
                return reviver.call(holder, key, value)
            }
            cx.lastIndex = 0;
            if (cx.test(text)) {
                text = text.replace(cx, function(a) {
                    return "\\u" + ("0000" + a.charCodeAt(0).toString(16)).slice(-4)
                })
            }
            if (/^[\],:{}\s]*$/.test(text.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:\s*\[)+/g, ""))) {
                j = eval("(" + text + ")");
                return typeof reviver === "function" ? walk({
                    "": j
                }, "") : j
            }
            throw new SyntaxError("JSON.parse")
        }
    }
}());
var isIE = (navigator.appVersion.indexOf("MSIE") != -1) ? true : false;
var isWin = (navigator.appVersion.toLowerCase().indexOf("win") != -1) ? true : false;
var isOpera = (navigator.userAgent.indexOf("Opera") != -1) ? true : false;

function ControlVersion() {
    var a;
    var b;
    var c;
    try {
        b = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7");
        a = b.GetVariable("$version")
    } catch (c) {}
    if (!a) {
        try {
            b = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6");
            a = "WIN 6,0,21,0";
            b.AllowScriptAccess = "always";
            a = b.GetVariable("$version")
        } catch (c) {}
    }
    if (!a) {
        try {
            b = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.3");
            a = b.GetVariable("$version")
        } catch (c) {}
    }
    if (!a) {
        try {
            b = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.3");
            a = "WIN 3,0,18,0"
        } catch (c) {}
    }
    if (!a) {
        try {
            b = new ActiveXObject("ShockwaveFlash.ShockwaveFlash");
            a = "WIN 2,0,0,11"
        } catch (c) {
            a = -1
        }
    }
    return a
}

function GetSwfVer() {
    var g = -1;
    if (navigator.plugins != null && navigator.plugins.length > 0) {
        if (navigator.plugins["Shockwave Flash 2.0"] || navigator.plugins["Shockwave Flash"]) {
            var f = navigator.plugins["Shockwave Flash 2.0"] ? " 2.0" : "";
            var a = navigator.plugins["Shockwave Flash" + f].description;
            var e = a.split(" ");
            var c = e[2].split(".");
            var h = c[0];
            var b = c[1];
            var d = e[3];
            if (d == "") {
                d = e[4]
            }
            if (d[0] == "d") {
                d = d.substring(1)
            } else {
                if (d[0] == "r") {
                    d = d.substring(1);
                    if (d.indexOf("d") > 0) {
                        d = d.substring(0, d.indexOf("d"))
                    }
                } else {
                    if (d[0] == "b") {
                        d = d.substring(1)
                    }
                }
            }
            var g = h + "." + b + "." + d
        }
    } else {
        if (navigator.userAgent.toLowerCase().indexOf("webtv/2.6") != -1) {
            g = 4
        } else {
            if (navigator.userAgent.toLowerCase().indexOf("webtv/2.5") != -1) {
                g = 3
            } else {
                if (navigator.userAgent.toLowerCase().indexOf("webtv") != -1) {
                    g = 2
                } else {
                    if (isIE && isWin && !isOpera) {
                        g = ControlVersion()
                    }
                }
            }
        }
    }
    return g
}

function DetectFlashVer(f, d, c) {
    versionStr = GetSwfVer();
    if (versionStr == -1) {
        return false
    } else {
        if (versionStr != 0) {
            if (isIE && isWin && !isOpera) {
                tempArray = versionStr.split(" ");
                tempString = tempArray[1];
                versionArray = tempString.split(",")
            } else {
                versionArray = versionStr.split(".")
            }
            var e = versionArray[0];
            var a = versionArray[1];
            var b = versionArray[2];
            if (e > parseFloat(f)) {
                return true
            } else {
                if (e == parseFloat(f)) {
                    if (a > parseFloat(d)) {
                        return true
                    } else {
                        if (a == parseFloat(d)) {
                            if (b >= parseFloat(c)) {
                                return true
                            }
                        }
                    }
                }
            }
            return false
        }
    }
}

function AC_AddExtension(b, a) {
    if (b.indexOf("?") != -1) {
        return b.replace(/\?/, a + "?")
    } else {
        return b + a
    }
}

function AC_Generateobj(e, d, a) {
    var c = "";
    if (isIE && isWin && !isOpera) {
        c += "<object ";
        for (var b in e) {
            c += b + '="' + e[b] + '" '
        }
        c += ">";
        for (var b in d) {
            c += '<param name="' + b + '" value="' + d[b] + '" /> '
        }
        c += "</object>"
    } else {
        c += "<embed ";
        for (var b in a) {
            c += b + '="' + a[b] + '" '
        }
        c += "> </embed>"
    }
    document.write(c)
}

function AC_FL_RunContent() {
    var a = AC_GetArgs(arguments, ".swf", "movie", "clsid:d27cdb6e-ae6d-11cf-96b8-444553540000", "application/x-shockwave-flash");
    AC_Generateobj(a.objAttrs, a.params, a.embedAttrs)
}

function AC_GetArgs(b, e, g, d, h) {
    var a = new Object();
    a.embedAttrs = new Object();
    a.params = new Object();
    a.objAttrs = new Object();
    for (var c = 0; c < b.length; c = c + 2) {
        var f = b[c].toLowerCase();
        switch (f) {
            case "classid":
                break;
            case "pluginspage":
                a.embedAttrs[b[c]] = b[c + 1];
                break;
            case "src":
            case "movie":
                b[c + 1] = AC_AddExtension(b[c + 1], e);
                a.embedAttrs.src = b[c + 1];
                a.params[g] = b[c + 1];
                break;
            case "onafterupdate":
            case "onbeforeupdate":
            case "onblur":
            case "oncellchange":
            case "onclick":
            case "ondblClick":
            case "ondrag":
            case "ondragend":
            case "ondragenter":
            case "ondragleave":
            case "ondragover":
            case "ondrop":
            case "onfinish":
            case "onfocus":
            case "onhelp":
            case "onmousedown":
            case "onmouseup":
            case "onmouseover":
            case "onmousemove":
            case "onmouseout":
            case "onkeypress":
            case "onkeydown":
            case "onkeyup":
            case "onload":
            case "onlosecapture":
            case "onpropertychange":
            case "onreadystatechange":
            case "onrowsdelete":
            case "onrowenter":
            case "onrowexit":
            case "onrowsinserted":
            case "onstart":
            case "onscroll":
            case "onbeforeeditfocus":
            case "onactivate":
            case "onbeforedeactivate":
            case "ondeactivate":
            case "type":
            case "codebase":
                a.objAttrs[b[c]] = b[c + 1];
                break;
            case "id":
            case "width":
            case "height":
            case "align":
            case "vspace":
            case "hspace":
            case "class":
            case "title":
            case "accesskey":
            case "name":
            case "tabindex":
                a.embedAttrs[b[c]] = a.objAttrs[b[c]] = b[c + 1];
                break;
            default:
                a.embedAttrs[b[c]] = a.params[b[c]] = b[c + 1]
        }
    }
    a.objAttrs.classid = d;
    if (h) {
        a.embedAttrs.type = h
    }
    return a
};


/**
 * Bootstrap.js by @fat & @mdo
 * plugins: bootstrap-dropdown.js, bootstrap-alert.js, bootstrap-button.js, bootstrap-carousel.js
 * Copyright 2013 Twitter, Inc.
 * http://www.apache.org/licenses/LICENSE-2.0.txt
 */
! function(a) {
    function d() {
        a(".dropdown-backdrop").remove(), a(b).each(function() {
            e(a(this)).removeClass("open")
        })
    }

    function e(b) {
        var c = b.attr("data-target"),
            d;
        c || (c = b.attr("href"), c = c && /#/.test(c) && c.replace(/.*(?=#[^\s]*$)/, "")), d = c && a(c);
        if (!d || !d.length) d = b.parent();
        return d
    }
    var b = "[data-toggle=dropdown]",
        c = function(b) {
            var c = a(b).on("click.dropdown.data-api", this.toggle);
            a("html").on("click.dropdown.data-api", function() {
                c.parent().removeClass("open")
            })
        };
    c.prototype = {
        constructor: c,
        toggle: function(b) {
            var c = a(this),
                f, g;
            if (c.is(".disabled, :disabled")) return;
            return f = e(c), g = f.hasClass("open"), d(), g || ("ontouchstart" in document.documentElement && a('<div class="dropdown-backdrop"/>').insertBefore(a(this)).on("click", d), f.toggleClass("open")), c.focus(), !1
        },
        keydown: function(c) {
            var d, f, g, h, i, j;
            if (!/(38|40|27)/.test(c.keyCode)) return;
            d = a(this), c.preventDefault(), c.stopPropagation();
            if (d.is(".disabled, :disabled")) return;
            h = e(d), i = h.hasClass("open");
            if (!i || i && c.keyCode == 27) return c.which == 27 && h.find(b).focus(), d.click();
            f = a("[role=menu] li:not(.divider):visible a", h);
            if (!f.length) return;
            j = f.index(f.filter(":focus")), c.keyCode == 38 && j > 0 && j--, c.keyCode == 40 && j < f.length - 1 && j++, ~j || (j = 0), f.eq(j).focus()
        }
    };
    var f = a.fn.dropdown;
    a.fn.dropdown = function(b) {
        return this.each(function() {
            var d = a(this),
                e = d.data("dropdown");
            e || d.data("dropdown", e = new c(this)), typeof b == "string" && e[b].call(d)
        })
    }, a.fn.dropdown.Constructor = c, a.fn.dropdown.noConflict = function() {
        return a.fn.dropdown = f, this
    }, a(document).on("click.dropdown.data-api", d).on("click.dropdown.data-api", ".dropdown form", function(a) {
        a.stopPropagation()
    }).on("click.dropdown.data-api", b, c.prototype.toggle).on("keydown.dropdown.data-api", b + ", [role=menu]", c.prototype.keydown)
}(window.jQuery), ! function(a) {
    var b = '[data-dismiss="alert"]',
        c = function(c) {
            a(c).on("click", b, this.close)
        };
    c.prototype.close = function(b) {
        function f() {
            e.trigger("closed").remove()
        }
        var c = a(this),
            d = c.attr("data-target"),
            e;
        d || (d = c.attr("href"), d = d && d.replace(/.*(?=#[^\s]*$)/, "")), e = a(d), b && b.preventDefault(), e.length || (e = c.hasClass("alert") ? c : c.parent()), e.trigger(b = a.Event("close"));
        if (b.isDefaultPrevented()) return;
        e.removeClass("in"), a.support.transition && e.hasClass("fade") ? e.on(a.support.transition.end, f) : f()
    };
    var d = a.fn.alert;
    a.fn.alert = function(b) {
        return this.each(function() {
            var d = a(this),
                e = d.data("alert");
            e || d.data("alert", e = new c(this)), typeof b == "string" && e[b].call(d)
        })
    }, a.fn.alert.Constructor = c, a.fn.alert.noConflict = function() {
        return a.fn.alert = d, this
    }, a(document).on("click.alert.data-api", b, c.prototype.close)
}(window.jQuery), ! function(a) {
    var b = function(b, c) {
        this.$element = a(b), this.options = a.extend({}, a.fn.button.defaults, c)
    };
    b.prototype.setState = function(a) {
        var b = "disabled",
            c = this.$element,
            d = c.data(),
            e = c.is("input") ? "val" : "html";
        a += "Text", d.resetText || c.data("resetText", c[e]()), c[e](d[a] || this.options[a]), setTimeout(function() {
            a == "loadingText" ? c.addClass(b).attr(b, b) : c.removeClass(b).removeAttr(b)
        }, 0)
    }, b.prototype.toggle = function() {
        var a = this.$element.closest('[data-toggle="buttons-radio"]');
        a && a.find(".active").removeClass("active"), this.$element.toggleClass("active")
    };
    var c = a.fn.button;
    a.fn.button = function(c) {
        return this.each(function() {
            var d = a(this),
                e = d.data("button"),
                f = typeof c == "object" && c;
            e || d.data("button", e = new b(this, f)), c == "toggle" ? e.toggle() : c && e.setState(c)
        })
    }, a.fn.button.defaults = {
        loadingText: "loading..."
    }, a.fn.button.Constructor = b, a.fn.button.noConflict = function() {
        return a.fn.button = c, this
    }, a(document).on("click.button.data-api", "[data-toggle^=button]", function(b) {
        var c = a(b.target);
        c.hasClass("btn") || (c = c.closest(".btn")), c.button("toggle")
    })
}(window.jQuery), ! function(a) {
    var b = function(b, c) {
        this.$element = a(b), this.$indicators = this.$element.find(".carousel-indicators"), this.options = c, this.options.pause == "hover" && this.$element.on("mouseenter", a.proxy(this.pause, this)).on("mouseleave", a.proxy(this.cycle, this))
    };
    b.prototype = {
        cycle: function(b) {
            return b || (this.paused = !1), this.interval && clearInterval(this.interval), this.options.interval && !this.paused && (this.interval = setInterval(a.proxy(this.next, this), this.options.interval)), this
        },
        getActiveIndex: function() {
            return this.$active = this.$element.find(".item.active"), this.$items = this.$active.parent().children(), this.$items.index(this.$active)
        },
        to: function(b) {
            var c = this.getActiveIndex(),
                d = this;
            if (b > this.$items.length - 1 || b < 0) return;
            return this.sliding ? this.$element.one("slid", function() {
                d.to(b)
            }) : c == b ? this.pause().cycle() : this.slide(b > c ? "next" : "prev", a(this.$items[b]))
        },
        pause: function(b) {
            return b || (this.paused = !0), this.$element.find(".next, .prev").length && a.support.transition.end && (this.$element.trigger(a.support.transition.end), this.cycle(!0)), clearInterval(this.interval), this.interval = null, this
        },
        next: function() {
            if (this.sliding) return;
            return this.slide("next")
        },
        prev: function() {
            if (this.sliding) return;
            return this.slide("prev")
        },
        slide: function(b, c) {
            var d = this.$element.find(".item.active"),
                e = c || d[b](),
                f = this.interval,
                g = b == "next" ? "left" : "right",
                h = b == "next" ? "first" : "last",
                i = this,
                j;
            this.sliding = !0, f && this.pause(), e = e.length ? e : this.$element.find(".item")[h](), j = a.Event("slide", {
                relatedTarget: e[0],
                direction: g
            });
            if (e.hasClass("active")) return;
            this.$indicators.length && (this.$indicators.find(".active").removeClass("active"), this.$element.one("slid", function() {
                var b = a(i.$indicators.children()[i.getActiveIndex()]);
                b && b.addClass("active")
            }));
            if (a.support.transition && this.$element.hasClass("slide")) {
                this.$element.trigger(j);
                if (j.isDefaultPrevented()) return;
                e.addClass(b), e[0].offsetWidth, d.addClass(g), e.addClass(g), this.$element.one(a.support.transition.end, function() {
                    e.removeClass([b, g].join(" ")).addClass("active"), d.removeClass(["active", g].join(" ")), i.sliding = !1, setTimeout(function() {
                        i.$element.trigger("slid")
                    }, 0)
                })
            } else {
                this.$element.trigger(j);
                if (j.isDefaultPrevented()) return;
                d.removeClass("active"), e.addClass("active"), this.sliding = !1, this.$element.trigger("slid")
            }
            return f && this.cycle(), this
        }
    };
    var c = a.fn.carousel;
    a.fn.carousel = function(c) {
        return this.each(function() {
            var d = a(this),
                e = d.data("carousel"),
                f = a.extend({}, a.fn.carousel.defaults, typeof c == "object" && c),
                g = typeof c == "string" ? c : f.slide;
            e || d.data("carousel", e = new b(this, f)), typeof c == "number" ? e.to(c) : g ? e[g]() : f.interval && e.pause().cycle()
        })
    }, a.fn.carousel.defaults = {
        interval: 5e3,
        pause: "hover"
    }, a.fn.carousel.Constructor = b, a.fn.carousel.noConflict = function() {
        return a.fn.carousel = c, this
    }, a(document).on("click.carousel.data-api", "[data-slide], [data-slide-to]", function(b) {
        var c = a(this),
            d, e = a(c.attr("data-target") || (d = c.attr("href")) && d.replace(/.*(?=#[^\s]+$)/, "")),
            f = a.extend({}, e.data(), c.data()),
            g;
        e.carousel(f), (g = c.attr("data-slide-to")) && e.data("carousel").pause().to(g).cycle(), b.preventDefault()
    })
}(window.jQuery)


/*!
 * bootstrap-select v1.3.5
 * http://silviomoreto.github.io/bootstrap-select/
 *
 * Copyright 2013 bootstrap-select
 * Licensed under the MIT license
 */

! function($) {

    "use strict";

    $.expr[":"].icontains = function(obj, index, meta) {
        return $(obj).text().toUpperCase().indexOf(meta[3].toUpperCase()) >= 0;
    };

    var Selectpicker = function(element, options, e) {
        if (e) {
            e.stopPropagation();
            e.preventDefault();
        }
        this.$element = $(element);
        this.$newElement = null;
        this.$button = null;
        this.$menu = null;

        //Merge defaults, options and data-attributes to make our options
        this.options = $.extend({}, $.fn.selectpicker.defaults, this.$element.data(), typeof options == 'object' && options);

        //If we have no title yet, check the attribute 'title' (this is missed by jq as its not a data-attribute
        if (this.options.title == null) {
            this.options.title = this.$element.attr('title');
        }

        //Expose public methods
        this.val = Selectpicker.prototype.val;
        this.render = Selectpicker.prototype.render;
        this.refresh = Selectpicker.prototype.refresh;
        this.setStyle = Selectpicker.prototype.setStyle;
        this.selectAll = Selectpicker.prototype.selectAll;
        this.deselectAll = Selectpicker.prototype.deselectAll;
        this.init();
    };

    Selectpicker.prototype = {

        constructor: Selectpicker,

        init: function() {
            this.$element.hide();
            this.multiple = this.$element.prop('multiple');
            var id = this.$element.attr('id');
            this.$newElement = this.createView();
            this.$element.after(this.$newElement);
            this.$menu = this.$newElement.find('> .dropdown-menu');
            this.$button = this.$newElement.find('> button');
            this.$searchbox = this.$newElement.find('input');

            if (id !== undefined) {
                var that = this;
                this.$button.attr('data-id', id);
                $('label[for="' + id + '"]').click(function(e) {
                    e.preventDefault();
                    that.$button.focus();
                });
            }

            this.checkDisabled();
            this.clickListener();
            this.liveSearchListener();
            this.render();
            this.liHeight();
            this.setStyle();
            this.setWidth();
            if (this.options.container) {
                this.selectPosition();
            }
            this.$menu.data('this', this);
            this.$newElement.data('this', this);
        },

        createDropdown: function() {
            //If we are multiple, then add the show-tick class by default
            var multiple = this.multiple ? ' show-tick' : '';
            var header = this.options.header ? '<div class="popover-title"><button type="button" class="close" aria-hidden="true">&times;</button>' + this.options.header + '</div>' : '';
            var searchbox = this.options.liveSearch ? '<div class="bootstrap-select-searchbox"><input type="text" class="input-block-level form-control" /></div>' : '';
            var drop =
                "<div class='btn-group bootstrap-select" + multiple + "'>" +
                "<button type='button' class='btn dropdown-toggle selectpicker' data-toggle='dropdown'>" +
                "<div class='filter-option pull-left'></div>&nbsp;" +
                "<div class='caret'></div>" +
                "</button>" +
                "<div class='dropdown-menu open'>" +
                header +
                searchbox +
                "<ul class='dropdown-menu inner selectpicker' role='menu'>" +
                "</ul>" +
                "</div>" +
                "</div>";

            return $(drop);
        },

        createView: function() {
            var $drop = this.createDropdown();
            var $li = this.createLi();
            $drop.find('ul').append($li);
            return $drop;
        },

        reloadLi: function() {
            //Remove all children.
            this.destroyLi();
            //Re build
            var $li = this.createLi();
            this.$menu.find('ul').append($li);
        },

        destroyLi: function() {
            this.$menu.find('li').remove();
        },

        createLi: function() {
            var that = this,
                _liA = [],
                _liHtml = '';

            this.$element.find('option').each(function() {
                var $this = $(this);

                //Get the class and text for the option
                var optionClass = $this.attr("class") || '';
                var inline = $this.attr("style") || '';
                var text = $this.data('content') ? $this.data('content') : $this.html();
                var subtext = $this.data('subtext') !== undefined ? '<small class="muted text-muted">' + $this.data('subtext') + '</small>' : '';
                var icon = $this.data('icon') !== undefined ? '<i class="glyphicon ' + $this.data('icon') + '"></i> ' : '';
                if (icon !== '' && ($this.is(':disabled') || $this.parent().is(':disabled'))) {
                    icon = '<span>' + icon + '</span>';
                }

                if (!$this.data('content')) {
                    //Prepend any icon and append any subtext to the main text.
                    text = icon + '<span class="text">' + text + subtext + '</span>';
                }

                if (that.options.hideDisabled && ($this.is(':disabled') || $this.parent().is(':disabled'))) {
                    _liA.push('<a style="min-height: 0; padding: 0"></a>');
                } else if ($this.parent().is('optgroup') && $this.data('divider') !== true) {
                    if ($this.index() == 0) {
                        //Get the opt group label
                        var label = $this.parent().attr('label');
                        var labelSubtext = $this.parent().data('subtext') !== undefined ? '<small class="muted text-muted">' + $this.parent().data('subtext') + '</small>' : '';
                        var labelIcon = $this.parent().data('icon') ? '<i class="' + $this.parent().data('icon') + '"></i> ' : '';
                        label = labelIcon + '<span class="text">' + label + labelSubtext + '</span>';

                        if ($this[0].index != 0) {
                            _liA.push(
                                '<div class="div-contain"><div class="divider"></div></div>' +
                                '<dt>' + label + '</dt>' +
                                that.createA(text, "opt " + optionClass, inline)
                            );
                        } else {
                            _liA.push(
                                '<dt>' + label + '</dt>' +
                                that.createA(text, "opt " + optionClass, inline));
                        }
                    } else {
                        _liA.push(that.createA(text, "opt " + optionClass, inline));
                    }
                } else if ($this.data('divider') === true) {
                    _liA.push('<div class="div-contain"><div class="divider"></div></div>');
                } else if ($(this).data('hidden') === true) {
                    _liA.push('');
                } else {
                    _liA.push(that.createA(text, optionClass, inline));
                }
            });

            $.each(_liA, function(i, item) {
                _liHtml += "<li rel=" + i + ">" + item + "</li>";
            });

            //If we are not multiple, and we dont have a selected item, and we dont have a title, select the first element so something is set in the button
            if (!this.multiple && this.$element.find('option:selected').length == 0 && !this.options.title) {
                this.$element.find('option').eq(0).prop('selected', true).attr('selected', 'selected');
            }

            return $(_liHtml);
        },

        createA: function(text, classes, inline) {
            return '<a tabindex="0" class="' + classes + '" style="' + inline + '">' +
                text +
                '<i class="glyphicon glyphicon-ok icon-ok check-mark"></i>' +
                '</a>';
        },

        render: function() {
            var that = this;

            //Update the LI to match the SELECT
            this.$element.find('option').each(function(index) {
                that.setDisabled(index, $(this).is(':disabled') || $(this).parent().is(':disabled'));
                that.setSelected(index, $(this).is(':selected'));
            });

            this.tabIndex();

            var selectedItems = this.$element.find('option:selected').map(function() {
                var $this = $(this);
                var icon = $this.data('icon') && that.options.showIcon ? '<i class="glyphicon ' + $this.data('icon') + '"></i> ' : '';
                var subtext;
                if (that.options.showSubtext && $this.attr('data-subtext') && !that.multiple) {
                    subtext = ' <small class="muted text-muted">' + $this.data('subtext') + '</small>';
                } else {
                    subtext = '';
                }
                if ($this.data('content') && that.options.showContent) {
                    return $this.data('content');
                } else if ($this.attr('title') != undefined) {
                    return $this.attr('title');
                } else {
                    return icon + $this.html() + subtext;
                }
            }).toArray();

            //Fixes issue in IE10 occurring when no default option is selected and at least one option is disabled
            //Convert all the values into a comma delimited string
            var title = !this.multiple ? selectedItems[0] : selectedItems.join(", ");

            //If this is multi select, and the selectText type is count, the show 1 of 2 selected etc..
            if (this.multiple && this.options.selectedTextFormat.indexOf('count') > -1) {
                var max = this.options.selectedTextFormat.split(">");
                var notDisabled = this.options.hideDisabled ? ':not([disabled])' : '';
                if ((max.length > 1 && selectedItems.length > max[1]) || (max.length == 1 && selectedItems.length >= 2)) {
                    title = this.options.countSelectedText.replace('{0}', selectedItems.length).replace('{1}', this.$element.find('option:not([data-divider="true"]):not([data-hidden="true"])' + notDisabled).length);
                }
            }

            //If we dont have a title, then use the default, or if nothing is set at all, use the not selected text
            if (!title) {
                title = this.options.title != undefined ? this.options.title : this.options.noneSelectedText;
            }

            this.$newElement.find('.filter-option').html(title);
        },

        setStyle: function(style, status) {
            if (this.$element.attr('class')) {
                this.$newElement.addClass(this.$element.attr('class').replace(/selectpicker|mobile-device/gi, ''));
            }

            var buttonClass = style ? style : this.options.style;

            if (status == 'add') {
                this.$button.addClass(buttonClass);
            } else if (status == 'remove') {
                this.$button.removeClass(buttonClass);
            } else {
                this.$button.removeClass(this.options.style);
                this.$button.addClass(buttonClass);
            }
        },

        liHeight: function() {
            var selectClone = this.$newElement.clone();
            selectClone.appendTo('body');
            var $menuClone = selectClone.addClass('open').find('> .dropdown-menu');
            var liHeight = $menuClone.find('li > a').outerHeight();
            var headerHeight = this.options.header ? $menuClone.find('.popover-title').outerHeight() : 0;
            var searchHeight = this.options.liveSearch ? $menuClone.find('.bootstrap-select-searchbox').outerHeight() : 0;
            selectClone.remove();
            this.$newElement.data('liHeight', liHeight).data('headerHeight', headerHeight).data('searchHeight', searchHeight);
        },

        setSize: function() {
            var that = this,
                menu = this.$menu,
                menuInner = menu.find('.inner'),
                selectHeight = this.$newElement.outerHeight(),
                liHeight = this.$newElement.data('liHeight'),
                headerHeight = this.$newElement.data('headerHeight'),
                searchHeight = this.$newElement.data('searchHeight'),
                divHeight = menu.find('li .divider').outerHeight(true),
                menuPadding = parseInt(menu.css('padding-top')) +
                    parseInt(menu.css('padding-bottom')) +
                    parseInt(menu.css('border-top-width')) +
                    parseInt(menu.css('border-bottom-width')),
                notDisabled = this.options.hideDisabled ? ':not(.disabled)' : '',
                $window = $(window),
                menuExtras = menuPadding + parseInt(menu.css('margin-top')) + parseInt(menu.css('margin-bottom')) + 2,
                menuHeight,
                selectOffsetTop,
                selectOffsetBot,
                posVert = function() {
                    selectOffsetTop = that.$newElement.offset().top - $window.scrollTop();
                    selectOffsetBot = $window.height() - selectOffsetTop - selectHeight;
                };
            posVert();
            if (this.options.header) menu.css('padding-top', 0);

            if (this.options.size == 'auto') {
                var getSize = function() {
                    var minHeight;
                    posVert();
                    menuHeight = selectOffsetBot - menuExtras;
                    that.$newElement.toggleClass('dropup', (selectOffsetTop > selectOffsetBot) && (menuHeight - menuExtras) < menu.height() && that.options.dropupAuto);
                    if (that.$newElement.hasClass('dropup')) {
                        menuHeight = selectOffsetTop - menuExtras;
                    }
                    if ((menu.find('li').length + menu.find('dt').length) > 3) {
                        minHeight = liHeight * 3 + menuExtras - 2;
                    } else {
                        minHeight = 0;
                    }
                    menu.css({
                        'max-height': menuHeight + 'px',
                        'overflow': 'hidden',
                        'min-height': minHeight + 'px'
                    });
                    menuInner.css({
                        'max-height': menuHeight - headerHeight - searchHeight - menuPadding + 'px',
                        'overflow-y': 'auto',
                        'min-height': minHeight - menuPadding + 'px'
                    });
                };
                getSize();
                $(window).resize(getSize);
                $(window).scroll(getSize);
            } else if (this.options.size && this.options.size != 'auto' && menu.find('li' + notDisabled).length > this.options.size) {
                var optIndex = menu.find("li" + notDisabled + " > *").filter(':not(.div-contain)').slice(0, this.options.size).last().parent().index();
                var divLength = menu.find("li").slice(0, optIndex + 1).find('.div-contain').length;
                menuHeight = liHeight * this.options.size + divLength * divHeight + menuPadding;
                this.$newElement.toggleClass('dropup', (selectOffsetTop > selectOffsetBot) && menuHeight < menu.height() && this.options.dropupAuto);
                menu.css({
                    'max-height': menuHeight + headerHeight + searchHeight + 'px',
                    'overflow': 'hidden'
                });
                menuInner.css({
                    'max-height': menuHeight - menuPadding + 'px',
                    'overflow-y': 'auto'
                });
            }
        },

        setWidth: function() {
            if (this.options.width == 'auto') {
                this.$menu.css('min-width', '0');

                // Get correct width if element hidden
                var selectClone = this.$newElement.clone().appendTo('body');
                var ulWidth = selectClone.find('> .dropdown-menu').css('width');
                selectClone.remove();

                this.$newElement.css('width', ulWidth);
            } else if (this.options.width == 'fit') {
                // Remove inline min-width so width can be changed from 'auto'
                this.$menu.css('min-width', '');
                this.$newElement.css('width', '').addClass('fit-width');
            } else if (this.options.width) {
                // Remove inline min-width so width can be changed from 'auto'
                this.$menu.css('min-width', '');
                this.$newElement.css('width', this.options.width);
            } else {
                // Remove inline min-width/width so width can be changed
                this.$menu.css('min-width', '');
                this.$newElement.css('width', '');
            }
            // Remove fit-width class if width is changed programmatically
            if (this.$newElement.hasClass('fit-width') && this.options.width !== 'fit') {
                this.$newElement.removeClass('fit-width');
            }
        },

        selectPosition: function() {
            var that = this,
                drop = "<div />",
                $drop = $(drop),
                pos,
                actualHeight,
                getPlacement = function($element) {
                    $drop.addClass($element.attr('class')).toggleClass('dropup', $element.hasClass('dropup'));
                    pos = $element.offset();
                    actualHeight = $element.hasClass('dropup') ? 0 : $element[0].offsetHeight;
                    $drop.css({
                        'top': pos.top + actualHeight,
                        'left': pos.left,
                        'width': $element[0].offsetWidth,
                        'position': 'absolute'
                    });
                };
            this.$newElement.on('click', function() {
                getPlacement($(this));
                $drop.appendTo(that.options.container);
                $drop.toggleClass('open', !$(this).hasClass('open'));
                $drop.append(that.$menu);
            });
            $(window).resize(function() {
                getPlacement(that.$newElement);
            });
            $(window).on('scroll', function() {
                getPlacement(that.$newElement);
            });
            $('html').on('click', function(e) {
                if ($(e.target).closest(that.$newElement).length < 1) {
                    $drop.removeClass('open');
                }
            });
        },

        mobile: function() {
            this.$element.addClass('mobile-device').appendTo(this.$newElement);
            if (this.options.container) this.$menu.hide();
        },

        refresh: function() {
            this.reloadLi();
            this.render();
            this.setWidth();
            this.setStyle();
            this.checkDisabled();
            this.liHeight();
        },

        update: function() {
            this.reloadLi();
            this.setWidth();
            this.setStyle();
            this.checkDisabled();
            this.liHeight();
        },

        setSelected: function(index, selected) {
            this.$menu.find('li').eq(index).toggleClass('selected', selected);
        },

        setDisabled: function(index, disabled) {
            if (disabled) {
                this.$menu.find('li').eq(index).addClass('disabled').find('a').attr('href', '#').attr('tabindex', -1);
            } else {
                this.$menu.find('li').eq(index).removeClass('disabled').find('a').removeAttr('href').attr('tabindex', 0);
            }
        },

        isDisabled: function() {
            return this.$element.is(':disabled');
        },

        checkDisabled: function() {
            var that = this;

            if (this.isDisabled()) {
                this.$button.addClass('disabled').attr('tabindex', -1);
            } else {
                if (this.$button.hasClass('disabled')) {
                    this.$button.removeClass('disabled');
                }

                if (this.$button.attr('tabindex') == -1) {
                    if (!this.$element.data('tabindex')) this.$button.removeAttr('tabindex');
                }
            }

            this.$button.click(function() {
                return !that.isDisabled();
            });
        },

        tabIndex: function() {
            if (this.$element.is('[tabindex]')) {
                this.$element.data('tabindex', this.$element.attr("tabindex"));
                this.$button.attr('tabindex', this.$element.data('tabindex'));
            }
        },

        clickListener: function() {
            var that = this;

            $('body').on('touchstart.dropdown', '.dropdown-menu', function(e) {
                e.stopPropagation();
            });

            this.$newElement.on('click', function() {
                that.setSize();
            });

            this.$menu.on('click', 'li a', function(e) {
                var clickedIndex = $(this).parent().index(),
                    prevValue = that.$element.val();

                //Dont close on multi choice menu
                if (that.multiple) {
                    e.stopPropagation();
                }

                e.preventDefault();

                //Dont run if we have been disabled
                if (!that.isDisabled() && !$(this).parent().hasClass('disabled')) {
                    var $options = that.$element.find('option');
                    var $option = $options.eq(clickedIndex);

                    //Deselect all others if not multi select box
                    if (!that.multiple) {
                        $options.prop('selected', false);
                        $option.prop('selected', true);
                    }
                    //Else toggle the one we have chosen if we are multi select.
                    else {
                        var state = $option.prop('selected');

                        $option.prop('selected', !state);
                    }

                    that.$button.focus();

                    // Trigger select 'change'
                    if (prevValue != that.$element.val()) {
                        that.$element.change();
                    }
                }
            });

            this.$menu.on('click', 'li.disabled a, li dt, li .div-contain, h3.popover-title', function(e) {
                if (e.target == this) {
                    e.preventDefault();
                    e.stopPropagation();
                    that.$button.focus();
                }
            });

            this.$searchbox.on('click', function(e) {
                e.stopPropagation();
            });

            this.$element.change(function() {
                that.render();
            });
        },

        liveSearchListener: function() {
            var that = this;

            this.$newElement.on('click.dropdown.data-api', function() {
                if (that.options.liveSearch) {
                    setTimeout(function() {
                        that.$searchbox.focus();
                    }, 10);
                }
            });

            this.$searchbox.on('keyup', function(e) {
                if (e.keyCode == 40) {
                    // Down-arrow should go to the first visible item.
                    that.$menu.find('li:not(.divider):visible a').first().focus();
                } else if (e.keyCode == 38) {
                    // Up-arrow should go to the last visible item.
                    that.$menu.find('li:not(.divider):visible a').last().focus();
                } else if (that.$searchbox.val()) {
                    that.$menu.find('li').show().not(':icontains(' + that.$searchbox.val() + ')').hide();
                } else {
                    that.$menu.find('li').show();
                }
            }).on('keydown', function(e) {
                if (e.keyCode == 13) {
                    // Prevent return from submitting any form here (needs to be in keydown instead of keyup).
                    // Closes the dropdown and focuses it.
                    that.$button.click().focus();
                    e.preventDefault();
                    return false;
                }
            });
        },

        val: function(value) {

            if (value != undefined) {
                this.$element.val(value);

                this.$element.change();
                return this.$element;
            } else {
                return this.$element.val();
            }
        },

        selectAll: function() {
            this.$element.find('option').prop('selected', true).attr('selected', 'selected');
            this.render();
        },

        deselectAll: function() {
            this.$element.find('option').prop('selected', false).removeAttr('selected');
            this.render();
        },

        keydown: function(e) {
            var that = $(this).parent().data('this');
            // If the dropdown is closed, open it and move focus to the search box, if there is one.
            if (that.$searchbox && that.$searchbox.is(':not(:visible)') && e.keyCode >= 48 && e.keyCode <= 90) {
                $(':focus').click();
                that.$searchbox.focus();
            }
        },

        keyup: function(e) {
            var $this,
                $items,
                $parent,
                that;

            $this = $(this);

            $parent = $this.parent();

            that = $parent.data('this');

            if (that.options.container) $parent = that.$menu;

            $items = $('[role=menu] li:not(.divider):visible a', $parent);

            if (!$items.length) return;

            if (/(38|40)/.test(e.keyCode) && that.$searchbox) {
                // Since we bind on keyup, the focus will have already changed here. Keep track of the last focused item and the current,
                // and if they match (and are at the top or bottom of the list), move the focus to the searchbox.
                var index = $items.index($(':focus'));
                var last = $this.data('lastIndex');
                $this.data('lastIndex', index);
                if (index == last) {
                    if (index == 0 || index == $items.length - 1) that.$searchbox.focus();
                }
            } else {
                var keyCodeMap = {
                    48: "0",
                    49: "1",
                    50: "2",
                    51: "3",
                    52: "4",
                    53: "5",
                    54: "6",
                    55: "7",
                    56: "8",
                    57: "9",
                    59: ";",
                    65: "a",
                    66: "b",
                    67: "c",
                    68: "d",
                    69: "e",
                    70: "f",
                    71: "g",
                    72: "h",
                    73: "i",
                    74: "j",
                    75: "k",
                    76: "l",
                    77: "m",
                    78: "n",
                    79: "o",
                    80: "p",
                    81: "q",
                    82: "r",
                    83: "s",
                    84: "t",
                    85: "u",
                    86: "v",
                    87: "w",
                    88: "x",
                    89: "y",
                    90: "z",
                    96: "0",
                    97: "1",
                    98: "2",
                    99: "3",
                    100: "4",
                    101: "5",
                    102: "6",
                    103: "7",
                    104: "8",
                    105: "9"
                };

                var keyIndex = [];

                $items.each(function() {
                    if ($(this).parent().is(':not(.disabled)')) {
                        if ($.trim($(this).text().toLowerCase()).substring(0, 1) == keyCodeMap[e.keyCode]) {
                            keyIndex.push($(this).parent().index());
                        }
                    }
                });

                var count = $(document).data('keycount');
                count++;
                $(document).data('keycount', count);

                var prevKey = $.trim($(':focus').text().toLowerCase()).substring(0, 1);

                if (prevKey != keyCodeMap[e.keyCode]) {
                    count = 1;
                    $(document).data('keycount', count);
                } else if (count >= keyIndex.length) {
                    $(document).data('keycount', 0);
                }

                $items.eq(keyIndex[count - 1]).focus();
            }

            // Select focused option if "Enter", "Spacebar", "Tab" are pressed inside the menu.
            if (/(13|32|9)/.test(e.keyCode) && $this.is('[role=menu]')) {
                e.preventDefault();
                $(':focus').click();
                $(document).data('keycount', 0);
            }
        },

        hide: function() {
            this.$newElement.hide();
        },

        show: function() {
            this.$newElement.show();
        },

        destroy: function() {
            this.$newElement.remove();
            this.$element.remove();
        }
    };

    $.fn.selectpicker = function(option, event) {
        //get the args of the outer function..
        var args = arguments;
        var value;
        var chain = this.each(function() {
            if ($(this).is('select')) {
                var $this = $(this),
                    data = $this.data('selectpicker'),
                    options = typeof option == 'object' && option;

                if (!data) {
                    $this.data('selectpicker', (data = new Selectpicker(this, options, event)));
                } else if (options) {
                    for (var i in options) {
                        data.options[i] = options[i];
                    }
                }

                if (typeof option == 'string') {
                    //Copy the value of option, as once we shift the arguments
                    //it also shifts the value of option.
                    var property = option;
                    if (data[property] instanceof Function) {
                        [].shift.apply(args);
                        value = data[property].apply(data, args);
                    } else {
                        value = data.options[property];
                    }
                }
            }
        });

        if (value != undefined) {
            return value;
        } else {
            return chain;
        }
    };

    $.fn.selectpicker.defaults = {
        style: 'btn-default',
        size: 'auto',
        title: null,
        selectedTextFormat: 'values',
        noneSelectedText: 'Nothing selected',
        countSelectedText: '{0} of {1} selected',
        width: false,
        container: false,
        hideDisabled: false,
        showSubtext: false,
        showIcon: true,
        showContent: true,
        dropupAuto: true,
        header: false,
        liveSearch: false
    };

    $(document)
        .data('keycount', 0)
        .on('keydown', '.selectpicker[data-toggle=dropdown], .selectpicker[role=menu]', Selectpicker.prototype.keydown)
        .on('keyup', '.selectpicker[data-toggle=dropdown], .selectpicker[role=menu]', Selectpicker.prototype.keyup);

}(window.jQuery);

// tocify
/* jquery Tocify - v1.9.0 - 2013-10-01
 * http://www.gregfranko.com/jquery.tocify.js/
 * Copyright (c) 2013 Greg Franko; Licensed MIT */

// Immediately-Invoked Function Expression (IIFE) [Ben Alman Blog Post](http://benalman.com/news/2010/11/immediately-invoked-function-expression/) that calls another IIFE that contains all of the plugin logic.  I used this pattern so that anyone viewing this code would not have to scroll to the bottom of the page to view the local parameters that were passed to the main IIFE.
(function(tocify) {

        // ECMAScript 5 Strict Mode: [John Resig Blog Post](http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/)
        "use strict";

        // Calls the second IIFE and locally passes in the global jQuery, window, and document objects
        tocify(window.jQuery, window, document);

    }

    // Locally passes in `jQuery`, the `window` object, the `document` object, and an `undefined` variable.  The `jQuery`, `window` and `document` objects are passed in locally, to improve performance, since javascript first searches for a variable match within the local variables set before searching the global variables set.  All of the global variables are also passed in locally to be minifier friendly. `undefined` can be passed in locally, because it is not a reserved word in JavaScript.
    (function($, window, document, undefined) {

        // ECMAScript 5 Strict Mode: [John Resig Blog Post](http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/)
        "use strict";

        var tocClassName = "tocify",
            tocClass = "." + tocClassName,
            tocFocusClassName = "tocify-focus",
            tocHoverClassName = "tocify-hover",
            hideTocClassName = "tocify-hide",
            hideTocClass = "." + hideTocClassName,
            headerClassName = "tocify-header",
            headerClass = "." + headerClassName,
            subheaderClassName = "tocify-subheader",
            subheaderClass = "." + subheaderClassName,
            itemClassName = "tocify-item",
            itemClass = "." + itemClassName,
            extendPageClassName = "tocify-extend-page",
            extendPageClass = "." + extendPageClassName;

        // Calling the jQueryUI Widget Factory Method
        $.widget("toc.tocify", {

            //Plugin version
            version: "1.9.0",

            // These options will be used as defaults
            options: {

                // **context**: Accepts String: Any jQuery selector
                // The container element that holds all of the elements used to generate the table of contents
                context: "body",

                // **ignoreSelector**: Accepts String: Any jQuery selector
                // A selector to any element that would be matched by selectors that you wish to be ignored
                ignoreSelector: null,

                // **selectors**: Accepts an Array of Strings: Any jQuery selectors
                // The element's used to generate the table of contents.  The order is very important since it will determine the table of content's nesting structure
                selectors: "h1, h2, h3",

                // **showAndHide**: Accepts a boolean: true or false
                // Used to determine if elements should be shown and hidden
                showAndHide: true,

                // **showEffect**: Accepts String: "none", "fadeIn", "show", or "slideDown"
                // Used to display any of the table of contents nested items
                showEffect: "slideDown",

                // **showEffectSpeed**: Accepts Number (milliseconds) or String: "slow", "medium", or "fast"
                // The time duration of the show animation
                showEffectSpeed: "medium",

                // **hideEffect**: Accepts String: "none", "fadeOut", "hide", or "slideUp"
                // Used to hide any of the table of contents nested items
                hideEffect: "slideUp",

                // **hideEffectSpeed**: Accepts Number (milliseconds) or String: "slow", "medium", or "fast"
                // The time duration of the hide animation
                hideEffectSpeed: "medium",

                // **smoothScroll**: Accepts a boolean: true or false
                // Determines if a jQuery animation should be used to scroll to specific table of contents items on the page
                smoothScroll: true,

                // **smoothScrollSpeed**: Accepts Number (milliseconds) or String: "slow", "medium", or "fast"
                // The time duration of the smoothScroll animation
                smoothScrollSpeed: "medium",

                // **scrollTo**: Accepts Number (pixels)
                // The amount of space between the top of page and the selected table of contents item after the page has been scrolled
                scrollTo: 0,

                // **showAndHideOnScroll**: Accepts a boolean: true or false
                // Determines if table of contents nested items should be shown and hidden while scrolling
                showAndHideOnScroll: true,

                // **highlightOnScroll**: Accepts a boolean: true or false
                // Determines if table of contents nested items should be highlighted (set to a different color) while scrolling
                highlightOnScroll: true,

                // **highlightOffset**: Accepts a number
                // The offset distance in pixels to trigger the next active table of contents item
                highlightOffset: 40,

                // **theme**: Accepts a string: "bootstrap", "jqueryui", or "none"
                // Determines if Twitter Bootstrap, jQueryUI, or Tocify classes should be added to the table of contents
                theme: "bootstrap",

                // **extendPage**: Accepts a boolean: true or false
                // If a user scrolls to the bottom of the page and the page is not tall enough to scroll to the last table of contents item, then the page height is increased
                extendPage: true,

                // **extendPageOffset**: Accepts a number: pixels
                // How close to the bottom of the page a user must scroll before the page is extended
                extendPageOffset: 100,

                // **history**: Accepts a boolean: true or false
                // Adds a hash to the page url to maintain history
                history: true,

                // **scrollHistory**: Accepts a boolean: true or false
                // Adds a hash to the page url, to maintain history, when scrolling to a TOC item
                scrollHistory: false,

                // **hashGenerator**: How the hash value (the anchor segment of the URL, following the
                // # character) will be generated.
                //
                // "compact" (default) - #CompressesEverythingTogether
                // "pretty" - #looks-like-a-nice-url-and-is-easily-readable
                // function(text, element){} - Your own hash generation function that accepts the text as an
                // argument, and returns the hash value.
                hashGenerator: "compact",

                // **highlightDefault**: Accepts a boolean: true or false
                // Set's the first TOC item as active if no other TOC item is active.
                highlightDefault: true

            },

            // _Create
            // -------
            //      Constructs the plugin.  Only called once.
            _create: function() {

                var self = this;

                self.extendPageScroll = true;

                // Internal array that keeps track of all TOC items (Helps to recognize if there are duplicate TOC item strings)
                self.items = [];

                // Generates the HTML for the dynamic table of contents
                self._generateToc();

                // Adds CSS classes to the newly generated table of contents HTML
                self._addCSSClasses();

                self.webkit = (function() {

                    for (var prop in window) {

                        if (prop) {

                            if (prop.toLowerCase().indexOf("webkit") !== -1) {

                                return true;

                            }

                        }

                    }

                    return false;

                }());

                // Adds jQuery event handlers to the newly generated table of contents
                self._setEventHandlers();

                // Binding to the Window load event to make sure the correct scrollTop is calculated
                $(window).load(function() {

                    // Sets the active TOC item
                    self._setActiveElement(true);

                    // Once all animations on the page are complete, this callback function will be called
                    $("html, body").promise().done(function() {

                        setTimeout(function() {

                            self.extendPageScroll = false;

                        }, 0);

                    });

                });

            },

            // _generateToc
            // ------------
            //      Generates the HTML for the dynamic table of contents
            _generateToc: function() {

                // _Local variables_

                // Stores the plugin context in the self variable
                var self = this,

                    // All of the HTML tags found within the context provided (i.e. body) that match the top level jQuery selector above
                    firstElem,

                    // Instantiated variable that will store the top level newly created unordered list DOM element
                    ul,
                    ignoreSelector = self.options.ignoreSelector;

                // If the selectors option has a comma within the string
                if (this.options.selectors.indexOf(",") !== -1) {

                    // Grabs the first selector from the string
                    firstElem = $(this.options.context).find(this.options.selectors.replace(/ /g, "").substr(0, this.options.selectors.indexOf(",")));

                }

                // If the selectors option does not have a comman within the string
                else {

                    // Grabs the first selector from the string and makes sure there are no spaces
                    firstElem = $(this.options.context).find(this.options.selectors.replace(/ /g, ""));

                }

                if (!firstElem.length) {

                    self.element.addClass(hideTocClassName);

                    return;

                }

                self.element.addClass(tocClassName);

                // Loops through each top level selector
                firstElem.each(function(index) {

                    //If the element matches the ignoreSelector then we skip it
                    if ($(this).is(ignoreSelector)) {
                        return;
                    }

                    // Creates an unordered list HTML element and adds a dynamic ID and standard class name
                    ul = $("<ul/>", {
                        "id": headerClassName + index,
                        "class": headerClassName
                    }).

                    // Appends a top level list item HTML element to the previously created HTML header
                    append(self._nestElements($(this), index));

                    // Add the created unordered list element to the HTML element calling the plugin
                    self.element.append(ul);

                    // Finds all of the HTML tags between the header and subheader elements
                    $(this).nextUntil(this.nodeName.toLowerCase()).each(function() {

                        // If there are no nested subheader elemements
                        if ($(this).find(self.options.selectors).length === 0) {

                            // Loops through all of the subheader elements
                            $(this).filter(self.options.selectors).each(function() {

                                //If the element matches the ignoreSelector then we skip it
                                if ($(this).is(ignoreSelector)) {
                                    return;
                                }

                                self._appendSubheaders.call(this, self, ul);

                            });

                        }

                        // If there are nested subheader elements
                        else {

                            // Loops through all of the subheader elements
                            $(this).find(self.options.selectors).each(function() {

                                //If the element matches the ignoreSelector then we skip it
                                if ($(this).is(ignoreSelector)) {
                                    return;
                                }

                                self._appendSubheaders.call(this, self, ul);

                            });

                        }

                    });

                });

            },

            _setActiveElement: function(pageload) {

                var self = this,

                    hash = window.location.hash.substring(1),

                    elem = self.element.find('li[data-unique="' + hash + '"]');

                if (hash.length) {

                    // Removes highlighting from all of the list item's
                    self.element.find("." + self.focusClass).removeClass(self.focusClass);

                    // Highlights the current list item that was clicked
                    elem.addClass(self.focusClass);

                    // If the showAndHide option is true
                    if (self.options.showAndHide) {

                        // Triggers the click event on the currently focused TOC item
                        elem.click();

                    }

                } else {

                    // Removes highlighting from all of the list item's
                    self.element.find("." + self.focusClass).removeClass(self.focusClass);

                    if (!hash.length && pageload && self.options.highlightDefault) {

                        // Highlights the first TOC item if no other items are highlighted
                        self.element.find(itemClass).first().addClass(self.focusClass);

                    }

                }

                return self;

            },

            // _nestElements
            // -------------
            //      Helps create the table of contents list by appending nested list items
            _nestElements: function(self, index) {

                var arr, item, hashValue;

                arr = $.grep(this.items, function(item) {

                    return item === self.text();

                });

                // If there is already a duplicate TOC item
                if (arr.length) {

                    // Adds the current TOC item text and index (for slight randomization) to the internal array
                    this.items.push(self.text() + index);

                }

                // If there not a duplicate TOC item
                else {

                    // Adds the current TOC item text to the internal array
                    this.items.push(self.text());

                }

                hashValue = this._generateHashValue(arr, self, index);

                // Appends a list item HTML element to the last unordered list HTML element found within the HTML element calling the plugin
                item = $("<li/>", {

                    // Sets a common class name to the list item
                    "class": itemClassName,

                    "data-unique": hashValue

                }).append($("<a/>", {

                    "text": self.text()

                }));

                // Adds an HTML anchor tag before the currently traversed HTML element
                self.before($("<div/>", {

                    // Sets a name attribute on the anchor tag to the text of the currently traversed HTML element (also making sure that all whitespace is replaced with an underscore)
                    "name": hashValue,

                    "data-unique": hashValue

                }));

                return item;

            },

            // _generateHashValue
            // ------------------
            //      Generates the hash value that will be used to refer to each item.
            _generateHashValue: function(arr, self, index) {

                var hashValue = "",
                    hashGeneratorOption = this.options.hashGenerator;

                if (hashGeneratorOption === "pretty") {

                    // prettify the text
                    hashValue = self.text().toLowerCase().replace(/\s/g, "-");

                    // fix double hyphens
                    while (hashValue.indexOf("--") > -1) {
                        hashValue = hashValue.replace(/--/g, "-");
                    }

                    // fix colon-space instances
                    while (hashValue.indexOf(":-") > -1) {
                        hashValue = hashValue.replace(/:-/g, "-");
                    }

                } else if (typeof hashGeneratorOption === "function") {

                    // call the function
                    hashValue = hashGeneratorOption(self.text(), self);

                } else {

                    // compact - the default
                    hashValue = self.text().replace(/\s/g, "");

                }

                // add the index if we need to
                if (arr.length) {
                    hashValue += "" + index;
                }

                // return the value
                return hashValue;

            },

            // _appendElements
            // ---------------
            //      Helps create the table of contents list by appending subheader elements

            _appendSubheaders: function(self, ul) {

                // The current element index
                var index = $(this).index(self.options.selectors),

                    // Finds the previous header DOM element
                    previousHeader = $(self.options.selectors).eq(index - 1),

                    currentTagName = +$(this).prop("tagName").charAt(1),

                    previousTagName = +previousHeader.prop("tagName").charAt(1),

                    lastSubheader;

                // If the current header DOM element is smaller than the previous header DOM element or the first subheader
                if (currentTagName < previousTagName) {

                    // Selects the last unordered list HTML found within the HTML element calling the plugin
                    self.element.find(subheaderClass + "[data-tag=" + currentTagName + "]").last().append(self._nestElements($(this), index));

                }

                // If the current header DOM element is the same type of header(eg. h4) as the previous header DOM element
                else if (currentTagName === previousTagName) {

                    ul.find(itemClass).last().after(self._nestElements($(this), index));

                } else {

                    // Selects the last unordered list HTML found within the HTML element calling the plugin
                    ul.find(itemClass).last().

                    // Appends an unorderedList HTML element to the dynamic `unorderedList` variable and sets a common class name
                    after($("<ul/>", {

                        "class": subheaderClassName,

                        "data-tag": currentTagName

                    })).next(subheaderClass).

                    // Appends a list item HTML element to the last unordered list HTML element found within the HTML element calling the plugin
                    append(self._nestElements($(this), index));
                }

            },

            // _setEventHandlers
            // ----------------
            //      Adds jQuery event handlers to the newly generated table of contents
            _setEventHandlers: function() {

                // _Local variables_

                // Stores the plugin context in the self variable
                var self = this,

                    // Instantiates a new variable that will be used to hold a specific element's context
                    $self,

                    // Instantiates a new variable that will be used to determine the smoothScroll animation time duration
                    duration;

                // Event delegation that looks for any clicks on list item elements inside of the HTML element calling the plugin
                this.element.on("click.tocify", "li", function(event) {

                    if (self.options.history) {

                        window.location.hash = $(this).attr("data-unique");

                    }

                    // Removes highlighting from all of the list item's
                    self.element.find("." + self.focusClass).removeClass(self.focusClass);

                    // Highlights the current list item that was clicked
                    $(this).addClass(self.focusClass);

                    // If the showAndHide option is true
                    if (self.options.showAndHide) {

                        var elem = $('li[data-unique="' + $(this).attr("data-unique") + '"]');

                        self._triggerShow(elem);

                    }

                    self._scrollTo($(this));

                });

                // Mouseenter and Mouseleave event handlers for the list item's within the HTML element calling the plugin
                this.element.find("li").on({

                    // Mouseenter event handler
                    "mouseenter.tocify": function() {

                        // Adds a hover CSS class to the current list item
                        $(this).addClass(self.hoverClass);

                        // Makes sure the cursor is set to the pointer icon
                        $(this).css("cursor", "pointer");

                    },

                    // Mouseleave event handler
                    "mouseleave.tocify": function() {

                        if (self.options.theme !== "bootstrap") {

                            // Removes the hover CSS class from the current list item
                            $(this).removeClass(self.hoverClass);

                        }

                    }
                });

                // only attach handler if needed (expensive in IE)
                if (self.options.extendPage || self.options.highlightOnScroll || self.options.scrollHistory || self.options.showAndHideOnScroll) {
                    // Window scroll event handler
                    $(window).on("scroll.tocify", function() {

                        // Once all animations on the page are complete, this callback function will be called
                        $("html, body").promise().done(function() {

                            // Local variables

                            // Stores how far the user has scrolled
                            var winScrollTop = $(window).scrollTop(),

                                // Stores the height of the window
                                winHeight = $(window).height(),

                                // Stores the height of the document
                                docHeight = $(document).height(),

                                scrollHeight = $("body")[0].scrollHeight,

                                // Instantiates a variable that will be used to hold a selected HTML element
                                elem,

                                lastElem,

                                lastElemOffset,

                                currentElem;

                            if (self.options.extendPage) {

                                // If the user has scrolled to the bottom of the page and the last toc item is not focused
                                if ((self.webkit && winScrollTop >= scrollHeight - winHeight - self.options.extendPageOffset) || (!self.webkit && winHeight + winScrollTop > docHeight - self.options.extendPageOffset)) {

                                    if (!$(extendPageClass).length) {

                                        lastElem = $('div[data-unique="' + $(itemClass).last().attr("data-unique") + '"]');

                                        if (!lastElem.length) return;

                                        // Gets the top offset of the page header that is linked to the last toc item
                                        lastElemOffset = lastElem.offset().top;

                                        // Appends a div to the bottom of the page and sets the height to the difference of the window scrollTop and the last element's position top offset
                                        $(self.options.context).append($("<div />", {

                                            "class": extendPageClassName,

                                            // "height": Math.abs(lastElemOffset - winScrollTop) + "px",
                                            "height": "0px",

                                            "data-unique": extendPageClassName

                                        }));

                                        if (self.extendPageScroll) {

                                            currentElem = self.element.find('li.active');

                                            self._scrollTo($('div[data-unique="' + currentElem.attr("data-unique") + '"]'));

                                        }

                                    }

                                }

                            }

                            // The zero timeout ensures the following code is run after the scroll events
                            setTimeout(function() {

                                // _Local variables_

                                // Stores the distance to the closest anchor
                                var closestAnchorDistance = null,

                                    // Stores the index of the closest anchor
                                    closestAnchorIdx = null,

                                    // Keeps a reference to all anchors
                                    anchors = $(self.options.context).find("div[data-unique]"),

                                    anchorText;

                                // Determines the index of the closest anchor
                                anchors.each(function(idx) {
                                    var distance = Math.abs(($(this).next().length ? $(this).next() : $(this)).offset().top - winScrollTop - self.options.highlightOffset);
                                    if (closestAnchorDistance == null || distance < closestAnchorDistance) {
                                        closestAnchorDistance = distance;
                                        closestAnchorIdx = idx;
                                    } else {
                                        return false;
                                    }
                                });

                                anchorText = $(anchors[closestAnchorIdx]).attr("data-unique");

                                // Stores the list item HTML element that corresponds to the currently traversed anchor tag
                                elem = $('li[data-unique="' + anchorText + '"]');

                                // If the `highlightOnScroll` option is true and a next element is found
                                if (self.options.highlightOnScroll && elem.length) {

                                    // Removes highlighting from all of the list item's
                                    self.element.find("." + self.focusClass).removeClass(self.focusClass);

                                    // Highlights the corresponding list item
                                    elem.addClass(self.focusClass);

                                }

                                if (self.options.scrollHistory) {

                                    if (window.location.hash !== "#" + anchorText) {

                                        window.location.replace("#" + anchorText);

                                    }
                                }

                                // If the `showAndHideOnScroll` option is true
                                if (self.options.showAndHideOnScroll && self.options.showAndHide) {

                                    self._triggerShow(elem, true);

                                }

                            }, 0);

                        });

                    });
                }

            },

            // Show
            // ----
            //      Opens the current sub-header
            show: function(elem, scroll) {

                // Stores the plugin context in the `self` variable
                var self = this,
                    element = elem;

                // If the sub-header is not already visible
                if (!elem.is(":visible")) {

                    // If the current element does not have any nested subheaders, is not a header, and its parent is not visible
                    if (!elem.find(subheaderClass).length && !elem.parent().is(headerClass) && !elem.parent().is(":visible")) {

                        // Sets the current element to all of the subheaders within the current header
                        elem = elem.parents(subheaderClass).add(elem);

                    }

                    // If the current element does not have any nested subheaders and is not a header
                    else if (!elem.children(subheaderClass).length && !elem.parent().is(headerClass)) {

                        // Sets the current element to the closest subheader
                        elem = elem.closest(subheaderClass);

                    }

                    //Determines what jQuery effect to use
                    switch (self.options.showEffect) {

                        //Uses `no effect`
                        case "none":

                            elem.show();

                            break;

                            //Uses the jQuery `show` special effect
                        case "show":

                            elem.show(self.options.showEffectSpeed);

                            break;

                            //Uses the jQuery `slideDown` special effect
                        case "slideDown":

                            elem.slideDown(self.options.showEffectSpeed);

                            break;

                            //Uses the jQuery `fadeIn` special effect
                        case "fadeIn":

                            elem.fadeIn(self.options.showEffectSpeed);

                            break;

                            //If none of the above options were passed, then a `jQueryUI show effect` is expected
                        default:

                            elem.show();

                            break;

                    }

                }

                // If the current subheader parent element is a header
                if (elem.parent().is(headerClass)) {

                    // Hides all non-active sub-headers
                    self.hide($(subheaderClass).not(elem));

                }

                // If the current subheader parent element is not a header
                else {

                    // Hides all non-active sub-headers
                    self.hide($(subheaderClass).not(elem.closest(headerClass).find(subheaderClass).not(elem.siblings())));

                }

                // Maintains chainablity
                return self;

            },

            // Hide
            // ----
            //      Closes the current sub-header
            hide: function(elem) {

                // Stores the plugin context in the `self` variable
                var self = this;

                //Determines what jQuery effect to use
                switch (self.options.hideEffect) {

                    // Uses `no effect`
                    case "none":

                        elem.hide();

                        break;

                        // Uses the jQuery `hide` special effect
                    case "hide":

                        elem.hide(self.options.hideEffectSpeed);

                        break;

                        // Uses the jQuery `slideUp` special effect
                    case "slideUp":

                        elem.slideUp(self.options.hideEffectSpeed);

                        break;

                        // Uses the jQuery `fadeOut` special effect
                    case "fadeOut":

                        elem.fadeOut(self.options.hideEffectSpeed);

                        break;

                        // If none of the above options were passed, then a `jqueryUI hide effect` is expected
                    default:

                        elem.hide();

                        break;

                }

                // Maintains chainablity
                return self;
            },

            // _triggerShow
            // ------------
            //      Determines what elements get shown on scroll and click
            _triggerShow: function(elem, scroll) {

                var self = this;

                // If the current element's parent is a header element or the next element is a nested subheader element
                if (elem.parent().is(headerClass) || elem.next().is(subheaderClass)) {

                    // Shows the next sub-header element
                    self.show(elem.next(subheaderClass), scroll);

                }

                // If the current element's parent is a subheader element
                else if (elem.parent().is(subheaderClass)) {

                    // Shows the parent sub-header element
                    self.show(elem.parent(), scroll);

                }

                // Maintains chainability
                return self;

            },

            // _addCSSClasses
            // --------------
            //      Adds CSS classes to the newly generated table of contents HTML
            _addCSSClasses: function() {

                // If the user wants a jqueryUI theme
                if (this.options.theme === "jqueryui") {

                    this.focusClass = "ui-state-default";

                    this.hoverClass = "ui-state-hover";

                    //Adds the default styling to the dropdown list
                    this.element.addClass("ui-widget").find(".toc-title").addClass("ui-widget-header").end().find("li").addClass("ui-widget-content");

                }

                // If the user wants a twitterBootstrap theme
                else if (this.options.theme === "bootstrap") {

                    this.element.find(headerClass + "," + subheaderClass).addClass("nav nav-list");

                    this.focusClass = "active";

                }

                // If a user does not want a prebuilt theme
                else {

                    // Adds more neutral classes (instead of jqueryui)

                    this.focusClass = tocFocusClassName;

                    this.hoverClass = tocHoverClassName;

                }

                //Maintains chainability
                return this;

            },

            // setOption
            // ---------
            //      Sets a single Tocify option after the plugin is invoked
            setOption: function() {

                // Calls the jQueryUI Widget Factory setOption method
                $.Widget.prototype._setOption.apply(this, arguments);

            },

            // setOptions
            // ----------
            //      Sets a single or multiple Tocify options after the plugin is invoked
            setOptions: function() {

                // Calls the jQueryUI Widget Factory setOptions method
                $.Widget.prototype._setOptions.apply(this, arguments);

            },

            // _scrollTo
            // ---------
            //      Scrolls to a specific element
            _scrollTo: function(elem) {

                var self = this,
                    duration = self.options.smoothScroll || 0,
                    scrollTo = self.options.scrollTo,
                    currentDiv = $('div[data-unique="' + elem.attr("data-unique") + '"]');

                if (!currentDiv.length) {

                    return self;

                }

                // Once all animations on the page are complete, this callback function will be called
                $("html, body").promise().done(function() {

                    // Animates the html and body element scrolltops
                    $("html, body").animate({

                        // Sets the jQuery `scrollTop` to the top offset of the HTML div tag that matches the current list item's `data-unique` tag
                        "scrollTop": currentDiv.offset().top - ($.isFunction(scrollTo) ? scrollTo.call() : scrollTo) + "px"

                    }, {

                        // Sets the smoothScroll animation time duration to the smoothScrollSpeed option
                        "duration": duration

                    });

                });

                // Maintains chainability
                return self;

            }

        });

    })); //end of plugin

// return to top
$(function() {
    // 给 window 对象绑定 scroll 事件
    $(window).bind("scroll", function() {

        // 获取网页文档对象滚动条的垂直偏移
        var scrollTopNum = $(document).scrollTop(),
            // 获取浏览器当前窗口的高度
            winHeight = $(window).height(),
            returnTop = $("div.returnTop");

        // 滚动条的垂直偏移大于 0 时显示，反之隐藏
        (scrollTopNum > 0) ? returnTop.fadeIn("fast") : returnTop.fadeOut("fast");

        // 给 IE6 定位
        if (!-[1, ] && !window.XMLHttpRequest) {
            returnTop.css("top", scrollTopNum + winHeight - 200);
        }

    });

    // 点击按钮后，滚动条的垂直方向的值逐渐变为0，也就是滑动向上的效果
    $("div.returnTop").click(function() {
        $("html, body").animate({
            scrollTop: 0
        }, 100);
    });

});
