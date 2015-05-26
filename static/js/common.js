$(document).ready(function () {
	//$('.content').animated('fadeIn','fadeOut');
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

	$('.dst-language').click(function() {
		destLang = $(this).attr("value");
		var lang = $(this).html();
		//$('.language').removeClass("active");
		//$(this).toggleClass("active");
		$('#dst-language').html(lang);
		$("#button_translate").attr("href", "javascript:translate('" + sourceLang + "', '" + destLang + "', 'textarea#original', 'textarea#translate');");
	});

	// Jumbotron Animation

	// var x = 120;
	// $(".banner").css('backgroundSize', x + '%');
	// window.setInterval(function() {  
 //                $(".banner").css("backgroundSize", x + '%');  
 //                x=x-0.01;  
 
 //            }, 90);

});
// $(window).load(function() {
// 	$(".loader_inner").fadeOut();
// 	$(".loader").delay(400).fadeOut("slow");
// });