<?php
/* captcha.php file*/

	session_start();
		
	header("Content-type: image/png");

	// beri nama session dengan nama Captcha
	$_SESSION["Captcha"]="";
	//tentukan ukuran gambar
	$gbr = imagecreate(140, 40);

	//warna background gambar
	imagecolorallocate($gbr, 89, 100, 187);

	$grey = imagecolorallocate($gbr, 217, 229, 238);

	$black = imagecolorallocate($gbr, 0, 0,0);

	// tentukan font
	$font = "fonts/monaco.ttf"; 

	// membuat nomor acak dan ditampilkan pada gambar
	for($i=0;$i<=5;$i++) {
		// jumlah karakter
		$nomor=rand(0, 9);

		$_SESSION["Captcha"].=$nomor;

		$sudut= rand(-25, 25);

		imagettftext($gbr, 20, $sudut, 8+20*$i, 30, $black, $font, $nomor);

		// efek shadow
		imagettftext ($gbr, 20, $sudut, 9+20*$i, 35, $grey, $font, $nomor);
	}
	//untuk membuat gambar 
	imagepng($gbr); 
	imagedestroy($gbr);

?>