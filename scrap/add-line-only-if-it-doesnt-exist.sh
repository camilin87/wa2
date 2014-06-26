#/bin/sh

tmp_file=/tmp/tmp_bash_profile
tmp_file2=/tmp/tmp_bash_profile_2

cp ~/.bash_profile $tmp_file

echo 'eval "$(pyenv init -)"' >> $tmp_file
echo 'eval "$(pyenv init -)"' >> $tmp_file
echo 'eval "$(pyenv init -)"' >> $tmp_file

# awk '!x[$0]++' $tmp_file
sed '$!N; /^\(.*\)\n\1$/!P; D' $tmp_file > $tmp_file2

cat $tmp_file2
