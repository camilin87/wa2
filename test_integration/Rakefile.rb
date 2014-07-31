import "api_tests_environment_setup.rb"

task :default => [:staging]

task :staging do |t|
    run_tests t.name
end

task :production do |t|
    run_tests t.name
end

task :debug do |t|
    # launch the debug webserver here
    run_tests t.name
    # shutdown the debug webserver here
end

def run_tests(env_name)
    Rake::Task[:run_tests_with_environment].invoke env_name
end
