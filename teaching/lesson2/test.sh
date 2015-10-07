python students.py > tmp/out0.txt
javac StudentRunner.java; java StudentRunner > tmp/out1.txt
ruby students.rb > tmp/out2.txt
go run student.go > tmp/out3.txt
g++ student.cc -std=c++11; ./a.out > tmp/out4.txt
scala Student.scala > tmp/out5.txt
php students.php > tmp/out6.txt

# Diff files
echo 'py vs. java'
diff tmp/out0.txt tmp/out1.txt > tmp/diff0.txt
cat tmp/diff0.txt

echo 'pv vs. ruby'
diff tmp/out0.txt tmp/out2.txt > tmp/diff1.txt
cat tmp/diff1.txt

echo 'pv vs. go'
diff tmp/out0.txt tmp/out3.txt > tmp/diff3.txt
cat tmp/diff3.txt

echo 'pv vs. c++'
diff tmp/out0.txt tmp/out4.txt > tmp/diff4.txt
cat tmp/diff4.txt

echo 'pv vs. scala'
diff tmp/out0.txt tmp/out5.txt > tmp/diff5.txt
cat tmp/diff5.txt

echo 'pv vs. php'
diff tmp/out0.txt tmp/out6.txt > tmp/diff6.txt
cat tmp/diff6.txt

