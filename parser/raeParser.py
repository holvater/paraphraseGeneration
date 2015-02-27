#!/usr/bin/env python3
###############################
# Rodrigo Cabrera Pena
# parser de rae.es para obtener definicion
# 01/10/2013
###############################

import urllib.request as request
import urllib.parse
import lxml.html

class Drae:
    _url = 'http://lema.rae.es/drae/srv/search'
    arg = 'val'

    def get_lemas(self, html):
        xpathQuery = """ ((//p[@class='q' and position() > 2][1] | //p[@class='q' and position() > 2][1]/following-sibling::p)
        [count(. | //p[@class='q' and position() > 2][1]
        /following-sibling::p
        [not(@class='q')][1]
        /preceding-sibling::*
        )
        =
        count(//p[@class='q' and position() > 2][1]
        /following-sibling::p
        [not(@class='q')][1]
        /preceding-sibling::*)])/span[@class='b']
        """
        root = lxml.html.fromstring(html, parser=lxml.html.HTMLParser(encoding='utf-8'))
        div_lema = root.xpath("/html/body/div")[0]
        lemas = []

        if div_lema is not None:
            div_suger = root.xpath("/html/body/ul/li/a")
            if div_suger:
                aviso = root.xpath("/html/body/p/span")
                return {
                    'aviso': aviso[0].text_content() if aviso else '',
                    'sugerencias': [s.text_content() for s in div_suger],
                }
            div_aviso = root.xpath("/html/body/p/font")
            if div_aviso:
                return {
                    'aviso': div_aviso[0].text_content(),
                }

        #for div_lema in div_lemas:
        lemas += [p.text_content() for p in div_lema.xpath(xpathQuery) if p.text_content()]
            
        return lemas

    def search(self, word=None):
        if not word:
            return
        word = word.encode('iso-8859-1')
        params = {
            'type': '3',
            'val_aux': '',
            'origen': 'RAE',
        }
        params.update({self.arg: word})
        qs = urllib.parse.urlencode(params)
        url = '{0}?{1}'.format(self._url, qs)
        response = request.urlopen(url)
        html = response.read()
        return self.get_lemas(html)

if __name__ == '__main__':
    d = Drae()
    print (d.search("boca"))






