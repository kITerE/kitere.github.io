// popup menu implamentation

var timeout	= 100;
var closetimer	= 0;
var ddmenuitem	= 0;

// open hidden layer
function mopen(id)
{	
	// cancel close timer
	mcancelclosetime();

	// close old layer
	if(ddmenuitem) ddmenuitem.style.visibility = 'hidden';

	// get new layer and show it
	ddmenuitem = document.getElementById(id);
	ddmenuitem.style.visibility = 'visible';

}
// close showed layer
function mclose()
{
	if(ddmenuitem) ddmenuitem.style.visibility = 'hidden';
}

// go close timer
function mclosetime()
{
	closetimer = window.setTimeout(mclose, timeout);
}

// cancel close timer
function mcancelclosetime()
{
	if(closetimer)
	{
		window.clearTimeout(closetimer);
		closetimer = null;
	}
}

// close layer when click-out
document.onclick = mclose; 


function nav_tools(prefix)
{
  document.write("<div id=\"m_tools\" onmouseover=\"mcancelclosetime()\" onmouseout=\"mclosetime()\">");
  document.write("<a href=\""+prefix+"tools/DefSound.html\" title=\"Установки аудио устройства по умолчанию\">DefSound</a>");
  document.write("<a href=\""+prefix+"tools/DSymLoad.html\" title=\"Загрузка отладочных символов в HIEW\">DSymLoad</a>");
  document.write("<a href=\""+prefix+"tools/UnDecSym.html\" title=\"Модуль UnDecSym (UnDecorate Symbol Name) для Python\">UnDecSym</a>");
  document.write("<a href=\""+prefix+"tools/diabind.html\" title=\"Модуль diabind: DIA (Debug Interface Access) SDK для Python\">diabind</a>");
  document.write("</div>");
}

