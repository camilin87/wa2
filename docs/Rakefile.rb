task :default => [:build_api_docs]

def basedir
   return File.expand_path ".."
end

def wa_pkg_dir
    return File.join(basedir, "wa/") 
end

def input_file
    return File.join(basedir, "docs/help_template.md")
end

def output_file
    return File.join(basedir, "docs/Readme-gen.md")
end

task :clean do
    system "rm output_file"
end

task :build_output do
    cp input_file, output_file
end

task :build_api_docs => [:clean, :build_output] do 
    puts "building api docs"
    set_value "VERSION", get_api_version
    set_value "HOST", get_api_host
end

def get_api_host
    rake_file_prod = File.join(basedir, "Rakefile-prod.rb")
    return get_ini_value rake_file_prod, "CN"
end

def get_api_version
    wa_setup_path = File.join(wa_pkg_dir, "setup.py")
    return get_ini_value wa_setup_path, "VERSION"
end

def get_ini_value(filename, key, equal_sign = "=")
    File.open(filename, "r") do |f|
        f.each_line do |line|
            pieces = line.split(equal_sign, 2)
            if pieces.count == 2
                found_key = pieces[0].strip

                if found_key == key
                    value = pieces[1].strip
                    value_unquoted = value.chomp('"').reverse.chomp('"').reverse
                    return value_unquoted
                end
            end
        end
    end

    return "UNKOWN"
end

def set_value(key, value)
    value_sanitized = value.gsub("\n", "")
    key_str = "{{#{key}}}"

    tmp_file = output_file + ".tmp"

    File.open(output_file, "r") do |input_file|
        input_file.each_line do |line|
            new_line = line.gsub key_str, value_sanitized

            open(tmp_file, 'a') do |f|
                f.puts new_line
            end
        end
    end

    cp tmp_file, output_file
    rm tmp_file
end
