import "api_tests_environment_setup.rb"

def basedir
   return File.expand_path ".."
end

task :default => [:staging]

task :staging do |t|
    run_tests t.name
end

task :production do |t|
    run_tests t.name
end

task :debug do |t|
    Rake::Task[:start_debug_server].invoke

    begin
        run_tests t.name
    ensure
        Rake::Task[:stop_debug_server].invoke
    end
end

task :start_debug_server do
    spawn(debug_server_executable)
    sleep(3)
end

task :stop_debug_server do
    pid = `ps -l | grep "#{debug_server_executable}" | grep -v "grep" | awk '{print $2}' | head -1`
    `kill #{pid}` unless pid.to_s.empty?
end

def debug_server_executable
    app_path = File.join(basedir, "webapp/app.py")
    return "python #{app_path}"
end

def run_tests(env_name)
    Rake::Task[:run_tests_with_environment].invoke env_name
end
