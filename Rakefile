task :default => [:clean, :all_tests, :reports]

$basedir = File.expand_path "."
$gitstats_dir = File.join($basedir, ".git-stats-src/")

$PYTHON_VERSION = "3.4.0"
$PYTHON_VERSION_GIT_STATS = "2.7.6"

$reports_dir = File.join($basedir, "code-reports/")
$cover_report_dir = File.join($reports_dir, "coverage")
$gitstats_report_dir = File.join($reports_dir, "gitstats")
$pylint_report_dir = File.join($reports_dir, "pylint")
$pep8_report_dir = File.join($reports_dir, "pep8")

task :configure_pyenv do
    bash_profile = File.expand_path "~/.bash_profile"

    if not File.readlines(bash_profile).grep(/pyenv init/).any?
        File.open(bash_profile, "a") do |f|
            f.puts 'eval "$(pyenv init -)"'
        end
    end
end

task :configure_pyenv_linux do
    bash_profile = File.expand_path "~/.profile"

    if not File.readlines(bash_profile).grep(/pyenv init/).any?
        File.open(bash_profile, "a") do |f|            
            f.puts 'export PATH="$HOME/.pyenv/bin:$PATH"'
            f.puts 'eval "$(pyenv init -)"'
            f.puts 'eval "$(pyenv virtualenv-init -)"'
        end
    end
end

task :install_dev_dependencies_mac do
    system %{brew install pyenv}
    system %{brew install xz}
    system %{brew install gnuplot --cairo --png}
    system %{sudo easy_install pip}

    Rake::Task["install_dev_dependencies"].execute
end

task :install_dev_dependencies do
    install_gitstats
    configure_python_version
    switch_to_dev_python_version
    install_pypi_dev_dependencies
    refresh_packages
end

task :install_prod_dependencies do
    system %{curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash}
    system %{pyenv update}
    system %{sudo apt-get install -y make gcc libssl-dev openssl }

    configure_python_version
    switch_to_dev_python_version
    install_pypi_prod_dependencies
    refresh_packages
end

def install_gitstats
    system "git clone --depth 1 git://github.com/hoxu/gitstats.git #{$gitstats_dir}"
    Dir.chdir($gitstats_dir){
        sh %{git pull} 
    }
end

def configure_python_version
    install_python $PYTHON_VERSION
    install_python $PYTHON_VERSION_GIT_STATS
    refresh_packages
end

def install_python(python_version)
    puts "install_python" + python_version
    system "yes N | pyenv install #{python_version}"
end

def switch_to_dev_python_version
    use_python $PYTHON_VERSION
end

def switch_to_git_stats_python_version
    use_python $PYTHON_VERSION_GIT_STATS
end

def use_python(python_version)
    puts "use_python" + python_version
    sh "pyenv local #{python_version}"
end

def install_pypi_dev_dependencies
    dev_packages = [
        "nose", "freezegun", "coverage",
        "pylint", "pep8", "python-forecastio",
        "bottle"
    ]
    install_pypi_packages dev_packages
end

def install_pypi_prod_dependencies
    prod_packages = [
        "python-forecastio", "bottle"
    ]
    install_pypi_packages prod_packages
end

def install_pypi_packages(pypi_packages)
    pypi_packages.each do |pkg|
        sh "sudo pip install --upgrade #{pkg}"
    end
end

def refresh_packages
    sh %{pyenv rehash}
end


task :clean => [:clean_pyc] do
    rm_rf $reports_dir
end

task :clean_pyc do
    rm_f FileList.new('*.pyc')
    rm_f FileList.new('**/*.pyc')
    rm_rf FileList.new('**/__pycache__/')
end

task :all_tests => [:tests, :integration]
task :tests => [:clean_pyc] do
    sh %{nosetests -s -a '!integration'}
end

task :integration => [:clean_pyc] do
    sh %{nosetests -s -a 'integration'}
end

task :create_reports_dir do
    mkdir $reports_dir unless File.exists? $reports_dir 
end

task :reports => [
    :create_reports_dir,
    :report_coverage, :report_pylint, :report_pep8,
    :report_gitstats, :report_lines_of_code
]

task :report_coverage => [:clean_pyc, :create_reports_dir] do
    sh %{nosetests -s --with-coverage --cover-html --cover-erase}

    $cover_report_old = File.join($basedir, "cover")
    File.rename($cover_report_old, $cover_report_dir)
end

task :report_pylint => :create_reports_dir do
    mkdir $pylint_report_dir unless File.exists? $pylint_report_dir

    links = Array.new
    get_packages.each do |pkg_info|
        output_filename = "#{pkg_info[:name]}.html"
        output_path = File.join($pylint_report_dir, output_filename)
        system "pylint #{pkg_info[:path]} > #{output_path}"

        links.push %{<a href="#{output_filename}">#{output_filename}</a></br>}
    end

    build_index_with links
end

def get_packages
    Dir.entries($basedir).select { |entry|
        File.directory? entry and !(entry =='.' || entry == '..') 
    }.map {|dir| {
        :name => dir,
        :path => File.join($basedir, dir)
    }}.compact.select { |dir_info|
        File.exists? File.join(dir_info[:path], "__init__.py")
    }
end

def build_index_with(links)
    report_path = File.join($pylint_report_dir, "index.html")
    File.open(report_path, "w") do |file|
        file.write "<html><body>"
        links.each do |l|
            file.write l
        end
        file.write "</body></html>"
    end
end

task :report_pep8 => :create_reports_dir do
    mkdir $pep8_report_dir unless File.exists? $pep8_report_dir

    report_output = File.join($pep8_report_dir, "report.txt")
    system "pep8 --max-line-length=100 */*.py > #{report_output}"
end

task :report_gitstats => :create_reports_dir do
    switch_to_git_stats_python_version

    gitstats_path = File.join($gitstats_dir, "gitstats")
    sh "#{gitstats_path} #{$basedir} #{$gitstats_report_dir} > /dev/null"

    switch_to_dev_python_version
end

task :report_lines_of_code do
    loc_test = `find #{$basedir} -type f -iname '*.py' -path '*/test/*' | xargs wc -l | tail -1`
    loc_prod = `find #{$basedir} -type f -iname '*.py' ! -path '*/test/*' | xargs wc -l | tail -1`

    puts "Lines of Code"
    puts "Test:       #{loc_test}"
    puts "Production: #{loc_prod}"
end


task :run_debug do
    `python -m bottle --bind 0.0.0.0:8080 --debug --reload webapp.app`
end
