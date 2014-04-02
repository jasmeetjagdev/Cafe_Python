function drawszlider(ossz, meik,counter){
	var szazalek=Math.round((meik*100)/ossz);
	document.getElementsByName("szliderbar")[counter].style.width=szazalek+'%';
	//document.getElementById("szazalek").innerHTML=szazalek+'%';
	
}