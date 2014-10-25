def host_url
    return "#{$env_data[:protocol]}://#{$env_data[:host]}:#{$env_data[:port]}"
end

def test_url_with(latitude, longitude, api_key="api_key")
    result_url = "#{host_url}/t/#{api_key}/#{latitude}/#{longitude}"
    return result_url
end

def staging_url_with(latitude, longitude)
    result_url = "#{host_url}/s/anyapikey/#{latitude}/#{longitude}"
    return result_url
end

def assert_true(task, condition, error_message="")
    if condition
        puts "."
    else
        raise "#{task.name} ERROR #{error_message}"
    end
end

def get_curl_command
    if $env_data[:verify_certificate]
        return "curl "
    else
        return "curl -k "
    end
end

def curl(url)
    command = "#{get_curl_command} -s -L #{url}"
    puts command
    return `#{command}`
end

def curl_headers(url)
    command = "#{get_curl_command} -s -I -L #{url}"
    puts command
    return `#{command}`
end

def cleanup_timestamp(response_body)
    return response_body.lines.reject { |line|
        line.include? "timestamp"
    }.join "\n"
end
