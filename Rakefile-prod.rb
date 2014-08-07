import 'Rakefile.rb'

def webapp_path
    return File.join(basedir, "webapp/")
end

task :configure_pyenv_linux do
    alias_filename = "~/.bash_aliases"
    bash_profile = File.expand_path alias_filename

    if not File.exists? bash_profile or not File.readlines(bash_profile).grep(/python=python3/).any?
        `echo alias python=python3 >> #{alias_filename}`
        puts "WARNING: close this shell before proceeding"
    end
end

task :install_prod_dependencies do
    install_prod_system_packages
    install_pypi_prod_dependencies

    Rake::Task[:install_prod_wa_packages].invoke

    Rake::Task[:configure_newrelic].invoke
    Rake::Task[:configure_uwsgi].invoke
    Rake::Task[:configure_nginx].invoke
end

task :install_prod_wa_packages do
    wa_packages.each do |pkg|
        pkg_setup_path = File.join(basedir, "#{pkg}/setup.py")
        sh "sudo python3 #{pkg_setup_path} -q install"
    end
end

def install_prod_system_packages
    pkg_dependencies = [
        "python3-pip", "python3-dev",
        "nginx"
    ]
    install_system_dependencies_linux pkg_dependencies
end

def install_system_dependencies_linux(packages)
    packages.each do |pkg|
        sh "sudo apt-get install -y #{pkg}"
    end
end

def install_pypi_prod_dependencies
    prod_packages = [
        "pkginit", "uwsgi", "python-forecastio", "Flask", "uwsgitop", "newrelic"
    ]
    sudo_install_pypi_packages prod_packages
end

def sudo_install_pypi_packages(pypi_packages)
    pypi_packages.each do |pkg|
        sh "sudo pip3 install --upgrade #{pkg}"
    end
end

def newrelic_config_path
    return File.join(basedir, "newrelic.ini")
end

task :configure_newrelic do
    new_relic_key = "550cb88ab17af890360b32fac5a898cd470274e6"
    sh "newrelic-admin generate-config #{new_relic_key} #{newrelic_config_path}"
end

task :reload_uwsgi do
    `sudo sh -c 'echo r > /tmp/wa2_uwsgi'`
end

task :start_uwsgi_manually do
    is_running_output = `ps aux | grep "uwsgi" | grep -v "grep"`
    if is_running_output.include? "uwsgi"
        `sudo sh -c 'echo q > /tmp/wa2_uwsgi'`
    end

    `sudo rm /tmp/wa2_uwsgi`

    `sed -i 's/daemonize/#daemonize/g' #{uwsgi_config_path}`

    `NEW_RELIC_CONFIG_FILE=#{newrelic_config_path} newrelic-admin run-program uwsgi #{uwsgi_config_path}`
end

task :uwsgi_stats do
    system "uwsgitop 127.0.0.1:1717"
end

task :configure_uwsgi do
    write_uwsgi_config
    upstart_config_path = "/etc/init/wa2_uwsgi.conf"
    upstart_config_contents = %{
start on runlevel [2345]
stop on runlevel [06]

exec NEW_RELIC_CONFIG_FILE=#{newrelic_config_path} newrelic-admin run-program uwsgi #{uwsgi_config_path}
}
    config_existed_before = File.file? upstart_config_path
    sudo_write_config upstart_config_path, upstart_config_contents

    if config_existed_before
        Rake::Task[:reload_uwsgi].invoke
    else
        puts "WARNING: Reboot required to launch uwsgi"
    end
end

task :disable_debug do
    write_uwsgi_config true

    Rake::Task[:reload_uwsgi].invoke
    Rake::Task[:clear_cache].invoke
end

task :log_debug do
    write_uwsgi_config false, true

    Rake::Task[:reload_uwsgi].invoke
    Rake::Task[:clear_cache].invoke
end

def uwsgi_config_path
    return File.join(basedir, "uwsgi_config.ini")
end

def write_uwsgi_config(disable_debug = false, log_debug = false)
    uwsgi_config_contents = %{
[uwsgi]
socket = 127.0.0.1:3031
pythonpath = #{webapp_path}
module = app
callable = app

vaccum = true
processes = 4
threads = 2

chmod-socket = 666
uid = www-data
gid = www-data
daemonize = /var/log/nginx/wa2_uwsgi.log

stats = 127.0.0.1:1717
memory-report = true
master = true
master-fifo = /tmp/wa2_uwsgi

add-header = Cache-Control: public, max-age=3600

; custom configuration setting for wa2 only
disable_debug = #{disable_debug}
log_debug = #{log_debug}
}
    write_config uwsgi_config_path, uwsgi_config_contents
end

def sudo_write_config(file_path, file_content)
    temp_path = File.join(basedir, "temp_file.txt")
    write_config(temp_path, file_content)
    sh "sudo mv #{temp_path} #{file_path}"
end

def write_config(file_path, file_content)
    File.open(file_path, "w") do |f|
        f.puts file_content
    end
end

def nginx_cache_dir
    return "/var/nginx/cache"
end

task :configure_nginx do
    configure_nginx
end

task :disable_cache => :clear_cache do
    configure_nginx true
end

def configure_nginx(no_cache = false)
    nginx_config = "/etc/nginx/sites-available/default"
    cache_config = get_nginx_cache_config
    if no_cache
        cache_config = ""
    end
    config_contents = get_nginx_config_contents cache_config

    system "sudo service nginx stop"

    system "sudo mkdir -p #{nginx_cache_dir}"
    sudo_write_config nginx_config, config_contents

    sh "sudo service nginx start"
end

def get_nginx_config_contents(cache_config)
    return %{
        upstream uwsgicluster {
            server 127.0.0.1:3031;
        }

        uwsgi_cache_path #{nginx_cache_dir} levels=1:2 keys_zone=one:10m max_size=2048m;

        server {
            listen 80;

            location / {
                include            uwsgi_params;
                uwsgi_pass         uwsgicluster;

                proxy_redirect     off;
                proxy_set_header   Host $host;
                proxy_set_header   X-Real-IP $remote_addr;

                proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header   X-Forwarded-Host $server_name;

                #{cache_config}
            }
        }
    }
end

def get_nginx_cache_config
    return %{
        uwsgi_cache        one;
        uwsgi_cache_key    $request_uri;
        uwsgi_cache_valid  200 302   60m;
        uwsgi_cache_valid  404     1440m;
    }
end

task :clear_cache do
    sh "sudo rm -R -f #{nginx_cache_dir}/*"
    Rake::Task[:reload_nginx].invoke
end

task :reload_nginx do
   sh "sudo service nginx restart" 
end

task :run_debug do
    `python3 webapp/app.py`
end
