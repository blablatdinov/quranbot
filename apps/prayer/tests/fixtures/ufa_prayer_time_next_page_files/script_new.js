$(document).ready(function(){
	
		$('img').each(function(){
		$(this).attr('src', $(this).data('src'));
	  });
	  

		setTimeout(function(){
			 
			   loadScript("//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js", function(){
          
				$('.google_ads').each(function(){
					
					$(this).html('<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-1295350984516471" data-ad-slot="3608689842" data-ad-format="auto" data-full-width-responsive="true"></ins>');
					(adsbygoogle = window.adsbygoogle || []).push({});
				});
				
				
					
				});
			 
			 
		
			 
			loadScript("https://www.googletagmanager.com/gtag/js?id=UA-158129949-1", function(){
          
				   window.dataLayer = window.dataLayer || [];
				  function gtag(){dataLayer.push(arguments);}
				  gtag('js', new Date());

				  gtag('config', 'UA-158129949-1');
					
				});
				
      	}, 2000);
	  

});



function menu_toggle(type){
   if(type == 'open')
      $('.menu').show();
   if(type == 'close')
      $('.menu').hide();
}

function scroll_to_top(){
   $('html, body').animate({ scrollTop: 0 }, 600);
}


	
function slide_top_window(){
	
	if(!$(".open").prop("checked")){

		$(".btn").html('X');
	}
	
	if($(".open").prop("checked")){
		$(".btn").html('Это должен знать каждый');
		
	}
	
}

 function time_to_eat(){	  
	
	dateObj = new Date();

let firstDate = $('#magrib_to_calc').text(); //20:19
let secondDate = $('#fajir_to_calc').text(); //02:29
let nowDate = dateObj.getHours() + ':' + dateObj.getMinutes(); //22:55
let add_text_to_result = 'Ифтар - Сухур <br /> закончится через: ';
let different, differentRes, hours, minuts;;
let getDate = (string) => new Date(0, 0,0, string.split(':')[0], string.split(':')[1]);




if((getDate(firstDate) - getDate(nowDate)) > 0 && (getDate(secondDate) - getDate(nowDate)) <= 0){
	
	secondDate = firstDate;
	firstDate = nowDate;
	add_text_to_result = 'Ифтар <br /> начнётся через: ';
	
	different = (getDate(secondDate) - getDate(nowDate));
	
}else{
	
	if((getDate(secondDate) - getDate(nowDate)) > 0){
		add_text_to_result = 'Сухур <br /> закончится через: ';
	}
	
	different = ((getDate(secondDate) - (15*60*1000) ) - getDate(nowDate));
	
}

	
	if(different > 0) {
	  differentRes = different;
	  hours = Math.floor((differentRes % 86400000) / 3600000);
	  minuts = Math.round(((differentRes % 86400000) % 3600000) / 60000);
	} else {
	  differentRes = Math.abs(((getDate(secondDate) - (15*60*1000) ) - getDate(nowDate)));
	  hours = Math.floor(24 - (differentRes % 86400000) / 3600000);
	  minuts = Math.round(((differentRes % 86400000) % 3600000) / 60000);
	  
	  if(minuts > 0){
		   minuts = (60 - minuts);
	  }
	}
	
	let result = add_text_to_result + hours + ' ч ' + minuts + ' мин';


$('.time_to_eat').html(result);
$('.time_to_eat').show();

	  
}	  


function load_time_namaz(city, asr=''){
		
		$.ajax({
		  type: 'POST',
		  url: '/ajax/load_time_namaz_new.php' ,
		  data: 'city='+city+'&asr='+asr,
		  success: function(data) {
			  
			  if(data != 2){
				  
				$("#time_namaz_city").html(data);

				$("#time_namaz_city").show();
				
				//time_to_eat();
				  
			  }

		  }

		});

}

 //#################################################################
  function search_city(result, widget=''){
	  
	 var search_string =  $('[name='+result+']').val();
	 var result_find = '';
		
		if(search_string.length >=2){
			
			$.ajax({
			  type: 'POST',
			  url: '/ajax/search_city.php' ,
			  data: 'city='+search_string+'&widget='+widget,
			  success: function(data) {
				  
				  result_find = 1;
				  
				  if(data != 2){
					  
					  
					$("#"+result).html(data);

					$("#"+result).show();
					  
				  }
				  
				  if(data == ''){
						
						$("#"+result).html('<a href="">По вашему запросу ничего не найдено</a>');

						$("#"+result).show();
						
					}

			  }

			});
			
			
			
		}else 
			{
				result_find = '';
				$("#"+result).hide();
				$("#"+result).html('');
				
			}

}

