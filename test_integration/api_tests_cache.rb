namespace :api_tests_cache do
    task :default => [:validate_cache]

    task :validate_cache do
        url_hialeah = test_url_with "25.86", "-80.30"
        url_lax = test_url_with "47.43", "-121.80"

        if not all_urls_return_different_responses([url_hialeah, url_lax])
            fail "cache error: different urls return the same result"
            return
        end

        cache_request_helper_path = File.join(basedir, "test/cacherequesthelper.py")
        cache_test_output = `python #{cache_request_helper_path} "#{url_hialeah}" #{$env_data[:cache_params][:ttl_seconds]}`

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
