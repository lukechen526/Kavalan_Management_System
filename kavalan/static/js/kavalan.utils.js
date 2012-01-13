//**************************
// Detects if the current device is an iPhone, iPad, or iPod Touch.
function DetectIDevice()
{
    var deviceIphone = "iphone";
    var deviceIpod = "ipod";
    var deviceIPad = "ipad"

    //Initialize our user agent string to lower case.
    var uagent = navigator.userAgent.toLowerCase();

    //**************************
    // Detects if the current device is an iPhone.
    function DetectIphone()
    {
       if (uagent.search(deviceIphone) > -1)
          return true;
       else
          return false;
    }

    //**************************
    // Detects if the current device is an iPod Touch.
    function DetectIpod()
    {
       if (uagent.search(deviceIpod) > -1)
          return true;
       else
          return false;
    }


    //**************************
    // Detects if the current device is an iPad.
    function DetectIpad()
    {
       if (uagent.search(deviceIPad) > -1)
          return true;
       else
          return false;
    }


    if (DetectIphone())
       return true;
    else if (DetectIpod())
       return true;
    else if (DetectIpad())
        return true;
    else
       return false;
}
