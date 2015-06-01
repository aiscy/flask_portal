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

	// Разметка обеденного меню
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
					.append('<td class="edit"><button class="btn btn-default btn-order" type="button">Заказать  <span class="badge"></span></button></td>');
				_table.find('tbody tr').has('td strong:contains("Комплекс")').find('td:last-child').addClass('edit').html('<button class="btn btn-default btn-order" type="button">Заказать  <span class="badge"></span></button>');
				_table.find('tbody tr').has('td strong:contains("Комплекс")').nextAll().find('td:last-child').html('<td></td>');
				_table.find('tbody tr').has("td:first-child:empty").find('td:last-child').removeClass('edit').html('<td></td>');
	});
};
TABLE.formwork('.table');

	// Событие на нажатие кнопки заказать
		
		$('.food_menu tr').has('td.edit').click(function() {
		var count = $(this).find('.badge').text();
		var food = $(this).find('td:first-child').text();
		function addFood() {
			$('#result').append($('<li>' + food +'<span></span></li>'));
		};
		if ($('#result li:contains("' + food + '")').text() = null) {
			alert($('#result li:contains("' + food + '")').text());
			};
		$(this).addClass('success');
		$(this).find('.badge').text(++count);

			addFood ();
	}); //||
//	$('.btn-order').click(function() {
//		var food = '';
//		food = $(this).parents('tr').find('td:first-child').text();
//		$(this).parents('tr').addClass('success');
//			addFood();
//	});

	
	// Отправка заказа

$('#submit').click(function () {
		var n=1;
		var cabinet = $('#InputCabinet').val();
		var initials = $('#InputInitials').val();
		var body_message = 'Кабинет №' + cabinet + ' ' + initials + '%0D%0D';
		$('#result li').each(function() {
			body_message += n + '. ' + $(this).text() + '%0D';
			n += 1;
		});
		var email = 'maxim_pavlov@uraltep.ru';
		var subject = 'ПИЦ УралТЭП Заказ';
			var mailto_link = 'mailto:' + email + '?subject=' + subject + '&body=' + body_message;
		$('#test').attr('href', mailto_link);
		win = window.open(mailto_link, 'emailWindow');
		if (win && win.open && !win.closed) win.close();
});
});
