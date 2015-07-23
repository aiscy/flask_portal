$(document).ready(function() {

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
			var totalPrice = $("#total").text();
			var n = 1;
		var cabinet = $('#InputCabinet').val();
		var initials = $('#InputInitials').val();
		var body_message = 'Кабинет №' + cabinet + ' ' + initials + '%0D%0D';
		$('#result li').each(function () {
			body_message += n + '. ' + $(this).find('span:first-child').text() + ' (' + $(this).find('span:nth-child(2)').text() + ') ' +$(this).find('span:last-child').text() + '%0D';
			n += 1;
		});
		
		var email = 'hmelnov@yandex.ru';
		var subject = 'ПИЦ УралТЭП Заказ';
		var mailto_link = 'mailto:' + email + '?subject=' + subject + '&body=' + body_message + '%0DСумма заказа: ' + totalPrice;
		$('#submit').attr('href', mailto_link);
		var win = window.open(mailto_link, 'emailWindow');
		if (win && win.open && !win.closed) win.close();
		}
	});
});