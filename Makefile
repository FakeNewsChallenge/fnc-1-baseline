help:
	@echo "make clean             remove features/*.npy and splits/*.txt"
clean:
	rm features/*.npy
	rm splits/hold_out_ids.txt
	rm splits/training_ids.txt
