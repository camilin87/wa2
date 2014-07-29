task :default => [:clean, :all_tests, :reports]

def basedir
   return File.expand_path "."
end

def wa_packages
    return ["wa"]
end

$gitstats_dir = File.join(basedir, ".git-stats-src/")

$PYTHON_VERSION = "3.4.0"
$PYTHON_VERSION_GIT_STATS = "2.7.6"

$reports_dir = File.join(basedir, "code-reports/")
$cover_report_dir = File.join($reports_dir, "coverage")
$gitstats_report_dir = File.join($reports_dir, "gitstats")
$pylint_report_dir = File.join($reports_dir, "pylint")
$pep8_report_dir = File.join($reports_dir, "pep8")

def use_python(python_version)
    puts "use_python" + python_version
    sh "pyenv local #{python_version}"
end

def ensure_python_is(python_version)
    current_version = `python -V`
    error_msg = "Error using python version. Expected: #{python_version} Actual: #{current_version}"
    fail error_msg unless current_version.include? python_version
end

task :install_wa do
    wa_packages.each do |pkg|
        pkg_setup_path = File.join(basedir, "#{pkg}/setup.py")
        sh "python #{pkg_setup_path} -q install"
    end
end

task :clean => [:clean_pyc] do
    rm_rf $reports_dir
    rm_rf File.join(basedir, "build/")
end

task :clean_pyc do
    rm_f FileList.new('*.pyc')
    rm_f FileList.new('**/*.pyc')
    rm_rf FileList.new('**/__pycache__/')
end

task :all_tests => [:tests, :integration]
task :tests => [:clean_pyc, :install_wa] do
    sh %{nosetests -s -a '!integration'}
end

task :integration => [:clean_pyc, :install_wa] do
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

    $cover_report_old = File.join(basedir, "cover")
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
    Dir.entries(basedir).select { |entry|
        File.directory? entry and !(entry =='.' || entry == '..') 
    }.map {|dir| {
        :name => dir,
        :path => File.join(basedir, dir)
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
    use_python $PYTHON_VERSION_GIT_STATS

    gitstats_path = File.join($gitstats_dir, "gitstats")
    sh "#{gitstats_path} #{basedir} #{$gitstats_report_dir} > /dev/null"

    use_python $PYTHON_VERSION
end

task :report_lines_of_code do
    loc_test = `find #{basedir} -type f -iname '*.py' -path '*/test/*' | xargs wc -l | tail -1`
    loc_prod = `find #{basedir} -type f -iname '*.py' ! -path '*/test/*' | xargs wc -l | tail -1`

    puts "Lines of Code"
    puts "Test:       #{loc_test}"
    puts "Production: #{loc_prod}"
end

task :validate_cache_debug do
    Rake::Task[:validate_cache].invoke("localhost", 8080)
end

task :validate_cache_prod_quick do
    Rake::Task[:validate_cache].invoke("localhost", 80)
end

task :validate_cache_prod do
    Rake::Task[:validate_cache].invoke("localhost", 80, 3600 - 1)
end

task :validate_cache, [:server, :port, :ttl_sec] do |t, args|
    args.with_defaults(:server => "localhost", :port => 80, :ttl_sec => 3)

    url_hialeah = "http://#{args[:server]}:#{args[:port]}/t/api_key/25.86/-80.30"
    puts url_hialeah

    url_lax = "http://#{args[:server]}:#{args[:port]}/t/api_key/47.43/-121.80"
    puts url_lax

    cache_ttl_sec = args[:ttl_sec]

    if not all_urls_return_different_responses([url_hialeah, url_lax])
        fail "cache error: different urls return the same result"
        return
    end

    cache_test_output = `python test/cacherequesthelper.py "#{url_hialeah}" #{cache_ttl_sec}`

    if not cache_test_output.include? "is_cached=True"
        fail "cache error"
        return
    end
        
    puts "Cache OK"        
end

def all_urls_return_different_responses(url_list)
    responses = []
    url_list.each { |url| responses.push `curl #{url}` }
    return responses.uniq.length == responses.length
end
