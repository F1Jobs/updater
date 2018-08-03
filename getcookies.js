var webPage = require('webpage');
var page = webPage.create();

var ferrariUrl = 'https://hr.ferrari.com/cvo3ferrari/servlet/hvse_bstart?Theme=SpTheme_ZIP&Parameter=PARADEING&Company=000001&Idcompany=000000&Language=ENG&pProcedure=hvse_welcome&pLogin=&pFreeappl=S&Idchannel'

page.settings.javascriptEnabled = false;    //Don't let the Ferrari website load JS. Not a good idea.
page.settings.loadImages = false;           //Don't let it load images as well.

page.open(ferrariUrl, function(status) {
    var cookies = page.cookies;
    for (var i in cookies) {
        if (cookies[i].name == 'spcookie' || cookies[i].name == 'JSESSIONID') {
            console.log(cookies[i].value);
        }
    }
    phantom.exit();
});
