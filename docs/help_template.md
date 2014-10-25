Wa Api Docs {{VERSION}}
===

#Request

    https://{{HOST}}/p/api_key/25.86/-80.30/

- **api_key** An alphanumeric string up to 100 characters
- **latitude** A valid latitude value with two decimal places of precision
- **longitude** A valid longitude value with two decimal places of precision

#Response

    {
      "errormsg": "",
      "intensity": "0",
      "pop": "0",
      "precip": "0",
      "result": "200",
      "summary": "Clear",
      "timestamp": "2014-08-12T12:38:40.032397"
    }

- **errormsg** An error message describing what went wrong
- **intensity** A value from the following list

{{INTENSITY_TYPES}}

- **pop** A percent value from 0 to 100
- **precip** A value from the following list

{{PRECIPITATION_TYPES}}

- **result** A value from the following list

{{API_RESULT}}

- **summary** A string with a summary of the weather
- **timestamp** The UTC time our server the response was issued

#Development
In a command line execute

    rake -f Rakefile-setup-dev.rb run_debug
Then consume the test api as follows

    http://localhost:8080/t/anykey/25.86/-80.30/
