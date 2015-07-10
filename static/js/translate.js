$(document).ready(function () {

	// Переключение языков
	var sourceLang = '';
	var destLang = 'ru';
	$('.language').click(function () {
		sourceLang = $(this).attr("value");
		var lang = $(this).html();
		//$('.language').removeClass("active");
		//$(this).toggleClass("active");
		$('#language').html(lang);
		$("#button_translate").attr("href", "javascript:translate('" + sourceLang + "', '" + destLang + "', 'textarea#original', 'textarea#translate');");
	});

	//Выбор языков в переводчике

	$('.dst-language').click(function () {
		destLang = $(this).attr("value");
		var lang = $(this).html();
		$('#dst-language').html(lang);
		$("#button_translate").attr("href", "javascript:translate('" + sourceLang + "', '" + destLang + "', 'textarea#original', 'textarea#translate');");
	});

});

function translate(sourceLang, destLang, sourceId, destId) {

	$(".img-preload").fadeIn(200); //Отображаем прелоадер на время запроса

	$.post('/service/_translate', {
		text: $(sourceId).val(), //
		sourceLang: sourceLang, //Данные для запроса
		destLang: destLang //
	}).done(function (translated) { //Действие при успешном запросе
		$(destId).val(translated['text']); // Заменяем текст в поле Перевод
		var x = $('.lang_menu li a[value="' + translated['auto_lang'] + '"]').html();
		$('#language').text(x + ' (Авто)').fadeIn(); //Отображаем текст источника если выбрано Автоопределение языка
		$(".img-preload").fadeOut(200); //Убираем прелоадер
	}).fail(function () { //Действие при ошибке
		$(".img-preload").fadeOut(200);
		$(destId).val("Ошибка Максима Валерьевича");
	});
};