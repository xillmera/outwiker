��          �   %   �      0  $   1  *   V  &   �  [  �  
                   .     3     9     G     Y     g     o     �  
   �     �     �     �     �     �     �  )     �  /  ?   �  B   	  A   _	  �  �	     �  $   �     �     �     �  *     ?   7     w     �  :   �     �     �  *        -     E  
   a  V   l  /   �  '   �     
                                      	                                                                                    <B>Source plugin: Encoding error</B> <B>Source plugin: File '{0}' not found</B> <B>Source plugin: Unknown encoding</B> Add command (:source:) in wiki parser. This command highlight your source code.

<B>Usage:</B>:
(:source params... :)
source code
(:sourceend:)

<B>Params:</B>
<I>lang</I> - programming language
<I>tabwidth</I> - tab size
<I>file</I> - attached source file
<I>encoding</I> - encoding of the attached source file (default encoding - utf8)
<I>style</I> - style of hightlighting

<B>Example 1:</B>
<PRE>(:source lang="python" tabwidth=4:)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>

<B>Example 2:</B>
<PRE>(:source lang="python" style="autumn":)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>

<B>Example 3:</B>
<PRE>(:source file="Attach:example.cs" encoding="cp1251":)(:sourceend:)</PRE>

<B>Example 4:</B>
<PRE>(:source file="Attach:example.txt" lang="python":)(:sourceend:)</PRE>
 Appearance Attach new files Attached file Auto Clear Default Style Default Tab Width File encoding General Insert source from file Language Select All Source Code (:source ...:) Source [Plugin] Source code Style Tab Width (0 - Default Value) Used Languages http://jenyay.net/Outwiker/SourcePluginEn Project-Id-Version: outwiker
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2013-02-17 14:10+0400
PO-Revision-Date: 2013-02-18 21:18+0300
Last-Translator: Eugeniy Ilin <jenyay.ilin@gmail.com>
Language-Team: Ukrainian
Language: uk_UA
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: crowdin.net
X-Poedit-Language: Ukrainian
X-Poedit-Country: UKRAINE
X-Poedit-SourceCharset: utf-8
 <B>Додаток Source: Помилка кодування</B> <B>Додаток Source: Файл '{0}' не знайдено</B> <B>Додаток Source: Невідоме кодування</B> Додаток додає вікі-команду (:source:) для розфарбовування тексту програми на різних мовах програмування.

<B>Використання:</B>:
(:source параметри... :)
Текст програми
(:sourceend:)

<B>Параметри:</B>
<I>lang</I> - мова програмування
<I>tabwidth</I> - розмір табуляції
<I>file</I> - долучений файл з текстом програми
<I>encoding</I> - кодування долученого файлу з текстом програми (кодування за замовчуванням - utf8)
<I>style</I> - стиль оформлення, що використовується

<B>Приклад 1:</B>
<PRE>(:source lang="python" tabwidth=4:)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>

<B>Приклад 2:</B>
<PRE>(:source lang="python" style="autumn":)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>

<B>Приклад 3:</B>
<PRE>(:source file="Attach:example.cs" encoding="cp1251":)(:sourceend:)</PRE>

<B>Приклад 4:</B>
<PRE>(:source file="Attach:example.txt" lang="python":)(:sourceend:)</PRE>
 Зовнішній вигляд Долучити нові файли Долучений файл Авто Очистити Стиль за замовчуванням Ширина табуляції за замовчуванням Кодування файлу Загальне Вставити текст програми з файлу Мова Виділити все Текст програми (:source ...:) Source [Додаток] Текст програми Стиль Ширина табуляції (0 - значення за замовчуванням) Мови, що використовуються http://jenyay.net/Outwiker/SourcePlugin 