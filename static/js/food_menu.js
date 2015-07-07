$(document).ready(function() {

	// Разметка обеденного меню
	var TABLE = {};
	var totalPrice = 0;
//	TABLE.formwork = function (table) {
//		var $tables = $(table);
//
//		$tables.each(function () {
//			var _table = $(this);
//			var _button = '<button class="btn btn-default btn-order" type="button">Заказать  <span class="badge"></span></button>'; // Разметка кнопки 'Заказать'
//			var _cancelButton = '<button type="button" class="btn btn-danger btn-cancel" aria-label="Left Align"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>'; // Разметка кнопки 'Отмена'
//
//			_table.find('tbody tr:has("td strong")').append($('<td></td>'));
//			_table.find('tbody tr').not(':has("td strong")').append('<td class="edit">' + _button + _cancelButton + '</td>');
//			_table.find('tbody tr').has('td strong:contains("Комплекс")').find('td:last-child').addClass('edit').html(_button + _cancelButton);
//			_table.find('tbody tr').has('td strong:contains("Комплекс")').nextAll().find('td:last-child').removeAttr("class").html('');
//			var strMessage1 = document.getElementsByClassName("food_menu");
//strMessage1[0].innerHTML = strMessage1[0].innerHTML.replace(/<td> <\/td>/g,'<td><\/td>');
//			_table.find('tbody tr').has("td:first-child:empty").find('td:last-child').removeAttr('class').html('<td></td>');
//		});
//	};
//	TABLE.formwork('.table');

	// Событие на нажатие кнопки заказать

	$('.food_menu tr').has('td.edit').click(function () {
		var foodID = $(this);
		var price = parseInt(foodID.find('td:nth-child(3)').text(),10);
		var count = foodID.find('.badge').text(); //Счетчик кол-ва заказа
		var food = foodID.find('td:first-child').text();  //Возвращает наименование выбранного товара
		foodID.find('.badge').text(++count); //При клике, добавляется +1 к счетчику
		
		// Если товар уже есть, то прибавляем +1 к количеству
		if ($('#result').find('li:contains("' + food + '")').html() != null) {
			var total = parseInt($('#result').find('li:contains("' + food + '") span.price').text()) + price;
			$('#result').find('li:contains("' + food + '") span.count').html(count + 'шт.');
			$('#result').find('li:contains("' + food + '") span.price').html(total + ' руб.')
		}
		// Если нет, то добавляем в заказ
		else {
			foodID.addClass('success');
			$('#result').append($('<li>' + food + '  <span class="count">' + count + 'шт.</span>  <span class="price">' + price + ' руб.</span></li>'));
			$('button#submit').removeAttr('disabled')
//			foodID.find('.btn-cancel').show();
		};
		
		totalPrice += price;
		$('#total').html(totalPrice + ' руб.');
		
		//Отображаем значок отмены
		
	});
	$('.btn-cancel').click(function() {
		$(this).parent().find('.badge').text('0');
	});

	// Отправка заказа, валидация

	$('#order_form').validate({
		
		rules: {
			cabinet:{
				required: true,
				rangelength: [2, 4],
				number: true
			},
		},
		messages: {
			cabinet: {
				required: "Это поле обязательно для заполнения",
				rangelength: "Число должно быть от 2 до 4 цифр",
				number: "Введите корректное число"
			},
		},
		highlight: function(element, errorClass, validClass) {
			$(element).addClass('error_input').removeClass(validClass);
		},
		unhighlight: function(element, errorClass, validClass) {
			$(element).removeClass('error_input').addClass(validClass);
		},	
		
		submitHandler: function(form) {
			var n = 1;
		var cabinet = $('#InputCabinet').val();
		var initials = $('#InputInitials').val();
		var body_message = 'Кабинет №' + cabinet + ' ' + initials + '%0D%0D';
		$('#result li').each(function () {
			body_message += n + '. ' + $(this).text() + '%0D';
			n += 1;
		});
		
		var email = 'hmelnov@yandex.ru';
		var subject = 'ПИЦ УралТЭП Заказ';
		var mailto_link = 'mailto:' + email + '?subject=' + subject + '&body=' + body_message + '%0DСумма заказа: ' + totalPrice + ' руб.';
		$('#submit').attr('href', mailto_link);
		var win = window.open(mailto_link, 'emailWindow');
		if (win && win.open && !win.closed) win.close();
		}
	});
});