namespace :api_tests_cache do
    task :default => [:validate_cache]

    def basedir
       return File.expand_path ".."
    end

    task :validate_cache do
        url_hialeah = "#{$env_data[:protocol]}://#{$env_data[:host]}:#{$env_data[:port]}/t/api_key/25.86/-80.30"
        puts url_hialeah

        url_lax = "#{$env_data[:protocol]}://#{$env_data[:host]}:#{$env_data[:port]}/t/api_key/47.43/-121.80"
        puts url_lax

        cache_ttl_sec = $env_data[:cache_params][:ttl_seconds]

        if not all_urls_return_different_responses([url_hialeah, url_lax])
            fail "cache error: different urls return the same result"
            return
        end

        cache_request_helper_path = File.join(basedir, "test/cacherequesthelper.py")
        cache_test_output = `python #{cache_request_helper_path} "#{url_hialeah}" #{cache_ttl_sec}`

        if not cache_test_output.include? "is_cached=True"
            fail "cache error"
            return
        end
            
        puts "Cache OK"
    end

    def all_urls_return_different_responses(url_list)
        responses = []
        url_list.each { |url| responses.push `curl #{url}` }
        return responses.uniq.length == responses.length
    end
end