//#################################################################
function click_on_rating(id,rating){
	
	//alert(id+' - '+rating);
	
	$.ajax({
		  type: 'POST',
		  url: '/ajax/click_on_rating.php' ,
		  data: 'id='+id+'&rating='+rating,
		  success: function(data) {
			$("#"+id+"_rating").html(data);

		  }

		});
	
}

//#################################################################
function load_mosque_adress(city,type){
	
	//alert(id+' - '+rating);
	
	$.ajax({
		  type: 'POST',
		  url: '/ajax/load_mosque_adress.php' ,
		  data: 'city='+city+'&type='+type,
		  success: function(data) {
			  if(data == 2){
				  alert('При загрузке информации возникли неполадки');
			  }else{
				$("#"+type+"_onClick").attr('onClick', "$('."+type+"_adress').toggle();");
				$("#"+type+"_adress").replaceWith(data);
			  }

		  }

		});
	
}
//#################################################################
function Load(city, month, year){
	
	var rus_month = new Array();
		rus_month[1] = 'Январь';
		rus_month[2] = 'Февраль';
		rus_month[3] = 'Март';
		rus_month[4] = 'Апрель';
		rus_month[5] = 'Май';
		rus_month[6] = 'Июнь';
		rus_month[7] = 'Июль';
		rus_month[8] = 'Август';
		rus_month[9] = 'Сентябрь';
		rus_month[10] = 'Октябрь';
		rus_month[11] = 'Ноябрь';
		rus_month[12] = 'Декабрь';
	
	$.ajax({
		  type: 'POST',
		  url: '/ajax/print_time_namaz.php' ,
		  data: 'city='+city+'&month='+month+'&year='+year+'&print_time=print',
		  success: function(data) {
			  
			  if(data != 2){
				  
				printwin = open('', 'printwin', 'width=500,height=300');
				printwin.document.open();
				printwin.document.writeln('<html><head><title></title></head><body onload=print();close()>');
				printwin.document.writeln('<style>table.namaz_time{border:none;border-collapse:collapse;font-size: 12pt;}table.namaz_time td, table.namaz_time th{text-align:center;padding:4px 3px;border:1px solid #000;}</style>');
				printwin.document.writeln("<h1>Расписание намаза в городе "+city+"</h1>Расписание составлено на "+rus_month[month]+" "+year+" года<br /><br />"+data);
				printwin.document.writeln('<div style="page-break-before:always;">');

				printwin.document.writeln('</div>');
				printwin.document.writeln('</body></html>');
				printwin.document.close();
				  
			  }

		  }

		});
	
}

