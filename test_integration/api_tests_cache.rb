namespace :api_tests_cache do
    task :default => [
        :all_urls_return_different_responses,
        :validate_cache,
        :validate_cache_for_different_api_keys,
        :cache_expiration_header,
        :cache_hit_header
    ]

    task :all_urls_return_different_responses do |t|
        urls_return_different = all_urls_return_different_responses([url_hialeah, url_lax])

        assert_true(t, urls_return_different)
    end

    task :validate_cache do |t|
        cache_request_helper_path = File.join(basedir, "test/cacherequesthelper.py")
        verify_ssl = $env_data[:verify_certificate] ? "True" : "False"

        cache_validation_command = %{python #{cache_request_helper_path} "#{url_hialeah}" #{$env_data[:cache_params][:ttl_seconds]} #{verify_ssl}}
        puts cache_validation_command
        
        cache_test_output = `#{cache_validation_command}`
        output_is_cached = cache_test_output.include? "is_cached=True"

        assert_true(t, output_is_cached)
    end

    task :validate_cache_for_different_api_keys do |t|
        url_list = [
            test_url_with("25.86", "-80.30", "apikey1"),
            test_url_with("25.86", "-80.30", "apikey2"),
        ]
        output_is_cached = all_urls_return_the_same_response url_list

        assert_true(t, output_is_cached)
    end

    task :cache_expiration_header do |t|
        cache_test_output = curl_headers url_hialeah 
        contains_cache_header = cache_test_output.include? "Cache-Control: public, max-age=3600"

        assert_true(t, contains_cache_header)
    end

    task :cache_hit_header do |t|
        curl_headers url_hialeah
        cache_test_output = curl_headers url_hialeah
        contains_cache_hit_header = cache_test_output.include? "X-Cache: HIT"

        assert_true(t, contains_cache_hit_header)
    end

    def url_hialeah
        test_url_with "25.86", "-80.30"
    end

    def url_lax
        return test_url_with "47.43", "-121.80"
    end

    def all_urls_return_different_responses(url_list)
        responses = get_responses url_list
        return responses.uniq.length == responses.length
    end

    def all_urls_return_the_same_response(url_list)
        responses = get_responses url_list
        return responses.uniq.length == 1
    end

    def get_responses(url_list)
        responses = []
        url_list.each { |url| responses.push curl url }
        return responses
    end
end
