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
end

def get_api_version
    wa_setup_path = File.join(wa_pkg_dir, "setup.py")
    File.open(wa_setup_path, "r") do |f|
        f.each_line do |line|
            if line.start_with? "VERSION ="
                return line
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
