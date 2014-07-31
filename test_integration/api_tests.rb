require "rake"

$env_protocol = "http"

task :default, [:env] do |t, args|
    $env_protocol = "https"
    puts "default task called #{args[:env]}"

    Rake::Task["run_tests"].execute
end

task :run_tests do
    puts "run_tests with protocol #{$env_protocol}"
end
