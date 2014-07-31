require "rake"

$env_data = {
    :protocol => "http",
    :host => "localhost",
    :port => 80,
    :validate_cache => false,
    :cache_params => {
        :ttl_seconds => 3
    }
}

task :default, [:env] do |t, args|
    configure_environment args[:env]
    Rake::Task["run_tests"].execute
end

def configure_environment(environment)
    case environment
    when "PRODUCTION"
        set_production_env_data
    when "STAGING"
        set_staging_env_data
    when "DEBUG"
        set_debug_env_data
    else
        raise "invalid environment specified"
    end
end

def set_production_env_data
    $env_data[:protocol] = "https"
    $env_data[:port] = 443
    $env_data[:host] = "api.v1.smartweatheralerts.com"
    $env_data[:validate_cache] = true
    $env_data[:cache_params][:ttl_seconds] = 3600 - 1
end

def set_staging_env_data
    $env_data[:validate_cache] = true
end

def set_debug_env_data
    $env_data[:port] = 8080
end

task :run_tests do
    puts "run_tests with environment"
    puts $env_data
end
