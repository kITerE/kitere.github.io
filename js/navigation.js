

function nav_open_mtools()
{
  mopen("m_tools");
}

function nav_write(prefix)
{
  document.write("<div id=\"navigation\">");
  document.write("<ul id=\"menu\">");
  document.write("<li><a href=\""+prefix+"index.htm\">��������� ��������</a></li>");
  document.write("<li><a href=\""+prefix+"Articles.html\">C�����, ���������</a></li>");
  document.write("<li><a href=\""+prefix+"WinDbg.html\">������� � WinDbg</a></li>");
  document.write("<li><a href=\""+prefix+"Downloads.html\">�������</a></li>");
  document.write("<li><a href=\""+prefix+"Links.html\">������� ������</a></li>");
  document.write("<li><a href=\""+prefix+"Overview.html\">��� ����</a></li>");
  document.write("<li><a href=\""+prefix+"Contacts.html\">��������</a></li>");
  document.write("<li>");
  document.write("<a href=\""+prefix+"Tools.html\" onmouseover=\"nav_open_mtools()\" onmouseout=\"mclosetime()\">�������</a>");
  document.write("<div id=\"m_tools\" onmouseover=\"mcancelclosetime()\" onmouseout=\"mclosetime()\">");
  document.write("<a href=\""+prefix+"tools/DefSound.html\" title=\"��������� ����� ���������� �� ���������\">DefSound</a>");
  document.write("<a href=\""+prefix+"tools/DSymLoad.html\" title=\"�������� ���������� �������� � HIEW\">DSymLoad</a>");
  document.write("<a href=\""+prefix+"tools/UnDecSym.html\" title=\"������ UnDecSym (UnDecorate Symbol Name) ��� Python\">UnDecSym</a>");
  document.write("<a href=\""+prefix+"tools/diabind.html\" title=\"������ diabind: DIA (Debug Interface Access) SDK ��� Python\">diabind</a>");
  document.write("</div>");
  document.write("</li>");
  document.write("</ul>");
  document.write("</div>");
  document.write("<div style=\"clear:both\"></div>");
}