<?php 
  $refId = rand(10000000000, 99999999999);
  $data = array(
    "tx_ref" => $refId,
    "amount" => 100,
    "currency" => "RWF",
    "customer" => array(
        "email" => "rithamari9@gmail.com",
        "phonenumber" => "0783879009",
        "name" => "Umutoni Ritha",
    ),
    "payment_options" => "card",
    "redirect_url" => "https://nyarugengemarket.herokuapp.com/",
    "customizations" => array(
        "title" => "Groceries payment",
        "description" => "This for groceries payment",
        "logo" => "https://res.cloudinary.com/auca/image/upload/v1614707944/logo2_lcz0bg.png",
    ),
);
$url = "https://api.flutterwave.com/v3/payments";
$authorization = "Authorization: Bearer FLWSECK_TEST-05f0494d5fe92f48a8dc76b9902dd92c-X";
$payload = json_encode($data);
//open connection
$ch = curl_init();
//set the url, number of POST vars, POST data
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json', $authorization));
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
//execute post
$result = curl_exec($ch);
$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
//close connection
curl_close($ch);
$proceed = json_decode($result);
$url = $proceed->data;
// print_r($url->link);
// return false;
header("Location: $url->link");
?> 






