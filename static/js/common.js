$(document).ready(function () {
	//$('.content').animated('fadeIn','fadeOut');
	
		// Дата в футере
	
	var date = new Date();
	$(".year").html(date.getFullYear());
	
		// Переключение языков
	var sourceLang = '';
	var destLang = 'ru';
	$('.language').click(function() {
		sourceLang = $(this).attr("value");
		var lang = $(this).html();
		//$('.language').removeClass("active");
		//$(this).toggleClass("active");
		$('#language').html(lang);
		$("#button_translate").attr("href", "javascript:translate('" + sourceLang + "', '" + destLang + "', 'textarea#original', 'textarea#translate');");
	});

	//Выбор языков в переводчике
	
	$('.dst-language').click(function() {
		destLang = $(this).attr("value");
		var lang = $(this).html();
		//$('.language').removeClass("active");
		//$(this).toggleClass("active");
		$('#dst-language').html(lang);
		$("#button_translate").attr("href", "javascript:translate('" + sourceLang + "', '" + destLang + "', 'textarea#original', 'textarea#translate');");
	});

	// парсинг обеденного меню
var TABLE = {};
TABLE.formwork = function (table) {
	var $tables = $(table);

	$tables.each(function () {
		var _table = $(this);

				_table
					.find('tbody tr:has("td strong")')
					.append($('<td></td>'));

				_table
					.find('tbody tr').not(':has("td strong")')
					.append($('<td class="edit"><input class="btn btn-default btn-order" type="button" value="Заказать"/></td>'))

	});
};
TABLE.formwork('.table');
	
	$('.btn-order').click(function() {
		var food = '';
		food = $(this).parents('tr').find('td:first-child').text();
		$(this).parents('tr').addClass('success');
		$('#result').append($('<p>' + food +'</p>'));
	});
	
	// Отправка заказа


$('#submit').click(function () {
		var body_message = $('#result').text();
var email = 'maxim_pavlov@uraltep.ru';
var subject = 'Заказ';
			var mailto_link = 'mailto:' + email + '?subject=' + subject + '&body=' + body_message;

			win = window.open(mailto_link, 'emailWindow');
			if (win && win.open && !win.closed) win.close();
});
});
// $(window).load(function() {
// 	$(".loader_inner").fadeOut();
// 	$(".loader").delay(400).fadeOut("slow");
// });