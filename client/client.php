<?php

namespace juwai\client;

require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/../gen-php/juwai/PropertyService.php';
require_once __DIR__ . '/../gen-php/juwai/Types.php';

use Thrift\Transport\TSocket;
use Thrift\Transport\TBufferedTransport;
use Thrift\Protocol\TBinaryProtocolAccelerated;
use juwai\PropertyServiceClient;

try {
	$socket = new TSocket('localhost', '9090');
	// $transport = new TBufferedTransport($socket);
	$transport = new TFramedTransport($socket);
	$protocol = new TBinaryProtocolAccelerated($transport);
	$client = new PropertyServiceClient($protocol);

	$transport->open();
	$property = $client->getProperty($argv[1]);
	$transport->close();

	var_dump($property);
} catch ( Exception $e ) {
	echo $e . PHP_EOL;
}
