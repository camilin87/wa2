namespace :api_tests_cache do
    task :default => [
        :all_urls_return_different_responses,
        :validate_cache,
        :cache_expiration_header
    ]

    task :all_urls_return_different_responses do |t|
        urls_return_different = all_urls_return_different_responses([url_hialeah, url_lax])

        assert_true(t, urls_return_different)
    end

    task :validate_cache do |t|
        cache_request_helper_path = File.join(basedir, "test/cacherequesthelper.py")
        cache_test_output = `python #{cache_request_helper_path} "#{url_hialeah}" #{$env_data[:cache_params][:ttl_seconds]}`
        output_is_cached = cache_test_output.include? "is_cached=True"

        assert_true(t, output_is_cached)
    end

    task :cache_expiration_header do |t|
        cache_test_output = curl_headers url_hialeah 
        contains_cache_header = cache_test_output.include? "Cache-Control: max-age=3600"

        assert_true(t, contains_cache_header)
    end

    def url_hialeah
        test_url_with "25.86", "-80.30"
    end

    def url_lax
        return test_url_with "47.43", "-121.80"
    end

    def all_urls_return_different_responses(url_list)
        responses = []
        url_list.each { |url| responses.push curl url }
        return responses.uniq.length == responses.length
    end
end
