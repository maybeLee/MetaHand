for dir in $(find ./ -type d -print)
do
  
  chmod -R 755 $dir
  echo "permission changed 777 for directory : ".$dir
done >output_file.log

for dir in $(find ./ -type f -print)
do
  
  chmod -R 666 $dir
  echo "permission changed 666 for file : "$dir
done >>output_file.log
chmod +x change_permission.sh
