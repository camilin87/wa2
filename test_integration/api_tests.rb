namespace :api_tests do
    task :default => [
        :api_takes_trailing_slash,
        :reads_hialeah_data
    ]

    task :api_takes_trailing_slash do |t|
        base_url = test_url_with "25.86", "-80.30"
        expected_data = cleanup_timestamp curl base_url
        actual_data = cleanup_timestamp curl base_url + "/"

        assert_true(t, expected_data == actual_data)
    end
   
    task :reads_hialeah_data do |t|
        actual_data = cleanup_timestamp curl url_hialeah

        [
            '"errormsg": "",',
            '"intensity": "',
            '"pop": "',
            '"result": "200",',
            '"summary": "'
        ].each { |response_piece|
            includes_piece = actual_data.include? response_piece
            assert_true(t, includes_piece)
        }
    end

    def url_hialeah
        return staging_url_with "25.86", "-80.30"
    end
end
