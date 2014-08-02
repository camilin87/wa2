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
    app_path = File.join(basedir, "webapp/app.py")
    spawned_process = "python #{app_path}"
    spawn(spawned_process)
    sleep(3)

    run_tests t.name

    pid = `ps -l | grep "#{spawned_process}" | grep -v "grep" | awk '{print $2}' | head -1`
    `kill #{pid}` unless pid.to_s.empty?
end

def run_tests(env_name)
    Rake::Task[:run_tests_with_environment].invoke env_name
end
