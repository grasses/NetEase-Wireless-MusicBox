$(document).ready(function(){

	//处理框架事件
	var myApp = new Framework7();
	var $$ = Dom7;
	var view1 = myApp.addView('#view-1');
	var view2 = myApp.addView('#view-2', {
    	dynamicNavbar: true,
    	attachEvents:true,
<<<<<<< HEAD
    	handleTouchEnd: function(e){
    		alert('end');
    	}
=======
>>>>>>> c71daf5b84e7275ce21792461cf95dbc11265f32
	});
	var view3 = myApp.addView('#view-3');
	var view4 = myApp.addView('#view-4');

<<<<<<< HEAD
	console.log(view2);
	
	$('.set_volume').click(function (e){
		alert('set');
	});
=======
	var mainView = myApp.addView('.item-content');
	console.log(view2);
	//

	view2.handleTouchStart = function (e){
		alert('handleTouchStart');
	}
>>>>>>> c71daf5b84e7275ce21792461cf95dbc11265f32

	$('#search').click( function (e){
		var data = {
			'key': $('#key').val(),
		}
		$.post('/ajaxSearch', data, function (res){
			if(res){
				var result = res['songs'];
				var html ='<li><div class="item-content"><div class="item-inner"><div class="item-title">歌曲</div><div class="item-after">歌手</div></div></div></li>';
				for( var i=0; i<result.length; i++){
					console.log( result[i]['id'] );
					html += '<li><a href="/song.html?sid='+result[i]['id']+'" class="item-link"><div class="item-content"><!--img src="'+result[i]['blurPicUrl']+'"--><div class="item-inner"><div class="item-title">'+result[i]['name']+'</div><div class="item-after">'+result[i]['artists'][0]['name']+'</div></div></div></a></li>';
					$('#list-album').html(html).slideDown( {duration: 1000});
				}
			}else{

			}
		},'json');
	});

	var load_new_albums = function(){
		$.ajax({
			url : '/ajaxNewAlbums',
			method : 'POST',
			dataType: 'json',
			data : {'offset': 0, 'limit':10 },
			beforeSend: function( xhr ) {
    			//菊花转起来
    		},
    		success: function( res ){
    			//console.log(res);
    			var result = res;
				var html ='<li><div class="item-content"><div class="item-inner"><div class="item-title">歌曲</div><div class="item-after">歌手</div></div></div></li>';
				for( var i=0; i<result.length; i++){
					//console.log( result[i]['id'] );
<<<<<<< HEAD
					html += '<li><a href="/album.html?aid='+result[i]['id']+'" class="item-link"><div class="item-content"><div class="item-inner"><div class="item-title">'+result[i]['name']+'</div><div class="item-after">'+result[i]['artists'][0]['name']+'</div></div></div></a></li>';
					$('#list-album').html(html).slideDown( {duration: 10, easing: 'easeOutQubic'});
				}
    		},
		});
	};

	var load_hot_song = function(){
		$.ajax({
			url : '/ajaxHotSong',
			method : 'POST',
			dataType: 'json',
			data : {'offset': 0, 'limit':10 },
			beforeSend: function( xhr ) {
    			//菊花转起来
    		},
    		success: function( res ){
    			//console.log(res);
    			var result = res;
				var html ='<li><div class="item-content"><div class="item-inner"><div class="item-title">歌曲</div><div class="item-after">歌手</div></div></div></li>';
				for( var i=0; i<result.length; i++){
					//console.log( result[i]['id'] );
					html += '<li><a href="/song.html?sid='+result[i]['id']+'" class="item-link"><div class="item-content"><div class="item-inner"><div class="item-title">'+result[i]['name']+'</div><div class="item-after">'+result[i]['artists'][0]['name']+'</div></div></div></a></li>';
					$('#list-hot-song').html(html).slideDown( {duration: 10, easing: 'easeOutQubic'});
=======
					html += '<li><a href="/song.html?sid='+result[i]['id']+'" class="item-link"><div class="item-content"><div class="item-inner"><div class="item-title">'+result[i]['name']+'</div><div class="item-after">'+result[i]['artists'][0]['name']+'</div></div></div></a></li>';
					$('#list-album').html(html).slideDown( {duration: 500, easing: 'easeOutQubic'});
>>>>>>> c71daf5b84e7275ce21792461cf95dbc11265f32
				}
    		},
		});
	};

	$('#menu-tab-search').click(function (e){
		load_new_albums();
<<<<<<< HEAD
		load_hot_song();
=======
>>>>>>> c71daf5b84e7275ce21792461cf95dbc11265f32
	});

	$('.player').click(function (e){
		alert('xxxx');
	});
});






















