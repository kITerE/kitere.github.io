

function nav_open_mtools()
{
  mopen("m_tools");
}

function nav_write(prefix)
{
  document.write("<div id=\"navigation\">");
  document.write("<ul id=\"menu\">");
  document.write("<li><a href=\""+prefix+"index.htm\">Стартовая страница</a></li>");
  document.write("<li><a href=\""+prefix+"Articles.html\">Cтатьи, исходники</a></li>");
  document.write("<li><a href=\""+prefix+"WinDbg.html\">Заметки о WinDbg</a></li>");
  document.write("<li><a href=\""+prefix+"Downloads.html\">Скачать</a></li>");
  document.write("<li><a href=\""+prefix+"Links.html\">Внешние ссылки</a></li>");
  document.write("<li><a href=\""+prefix+"Overview.html\">Обо всем</a></li>");
  document.write("<li><a href=\""+prefix+"Contacts.html\">Контакты</a></li>");
  document.write("<li>");
  document.write("<a href=\""+prefix+"Tools.html\" onmouseover=\"nav_open_mtools()\" onmouseout=\"mclosetime()\">Утилиты</a>");
  document.write("<div id=\"m_tools\" onmouseover=\"mcancelclosetime()\" onmouseout=\"mclosetime()\">");
  document.write("<a href=\""+prefix+"tools/DefSound.html\" title=\"Установки аудио устройства по умолчанию\">DefSound</a>");
  document.write("<a href=\""+prefix+"tools/DSymLoad.html\" title=\"Загрузка отладочных символов в HIEW\">DSymLoad</a>");
  document.write("<a href=\""+prefix+"tools/UnDecSym.html\" title=\"Модуль UnDecSym (UnDecorate Symbol Name) для Python\">UnDecSym</a>");
  document.write("<a href=\""+prefix+"tools/diabind.html\" title=\"Модуль diabind: DIA (Debug Interface Access) SDK для Python\">diabind</a>");
  document.write("</div>");
  document.write("</li>");
  document.write("</ul>");
  document.write("</div>");
  document.write("<div style=\"clear:both\"></div>");
}