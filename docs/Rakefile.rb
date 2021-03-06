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
    return File.join(basedir, "docs/WebApiDocs-gen.md")
end

task :clean do
    system "rm #{output_file}"
end

task :build_output do
    cp input_file, output_file
end

task :build_api_docs => [:clean, :build_output] do 
    puts "building api docs"
    set_value "VERSION", get_api_version
    set_value "HOST", get_production_host
    set_value "INTENSITY_TYPES", get_intensity_types
    set_value "PRECIPITATION_TYPES", get_precipitation_types
    set_value "API_RESULT", get_api_result
end

def get_api_result
    precipitation_types_path = File.join(wa_pkg_dir, "api/returncode.py")

    return read_code_file precipitation_types_path, 8
end

def get_precipitation_types
    precipitation_types_path = File.join(wa_pkg_dir, "engine/precipitationtype.py")

    return read_code_file precipitation_types_path, 8
end

def get_intensity_types
    intensity_types_path = File.join(wa_pkg_dir, "engine/intensitytype.py")

    return read_code_file intensity_types_path, 8
end

def read_code_file(filename, tabs = 4)
    result = ""

    File.open(filename, "rb") do |f|
        f.each_line do |line|
            result += (" " * tabs) + line
        end
    end

    return result
end

def get_production_host
    host_file = File.join(basedir, "host.txt")
    return File.open(host_file, &:gets)
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
    # value_sanitized = value.gsub("\n", "")
    value_sanitized = value
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
