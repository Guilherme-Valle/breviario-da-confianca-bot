# breviario-da-confianca-bot

A aplicação consiste em um bot para Telegram, desenvolvido em Python, que retorna a meditação do dia do livro "Breviário da Confiança" do mons. Ascânio Brandão, cujos capítulos estão públicos na web (https://rumoasantidade.com.br/livro-breviario-confianca/). O algoritmo, após a requisição do bot, busca a data presente e realiza um simples scrapping para extrair o texto da meditação do website já citado, processando-o e retornando-o para o bot. As bibliotecas utilizadas foram o [python-telegram-bot](https://github.com/python-telegram-bot/) e o [Scrappy](https://github.com/scrapy/scrapy).
O nome do bot no telegram é [@AscanioBreviarioBot](https://t.me/AscanioBreviarioBot)

Atualmente o bot apenas retorna a meditação do dia através da chamada /meditacaodehoje, mas muitas melhorias são possíveis.
