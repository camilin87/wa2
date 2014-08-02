def test_url_with(latitude, longitude)
    result_url = "#{$env_data[:protocol]}://#{$env_data[:host]}:#{$env_data[:port]}/t/api_key/#{latitude}/#{longitude}" 
    puts result_url
    return result_url
end
