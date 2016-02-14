/*
  With additiopnal work and partial conversion to the jQuery framework by
  Gavin Burnell
  
  Expandable Listmenu Script
  Author : Thomas Bakketun
  http://www.bakketun.net/listmenu/

  Based on script by:
  Author : Daniel Nolan
  http://www.bleedingego.co.uk/webdev.php
  
  $Id: listmenu.js,v 1.7 2009/04/13 22:24:48 cvs Exp $
*/


function initMenus(classname) {

  $("ul."+classname).each(function(i){
  	  initMenu(this,$(this).hasClass("singleopen"),$(this).hasClass("keepopen" ));
	});
}

function getChildNodes( element, tag ) {
	return $(element).children(tag).get();
}

function createA(menu) {
  var a, text;
  text = menu.firstChild;
  a = document.createElement("a");
  a.href = "#";
  menu.replaceChild(a, text);
  a.appendChild(text);
  return a;
}

function initMenu(menu, singleopen, keepopen) {
  var open;
  open = false;
  $(menu).children("li").each(function(i) {
    var a = $(this).children("a").get(0);
    var submenu = $(this).children("ul").get(0);
	var subtable= $(this).children("table").get(0);
    if (submenu || subtable) {
      if (!a) {
        a = createA(this);
      }
	  if (submenu) {
		      open = initMenu(submenu, singleopen, keepopen) || open;
	  }
	  if (subtable) {
		  a.className = "treeclosed";
		  subtable.style.display = "none";

	  }
      $(a).click(function() { return menuonclick(this, singleopen); });
    } else {
      if (a) open = open || (keepopen && a.href == window.location);
    }
    if ($(this).hasClass("treenodeopen") ) setMenu(this, true);
    open = open || $(this).hasClass("treenodeopen");
  });
  setMenu(menu.parentNode, open);
  return open;
}

function menuonclick(a, singleopen) {
  setMenu(a.parentNode, $(a).hasClass("treeclosed"));
  if (singleopen) {
	$(a.parentNode.parentNode).children("li").each(function(i) {
      if (this != a.parentNode) {
        setMenu(this, false);
      }
    });
  }
  matchHeights();
  return false;
}

function setMenu(menu, open) {
  var a = $(menu).children("a").get(0);
  var ul = $(menu).children("ul,table").get(0);
  if (a && ul) {
    if (open) {
		$(a).removeClass("treeclosed").addClass("treeopen");
		ul.style.display = "block";
    } else {
		$(a).removeClass("treeopen").addClass("treeclosed");
      ul.style.display = "none";
    }
  }

}

initMenus("treemenu");