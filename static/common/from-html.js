var doc = new jsPDF();



// All units are in the set measurement for the document
// This can be changed to "pt" (points), "mm" (Default), "cm", "in"
doc.fromHTML($('.content').get(0), 15, 15, {
	'width': 170, 

});
var string = doc.output('datauristring');
$('.preview-pane').attr('src', string);
