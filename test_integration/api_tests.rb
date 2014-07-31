namespace :api_tests do
    task :default => [:test_1, :test_2]

    task :test_1 do
        puts "api_tests.rb test_1 => ", $env_data
    end

    task :test_2 do
        puts "api_tests.rb test_2 => ", $env_data
    end
end
