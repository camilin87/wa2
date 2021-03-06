import "api_tests_utils.rb"
import "api_tests_cache.rb"
import "api_tests.rb"

$env_data = {
    :name => "default",
    :protocol => "http",
    :verify_certificate => false,
    :host => "localhost",
    :port => 80,
    :validate_cache => false,
    :cache_params => {
        :ttl_seconds => 3
    }
}

task :run_tests_with_environment, [:env] do |t, args|
    configure_environment args[:env]
    Rake::Task[:run_tests].invoke
end

def configure_environment(environment)
    $env_data[:name] = environment

    case environment
    when "production"
        set_production_env_data
    when "staging"
        set_staging_env_data
    when "staging_ssl"
        set_staging_ssl_env_data
    when "debug"
        set_debug_env_data
    else
        raise "invalid environment specified"
    end
end

def set_production_env_data
    $env_data[:protocol] = "https"
    $env_data[:port] = 443
    $env_data[:host] = get_production_host
    $env_data[:verify_certificate] = true
    $env_data[:validate_cache] = true
    $env_data[:cache_params][:ttl_seconds] = 10 - 1
end

def get_production_host
    host_file = File.join(basedir, "host.txt")
    return File.open(host_file, &:gets)
end

def set_staging_env_data
    $env_data[:validate_cache] = true
end

def set_staging_ssl_env_data
    $env_data[:protocol] = "https"
    $env_data[:port] = 443
    $env_data[:validate_cache] = true
end

def set_debug_env_data
    $env_data[:port] = 8080
end

task :run_tests do
    puts "run_tests with environment"
    puts $env_data

    if $env_data[:validate_cache]
        Rake::Task["api_tests_cache:default"].invoke
    end

    Rake::Task["api_tests:default"].invoke
end
