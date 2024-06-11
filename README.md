Este projeto é protótipo de uma de rede social voltado para eventos chamado **Ond**.

Essa rede viria com o objeto de suprir uma lacuna que existe na divulgação de eventos, tanto "oficiais" como "não-oficiais". Essa lacuna é se deu por dois fatos:

1. a diminuição do uso do Facebook, que tinha a secção de eventos;
2. a subsequente fragmentação da informação do que tem "pra fazer por aí". Para se buscar essa informação se depende do boca-a-boca ou seguir perfis específicos no Whatsapp ou Instagram.

O **Ond** seria onde (rsrs) o público criaria e procuraria eventos que existem na cidade, ampliando a divulgação da informação além de circuitos menores.

## (Pilha de) Software

### Django

Talvez o principal _framework web_ do Python, foi escolhido por ter a filosofia do _batteries included_: ele já vem com templates, ORM, roteamento, etc. o que torna acelerado o processo de desenvolvimento. Além disso contém uma grande comunidade e ecosistema.

### HTMX

Biblioteca _Javascript_ que permite a realização do AJAX por meio de atributos das tags do HTML. Com ele é possível dar mais dinâmica para as pagínas com pouco ou nenhum javascript. Como a natureza do aplicativo é fortemente _CRUD (Create, Read, Update, Delete)_ e baseada no _back-end_, optei pelo **HTMX**, que enriquece o bom e velho HTML, do que soluções _Single Page Application_.

### Hyperscript

Linguagem de _scripting_ que permite interagir com o DOM, por meio de comandos inclusos de forma _inline_ no HTML. Fiz uso dela de modo experimental para explorar o [Princípio da Localidade do Comportamento](https://htmx.org/essays/locality-of-behaviour/), polo oposto do muito predominante [Princípio da Separação dos Conceitos](https://pt.wikipedia.org/wiki/Separa%C3%A7%C3%A3o_de_conceitos).

Outras opções desta mesma natureza:

-   [Alpine.js](https://alpinejs.dev/)
-   [Surreal.js](https://github.com/gnat/surreal)

### Tailwindcss

Abordagem _utility-first_ do _CSS_ de uso generalizado no desenvolvimento _web_. Usei-o para evitar o problema da criação e nomeamento de classes (e subclasses) que existe no CSS padrão.

## Setup

-   pip install -r requirements.txt
-   python manage.py initenv
-   python manage.py migrate
-   python manage.py popular
-   python manage.py runserver

## Demonstração

### Consulta de Eventos

![Demonstração da consulta de eventos](https://github.com/lrpohlmann/rede-social-eventos/blob/master/docs/gif/demonstracao_consulta_evento.gif)

### Comentar Evento

![Demonstração funcionalidade de comentar no evento](https://github.com/lrpohlmann/rede-social-eventos/blob/master/docs/gif/demonstracao_comentar.gif)

### Edição de Perfil

![Demonstração funcionalidade de editar o perfil](https://github.com/lrpohlmann/rede-social-eventos/blob/master/docs/gif/demonstracao_edicao_perfil.gif)