//#################################################################
function change_table(city, month, year, table_type, asr){
	
	if(table_type == 'block'){
		
		document.cookie = "table_type=block; max-age=6048000";
		document.cookie = "asr="+asr+"; max-age=6048000";
		$('#icon-arrow3').removeClass("icon-active3");
		$('#icon-arrow2').addClass("icon-active2");
		
		var url = $('#time_namaz_to_pdf').attr("href");
		var split_url = url.split("_");
		$('#time_namaz_to_pdf').attr("href", "/time_"+split_url[1]+"_"+month+"_"+year+"_"+asr+".pdf");
	}
	
	if(table_type == 'table'){
		
		//$.cookie("table_type", "table", { expires : 60 });
		//$.cookie("asr", asr, { expires : 60 });
		document.cookie = "table_type=table; max-age=6048000";
		document.cookie = "asr="+asr+"; max-age=6048000";
		$('#icon-arrow2').removeClass("icon-active2");
		$('#icon-arrow3').addClass("icon-active3");
		
		var url = $('#time_namaz_to_pdf').attr("href");
		var split_url = url.split("_");
		$('#time_namaz_to_pdf').attr("href", "/time_"+split_url[1]+"_"+month+"_"+year+"_"+asr+".pdf");
	}
	
	
	
	$.ajax({
		  type: 'POST',
		  url: '/ajax/print_time_namaz.php' ,
		  data: 'city='+city+'&month='+month+'&year='+year+'&print_time=print'+'&table_type='+table_type+'&asr='+asr,
		  success: function(data) {
			  
			  if(data != 2){
				  
				$("#table_for_change").html(data);
				load_time_namaz(city, asr);
				  
			  }

		  }

		});
	
}



//Переменная для определения была ли хоть раз загружена Яндекс.Карта (чтобы избежать повторной загрузки при наведении)
var check_if_load = false;

 

// Функция загрузки API Яндекс.Карт по требованию (в нашем случае при наведении)
function loadScript(url, callback){
  var script = document.createElement("script");
 
  if (script.readyState){  // IE
    script.onreadystatechange = function(){
      if (script.readyState == "loaded" ||
              script.readyState == "complete"){
        script.onreadystatechange = null;
        callback();
      }
    };
  } else {  // Другие браузеры
    script.onload = function(){
      callback();
    };
  }
 
  script.src = url;
  document.getElementsByTagName("head")[0].appendChild(script);
}
 
// Основная функция, которая проверяет когда мы навели на блок с классом &#34;ymap-container&#34;
var ymap = function() {
  $('#map').click(function(){
      if (!check_if_load) { // проверяем первый ли раз загружается Яндекс.Карта, если да, то загружаем
 
	  	// Чтобы не было повторной загрузки карты, мы изменяем значение переменной
        check_if_load = true; 
 
		// Показываем индикатор загрузки до тех пор, пока карта не загрузится
		$('.loader').addClass('loader-default');
        $('.loader').addClass('is-active');
 
		// Загружаем API Яндекс.Карт
        loadScript("https://api-maps.yandex.ru/2.1/?lang=ru_RU&apikey=ee9395fc-3382-4c0d-b84e-000c1e0b4be2", function(){
           // Как только API Яндекс.Карт загрузились, сразу формируем карту и помещаем в блок с идентификатором &#34;map-yandex&#34;
           ymaps.load(init);
		   setTimeout(function(){
			  $('.loader').removeClass('is-active');
			}, 2000);
		    
        });                
      }
    }
  );  
}
 
$(function() {
 
  //Запускаем основную функцию
  ymap();
 
});



var play = 0;
function audio_play(){

	if(play == 0){
		document.getElementById('azan_audio').play();
		play = 1;
	}else{
		document.getElementById('azan_audio').pause();
		play = 0;
	}
	
}
function azan_close(type){

	if(type == 'close'){
		$('.pulse').hide();
		$('.azan_close').attr('onclick', "azan_close('open');");
		$('.azan_close').attr('class', "azan_open");
		document.cookie = "azan_audio=close; max-age=6048000";
	}
	if(type == 'open'){
		$('.pulse').show();
		$('.azan_open').attr('onclick', "azan_close('close');");
		$('.azan_open').attr('class', "azan_close");
		document.cookie = "azan_audio=open; max-age=6048000";
	}
	
	
}

 function qibla_show(type){
	   if(type == 'open'){
		  $('.back_shadow').show();
		  //$('.loader').addClass('loader-default');
		  //$('.loader').addClass('is-active');
		  $('#qibla_show').html();
		  $('#qibla_show').show();
		  
		   //setTimeout(function(){
			//  $('#qibla_loader').remove();
			//}, 2000);
	   }
	   if(type == 'close'){
		  $('#qibla_show').hide();
		  $('.back_shadow').hide();
	   }
	}


	
	