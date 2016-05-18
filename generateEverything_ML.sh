# !/bin/bash

python ../split_data_8-1-1_sample_item.py

../sim-cosine -u 6041 -i 3953 -r ratings_train_80.dat -t ratings_train_input.dat > ./similarity_ub_cos
../sim-jaccard -u 6041 -i 3953 -r ratings_train_80.dat -t ratings_train_input.dat > ./similarity_ub_jaccard
../sim-cosine -u 6041 -i 3953 -r ratings_train_80.dat -t ratings_train_input.dat -q 1 -a 0 > ./similarity_ub_q1a0
# ../sim-cosine -u 6041 -i 3953 -r ratings_train_80.dat -t ratings_train_input.dat -q 1 -a 0.5 > ./similarity_ub_q1a0.5
../sim-cosine -u 6041 -i 3953 -r ratings_train_80.dat -t ratings_train_input.dat -q 5 -a 0 > ./similarity_ub_q5a0
../sim-cosine -u 6041 -i 3953 -r ratings_train_80.dat -t ratings_train_input.dat -q 5 -a 0.5 > ./similarity_ub_q5a0.5

for i in `ls | grep "similarity_ub" | sed 's/similarity_//'`
do
	echo `date '+%m-%d-%Y %H:%M:%S'` "$i"
	python ../complete_degrees_ML.py ub ./similarity_$i
	../socialfiltering -u 6041 -i 3953 -r ratings_train_80.dat -t train_target_users.dat -l ratings_train_input.dat -g similarity_"$i"_complete -k 10 -a recweighted_"$i" > ./recavg_"$i"
done

../sim-cosine -i 6041 -u 3953 -r ratings_train_80_iuv.dat -t ratings_train_80_iuv.dat > ./similarity_ib_cos
../sim-jaccard -i 6041 -u 3953 -r ratings_train_80_iuv.dat -t ratings_train_80_iuv.dat > ./similarity_ib_jaccard
../sim-cosine -i 6041 -u 3953 -r ratings_train_80_iuv.dat -t ratings_train_80_iuv.dat -q 1 -a 0 > ./similarity_ib_q1a0
# ../sim-cosine -i 6041 -u 3953 -r ratings_train_80_iuv.dat -t ratings_train_80_iuv.dat -q 1 -a 0.5 > ./similarity_ib_q1a0.5
../sim-cosine -i 6041 -u 3953 -r ratings_train_80_iuv.dat -t ratings_train_80_iuv.dat -q 5 -a 0 > ./similarity_ib_q5a0
../sim-cosine -i 6041 -u 3953 -r ratings_train_80_iuv.dat -t ratings_train_80_iuv.dat -q 5 -a 0.5 > ./similarity_ib_q5a0.5
echo `date '+%m-%d-%Y %H:%M:%S'` "Generating sim-arule"
../apriori-simple.py ratings_train_80.dat # get ./sim-arule
sed '/-/d;/inf/d;/^$/d' sim_arule > ./similarity_ib_arule

for i in `ls | grep "similarity_ib" | sed 's/similarity_//'`
do
	echo `date '+%m-%d-%Y %H:%M:%S'` "$i"
	python ../complete_degrees_ML.py ib ./similarity_$i
	../socialfiltering -u 6041 -i 3953 -r ratings_train_80.dat -t train_target_users.dat -l ratings_train_input.dat -g similarity_"$i"_complete -k 10 -b 1 -a recweighted_"$i" > ./recavg_"$i"
done

echo `date '+%m-%d-%Y %H:%M:%S'` "Merging..."
python ../calc_result_ML_8-1-1.py `ls | grep rec | tr "\n" " "`
echo `date '+%m-%d-%Y %H:%M:%S'` "Done."
