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
    pid = spawn("python #{app_path}")
    sleep(3)

    run_tests t.name

    Process.kill("HUP", pid)
end

def run_tests(env_name)
    Rake::Task[:run_tests_with_environment].invoke env_name
end
