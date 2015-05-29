__author__ = 'pavlomv'
from flask.ext.script import Manager
from flask_portal import app

manager = Manager(app)

# TEST

@manager.command
def get_quote_of_day():
    """
    Получаем цитату дня для вывода на сайте
    """
    db = None
    import requests
    import sqlite3
    request = requests.get(url='http://api.forismatic.com/api/1.0/',
                           params=dict(method='getQuote',
                                       format='json',
                                       lang='ru')).json()
    try:
        db = sqlite3.connect(app.config['DATABASE'])
        cursor = db.cursor()
        cursor.executemany('INSERT OR REPLACE INTO quote_of_day (id, quote_text, quote_author) VALUES (?, ?, ?)',
                           [(1, request.get('quoteText'), request.get('quoteAuthor'))])
        db.commit()
    finally:
        db.close()


@manager.command
def get_food_menu():
    """
    Грабим обеденное меню:D и записываем результат в базу
    """
    import sqlite3
    import html
    import re
    from grab import Grab
    from lxml import html
    from lxml.html import clean
    from lxml.html import builder as E
    html_str = '''

    <!doctype html>
<!--[if lt IE 7]>
<html class="nojs ie-lt7 ie-lt8 ie-lt9 ie-lt10 ie">
<![endif]-->
<!--[if lt IE 8]>
<html class="nojs ie-lt8 ie-lt9 ie-lt10 ie">
<![endif]-->
<!--[if lt IE 9]>
<html class="nojs ie-lt9 ie-lt10 ie">
<![endif]-->
<!--[if lt IE 10]>
<html class="nojs ie-lt10 ie">
<![endif]-->
<!--[if gt IE 8]> <!-->
<html class="nojs">
<!--><![endif]-->
<head>
		<title>Меню — Привет Буфет</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="keywords" content="Меню" />
	<meta property="og:title" content="Меню" />
<meta property="og:site_name" content="Www.privet-bufet.ru" />




	<meta http-equiv="Content-Language" content="ru"/>
	<link rel="shortcut icon" href="/uploads/favicon.ico" type="image/x-icon"/>

	<!--[if IE]>
	<meta content="IE=edge" http-equiv="X-UA-Compatible">
	<![endif]-->
	<!--[if IE 6]>
	<link rel="stylesheet" type="text/css" media="screen" href="/designs/design_3/common/styles/style.ie6.css"/>
	<script type="text/javascript" src="/designs/design_3/common/scripts/DD_belatedPNG_0.0.8a-min.js"></script>
	<script type="text/javascript">
		DD_belatedPNG.fix('.png');
		DD_belatedPNG.fix('.prefix');
		DD_belatedPNG.fix('.header-contacts');
		DD_belatedPNG.fix('.admin-panel');
	</script>
	<![endif]-->
	<!--[if IE 7]>
	<link rel="stylesheet" type="text/css" media="screen" href="/designs/design_3/common/styles/style.ie7.css"/>
	<![endif]-->
	<!--[if lt IE 7]>
	<script type="text/javascript" src="/designs/design_3/common/scripts/ie_stylesheet.js"></script>
	<script type="text/javascript" src="/designs/design_3/common/scripts/ie_png_ail.js"></script>
	<![endif]-->

	<script type="text/javascript">
		var current_design = 3,
			current_language = "ru";
		document.documentElement.className = document.documentElement.className.replace('nojs', 'js');
	</script>

	<link href="/designs/design_3/includes.min.css" rel="stylesheet" type="text/css"/>
	<link rel="stylesheet" type="text/css" href="/dynamic/styles.css" media="all"/>
	<link href="/addon/gadget-color.css" rel="stylesheet" type="text/css" media="screen"/>

	<script type="text/javascript" src="/designs/design_3/includes.min.js"></script>
	<script type="text/javascript" src="/addon/customize.js"></script>
</head>
<body class="panda-bg-color design_3 panda-module-article panda-user">
<!--[if lt IE 8]>
<p class="browsehappy">Вы используете <strong>устаревший</strong> браузер. Пожалуйста <a href="http://browsehappy.com/">обновите
	браузер</a>, чтобы получить больше возможноcтей.</p>
<![endif]-->


<div class="panda-admin-panel__header">



<script type="text/javascript">
		function killFSlash( string ) {
			while ( string.substring (0,1) == '/' ) string = string.substr(1);
			return string;
		}
		var seo_url = location.href.replace( location.host, "" ).replace(location.protocol, "");
		seo_url = killFSlash(seo_url);
	</script>

<div class="seo-panel" id="seo_panel_div" style="display:none;"></div>

	</div>

<div class="panda-wrapper"
     style="background:url('/uploads/shapka.png') no-repeat scroll center top transparent">
	<div class="panda-wrapper__header">
		<div class="panda-header panda-block__dynamic-width">



								<div class="panda-logo">
						<a href="/" class="panda-logo-link">
				<img src="/uploads/logo.png" class="ie-png-ail" alt="Привет Буфет" title="Привет Буфет" />
			</a>
			</div>
				<div class="panda-search__header">
																										<div class="top-phone panda-header__phone panda-secondary-font">
			<p><span style="font-size: small;font-family: arial;color: #ea1d22;"><em>Для контактной связи </em></span><br />
<img align="left" alt="" height="32" hspace="5" src="/uploads/image/phone.png" vspace="13" width="24" />+7 (904) 548-42-57;<br />
+7 (904) 169-63-43;</p>

<p>&nbsp; &nbsp; &nbsp; +7 (343) 200-42-11&nbsp;</p>
	</div>									</div>




	<ul class="panda-menu__horizontal-header panda-context-novis">
												<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-0">
											<a href="/" class="panda-menu__horizontal-header-item-text panda-shadow-color-hover panda-gradient-hover rounded rc5 rocon__7 rocon-init">
							<ins>Главная</ins>
							<span class="rocon rocon-br"></span>
							<span class="rocon rocon-bl"></span>
							<span class="rocon rocon-tr"></span>
							<span class="rocon rocon-tl"></span>
						</a>

														</li>
															<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-1">
											<a href="/article/stol-zakazov" class="panda-menu__horizontal-header-item-text panda-shadow-color-hover panda-gradient-hover rounded rc5 rocon__7 rocon-init">
							<ins>Стол заказов</ins>
							<span class="rocon rocon-br"></span>
							<span class="rocon rocon-bl"></span>
							<span class="rocon rocon-tr"></span>
							<span class="rocon rocon-tl"></span>
						</a>

														</li>
															<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-2">
																								<span class="panda-menu__horizontal-header-item-text panda-shadow-color panda-gradient rounded rc5 rocon__7 rocon-init">
								<ins>Меню</ins>
								<span class="rocon rocon-br"></span>
								<span class="rocon rocon-bl"></span>
								<span class="rocon rocon-tr"></span>
								<span class="rocon rocon-tl"></span>
							</span>

														</li>
															<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-3">
											<a href="/article/spetspredlozheniya" class="panda-menu__horizontal-header-item-text panda-shadow-color-hover panda-gradient-hover rounded rc5 rocon__7 rocon-init">
							<ins>Спецпредложения</ins>
							<span class="rocon rocon-br"></span>
							<span class="rocon rocon-bl"></span>
							<span class="rocon rocon-tr"></span>
							<span class="rocon rocon-tl"></span>
						</a>

														</li>
															<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-4">
											<a href="/article/myod-1" class="panda-menu__horizontal-header-item-text panda-shadow-color-hover panda-gradient-hover rounded rc5 rocon__7 rocon-init">
							<ins>Мёд</ins>
							<span class="rocon rocon-br"></span>
							<span class="rocon rocon-bl"></span>
							<span class="rocon rocon-tr"></span>
							<span class="rocon rocon-tl"></span>
						</a>

														</li>
															<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-5">
											<a href="/article/pirogi" class="panda-menu__horizontal-header-item-text panda-shadow-color-hover panda-gradient-hover rounded rc5 rocon__7 rocon-init">
							<ins>Пироги</ins>
							<span class="rocon rocon-br"></span>
							<span class="rocon rocon-bl"></span>
							<span class="rocon rocon-tr"></span>
							<span class="rocon rocon-tl"></span>
						</a>

														</li>
															<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-6">
											<a href="/article/dostavka-obedov" class="panda-menu__horizontal-header-item-text panda-shadow-color-hover panda-gradient-hover rounded rc5 rocon__7 rocon-init">
							<ins>Комплексные обеды</ins>
							<span class="rocon rocon-br"></span>
							<span class="rocon rocon-bl"></span>
							<span class="rocon rocon-tr"></span>
							<span class="rocon rocon-tl"></span>
						</a>

														</li>
															<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-7">
											<a href="/article/obsluzhivanie-meropriyatiy" class="panda-menu__horizontal-header-item-text panda-shadow-color-hover panda-gradient-hover rounded rc5 rocon__7 rocon-init">
							<ins>Обслуживание мероприятий</ins>
							<span class="rocon rocon-br"></span>
							<span class="rocon rocon-bl"></span>
							<span class="rocon rocon-tr"></span>
							<span class="rocon rocon-tl"></span>
						</a>

														</li>
															<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-8">
											<a href="/feedback" class="panda-menu__horizontal-header-item-text panda-shadow-color-hover panda-gradient-hover rounded rc5 rocon__7 rocon-init">
							<ins>Книга жалоб и предложений</ins>
							<span class="rocon rocon-br"></span>
							<span class="rocon rocon-bl"></span>
							<span class="rocon rocon-tr"></span>
							<span class="rocon rocon-tl"></span>
						</a>

														</li>
															<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-9">
											<a href="/news" class="panda-menu__horizontal-header-item-text panda-shadow-color-hover panda-gradient-hover rounded rc5 rocon__7 rocon-init">
							<ins>Новости</ins>
							<span class="rocon rocon-br"></span>
							<span class="rocon rocon-bl"></span>
							<span class="rocon rocon-tr"></span>
							<span class="rocon rocon-tl"></span>
						</a>

														</li>
															<li class="panda-menu__horizontal-header-item panda-menu__horizontal-header-item-10">
											<a href="/contacts" class="panda-menu__horizontal-header-item-text panda-shadow-color-hover panda-gradient-hover rounded rc5 rocon__7 rocon-init">
							<ins>Контакты</ins>
							<span class="rocon rocon-br"></span>
							<span class="rocon rocon-bl"></span>
							<span class="rocon rocon-tr"></span>
							<span class="rocon rocon-tl"></span>
						</a>

														</li>
						</ul>

	<ul class="panda-buttons-social__header">
		<li>
			<a class="panda-mini-ico__home" href="/"></a>
	</li>		<li>
			<a class="panda-mini-ico__map" href="/sitemap"></a>
	</li>		<li>
	<a class="panda-mini-ico__mail" href="mailto:info@privet-bufet.ru"></a>
</li>	</ul>


		</div>
		<div class="panda-basket__header">
								</div>
	</div>


	<div class="panda-wrapper__main">

<div class="panda-main panda-block__dynamic-width">
	<div class="panda-grid-wrapper panda-context-vis">

		<div class="panda-grid__8 panda-grid__margin0">






<div class="panda-gadget__main panda-gadget-text" id="gadget_block_20">
			<span class="h1">Внимание!!!</span>

	<div id="gadget_view_20">
		<h2>Антикризисное предложение - комплекс за 100 рублей!</h2>

<p><strong>3 варианта на выбор:</strong></p>

<p><strong>1. суп и второе</strong></p>

<p><strong>2. выпечка и второе</strong></p>

<p><strong>3. салат и второе</strong></p>

<p><span style="font-size:10px;">Примечание: комплекс составляется на наше усмотрение. Заказ принимается не меньше, чем на 5 человек.</span></p>
	</div>

	</div>








		</div>

		<div class="panda-grid__16 panda-grid__margin8">

			<ul class="panda-path panda-block__set-last-child">
				<li><a href="/">Главная</a></li>
								<li>Меню</li>
			</ul>

			<div class="panda-article">

				<h1>Меню</h1>


				<table border="1" cellpadding="0" cellspacing="0" style="width:642px;" width="642">
	<tbody>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong>Меню на 2</strong><strong>8.</strong><strong>05.1</strong><strong>5</strong></p>
			</td>
			<td style="width:85px;">
			<p align="center"><strong>Выход</strong></p>

			<p align="center"><strong>(граммы)</strong></p>
			</td>
			<td style="width:105px;">
			<p align="center"><strong>Цена</strong></p>

			<p align="center"><strong>(рублей)</strong></p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Салаты</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Салат из моркови с кальмарами (морковь, кальмары, яйца, зелёный лук, зелёный горошек, майонез)</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">40-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Салат из капусты с огурцами и помидорами</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">35-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:21px;">
			<p>&nbsp;</p>
			</td>
			<td style="width:85px;height:21px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;height:21px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:19px;">
			<p>Каша «рисовая» на молоке</p>
			</td>
			<td style="width:85px;height:19px;">
			<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 210</p>
			</td>
			<td style="width:105px;height:19px;">
			<p align="center">35-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:19px;">
			<p>Запеканка из творога со сгущённым молоком</p>
			</td>
			<td style="width:85px;height:19px;">
			<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 150</p>
			</td>
			<td style="width:105px;height:19px;">
			<p align="center">45-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:19px;">
			<p>Омлет натуральный</p>
			</td>
			<td style="width:85px;height:19px;">
			<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 150</p>
			</td>
			<td style="width:105px;height:19px;">
			<p align="center">30-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p><strong><em>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Супы</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Окрошка с квасом со сметаной</p>
			</td>
			<td style="width:85px;">
			<p align="center">300/20</p>
			</td>
			<td style="width:105px;">
			<p align="center">35-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Суп картофельный с горохом</p>
			</td>
			<td style="width:85px;">
			<p align="center">300</p>
			</td>
			<td style="width:105px;">
			<p align="center">30-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Мясные блюда</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Горбуша запечённая с грибами и сыром</p>
			</td>
			<td style="width:85px;">
			<p align="center">100</p>
			</td>
			<td style="width:105px;">
			<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 75-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Шницель «по-столичному» (филе куры в сухариках)</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">75-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:5px;">
			<p>Гуляш из говядины</p>
			</td>
			<td style="width:85px;height:5px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;height:5px;">
			<p align="center">80-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Рагу из картофеля с курой</p>
			</td>
			<td style="width:85px;">
			<p align="center">300</p>
			</td>
			<td style="width:105px;">
			<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 90-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Голубцы ленивые</p>
			</td>
			<td style="width:85px;">
			<p align="center">2шт.</p>
			</td>
			<td style="width:105px;">
			<p align="center">60-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Гарниры </em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Макароны отварные</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:5px;">
			<p>Греча рассыпчатая</p>
			</td>
			<td style="width:85px;height:5px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;height:5px;">
			<p align="center">20-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Капуста тушёная</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">30-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Рис отварной</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">20-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пюре картофельное</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">30-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Выпечка</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пицца с колбасой</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">45-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Сосиска в тесте</p>
			</td>
			<td style="width:85px;">
			<p align="center">100</p>
			</td>
			<td style="width:105px;">
			<p align="center">25-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Чебурек с мясом</p>
			</td>
			<td style="width:85px;">
			<p align="center">110</p>
			</td>
			<td style="width:105px;">
			<p align="center">45-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Самса с курицей</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">45-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Слойка с ветчиной и сыром</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">30-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Слойка с творогом</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">30-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Шаньга с картошкой</p>
			</td>
			<td style="width:85px;">
			<p align="center">100</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пирожок с вишней</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">20-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пирожок с яблоками</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пирожок с капустой</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пирожок с яйцом, рисом и зелёным луком</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Напитки</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Сок в ассортименте</p>
			</td>
			<td style="width:85px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;">
			<p align="center">20-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Компот</p>
			</td>
			<td style="width:85px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Чай с сахаром</p>
			</td>
			<td style="width:85px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;">
			<p align="center">7-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Чай с лимоном</p>
			</td>
			<td style="width:85px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;">
			<p align="center">10-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Кофе 3 в 1</p>
			</td>
			<td style="width:85px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;">
			<p align="center">12-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Комплекс</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">135-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Салат из капусты с огурцами и помидорами</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Суп картофельный с горохом</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Рагу из картофеля с курой</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Компот</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Хлеб</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
	</tbody>
</table>

<p>&nbsp;</p>

<p>&nbsp;</p>

<table border="1" cellpadding="0" cellspacing="0" style="width:642px;" width="642">
	<tbody>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong>Меню на 2</strong><strong>9.</strong><strong>05.1</strong><strong>5</strong></p>
			</td>
			<td style="width:85px;">
			<p align="center"><strong>Выход</strong></p>

			<p align="center"><strong>(граммы)</strong></p>
			</td>
			<td style="width:105px;">
			<p align="center"><strong>Цена</strong></p>

			<p align="center"><strong>(рублей)</strong></p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Салаты</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Салат из капусты с копчёной курой</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">38-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Салат из огурцов и помидоров с маслом растительным</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">35-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Яйцо под майонезом с подгарнировкой</p>
			</td>
			<td style="width:85px;">
			<p align="center">100</p>
			</td>
			<td style="width:105px;">
			<p align="center">25-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:21px;">
			<p>&nbsp;</p>
			</td>
			<td style="width:85px;height:21px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;height:21px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:19px;">
			<p>Каша «пшённая» на молоке</p>
			</td>
			<td style="width:85px;height:19px;">
			<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 210</p>
			</td>
			<td style="width:105px;height:19px;">
			<p align="center">35-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:19px;">
			<p>Оладьи со сгущённым молоком</p>
			</td>
			<td style="width:85px;height:19px;">
			<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2шт.</p>
			</td>
			<td style="width:105px;height:19px;">
			<p align="center">30-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p><strong><em>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Супы</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Солянка «по-домашнему» со сметаной</p>
			</td>
			<td style="width:85px;">
			<p align="center">300/20</p>
			</td>
			<td style="width:105px;">
			<p align="center">50-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Окрошка с квасом со сметаной</p>
			</td>
			<td style="width:85px;">
			<p align="center">300/20</p>
			</td>
			<td style="width:105px;">
			<p align="center">35-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Мясные блюда</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Кета тушёная в сметанном соусе</p>
			</td>
			<td style="width:85px;">
			<p align="center">100</p>
			</td>
			<td style="width:105px;">
			<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 75-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Курица запечённая «по-восточному»</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">75-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:5px;">
			<p>Хинкали со сметаной</p>
			</td>
			<td style="width:85px;height:5px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;height:5px;">
			<p align="center">75-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Гуляш из свинины «по-венгерски»</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 80-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Котлета «столичная»</p>
			</td>
			<td style="width:85px;">
			<p align="center">80</p>
			</td>
			<td style="width:105px;">
			<p align="center">45-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Гарниры </em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Макароны отварные</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;height:5px;">
			<p>Греча рассыпчатая</p>
			</td>
			<td style="width:85px;height:5px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;height:5px;">
			<p align="center">20-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Капуста тушёная</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">30-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Рис отварной</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">20-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пюре картофельное</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">30-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Выпечка</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Сосиска в тесте</p>
			</td>
			<td style="width:85px;">
			<p align="center">100</p>
			</td>
			<td style="width:105px;">
			<p align="center">25-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Расстегай с горбушей</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">25-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Самса с мясом</p>
			</td>
			<td style="width:85px;">
			<p align="center">150</p>
			</td>
			<td style="width:105px;">
			<p align="center">50-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Шаньга с картошкой</p>
			</td>
			<td style="width:85px;">
			<p align="center">100</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Сдоба с курагой</p>
			</td>
			<td style="width:85px;">
			<p align="center">100</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пирожок с брусникой</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">20-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пирожок с яблоками</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пирожок с капустой</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Пирожок с яйцом, рисом и зелёным луком</p>
			</td>
			<td style="width:85px;">
			<p align="center">75</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Напитки</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Сок в ассортименте</p>
			</td>
			<td style="width:85px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;">
			<p align="center">20-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Компот</p>
			</td>
			<td style="width:85px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;">
			<p align="center">15-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Чай с сахаром</p>
			</td>
			<td style="width:85px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;">
			<p align="center">7-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Чай с лимоном</p>
			</td>
			<td style="width:85px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;">
			<p align="center">10-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Кофе 3 в 1</p>
			</td>
			<td style="width:85px;">
			<p align="center">200</p>
			</td>
			<td style="width:105px;">
			<p align="center">12-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p align="center"><strong><em>Комплекс</em></strong></p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">135-00</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Салат из капусты с копчёной курой</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Окрошка с квасом со сметаной</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Гуляш из свинины «по-венгерски»</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Греча рассыпчатая</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Компот</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
		<tr>
			<td style="width:453px;">
			<p>Хлеб</p>
			</td>
			<td style="width:85px;">
			<p align="center">&nbsp;</p>
			</td>
			<td style="width:105px;">
			<p align="center">&nbsp;</p>
			</td>
		</tr>
	</tbody>
</table>

									<h2>Файлы для скачивания:</h2>

											<p><span class="doc-file"><a href="/uploads/article_file/113/dogovor_1.docx">Договор</a></span> <em>(0.02 Мб)</em><br />

</p>
											<p><span class="doc-file"><a href="/uploads/article_file/150/menyu_na_280515.docx">Меню на 28.05.15</a></span> <em>(0.02 Мб)</em><br />

</p>
											<p><span class="doc-file"><a href="/uploads/article_file/161/menyu_na_290515.docx">Меню на 29.05.15</a></span> <em>(0.02 Мб)</em><br />

</p>
												</div>
		</div>
	</div>

	<div class="panda-gadget__grid-2">





		</div></div>	</div>
</div>
<div class="panda-wrapper__footer panda-area-color">
	<div class="panda-footer panda-block__dynamic-width">


							<noindex>
		<ul class="panda-footer-menu panda-context-vis">
																						<li class="panda-footer-menu-item">
							<a href="/" rel="nofollow">Главная</a> <ins>:</ins>						</li>
																															<li class="panda-footer-menu-item">
							<a href="/article/stol-zakazov" rel="nofollow">Стол заказов</a> <ins>:</ins>						</li>
																															<li class="panda-footer-menu-item__active">
																							<span class="active">Меню</span> <ins>:</ins>													</li>
																															<li class="panda-footer-menu-item">
							<a href="/article/spetspredlozheniya" rel="nofollow">Спецпредложения</a> <ins>:</ins>						</li>
																															<li class="panda-footer-menu-item">
							<a href="/article/myod-1" rel="nofollow">Мёд</a> <ins>:</ins>						</li>
																															<li class="panda-footer-menu-item">
							<a href="/article/pirogi" rel="nofollow">Пироги</a> <ins>:</ins>						</li>
																															<li class="panda-footer-menu-item">
							<a href="/article/dostavka-obedov" rel="nofollow">Комплексные обеды</a> <ins>:</ins>						</li>
																															<li class="panda-footer-menu-item">
							<a href="/article/obsluzhivanie-meropriyatiy" rel="nofollow">Обслуживание мероприятий</a> <ins>:</ins>						</li>
																															<li class="panda-footer-menu-item">
							<a href="/feedback" rel="nofollow">Книга жалоб и предложений</a> <ins>:</ins>						</li>
																															<li class="panda-footer-menu-item">
							<a href="/news" rel="nofollow">Новости</a> <ins>:</ins>						</li>
																															<li class="panda-footer-menu-item">
							<a href="/contacts" rel="nofollow">Контакты</a>						</li>
														</ul>
	</noindex>
			<div class="panda-footer__info">
								<div class="panda_copy revert-link-color">
	Привет Буфет &copy;
					2015		</div>

<div class="panda-footer__phone panda-secondary-font">
			<p><strong>Адрес: </strong>г. Екатеринбург, ул Гаршина 1а</p>

<p><strong>Телефон:</strong> (904) 548-42-57; (904) 169-63-43; (982)724-08-00;&nbsp;(343) 200-42-11</p>

<p><strong>E-mail: </strong><a href="mailto:info@privet-bufet.ru">info@privet-bufet.ru</a></p>
	</div>

<div class="panda-footer__email">
	Электронная почта: <a class="mail-link" href="&#109;&#x61;i&#108;&#x74;&#111;&#58;&#x69;&#x6e;&#x66;&#111;&#x40;&#112;&#x72;&#105;&#x76;&#x65;&#116;-&#98;u&#102;&#101;t&#46;&#114;&#117;">info@privet-bufet.ru</a></div>
			</div>
				<div class="panda-footer-ancors">
					</div>
	<div class="clear:right;"></div>
			<div class="panda-clickzone__footer">
									<div class="panda-block-text-zone">
		<br>
<!--LiveInternet counter--><script type="text/javascript"><!--
document.write("<a href='http://www.liveinternet.ru/click' "+
"target=_blank><img src='//counter.yadro.ru/hit?t11.3;r"+
escape(document.referrer)+((typeof(screen)=="undefined")?"":
";s"+screen.width+"*"+screen.height+"*"+(screen.colorDepth?
screen.colorDepth:screen.pixelDepth))+";u"+escape(document.URL)+
";"+Math.random()+
"' alt='' title='LiveInternet: показано число просмотров за 24"+
" часа, посетителей за 24 часа и за сегодня' "+
"border='0' width='88' height='31'><\/a>")
//--></script><!--/LiveInternet-->
	</div>
<div style="clear: right"></div>			</div>


		<div class="panda-contacts__footer">
												<span id="itpanda"
						  title="Создание сайтов" alt="Создание сайтов"></span>
									</div>


							<div class="panda-login-link">
					<a href="/login">
						<img src="/designs/design_3/common/images/footer/login-link.png" class="ie-png-ail-image"/>
					</a>
				</div>

				</div>
	<div style="clear:both"></div>
</div>




<script type="text/javascript" src="/designs/design_3/common/scripts/vendors/jquery_easing.js"></script>
<script type="text/javascript" src="/designs/design_3/common/scripts/vendors/jquery_fancybox.js"></script>
<script type="text/javascript" src="/js/seo.js"></script>
<link rel="stylesheet" type="text/css" media="screen" href="/css/seopanel.css" />
<link rel="stylesheet" type="text/css" media="screen" href="/designs/design_3/common/styles/fancybox.css" />
<div id="popupcontainer" class="popupcontainerTarget" style="display:none"></div>
<link href="/addon/gadget-color-bottom.css" rel="stylesheet" type="text/css" media="screen"/>
<script type="text/javascript" src="/addon/customize-bottom.js"></script>
</body>
</html>

    '''
    db = None
    # g = Grab()
    # g.go('http://www.privet-bufet.ru/article/menyu-na-segodnya')
    # request = g.doc.select('//div[@class="panda-article"]').html()
    doc = html.document_fromstring(html_str)
    cleaner = clean.Cleaner(style=True, remove_tags=['p', 'em'])
    # style:
    # Removes any style tags or attributes.
    # remove_tags:
    # A list of tags to remove. Only the tags will be removed, their content will get pulled up into the parent tag.
    # Оставляем только таблицу с меню на завтра
    doc = cleaner.clean_html(doc)
    html_new = html.tostring(E.DIV(E.TABLE(E.CLASS("table table-striped food_menu"), doc.cssselect('tbody')[-1])),
                             encoding='unicode')
    try:
        db = sqlite3.connect(app.config['DATABASE'])
        cursor = db.cursor()
        cursor.executemany('INSERT OR REPLACE INTO food_menu (id, html) VALUES (?, ?)',
                           [(1, re.sub(r'\s{2,}', ' ', html_new))])
        db.commit()
    finally:
        db.close()



if __name__ == '__main__':
    manager.run()
