namespace :api_tests do
    task :default => [:api_takes_trailing_slash, :test_2]

    task :api_takes_trailing_slash do |t|
        base_url = test_url_with "25.86", "-80.30"
        expected_data = cleanup_timestamp curl base_url
        actual_data = cleanup_timestamp curl base_url + "/"

        assert_true(t, expected_data == actual_data)
    end

    def cleanup_timestamp(response_body)
        return response_body.lines.reject { |line|
            line.include? "timestamp"
        }.join "\n"
    end

    task :test_2 do
        puts "api_tests.rb test_2 #{basedir} => ", $env_data
    end
end
