Wa Api Docs {{VERSION}}
===

#Request
##Url
    https://{{HOST}}/p/api_key/25.86/-80.30/
##Fields
- api_key
    An alphanumeric string up to 100 characters
- latitude
    A valid latitude value with two decimal places of precision
- longitude
    A valid longitude value with two decimal places of precision

#Response
##Sample Response
    {
      "errormsg": "",
      "intensity": "0",
      "pop": "0",
      "precip": "0",
      "result": "200",
      "summary": "Clear",
      "timestamp": "2014-08-12T12:38:40.032397"
    }
##Fields
- errormsg
- intensity
    A value from the following list

{{INTENSITY_TYPES}}

- pop
